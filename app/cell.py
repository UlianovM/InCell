from typing import NamedTuple, Optional
from enum import Enum



class CellType (int, Enum):
    IMAGE = 0
    ...



class Cell (NamedTuple):
    type: CellType
    hash: str
    ext: str
    width: int|None
    height: int|None
    weight: int
    extra: str|None
