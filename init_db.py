"""
Database initialization script for NailsbyBrookJ
Reads schema.sql and executes it against the database
"""

import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def init_database():
    """Initialize the database with the schema"""

    # Database connection parameters from .env
    db_config = {
        'host': os.getenv('DB_HOST'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME'),
        'port': int(os.getenv('DB_PORT', 3306))
    }

    print(f"Connecting to database: {db_config['database']} at {db_config['host']}")

    try:
        # Connect to database
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()

        print("Connected successfully!")

        # Read schema file
        with open('schema.sql', 'r') as f:
            schema_sql = f.read()

        # Split by semicolons and execute each statement
        statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]

        print(f"\nExecuting {len(statements)} SQL statements...")

        for i, statement in enumerate(statements, 1):
            if statement:
                try:
                    cursor.execute(statement)
                    # Check if it's a CREATE TABLE or INSERT statement
                    if 'CREATE TABLE' in statement.upper():
                        table_name = statement.split('CREATE TABLE')[1].split('(')[0].strip()
                        print(f"  [{i}] Created table: {table_name}")
                    elif 'INSERT INTO' in statement.upper():
                        table_name = statement.split('INSERT INTO')[1].split('(')[0].strip()
                        print(f"  [{i}] Inserted data into: {table_name}")
                    elif 'DROP TABLE' in statement.upper():
                        print(f"  [{i}] Dropped table (if exists)")
                    else:
                        print(f"  [{i}] Executed statement")
                except Exception as e:
                    print(f"  [ERROR] Statement {i}: {str(e)}")
                    print(f"  Statement: {statement[:100]}...")

        connection.commit()
        print("\nDatabase initialized successfully!")

        # Display table counts
        print("\n--- Database Summary ---")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        for (table_name,) in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"  {table_name}: {count} rows")

        cursor.close()
        connection.close()

        print("\nDatabase connection closed.")

    except Exception as e:
        print(f"\nError initializing database: {e}")
        return False

    return True

if __name__ == '__main__':
    print("=" * 50)
    print("NailsbyBrookJ - Database Initialization")
    print("=" * 50)
    init_database()
