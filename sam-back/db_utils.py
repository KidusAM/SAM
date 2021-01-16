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

"""
Format of schedule_text is "1,12,17,21" to mean the user is available at
1 AM,  12 PM, 5 PM and 9 PM
"""
class Schedule():
    def __init__(self, schedule_text):
        self.available_times = list()

        for hour in schedule_text.split(','):
            self.available_times.append(hour)

@conn_db
def add_schedule(cursor, uid, group_id, schedule):
    for hour in schedule.available_times:
        cursor.execute("INSERT INTO schedule(uid, date, time, group_id) \
                       VALUES(?, ?, ?, ?)", (uid, "today", hour, group_id))

