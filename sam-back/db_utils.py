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
def add_user(cursor, uid, group_id, name):
    try:
        cursor.execute('INSERT INTO users(uid, group_id, name) VALUES(?, ?, ?)',
                   (uid, group_id, name))
    except:
        cursor.execute('UPDATE users SET group_id = ? WHERE uid = ?',
                       (group_id, uid))


"""
Format of schedule_text is "1,12,17,21" to mean the user is available at
1 AM,  12 PM, 5 PM and 9 PM
"""
class Schedule():
    def __init__(self, schedule_text):
        self.available_times = list()
        for hour in schedule_text.split(','):
            self.available_times.append(hour)

def add_schedule(socket, uid, schedule):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    group_id, name  = \
    cursor.execute("SELECT group_id, name FROM users WHERE uid = ?",
                   (uid,)).fetchone()

    print("add_schedule", "group_id: ", group_id, "name: ", name)

    for hour in schedule.available_times:
        try:
            cursor.execute("DELETE FROM schedule WHERE uid = ? AND time = ? AND\
                           group_id = ?", (uid, hour, group_id))
        except:
            pass

        cursor.execute("INSERT INTO schedule(uid, date, time, group_id) \
                           VALUES(?, ?, ?, ?)", (uid, "today", hour, group_id))

        print("[group_id]", group_id, "[hour]", hour)
        others = cursor.execute("""SELECT schedule.uid, users.name FROM
                                (schedule JOIN users ON schedule.uid =
                                users.uid) WHERE schedule.group_id = ?
                                AND time = ?""", (group_id, hour)).fetchall()
        if(len(others) > 1):
            request = str(hour)
            request += " "
            for uid, name in others:
                request += str(uid) + ";" + name
                request += ","
            print(request)
            socket.sendall(request[0:-1].encode())
            print(others)

    conn.commit()
    conn.close()

