import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

server = 'postcard-server-123.database.windows.net'
database = 'postcard-db'
username = 'sqladmin'
password = 'Rty567jkl90'
driver = '{ODBC Driver 18 for SQL Server}'

print(f"Connecting to {server}...")

try:
    conn = pyodbc.connect(
        f'DRIVER={driver};SERVER=tcp:{server},1433;DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
    )
    print("Connection successful!")
    cursor = conn.cursor()
    cursor.execute("SELECT @@VERSION")
    row = cursor.fetchone()
    print(f"Server version: {row[0]}")
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")
