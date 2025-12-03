# test_db.py
import sqlite3

conn = sqlite3.connect("test.db")
conn.execute("CREATE TABLE IF NOT EXISTS test (msg TEXT)")
conn.execute("INSERT INTO test (msg) VALUES (?)", ("Hello DB!",))
conn.commit()

cursor = conn.execute("SELECT msg FROM test")
print(cursor.fetchone()[0])  

conn.close()