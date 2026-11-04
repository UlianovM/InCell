import sqlite3 as sql
from sqlite3 import Connection, Cursor
import json
from enum import Enum
from os import getcwd
from os import path as pt



db_path = pt.join(getcwd(), "data", "cells.db")
schema_path = pt.join(getcwd(), "app", "schema.sql")



def connect() -> Connection:
    conn = sql.connect(db_path)

    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    
    with open(schema_path, 'r', encoding="UTF-8") as schema:
        conn.executescript(schema.read())

    return conn



class CellType (Enum):
    IMAGE = 0

    def __int__(self):
        return self.value



def add_cell(
        cursor: Cursor,
        cell_type: CellType,
        file_hash: str,
        ext: str,
        width: int|None,
        height: int|None,
        size: int,
        extra: dict|None) -> Cursor:
    if extra:
        extra_str = json.dumps(extra)
    else:
        extra_str = ""

    return cursor.execute(\
        "INSERT INTO cells (type, hash, ext, width, height, size, extra)"\
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (int(cell_type), file_hash, ext, width, height, size, extra_str))

def add_image(
        cursor: Cursor,
        image_hash: str,
        ext: str,
        width: int|None,
        height: int|None,
        size: int) -> Cursor:
    return add_cell(cursor, CellType.IMAGE, image_hash, ext, width, height, size, None)

def print_cells(cursor: Cursor):
    ...



if __name__ == "__main__":
    conn = connect()
