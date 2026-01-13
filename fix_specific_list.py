import sqlite3
import time
import requests
from urllib.parse import quote

DB_PATH = 'businesses.db'
USER_AGENT = "BlackBoxCRM/1.0 (internal-tool)"

TARGETS = [
    "Clarendale of St. Peters",
    "Clinical Research Professionals, LLC",
    "Herbig Mechanical, Inc.",
    "Laney Enterprises Inc",
    "Quality Glass Tinting, Inc.",
    "Ram International Incorporated",
    "Riegel Dairy, Inc.",
    "Steve Crawford Trucking, Inc.",
    "First Choice Facilities"
]

def geocode_nom(address, city, zip_code):
    """
    Try strict address first, then city+zip fallback.
    Restricts search to Missouri/US.
    """
    # 1. Try Full Address
    query = f"{address}, {city}, MO {zip_code}"
    # Use structured query if possible for better results, but 'q' is flexible
    url = f"https://nominatim.openstreetmap.org/search?q={quote(query)}&format=json&limit=1&state=MO&countrycodes=us"
    
    try:
        time.sleep(1.2)
        headers = {'User-Agent': USER_AGENT}
        resp = requests.get(url, headers=headers, timeout=5)
        data = resp.json()
        if data:
            return float(data[0]['lat']), float(data[0]['lon']), "Address Match"
    except Exception as e:
        print(f"Error on strict geocode: {e}")

    # 2. Fallback to City/Zip
    print(f"   -> Fallback to Zip for {city}...")
    query_zip = f"{city}, MO {zip_code}"
    url_zip = f"https://nominatim.openstreetmap.org/search?q={quote(query_zip)}&format=json&limit=1" # relaxing state constraint slightly incase boundary issue, but query has MO
    
    try:
        time.sleep(1.2)
        resp = requests.get(url_zip, headers=headers, timeout=5)
        data = resp.json()
        if data:
             return float(data[0]['lat']), float(data[0]['lon']), "Zip Center"
    except:
        pass
        
    return None, None, "Failed"

def fix_list():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print(f"Fixing {len(TARGETS)} specific businesses...")
    
    for name_partial in TARGETS:
        cursor.execute("SELECT * FROM businesses WHERE name LIKE ?", (f"%{name_partial}%",))
        rows = cursor.fetchall()
        
        for row in rows:
            print(f"Processing: {row['name']}")
            lat, lng, method = geocode_nom(row['address'], row['city'], row['zipCode'])
            
            if lat:
                cursor.execute("UPDATE businesses SET lat=?, lng=? WHERE id=?", (lat, lng, row['id']))
                print(f"   ✅ Fixed via {method}: {lat}, {lng}")
            else:
                print("   ❌ Could not geocode.")
                
        conn.commit()

    conn.close()
    print("Done.")

if __name__ == "__main__":
    fix_list()
