import json
import os
import database

def init_db():
    print(f"Initializing database (Engine: {database.get_engine()})...")
    
    conn = database.get_connection()
    c = conn.cursor()
    
    # Create tables
    database.init_tables(conn)

    # Load initial data from JSON
    try:
        with open('data/businesses.json', 'r') as f:
            data = json.load(f)
            businesses = data.get('businesses', [])
            
            # Check if table is empty before seeding
            c.execute("SELECT COUNT(*) FROM businesses")
            # Handle different cursor types (dict vs tuple) logic or just simple fetch
            # RealDictCursor returns dict, sqlite returns row
            count_result = c.fetchone()
            if isinstance(count_result, dict):
                count = count_result['count']
            else:
                count = count_result[0]
                
            if count > 0:
                print(f"Table already has {count} rows. Skipping seed.")
                return

            print(f"Seeding {len(businesses)} businesses...")
            
            for b in businesses:
                contacts_json = json.dumps(b.get('contacts', []))
                visits_json = json.dumps(b.get('visits', []))
                
                sql = '''
                    INSERT INTO businesses (
                        id, name, address, city, zipCode, lat, lng, type, 
                        customerStatus, interactionCount, lastVisit, priority, phone, 
                        contacts, visits
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                '''
                
                # Use prepare_query to handle placeholders
                sql = database.prepare_query(sql)
                
                c.execute(sql, (
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
            
            # If Postgres, reset the ID sequence to avoid collisions with next insert
            if database.get_engine() == 'postgres':
                print("Resetting Postgres ID sequence...")
                c.execute("SELECT setval('businesses_id_seq', (SELECT MAX(id) FROM businesses))")
            
            print(f"✅ Imported {len(businesses)} businesses.")
            
    except FileNotFoundError:
        print("⚠️ data/businesses.json not found. Database initialized empty.")
    except Exception as e:
        print(f"❌ Error importing data: {e}")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
