import sqlite3
from pathlib import Path
from datetime import datetime

DB = Path(__file__).with_name("maya_salon.db")

def connect():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c

def init_db():
    c = connect()
    c.execute("""CREATE TABLE IF NOT EXISTS reservations (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL, phone TEXT NOT NULL, service TEXT NOT NULL,
      date TEXT NOT NULL, time TEXT NOT NULL, note TEXT,
      status TEXT NOT NULL DEFAULT 'Pending', created_at TEXT NOT NULL
    )""")
    c.commit(); c.close()

def create_reservation(name, phone, service, date, time, note=""):
    c = connect()
    cur = c.execute("""INSERT INTO reservations
      (name,phone,service,date,time,note,created_at)
      VALUES (?,?,?,?,?,?,?)""",
      (name,phone,service,date,time,note,datetime.now().isoformat(timespec="seconds")))
    c.commit(); rid=cur.lastrowid; c.close(); return rid

def list_reservations(limit=100):
    c=connect()
    rows=c.execute("SELECT * FROM reservations ORDER BY date ASC,time ASC,id DESC LIMIT ?",(limit,)).fetchall()
    c.close(); return rows

def reservation_exists(date,time):
    c=connect()
    row=c.execute("SELECT id FROM reservations WHERE date=? AND time=? AND status!='Cancelled'",(date,time)).fetchone()
    c.close(); return row is not None
