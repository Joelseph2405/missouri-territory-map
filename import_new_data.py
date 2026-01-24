import openpyxl
import sqlite3
import shutil
import time
import requests
import json
import os
import database  # Uses existing database.py

EXCEL_FILE = "Joel's Recently Updated Accounts (1).xlsx"
DB_FILE = "businesses.db"
BACKUP_FILE = f"businesses_backup_{int(time.time())}.db"

# Zip Code Centers (Fallback)
ZIP_CENTERS = {
    "63301": (38.7881, -90.4974),
    "63376": (38.8003, -90.6298),
    "63368": (38.8106, -90.7126),
    "63385": (38.9867, -90.7387)
}

def get_location_cache():
    """Reads existing DB to cache known locations for addresses."""
    cache = {}
    if not os.path.exists(DB_FILE):
        return cache
        
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        # Grab address components and lat/lng
        c.execute("SELECT address, city, zipCode, lat, lng FROM businesses WHERE lat IS NOT NULL")
        rows = c.fetchall()
        for r in rows:
            # Key: address|city|zip
            key = f"{str(r[0]).lower().strip()}|{str(r[1]).lower().strip()}|{str(r[2]).strip()}"
            cache[key] = (r[3], r[4])
        conn.close()
        print(f"✅ Cached {len(cache)} existing locations.")
    except Exception as e:
        print(f"⚠️ Could not read existing DB for cache: {e}")
    return cache

def geocode(address, city, zip_code, cache):
    # 1. Check Cache
    key = f"{str(address).lower().strip()}|{str(city).lower().strip()}|{str(zip_code).strip()}"
    if key in cache:
        return cache[key][0], cache[key][1], "cache"

    # 2. Nominatim API
    full_address = f"{address}, {city}, MO {zip_code}, USA"
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': full_address,
            'format': 'json',
            'limit': 1
        }
        headers = {'User-Agent': 'BMG_Black_Box_Importer/2.0'}
        
        # RESPECT RATE LIMITS
        time.sleep(1.1) 
        
        response = requests.get(url, params=params, headers=headers, timeout=5)
        data = response.json()
        
        if data:
            lat = float(data[0]['lat'])
            lng = float(data[0]['lon'])
            return lat, lng, "api"
            
    except Exception as e:
        print(f"  ❌ Geocode failed for {full_address}: {e}")

    # 3. Fallback to Zip Center
    if str(zip_code) in ZIP_CENTERS:
        lat, lng = ZIP_CENTERS[str(zip_code)]
        return lat, lng, "zip_fallback"
        
    return None, None, "failed"

def run_import():
    # 1. Backup
    if os.path.exists(DB_FILE):
        shutil.copy(DB_FILE, BACKUP_FILE)
        print(f"📦 Database backed up to {BACKUP_FILE}")

    # 2. Load Cache
    location_cache = get_location_cache()

    # 3. Wipe & Init DB
    print("🧹 Wiping existing data...")
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS businesses")
    database.init_tables(conn)
    conn.commit()

    # 4. Read Excel
    print(f"📖 Reading {EXCEL_FILE}...")
    wb = openpyxl.load_workbook(EXCEL_FILE)
    sheet = wb.active
    
    # Headers are on Row 2, Data starts Row 3
    # Mappings (index 0-based from openpyxl verification):
    # 0: Account Name
    # 1: Account Segment (Type)
    # 3: Account Status (Active/Prospect)
    # 7: Street
    # 8: City
    # 10: Zip
    
    rows = list(sheet.iter_rows(min_row=3, values_only=True))
    print(f"Processing {len(rows)} records...")

    success_count = 0
    skip_count = 0
    
    for i, row in enumerate(rows):
        try:
            name = row[0]
            if not name: continue # Skip empty rows

            biz_type = row[1] or 'Unknown'
            status_raw = row[3]
            customer_status = 'existing' if status_raw == 'Active' else 'prospective'
            
            address = row[7]
            city = row[8]
            zip_code = row[10]

            # Geocode
            lat, lng, source = geocode(address, city, zip_code, location_cache)
            
            if source == "api":
                print(f"  📍 Geocoded ({i+1}/{len(rows)}): {name} -> {source}")
            elif source == "failed":
                print(f"  ⚠️ Location missing for: {name}")

            # Insert
            # Using database.py logic or raw sql
            # ID will be auto-generated (integer primary key) since we aren't supplying one
            # Postgres needs explicit sequence handling usually, but here we are using SQLite locally?
            # User environment is Mac, running locally. database.py handles it.
            
            c.execute('''
                INSERT INTO businesses (
                    name, address, city, zipCode, lat, lng, type, 
                    customerStatus, interactionCount, priority, 
                    contacts, visits
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                name, address, city, zip_code, lat, lng, biz_type,
                customer_status, 0, 'medium',
                '[]', '[]' # Empty JSON lists
            ))
            
            success_count += 1
            
        except Exception as e:
            print(f"❌ Error row {i}: {e}")
            skip_count += 1

    conn.commit()
    conn.close()
    
    print(f"\n✅ Import Complete!")
    print(f"   Imported: {success_count}")
    print(f"   Skipped: {skip_count}")
    print(f"   Backup: {BACKUP_FILE}")

if __name__ == "__main__":
    run_import()
