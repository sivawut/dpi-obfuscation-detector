import sqlite3
conn = sqlite3.connect("data/db.sqlite3")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS urls (url TEXT, src_ip TEXT, timestamp TEXT)")
conn.commit()
conn.close()