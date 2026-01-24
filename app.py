from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sqlite3
import json
import os
import csv
import io
import geocoder
from init_db import init_db
import database

app = Flask(__name__, static_folder='.')
CORS(app)

# Initialize database if needed (mostly for local SQLite)
# For Postgres, one-time migration script is better, but this check is harmless if fast
# Initialize database (checks for tables/data and seeds if empty)
try:
    init_db()
except Exception as e:
    print(f"Startup initialization failed (non-critical if DB exists): {e}")

def get_db_connection():
    return database.get_connection()

def business_from_row(row):
    b = dict(row)
    # Parse JSON fields back to lists
    if b.get('contacts'):
        try:
            b['contacts'] = json.loads(b['contacts'])
        except:
            b['contacts'] = []
    if b.get('visits'):
        try:
            b['visits'] = json.loads(b['visits'])
        except:
            b['visits'] = []
    return b

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@app.route('/api/businesses', methods=['GET'])
def get_businesses():
    print("DEBUG: Entering get_businesses")
    conn = get_db_connection()
    cursor = conn.cursor()
    # No params, simple query
    print("DEBUG: Executing query")
    cursor.execute('SELECT * FROM businesses')
    businesses = cursor.fetchall()
    print(f"DEBUG: Fetched {len(businesses)} rows")
    conn.close()
    
    data = [business_from_row(b) for b in businesses]
    print("DEBUG: Serialized data")
    return jsonify({
        'businesses': data
    })

@app.route('/api/force_reset_db', methods=['GET'])
def force_reset_db():
    """Emergency endpoint to wipe and re-seed database"""
    # Security: In a real app, this needs Auth. 
    # For this prototype/debugging phase, it's open but obscure.
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS businesses")
        conn.commit()
        conn.close()
        
        # Re-run init
        init_db()
        
        return jsonify({"status": "success", "message": "Database wiped and re-seeded from JSON."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/businesses', methods=['POST'])
def add_business():
    new_business = request.json
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Handle optional fields with defaults
    contacts_json = json.dumps(new_business.get('contacts', []))
    visits_json = json.dumps(new_business.get('visits', []))
    
    # Simple ID generation (in a real app, let DB handle it, but we want to return it immediately)
    # Actually, let's let DB Autoincrement do the work if ID is not provided
    # But for migration consistency with frontend that might generate IDs, let's check.
    # The current frontend setup often relies on maxId + 1 logic.
    # For this backend approach, it's safer to let the DB generate the ID if it's new.
    
    # The current frontend setup often relies on maxId + 1 logic.
    # For this backend approach, it's safer to let the DB generate the ID if it's new.
    
    sql = '''
        INSERT INTO businesses (
            name, address, city, zipCode, lat, lng, type, 
            customerStatus, interactionCount, lastVisit, priority, phone, 
            contacts, visits
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    
    params = (
        new_business.get('name'),
        new_business.get('address'),
        new_business.get('city'),
        new_business.get('zipCode'),
        new_business.get('lat'),
        new_business.get('lng'),
        new_business.get('type'),
        new_business.get('customerStatus'),
        new_business.get('interactionCount', 0),
        new_business.get('lastVisit'),
        new_business.get('priority'),
        new_business.get('phone'),
        contacts_json,
        visits_json
    )
    
    new_id = database.execute_insert_returning_id(cursor, sql, params)
    conn.commit()
    conn.close()
    
    # Return the full object with the new ID
    new_business['id'] = new_id
    if 'contacts' not in new_business: new_business['contacts'] = []
    if 'visits' not in new_business: new_business['visits'] = []
            
    return jsonify(new_business), 201

@app.route('/api/businesses/<int:id>', methods=['PUT'])
def update_business(id):
    updated_business = request.json
    
    contacts_json = json.dumps(updated_business.get('contacts', []))
    visits_json = json.dumps(updated_business.get('visits', []))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    sql = '''
        UPDATE businesses SET
            name = ?, address = ?, city = ?, zipCode = ?, lat = ?, lng = ?, 
            type = ?, customerStatus = ?, interactionCount = ?, lastVisit = ?, 
            priority = ?, phone = ?, contacts = ?, visits = ?
        WHERE id = ?
    '''
    
    cursor.execute(database.prepare_query(sql), (
        updated_business.get('name'),
        updated_business.get('address'),
        updated_business.get('city'),
        updated_business.get('zipCode'),
        updated_business.get('lat'),
        updated_business.get('lng'),
        updated_business.get('type'),
        updated_business.get('customerStatus'),
        updated_business.get('interactionCount'),
        updated_business.get('lastVisit'),
        updated_business.get('priority'),
        updated_business.get('phone'),
        contacts_json,
        visits_json,
        id
    ))
    
    conn.commit()
    conn.close()
    
    return jsonify(updated_business)

@app.route('/api/businesses/<int:id>', methods=['DELETE'])
def delete_business(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    sql = 'DELETE FROM businesses WHERE id = ?'
    cursor.execute(database.prepare_query(sql), (id,))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/api/health', methods=['GET'])
def health_check():
    status = {
        'status': 'ok',
        'engine': database.get_engine(),
        'db_path': database.DB_FILE if database.get_engine() == 'sqlite' else 'postgres',
    }
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check table existence
        if database.get_engine() == 'postgres':
             cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'businesses')")
             table_exists = cursor.fetchone()['exists']
        else:
             cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='businesses'")
             table_exists = cursor.fetchone() is not None
             
        status['table_exists'] = table_exists
        
        if table_exists:
            cursor.execute('SELECT COUNT(*) as count FROM businesses')
            row = cursor.fetchone()
            # Handle RealDictCursor vs tuple
            if isinstance(row, dict):
                status['row_count'] = row['count']
            else:
                status['row_count'] = row[0]
                
        conn.close()
    except Exception as e:
        status['error'] = str(e)
        status['status'] = 'error'
        
    return jsonify(status)

# --- CONTACTS API ---

@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    conn = get_db_connection()
    c = conn.cursor()
    
    # Left join to get business name for context
    sql = '''
        SELECT c.*, b.name as business_name, b.address as business_address 
        FROM contacts c
        LEFT JOIN businesses b ON c.business_id = b.id
        ORDER BY c.name ASC
    '''
    
    c.execute(sql)
    rows = c.fetchall()
    conn.close()
    
    contacts = [dict(row) for row in rows]
    return jsonify({'contacts': contacts})

@app.route('/api/contacts', methods=['POST'])
def add_contact():
    data = request.json
    
    # Validation
    if not data.get('name'):
        return jsonify({'error': 'Name is required'}), 400
        
    conn = get_db_connection()
    c = conn.cursor()
    
    sql = '''
        INSERT INTO contacts (business_id, name, title, phone, email, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    '''
    
    params = (
        data.get('business_id'), # Can be None if unlinked (global only)
        data.get('name'),
        data.get('title'),
        data.get('phone'),
        data.get('email'),
        data.get('notes')
    )
    
    new_id = database.execute_insert_returning_id(c, sql, params)
    conn.commit()
    conn.close()
    
    return jsonify({'id': new_id, 'message': 'Contact created'}), 201

# --- REMINDERS API ---

@app.route('/api/reminders', methods=['GET'])
def get_reminders():
    # Optional filter: due_before (YYYY-MM-DD)
    due_before = request.args.get('due_before')
    status_filter = request.args.get('status', 'pending') # Default to pending only
    
    conn = get_db_connection()
    c = conn.cursor()
    
    sql = '''
        SELECT r.*, b.name as business_name, c.name as contact_name
        FROM reminders r
        LEFT JOIN businesses b ON r.business_id = b.id
        LEFT JOIN contacts c ON r.contact_id = c.id
        WHERE r.status = ?
    '''
    params = [status_filter]
    
    if due_before:
        # Append logic for due date
        # Note: We store dates as TEXT YYYY-MM-DD, so string comparison works
        sql += " AND r.due_date <= ?"
        params.append(due_before)
        
    sql += " ORDER BY r.due_date ASC"
    
    c.execute(database.prepare_query(sql), tuple(params))
    rows = c.fetchall()
    conn.close()
    
    return jsonify({'reminders': [dict(row) for row in rows]})

@app.route('/api/reminders', methods=['POST'])
def add_reminder():
    data = request.json
    
    if not data.get('due_date'):
        return jsonify({'error': 'Due date is required'}), 400
        
    conn = get_db_connection()
    c = conn.cursor()
    
    sql = '''
        INSERT INTO reminders (business_id, contact_id, due_date, note, status)
        VALUES (?, ?, ?, ?, 'pending')
    '''
    
    params = (
        data.get('business_id'),
        data.get('contact_id'),
        data.get('due_date'),
        data.get('note', '')
    )
    
    new_id = database.execute_insert_returning_id(c, sql, params)
    conn.commit()
    conn.close()
    
    return jsonify({'id': new_id, 'message': 'Reminder created'}), 201

@app.route('/api/reminders/<int:id>/complete', methods=['PUT'])
def complete_reminder(id):
    conn = get_db_connection()
    c = conn.cursor()
    
    sql = "UPDATE reminders SET status = 'completed' WHERE id = ?"
    c.execute(database.prepare_query(sql), (id,))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/api/import_csv', methods=['POST'])
def import_csv():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
        
    file = request.files['file']
    import_status = request.form.get('status', 'prospective') # Default to prospective
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'File must be a CSV'}), 400

    # Read CSV
    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.DictReader(stream)
    
    # Process rows
    added_count = 0
    skipped_count = 0
    errors = []
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        for i, row in enumerate(csv_input):
            try:
                # Basic Validation
                name = row.get('Name') or row.get('name')
                address = row.get('Address') or row.get('address')
                city = row.get('City') or row.get('city')
                zip_code = row.get('Zip') or row.get('zip') or row.get('Zip Code') or row.get('zipCode')
                
                if not name or not address:
                    errors.append(f"Row {i+1}: Missing Name or Address")
                    skipped_count += 1
                    continue
                    
                # Check for duplicates (Name + Zip combo)
                cursor.execute("SELECT id FROM businesses WHERE name = ? AND zipCode = ?", (name, zip_code))
                if cursor.fetchone():
                    skipped_count += 1
                    continue
                
                # Geocode
                lat, lng = geocoder.geocode_address(address, city, zip_code)
                if not lat:
                    errors.append(f"Row {i+1}: Could not geocode '{address}'")
                    # Optionally insert anyway with 0,0? No, map app needs coords.
                    skipped_count += 1
                    continue
                
                # Insert
                business_type = row.get('Type') or row.get('type') or 'Other'
                
                sql = '''
                    INSERT INTO businesses (
                        name, address, city, zipCode, lat, lng, type, 
                        customerStatus, interactionCount, priority, contacts, visits
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0, 'medium', '[]', '[]')
                '''
                
                cursor.execute(sql, (name, address, city, zip_code, lat, lng, business_type, import_status))
                added_count += 1
                
                # Commit every 10 rows to be safe/incremental? No, transaction is better.
                
            except Exception as e:
                errors.append(f"Row {i+1} Error: {str(e)}")
                skipped_count += 1
        
        conn.commit()
        
    except Exception as e:
        conn.rollback()
        return jsonify({'error': f"Processing failed: {str(e)}"}), 500
    finally:
        conn.close()

    return jsonify({
        'success': True,
        'added': added_count,
        'skipped': skipped_count,
        'errors': errors
    })

if __name__ == '__main__':

        
    app.run(debug=True, port=8000, threaded=True, use_reloader=False)
