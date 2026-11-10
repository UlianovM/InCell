from .cell import Cell
from typing import List
from sqlite3 import Connection, Cursor, Row



def add_cell(cursor: Cursor|Connection, cell: Cell) -> None:
    command = "INSERT INTO cells (type, hash, ext, width, height, weight, extra) "\
        "VALUES (?, ?, ?, ?, ?, ?, ?)"
    cursor.execute(command, cell)



def gat_cells(cursor: Cursor) -> List[Row]:
    return cursor.execute("SELECT hash, width, height, extra FROM cells").fetchall()



def print_cells(cursor: Cursor) -> None:
    cursor.execute("SELECT * FROM cells")
    print(*cursor.fetchall(), sep="\n")



def get_source_ext(cursor: Cursor|Connection, cell_hash: str) -> str | None:
    result = cursor.execute("SELECT ext FROM cells WHERE hash=?", (cell_hash,)).fetchall()
    
    if not result:
        return None
    
    return f"{cell_hash}.{result[0][0]}"
