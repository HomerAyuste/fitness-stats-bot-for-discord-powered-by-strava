import sqlite3

TABLE = "user_codes"
con = sqlite3.connect("strava_bot.db")
cur = con.cursor()

if(cur.execute(f"SELECT name FROM sqlite_master WHERE name='{TABLE}'").fetchone() is None):
    cur.execute(f"""CREATE TABLE {TABLE}
                (user_id TEXT NOT NULL PRIMARY KEY,
                auth_code TEXT,
                access_token TEXT,
                refresh_token TEXT,
                expires_at TEXT,
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
    print("successful insert!")
    con.close()

def fetch_access_tokens(user_id):
    try:
        con = sqlite3.connect("strava_bot.db")
        cur = con.cursor()
        res = cur.execute(f"SELECT access_token, refresh_token, expires_at FROM {TABLE} WHERE user_id='?'", (user_id,))
        access_token, refresh_token, expires_at = res.fetchone()
        con.close()
        return access_token, refresh_token, expires_at
    except:
        return None

def update_tokens(user_id,access_token,refresh_token,expires_at):
    con = sqlite3.connect("strava_bot.db")
    cur = con.cursor()
    cur.execute(f'UPDATE {TABLE} SET access_token=?, refresh_token=?,expires_at=? WHERE user_id=?',
                (access_token,refresh_token,expires_at,user_id))
    con.commit()
    con.close()