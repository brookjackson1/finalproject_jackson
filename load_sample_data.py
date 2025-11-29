"""
Load sample data into NailsbyBrookJ database
Run this after init_db.py to populate with demo data
"""

import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def load_sample_data():
    """Load sample data from sample_data.sql"""

    # Database connection parameters
    db_config = {
        'host': os.getenv('DB_HOST'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME'),
        'port': int(os.getenv('DB_PORT', 3306))
    }

    print(f"Connecting to database: {db_config['database']} at {db_config['host']}")

    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()

        print("Connected successfully!")

        # Read sample data file
        with open('sample_data.sql', 'r', encoding='utf-8') as f:
            sql_content = f.read()

        # Remove comments and split by semicolons
        lines = sql_content.split('\n')
        clean_lines = [line for line in lines if line.strip() and not line.strip().startswith('--')]
        clean_sql = '\n'.join(clean_lines)

        statements = [stmt.strip() for stmt in clean_sql.split(';') if stmt.strip()]

        print(f"\nLoading {len(statements)} data statements...")

        for i, statement in enumerate(statements, 1):
            if statement and not statement.startswith('--'):
                try:
                    cursor.execute(statement)
                    if 'INSERT INTO' in statement.upper():
                        table_name = statement.split('INSERT INTO')[1].split('(')[0].strip()
                        print(f"  [{i}] Loaded data into: {table_name}")
                except Exception as e:
                    print(f"  [ERROR] Statement {i}: {str(e)}")

        connection.commit()
        print("\nSample data loaded successfully!")

        # Display summary
        print("\n--- Database Summary ---")

        cursor.execute("SELECT COUNT(*) FROM Clients")
        print(f"  Clients: {cursor.fetchone()[0]} records")

        cursor.execute("SELECT COUNT(*) FROM Appointments")
        print(f"  Appointments: {cursor.fetchone()[0]} records")

        cursor.execute("SELECT COUNT(*) FROM PortfolioPhotos")
        print(f"  Portfolio Photos: {cursor.fetchone()[0]} records")

        cursor.execute("SELECT COUNT(*) FROM LoyaltyPoints")
        print(f"  Loyalty Points: {cursor.fetchone()[0]} records")

        cursor.execute("SELECT COUNT(*) FROM ServiceItems")
        print(f"  Service-Inventory Links: {cursor.fetchone()[0]} records")

        cursor.close()
        connection.close()

        print("\nYour app now has realistic demo data!")
        print("Visit http://localhost:5000 to see it in action")

    except Exception as e:
        print(f"\nError loading sample data: {e}")
        return False

    return True

if __name__ == '__main__':
    print("=" * 60)
    print("NailsbyBrookJ - Sample Data Loader")
    print("=" * 60)
    load_sample_data()
