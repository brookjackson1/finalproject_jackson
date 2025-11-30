"""
Setup script to load schema into JawsDB MySQL on Heroku
Run this to initialize your Heroku database with the required schema and data
"""

import pymysql
import os
from urllib.parse import urlparse

# Get JawsDB URL from environment or manual input
jawsdb_url = input("Paste your JAWSDB_URL here (from Heroku config vars): ").strip()

# Parse the URL
url = urlparse(jawsdb_url)

print(f"\nConnecting to JawsDB at {url.hostname}...")

try:
    # Connect to database
    connection = pymysql.connect(
        host=url.hostname,
        user=url.username,
        password=url.password,
        database=url.path[1:],  # Remove leading '/'
        port=url.port or 3306
    )

    cursor = connection.cursor()
    print("[OK] Connected successfully!")

    # Load schema
    print("\n1. Loading database schema...")
    with open('schema.sql', 'r', encoding='utf-8') as f:
        schema_sql = f.read()

    # Split by semicolon and execute each statement
    statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]

    for i, statement in enumerate(statements, 1):
        try:
            cursor.execute(statement)
            print(f"   [OK] Executed statement {i}/{len(statements)}")
        except Exception as e:
            print(f"   [ERROR] Error on statement {i}: {e}")

    connection.commit()
    print("[OK] Schema loaded successfully!")

    # Load sample data
    print("\n2. Loading sample data...")
    try:
        with open('sample_data.sql', 'r', encoding='utf-8') as f:
            data_sql = f.read()

        statements = [stmt.strip() for stmt in data_sql.split(';') if stmt.strip()]

        for i, statement in enumerate(statements, 1):
            try:
                cursor.execute(statement)
            except Exception as e:
                print(f"   [ERROR] Error on statement {i}: {e}")

        connection.commit()
        print("[OK] Sample data loaded successfully!")
    except FileNotFoundError:
        print("   (No sample_data.sql file found, skipping)")

    # Verify tables were created
    print("\n3. Verifying tables...")
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    print(f"\n   Found {len(tables)} tables:")
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) as count FROM {table[0]}")
        count = cursor.fetchone()[0]
        print(f"   [OK] {table[0]} ({count} rows)")

    cursor.close()
    connection.close()

    print("\n" + "="*50)
    print("SUCCESS! Your JawsDB database is ready!")
    print("="*50)
    print("\nYou can now deploy your Heroku app.")

except Exception as e:
    print(f"\n[ERROR] Error: {e}")
    print("\nMake sure you:")
    print("1. Copied the full JAWSDB_URL from Heroku config vars")
    print("2. Have schema.sql in the current directory")
