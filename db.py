import os
import sqlite3
from pathlib import Path
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
SQLITE_DB = Path(__file__).with_name("maya_salon.db")

def _is_postgres():
    return DATABASE_URL.startswith(("postgres://", "postgresql://"))

def connect():
    if _is_postgres():
        import psycopg
        from psycopg.rows import dict_row

        url = DATABASE_URL
        if url.startswith("postgres://"):
            url = "postgresql://" + url[len("postgres://"):]
        return psycopg.connect(url, row_factory=dict_row)

    c = sqlite3.connect(SQLITE_DB)
    c.row_factory = sqlite3.Row
    return c

def init_db():
    c = connect()
    if _is_postgres():
        c.execute("""CREATE TABLE IF NOT EXISTS reservations (
          id BIGSERIAL PRIMARY KEY,
          name TEXT NOT NULL,
          phone TEXT NOT NULL,
          service TEXT NOT NULL,
          date TEXT NOT NULL,
          time TEXT NOT NULL,
          note TEXT,
          status TEXT NOT NULL DEFAULT 'Pending',
          created_at TEXT NOT NULL
        )""")
    else:
        c.execute("""CREATE TABLE IF NOT EXISTS reservations (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,
          phone TEXT NOT NULL,
          service TEXT NOT NULL,
          date TEXT NOT NULL,
          time TEXT NOT NULL,
          note TEXT,
          status TEXT NOT NULL DEFAULT 'Pending',
          created_at TEXT NOT NULL
        )""")
    c.commit()
    c.close()

def create_reservation(name, phone, service, date, time, note=""):
    c = connect()
    now = datetime.now().isoformat(timespec="seconds")
    if _is_postgres():
        cur = c.execute(
            """INSERT INTO reservations
            (name, phone, service, date, time, note, created_at)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            RETURNING id""",
            (name, phone, service, date, time, note, now)
        )
        rid = cur.fetchone()["id"]
    else:
        cur = c.execute(
            """INSERT INTO reservations
            (name, phone, service, date, time, note, created_at)
            VALUES (?,?,?,?,?,?,?)""",
            (name, phone, service, date, time, note, now)
        )
        rid = cur.lastrowid
    c.commit()
    c.close()
    return rid

def list_reservations(limit=100):
    c = connect()
    if _is_postgres():
        rows = c.execute(
            """SELECT id, name, phone, service, date, time, note, status, created_at
            FROM reservations
            ORDER BY date ASC, time ASC, id DESC
            LIMIT %s""", (limit,)
        ).fetchall()
    else:
        rows = c.execute(
            """SELECT * FROM reservations
            ORDER BY date ASC, time ASC, id DESC
            LIMIT ?""", (limit,)
        ).fetchall()
    c.close()
    return rows

def reservation_exists(date, time):
    c = connect()
    if _is_postgres():
        row = c.execute(
            """SELECT id FROM reservations
            WHERE date=%s AND time=%s AND status <> 'Cancelled'
            LIMIT 1""", (date, time)
        ).fetchone()
    else:
        row = c.execute(
            """SELECT id FROM reservations
            WHERE date=? AND time=? AND status!='Cancelled'
            LIMIT 1""", (date, time)
        ).fetchone()
    c.close()
    return row is not None
