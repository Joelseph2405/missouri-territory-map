import sqlite3
import time
from geocoder import geocode_address

DB_PATH = 'businesses.db'

def fix_locations():
    conn = sqlite3.connect(DB_PATH)
    # Use Row factory to access columns by name
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Select all businesses
    # Select only businesses that need fixing (Lat > 42 is likely Canada/North, < 30 is South)
    # Missouri is roughly Lat 36-40. So anything outside 35-41 is suspect.
    print("Fetching businesses with invalid coordinates...")
    cursor.execute("SELECT id, name, address, city, zipCode FROM businesses WHERE lat > 41 OR lat < 35 OR lat IS NULL")
    rows = cursor.fetchall()
    
    total = len(rows)
    print(f"Found {total} businesses. Starting Geocoding process...")
    print("NOTE: This will take time due to rate limiting (approx 1.5s per record).")

    updated_count = 0
    failed_count = 0

    for i, row in enumerate(rows):
        b_id = row['id']
        name = row['name']
        
        # Geocode
        lat, lng = geocode_address(row['address'], row['city'], row['zipCode'])
        
        if lat and lng:
            cursor.execute("UPDATE businesses SET lat = ?, lng = ? WHERE id = ?", (lat, lng, b_id))
            updated_count += 1
            print(f"[{i+1}/{total}] ✅ Fixed '{name}': {lat}, {lng}")
        else:
            failed_count += 1
            print(f"[{i+1}/{total}] ⚠️ Could not geocode '{name}' ({row['address']})")

        # Commit every 10 records to save progress
        if i % 10 == 0:
            conn.commit()
            
    conn.commit()
    conn.close()
    
    print("="*40)
    print(f"DONE! Updated: {updated_count}, Failed: {failed_count}")

if __name__ == "__main__":
    fix_locations()
