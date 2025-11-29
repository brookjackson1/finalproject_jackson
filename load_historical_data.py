"""
Load historical appointment data for revenue trend visualization
Adds 4 months of historical appointments (July - October 2025)
"""

import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def load_historical_data():
    """Load historical appointment data from add_historical_data.sql"""

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

        # Read historical data file
        with open('add_historical_data.sql', 'r', encoding='utf-8') as f:
            sql_content = f.read()

        # Remove comments and split by semicolons
        lines = sql_content.split('\n')
        clean_lines = [line for line in lines if line.strip() and not line.strip().startswith('--')]
        clean_sql = '\n'.join(clean_lines)

        statements = [stmt.strip() for stmt in clean_sql.split(';') if stmt.strip()]

        print(f"\nLoading {len(statements)} appointment records...")

        total_inserted = 0
        for i, statement in enumerate(statements, 1):
            if statement and 'INSERT INTO' in statement.upper():
                try:
                    cursor.execute(statement)
                    # Count how many rows this INSERT added
                    rows_affected = cursor.rowcount
                    total_inserted += rows_affected
                    month = ''
                    if '2025-07' in statement:
                        month = 'July 2025'
                    elif '2025-08' in statement:
                        month = 'August 2025'
                    elif '2025-09' in statement:
                        month = 'September 2025'
                    elif '2025-10' in statement:
                        month = 'October 2025'
                    print(f"  [{i}] Added {rows_affected} appointments for {month}")
                except Exception as e:
                    print(f"  [ERROR] Statement {i}: {str(e)}")

        connection.commit()
        print(f"\n{total_inserted} historical appointments loaded successfully!")

        # Display summary by month
        print("\n--- Revenue by Month ---")

        cursor.execute("""
            SELECT DATE_FORMAT(appt_date, '%Y-%m') as month,
                   COUNT(*) as appointments,
                   SUM(price) as revenue
            FROM Appointments
            WHERE status = 'completed'
            GROUP BY month
            ORDER BY month
        """)

        for row in cursor.fetchall():
            print(f"  {row[0]}: {row[1]} appointments, ${row[2]:.2f} revenue")

        cursor.close()
        connection.close()

        print("\nYour dashboard will now show a beautiful revenue trend!")
        print("Visit http://localhost:5000/dashboard to see the chart")

    except Exception as e:
        print(f"\nError loading historical data: {e}")
        return False

    return True

if __name__ == '__main__':
    print("=" * 60)
    print("NailsbyBrookJ - Historical Data Loader")
    print("=" * 60)
    load_historical_data()
