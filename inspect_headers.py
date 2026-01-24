
import openpyxl
import sys

def inspect_headers(file_path):
    try:
        wb = openpyxl.load_workbook(file_path, read_only=True)
        sheet = wb.active
        # Get first row
        # Get first 5 rows
        for i, row in enumerate(sheet.iter_rows(min_row=1, max_row=5)):
            row_values = [cell.value for cell in row]
            print(f"Row {i+1}: {row_values}")
    except Exception as e:
        print(f"Error reading file: {e}")

if __name__ == "__main__":
    inspect_headers("Joel's Recently Updated Accounts (1).xlsx")
