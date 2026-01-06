import os
import sys

# Ensure dependencies are loaded
try:
    import psycopg2
except ImportError:
    print("❌ Critical Error: psycopg2 is not installed.")
    print("Please wait for the 'pip install' command to finish, then try again.")
    sys.exit(1)

import database

print("\n" + "="*50)
print("  SUPABASE CONNECTION TESTER  ")
print("="*50)
print("Paste your Supabase Connection String below.")
print("It looks like: postgresql://postgres.abc:password@aws-0...:5432/postgres")
print("="*50 + "\n")

url = input("Connection String > ").strip()

# Set environment variable for this session
os.environ['DATABASE_URL'] = url

print("\n🔄 Attempting to connect...")

try:
    # Force engine check
    if database.get_engine() != 'postgres':
        print("❌ Error: Script failed to detect Postgres mode. (Internal logic error?)")
        sys.exit(1)

    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT version();")
    version = c.fetchone()
    
    print("\n✅ SUCCESS! Connected successfully.")
    print(f"Server version: {version['version'][:50]}...")
    print("\nNext Step: This URL is correct. Go paste it into Render!")
    
    conn.close()

except Exception as e:
    print("\n❌ CONNECTION FAILED")
    print("-" * 20)
    print(e)
    print("-" * 20)
    print("\nCommon fixes:")
    print("1. Did you replace [YOUR-PASSWORD] with your real password?")
    print("2. Are there brackets [] around the password? Remove them!")
    print("3. Did you select 'Session Mode' (port 5432)?")
