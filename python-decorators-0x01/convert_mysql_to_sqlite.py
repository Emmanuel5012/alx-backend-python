import sqlite3
import mysql.connector

mysql_conn = mysql.connector.connect(
    host="localhost",
    user="alx_prodev",
    password="",
    database="alx_prodev",
    port=3306
)

mysql_cursor = mysql_conn.cursor()
mysql_cursor.execute("SELECT * FROM users")
rows = mysql_cursor.fetchall()

#Step 2: Connect to SQLite
sqlite_conn = sqlite3.connect('users.db')
sqlite_cursor = sqlite_conn.cursor()

#Step 3: Create the same table
sqlite_cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL
    )
""")


# Step 4: Insert data into SQLite
sqlite_cursor.executemany("INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?)", rows)

# Step 5: Save and close both connections
sqlite_conn.commit()
sqlite_conn.close()
mysql_conn.close()

print("✅ Data migrated from MySQL to SQLite.")