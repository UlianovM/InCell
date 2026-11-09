from sqlite3 import connect, Cursor, Connection, Row
from flask import g
from os import getcwd
from os import path as pt



db_path = pt.join(getcwd(), "data", "cells.db")
schema_path = pt.join(getcwd(), "app", "schema.sql")



def init_conn() -> None:
    """Инициалиализация базы данных"""
    conn = connect(db_path)
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA foreign_keys = ON")
    
    # conn.cursor().execute("DROP TABLE cells;")

    with open(schema_path, 'r', encoding="UTF-8") as schema:
        conn.executescript(schema.read())
    conn.close()



def get_raw_conn() -> Connection:
    """Создаёт обычное подключение"""
    conn = connect(db_path)
    conn.row_factory = Row
    conn.autocommit = True
    conn.execute("PRAGMA foreign_keys = ON")
    return conn



def get_conn() -> Connection:
    """Открывает подключение для контекста запроса"""
    if "db" not in g:
        g.db = connect(db_path)
        g.db.row_factory = Row
        g.db.autocommit = True
        g.db.execute("PRAGMA foreign_keys = ON")

    return g.db



def close_conn() -> None:
    """Закрывает подключение для контекста запроса"""
    db = g.pop("db", None)

    if db is not None:
        db.close()



if __name__ == "__main__":
    init_conn()