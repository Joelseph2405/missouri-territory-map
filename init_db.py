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
                
            print(f"Checking data synchronization ({count} existing vs {len(businesses)} in file)...")
            
            # AGGRESSIVE RESET: If we have very few records (like the 3 seed ones) but a big file,
            # assume we are recovering from a bad state and wipe it.
            if count < 100 and len(businesses) > 1000:
                 print("⚠️ Detected potential stale seed data. PERFORMING HARD RESET (DROP TABLE).")
                 c.execute("DROP TABLE businesses")
                 database.init_tables(conn) # Recreate empty
                 print("✅ Table recreated.")
                 count = 0 # Now it's empty
            
            # Seed if we have more data in file than in DB, or just try to add missing ones
            # We removed the 'return' so we always attempt to sync new records
            
            print(f"Syncing {len(businesses)} businesses...")
            
            added = 0
            skipped = 0
            
            for b in businesses:
                try:
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
                    added += 1
                except Exception as e:
                    # ID conflict? Let's UPDATE the record to ensure fresh data
                    # This is important for location fixes etc.
                    try:
                        sql_update = '''
                            UPDATE businesses SET
                                name=?, address=?, city=?, zipCode=?, lat=?, lng=?, type=?, 
                                customerStatus=?, interactionCount=?, lastVisit=?, priority=?, phone=?, 
                                contacts=?, visits=?
                            WHERE id=?
                        '''
                        sql_update = database.prepare_query(sql_update)
                        
                        c.execute(sql_update, (
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
                            visits_json,
                            b.get('id')
                        ))
                        # print(f"Updated id {b.get('id')}")
                    except Exception as update_e:
                        print(f"Failed to update {b.get('id')}: {update_e}")
                        skipped += 1
                    pass
            
            print(f"Sync complete: Added {added}, Skipped {skipped} (duplicates).")
            
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
