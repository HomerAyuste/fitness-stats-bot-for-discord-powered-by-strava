import sqlite3

TABLE = "user_codes"
con = sqlite3.connect("strava_bot.db")
cur = con.cursor()

if(cur.execute(f"SELECT name FROM sqlite_master WHERE name='{TABLE}'").fetchone() is None):
    cur.execute(f"""CREATE TABLE {TABLE}
                (user_id TEXT NOT NULL PRIMARY KEY,
                auth_code TEXT,
                access_token TEXT,
                UNIQUE(user_id,auth_code))""")
con.close()

def insert_val(user_id,auth_code,access_token):
    con = sqlite3.connect("strava_bot.db")
    cur = con.cursor()
    if(not(cur.execute(f"SELECT * FROM {TABLE} WHERE name=?",(user_id,)).fetchall() is None)):
        cur.execute(f"DELETE FROM {TABLE} WHERE name=?", (user_id,))
        cur.commit()
    cur.execute(f"INSERT INTO {TABLE} VALUES(?,?,?)",(user_id,auth_code,access_token,))
    con.commit()
    con.close()

def fetch_access_token(user_id):
    con = sqlite3.connect("strava_bot.db")
    cur = con.cursor()
    res = cur.execute(f"SELECT access_token FROM {TABLE} WHERE user_id='?'", (user_id,))
    access_token = res.fetchone()
    con.close()
    return access_token