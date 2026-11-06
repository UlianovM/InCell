from typing import Tuple
from enum import Enum
import sqlite3 as sql
from sqlite3 import Connection, Cursor
import json



class CellType (int, Enum):
    IMAGE = 0



def add_cell(
        cursor: Cursor,
        cell_type: CellType,
        file_hash: str,
        ext: str,
        width: int|None,
        height: int|None,
        size: int,
        extra: dict|None) -> None:
    if extra:
        extra_str = json.dumps(extra)
    else:
        extra_str = ""

    cursor.execute(\
        "INSERT INTO cells (type, hash, ext, width, height, size, extra)"\
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (int(cell_type), file_hash, ext, width, height, size, extra_str))



def add_image(
        cursor: Cursor,
        image_hash: str,
        ext: str,
        width: int|None,
        height: int|None,
        size: int) -> None:
    add_cell(cursor, CellType.IMAGE, image_hash, ext, width, height, size, None)



def print_cells(cursor: Cursor) -> None:
    cursor.execute("SELECT * FROM cells")
    print(*cursor.fetchall(), sep="\n")



def get_source_by_hash(cursor: Cursor|Connection, cell_hash: str) -> str | None:
    result = cursor.execute("SELECT ext FROM cells WHERE hash=?", (cell_hash,)).fetchall()
    
    if not result:
        return None
    
    return f"{cell_hash}.{result[0][0]}"
