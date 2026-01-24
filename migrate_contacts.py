import database
import json
import sqlite3

def migrate_contacts():
    print("🚀 Starting contact migration...")
    conn = database.get_connection()
    c = conn.cursor()
    
    # Get all businesses with contacts
    # We select ID and the raw contacts JSON string
    c.execute("SELECT id, name, contacts FROM businesses WHERE contacts IS NOT NULL AND contacts != '[]' AND contacts != ''")
    rows = c.fetchall()
    
    migrated_count = 0
    error_count = 0
    
    print(f"Found {len(rows)} businesses with potential contacts.")
    
    for row in rows:
        b_id = row['id'] if isinstance(row, dict) else row[0]
        # Handle dict vs tuple for other fields
        b_name_idx = 1 if not isinstance(row, dict) else 'name'
        b_contacts_idx = 2 if not isinstance(row, dict) else 'contacts'
        
        b_name = row[b_name_idx]
        contacts_raw = row[b_contacts_idx]
        
        try:
            contacts_list = json.loads(contacts_raw)
            
            if not isinstance(contacts_list, list):
                print(f"⚠️ Warning: Contacts for business {b_id} is not a list. Skipping.")
                continue
                
            for contact in contacts_list:
                name = contact.get('name')
                if not name:
                    continue
                    
                title = contact.get('title', '')
                phone = contact.get('phone', '')
                email = contact.get('email', '')
                notes = contact.get('notes', '')
                
                # Insert into new table
                sql = '''
                    INSERT INTO contacts (business_id, name, title, phone, email, notes)
                    VALUES (?, ?, ?, ?, ?, ?)
                '''
                
                # Check for duplicates before inserting (Name + BizID)
                check_sql = "SELECT id FROM contacts WHERE business_id = ? AND name = ?"
                
                # Handle Postgres vs SQLite placeholders
                if database.get_engine() == 'postgres':
                    sql = sql.replace('?', '%s')
                    check_sql = check_sql.replace('?', '%s')
                
                c.execute(check_sql, (b_id, name))
                if c.fetchone():
                    # print(f"   Skipping duplicate: {name} @ {b_name}")
                    continue
                
                c.execute(sql, (b_id, name, title, phone, email, notes))
                migrated_count += 1
                
        except json.JSONDecodeError:
            print(f"❌ Error decoding JSON for business {b_id}")
            error_count += 1
        except Exception as e:
            print(f"❌ Error processing business {b_id}: {e}")
            error_count += 1
            
    conn.commit()
    conn.close()
    
    print(f"✅ Migration Complete.")
    print(f"   - Migrated Contacts: {migrated_count}")
    print(f"   - Errors: {error_count}")

if __name__ == '__main__':
    migrate_contacts()
