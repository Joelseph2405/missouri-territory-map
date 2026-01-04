from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sqlite3
import json
import os

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
    conn = get_db_connection()
    cursor = conn.cursor()
    # No params, simple query
    cursor.execute('SELECT * FROM businesses')
    businesses = cursor.fetchall()
    conn.close()
    
    return jsonify({
        'businesses': [business_from_row(b) for b in businesses]
    })

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

if __name__ == '__main__':

        
    app.run(debug=True, port=5000)
