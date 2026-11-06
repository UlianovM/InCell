import sqlite3 as sql
from sqlite3 import Connection
from flask import g
from os import getcwd
from os import path as pt



db_path = pt.join(getcwd(), "data", "cells.db")
schema_path = pt.join(getcwd(), "app", "schema.sql")



def init_conn() -> None:
    conn = sql.connect(db_path)
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA foreign_keys = ON")

    with open(schema_path, 'r', encoding="UTF-8") as schema:
        conn.executescript(schema.read())
    
    # conn.cursor().execute("DROP TABLE cells;")
    conn.close()



def get_conn() -> Connection:
    if "db" not in g:
        g.db = sql.connect(db_path)
        g.db.row_factory = sql.Row
        g.db.autocommit = True
        g.db.execute("PRAGMA foreign_keys = ON")

    return g.db



def close_conn() -> None:
    db = g.pop("db", None)

    if db is not None:
        db.close()
