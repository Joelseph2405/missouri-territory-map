import openpyxl
import sqlite3
import sys
import os

DB_PATH = 'businesses.db'
EXCEL_FILE = "Joel's Recently Updated Accounts (1).xlsx"

def ingest_excel():
    if not os.path.exists(EXCEL_FILE):
        print(f"❌ Error: File '{EXCEL_FILE}' not found.")
        return

    print(f"Reading {EXCEL_FILE}...")
    
    try:
        wb = openpyxl.load_workbook(EXCEL_FILE, read_only=True)
        sheet = wb.active
        
        # Headers are on row 2
        # Data starts on row 3
        
        headers = {} # Map header name to column index (0-based)
        rows_iter = sheet.iter_rows(min_row=2)
        
        # Get Headers
        header_row = next(rows_iter)
        for i, cell in enumerate(header_row):
            if cell.value:
                headers[cell.value.strip()] = i
        
        print(f"Headers found: {list(headers.keys())}")
        
        # Required columns check
        required = ['Account Name', 'Physical Address (Street)', 'Physical Address (City)', 'Physical Address (ZIP/Postal Code)']
        for r in required:
            if r not in headers:
                print(f"❌ Missing required column: {r}")
                return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        count_added = 0
        count_updated = 0
        count_skipped = 0
        
        for row in rows_iter:
            # Row is a tuple of cells
            # Helper to get value by header name
            def get_val(header_name):
                idx = headers.get(header_name)
                if idx is not None and idx < len(row):
                    val = row[idx].value
                    return str(val).strip() if val is not None else ''
                return ''

            name = get_val('Account Name')
            if not name:
                continue

            address = get_val('Physical Address (Street)')
            city = get_val('Physical Address (City)')
            zip_code = get_val('Physical Address (ZIP/Postal Code)')
            
            employees_str = get_val('Employee Count - This Location')
            try:
                employees = int(float(employees_str)) if employees_str else 0
            except ValueError:
                employees = 0
                
            industry = get_val('Account Segment')
            
            raw_status = get_val('Account Status')
            status = 'unknown'
            if raw_status.lower() == 'active':
                status = 'existing'
            elif raw_status:
                status = raw_status.lower()

            # Lat/Lng are not in this file, default to 0.0
            lat = 0.0
            lng = 0.0

            # Check for existing business by Name
            cursor.execute("SELECT id FROM businesses WHERE name = ?", (name,))
            existing = cursor.fetchone()

            if existing:
                # UPDATE
                bid = existing[0]
                cursor.execute("""
                    UPDATE businesses SET 
                        address=?, city=?, zipCode=?, 
                        type=?, customerStatus=?, employees=?
                    WHERE id=?
                """, (address, city, zip_code, industry, status, employees, bid))
                count_updated += 1
            else:
                # INSERT
                cursor.execute("""
                    INSERT INTO businesses (name, address, city, zipCode, lat, lng, type, customerStatus, employees, interactionCount)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
                """, (name, address, city, zip_code, lat, lng, industry, status, employees))
                count_added += 1

        conn.commit()
        conn.close()
        print(f"✅ Import Complete! Added: {count_added}, Updated: {count_updated}")

    except Exception as e:
        print(f"❌ Error during import: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    ingest_excel()
