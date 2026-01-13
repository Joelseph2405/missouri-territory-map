import sqlite3
import csv
import sys

DB_PATH = 'businesses.db'
DATA_FILE = 'upload.txt'

def ingest_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print(f"Reading {DATA_FILE}...")
    
    count_added = 0
    count_updated = 0
    
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            # Check if likely tab or comma separated
            first_line = f.readline()
            f.seek(0)
            
            delimiter = '\t'
            if '\t' not in first_line and ',' in first_line:
                delimiter = ','
            
            reader = csv.DictReader(f, delimiter=delimiter)
            
            # Normalize headers (strip whitespace)
            reader.fieldnames = [name.strip() for name in reader.fieldnames]
            print(f"Columns found: {reader.fieldnames}")

            for row in reader:
                # Extract fields
                # Mapping: 'Type', 'Business Name', 'Address', 'City', 'State', 'Zip Code', 'Industry', 'Employees Here', 'Longitude', 'Latitude'
                
                raw_type = row.get('Type', '').strip()
                name = row.get('Business Name', '').strip()
                address = row.get('Address', '').strip()
                city = row.get('City', '').strip()
                state = row.get('State', '').strip()
                zip_code = row.get('Zip Code', '').strip()
                industry = row.get('Industry', '').strip()
                employees = row.get('Employees Here', '0').strip()
                lng = row.get('Longitude', '0')
                lat = row.get('Latitude', '0')

                if not name:
                    continue

                # Normalization
                status = 'unknown'
                if 'xisting' in raw_type or 'Existing' in raw_type:
                    status = 'existing'
                elif 'rospect' in raw_type or 'Prospective' in raw_type:
                    status = 'prospective'
                
                # Check for existing business by Name
                cursor.execute("SELECT id FROM businesses WHERE name = ?", (name,))
                existing = cursor.fetchone()

                if existing:
                    # UPDATE
                    bid = existing[0]
                    cursor.execute("""
                        UPDATE businesses SET 
                            address=?, city=?, zipCode=?, 
                            lat=?, lng=?, 
                            type=?, customerStatus=?, employees=?
                        WHERE id=?
                    """, (address, city, zip_code, lat, lng, industry, status, employees, bid))
                    count_updated += 1
                else:
                    # INSERT
                    cursor.execute("""
                        INSERT INTO businesses (name, address, city, zipCode, lat, lng, type, customerStatus, employees, interactionCount)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
                    """, (name, address, city, zip_code, lat, lng, industry, status, employees))
                    count_added += 1

        conn.commit()
        print(f"✅ Success! Added: {count_added}, Updated: {count_updated}")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    ingest_data()
