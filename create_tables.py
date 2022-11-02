import sqlite3
conn = sqlite3.connect("data.db")
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS tables")
cur.execute("CREATE TABLE tables_input(timestamp DATETIME, x interger, y interger, z interger, v interger)")
conn.close()
