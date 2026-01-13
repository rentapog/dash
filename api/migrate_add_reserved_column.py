import sqlite3

DB_PATH = 'local_seobrain.db'

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Add 'reserved' column to users table if it doesn't exist
try:
    cursor.execute("ALTER TABLE user ADD COLUMN reserved INTEGER DEFAULT 0")
    print("Column 'reserved' added to user table.")
except sqlite3.OperationalError as e:
    if 'duplicate column name' in str(e):
        print("Column 'reserved' already exists.")
    else:
        print(f"Error: {e}")

conn.commit()
conn.close()
