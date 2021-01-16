"""
Group of functions for handling the communication with the database
"""
import sqlite3

DB = "db/data.db"

def conn_db(func):
    def tmp(*args, **kwargs):
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()
        func(cursor, *args, **kwargs)
        conn.commit()
        conn.close()
    return tmp

@conn_db
def add_user(cursor, uid, name):
    cursor.execute('INSERT INTO users(uid, name) VALUES(?, ?)', (uid, name))


