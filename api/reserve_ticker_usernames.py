import sqlite3

# List of reserved usernames for the ticker
reserved_usernames = [
    'pogTitan', 'empirePro', 'starterGuy', 'basicQueen', 'proMax', 'eliteWolf', 'titanMaster',
    'advancedHero', 'titanLegend', 'megaTitan', 'empireKing', 'proUser99', 'eliteStar', 'titanElite',
    'starterAce', 'basicChamp', 'advancedGuru', 'titanPower', 'empireBoss', 'proChamp', 'eliteChamp',
    'titanForce', 'starterPro', 'basicHero', 'advancedChamp', 'titanChamp'
]

# Path to your SQLite database
DB_PATH = 'local_seobrain.db'

# Connect to the database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Ensure the users table has a 'reserved' column (boolean)
cursor.execute('''
    ALTER TABLE users ADD COLUMN reserved INTEGER DEFAULT 0
''')

# Insert reserved usernames if not already present
for username in reserved_usernames:
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, reserved) VALUES (?, 1)
    ''', (username,))

conn.commit()
conn.close()

print('Reserved usernames added to the database.')
