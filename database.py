import sqlite3

con = sqlite3.connect("strava_bot.db")
cur = con.cursor()

if(cur.execute("SELECT name FROM sqlite_master WHERE name=''") is None):
    cur.execute("CREATE TABLE ")