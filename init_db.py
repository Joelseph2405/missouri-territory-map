import sqlite3
import json
import os

DB_FILE = 'businesses.db'

def init_db(db_file_path=DB_FILE):
    if os.path.exists(db_file_path):
        os.remove(db_file_path)

    conn = sqlite3.connect(db_file_path)
    c = conn.cursor()

    # Create table matching JSON structure
    # Storing lists (contacts, visits) as JSON strings for simplicity and compatibility
    c.execute('''
        CREATE TABLE businesses (
            id INTEGER PRIMARY KEY,
            name TEXT,
            address TEXT,
            city TEXT,
            zipCode TEXT,
            lat REAL,
            lng REAL,
            type TEXT,
            customerStatus TEXT,
            interactionCount INTEGER,
            lastVisit TEXT,
            priority TEXT,
            phone TEXT,
            contacts TEXT,
            visits TEXT
        )
    ''')

    # Load initial data from JSON
    try:
        with open('data/businesses.json', 'r') as f:
            data = json.load(f)
            businesses = data.get('businesses', [])
            
            for b in businesses:
                contacts_json = json.dumps(b.get('contacts', []))
                visits_json = json.dumps(b.get('visits', []))
                
                c.execute('''
                    INSERT INTO businesses (
                        id, name, address, city, zipCode, lat, lng, type, 
                        customerStatus, interactionCount, lastVisit, priority, phone, 
                        contacts, visits
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    b.get('id'),
                    b.get('name'),
                    b.get('address'),
                    b.get('city'),
                    b.get('zipCode'),
                    b.get('lat'),
                    b.get('lng'),
                    b.get('type'),
                    b.get('customerStatus'),
                    b.get('interactionCount', 0),
                    b.get('lastVisit'),
                    b.get('priority', 'medium'),
                    b.get('phone'),
                    contacts_json,
                    visits_json
                ))
            
            print(f"✅ Imported {len(businesses)} businesses into {db_file_path}")
            
    except FileNotFoundError:
        print("⚠️ data/businesses.json not found. Database initialized empty.")
    except Exception as e:
        print(f"❌ Error importing data: {e}")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
