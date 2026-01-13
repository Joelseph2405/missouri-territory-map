import sqlite3
import time
from geocoder import geocode_address
import requests
from urllib.parse import quote

DB_PATH = 'businesses.db'
USER_AGENT = "BlackBoxCRM/1.0 (internal-tool)"

def geocode_zip_fallback(city, zip_code):
    """Geocode based on City/Zip only."""
    query = f"{city}, MO {zip_code}"
    encoded_query = quote(query)
    url = f"https://nominatim.openstreetmap.org/search?q={encoded_query}&format=json&limit=1"
    
    try:
        time.sleep(1.1) 
        headers = {'User-Agent': USER_AGENT}
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data:
                return float(data[0]['lat']), float(data[0]['lon'])
    except:
        pass
    return None, None

def fix_failed_locations():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Select businesses that are STILL broken (outside MO bounds)
    print("Finding remaining invalid businesses...")
    cursor.execute("SELECT id, name, address, city, zipCode FROM businesses WHERE lat > 41 OR lat < 36 OR lat IS NULL")
    rows = cursor.fetchall()
    
    total = len(rows)
    print(f"Found {total} stubbron businesses. Attempting Zip Code Fallback...")

    updated_count = 0
    failed_count = 0

    for i, row in enumerate(rows):
        b_id = row['id']
        name = row['name']
        
        # Try Zip Fallback immediately (since exact address likely failed already)
        lat, lng = geocode_zip_fallback(row['city'], row['zipCode'])
        
        if lat and lng:
            cursor.execute("UPDATE businesses SET lat = ?, lng = ? WHERE id = ?", (lat, lng, b_id))
            updated_count += 1
            print(f"[{i+1}/{total}] 📍 Zip Fallback for '{name}': {lat}, {lng}")
        else:
            failed_count += 1
            print(f"[{i+1}/{total}] ❌ COMPLETELY FAILED '{name}'")

        if i % 5 == 0:
            conn.commit()
            
    conn.commit()
    conn.close()
    
    print("="*40)
    print(f"DONE! Saved: {updated_count}, Still Lost: {failed_count}")

if __name__ == "__main__":
    fix_failed_locations()
