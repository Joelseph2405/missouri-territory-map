import sqlite3
import json

DB_PATH = 'businesses.db'
TERRITORY_FILE = 'data/territory.json'

def cleanup_territory():
    # 1. Load Allowed Zips
    try:
        with open(TERRITORY_FILE, 'r') as f:
            data = json.load(f)
            allowed_zips = list(data.get('zipCodes', {}).keys())
            print(f"Loaded {len(allowed_zips)} allowed zip codes.")
    except Exception as e:
        print(f"Error loading territory file: {e}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 2. Count before
    cursor.execute("SELECT count(*) FROM businesses")
    total_before = cursor.fetchone()[0]

    # 3. Identify Out-of-Territory
    placeholders = ','.join(['?'] * len(allowed_zips))
    query = f"SELECT count(*) FROM businesses WHERE zipCode NOT IN ({placeholders})"
    cursor.execute(query, allowed_zips)
    to_delete = cursor.fetchone()[0]

    if to_delete == 0:
        print("✅ No out-of-territory businesses found. Database is clean.")
        conn.close()
        return

    print(f"⚠️ Found {to_delete} businesses outside your territory.")
    
    # 4. Execute Delete
    delete_query = f"DELETE FROM businesses WHERE zipCode NOT IN ({placeholders})"
    cursor.execute(delete_query, allowed_zips)
    conn.commit()
    
    # 5. Verify
    cursor.execute("SELECT count(*) FROM businesses")
    total_after = cursor.fetchone()[0]
    
    print(f"🗑️ Deleted {to_delete} records.")
    print(f"📉 Total Businesses: {total_before} -> {total_after}")
    conn.close()

if __name__ == "__main__":
    cleanup_territory()
