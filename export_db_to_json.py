import sqlite3
import json
import os
import database

def export_to_json():
    print("Exporting local DB to data/businesses.json...")
    conn = database.get_connection()
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    c.execute("SELECT * FROM businesses")
    rows = c.fetchall()
    
    businesses = []
    for row in rows:
        b = dict(row)
        # Parse JSON fields
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
        businesses.append(b)
        
    data = {"businesses": businesses}
    
    with open('data/businesses.json', 'w') as f:
        json.dump(data, f, indent=2)
        
    print(f"✅ Exported {len(businesses)} businesses to data/businesses.json")
    conn.close()

if __name__ == '__main__':
    export_to_json()
