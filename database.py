import sqlite3

TABLE = "user_codes"
con = sqlite3.connect("strava_bot.db")
cur = con.cursor()

if(cur.execute(f"SELECT name FROM sqlite_master WHERE name='{TABLE}'") is None):
    cur.execute(f"""CREATE TABLE {TABLE}
                (user_id INTEGER NOT NULL PRIMARY KEY,
                auth_code ,
                access_token)""")

def insert_val(user_id,auth_code,access_token):
    cur.execute(f"INSERT INTO {TABLE} VALUES(?,?,?)",(user_id,auth_code,access_token))