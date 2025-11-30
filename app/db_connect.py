import pymysql
import pymysql.cursors
from flask import g
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

def get_db():
    if 'db' not in g or not is_connection_open(g.db):
        print("Re-establishing closed database connection.")
        try:
            # Check if JAWSDB_URL exists (Heroku deployment)
            jawsdb_url = os.getenv('JAWSDB_URL')

            if jawsdb_url:
                # Parse JawsDB URL format: mysql://username:password@hostname:port/database
                print("Using JawsDB connection")
                url = urlparse(jawsdb_url)
                print(f"Connecting to JawsDB at {url.hostname}")
                g.db = pymysql.connect(
                    host=url.hostname,
                    user=url.username,
                    password=url.password,
                    database=url.path[1:],  # Remove leading '/'
                    port=url.port or 3306,
                    cursorclass=pymysql.cursors.DictCursor
                )
                print("JawsDB connection successful")
            else:
                # Use individual environment variables (local development)
                print("JAWSDB_URL not found, using local database connection")
                db_host = os.getenv('DB_HOST')
                if not db_host:
                    print("ERROR: Neither JAWSDB_URL nor DB_HOST is set!")
                    g.db = None
                    return None
                print(f"Connecting to local database at {db_host}")
                g.db = pymysql.connect(
                    host=db_host,
                    user=os.getenv('DB_USER'),
                    password=os.getenv('DB_PASSWORD'),
                    database=os.getenv('DB_NAME'),
                    port=int(os.getenv('DB_PORT', 3306)),
                    cursorclass=pymysql.cursors.DictCursor
                )
                print("Local database connection successful")
        except Exception as e:
            print(f"Database connection failed: {e}")
            print(f"Exception type: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            g.db = None
            return None
    return g.db

def is_connection_open(conn):
    try:
        conn.ping(reconnect=True)  # PyMySQL's way to check connection health
        return True
    except:
        return False

def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None and not db._closed:
        print("Closing database connection.")
        db.close()