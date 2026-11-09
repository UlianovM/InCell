from .cell import CellType, Cell
from PIL import Image
from hashlib import sha256
from os.path import getsize, split
from json import dumps



MIB = 1024 * 1024
WHITELIST = ["png", "jpeg"]



def validate_image_file(fullpath: str) -> bool:
    """
    Проверяет реальный формат изображения.
    Возвращает реальный тип файла, или `None` если файл вне белого списка
    """
    with Image.open(fullpath) as img:
        ext = str(img.format).lower() 
    return ext in WHITELIST



def generate_thumbnail(image_fullpath: str) -> Image.Image:
    """Создаёт лёгкую миниатюру для изображения"""
    with Image.open(image_fullpath) as img:
        img.thumbnail((480, 960), Image.Resampling.LANCZOS)
        result = img.copy()
    
    return result



def calculate_hash(fullpath: str) -> str:
    """Считает sha256 hash, загружая изображение в память не полностью"""
    result = sha256()

    with open(fullpath, "rb") as binary:
        while chunk := binary.read(MIB):
            result.update(chunk)

    return result.hexdigest()



def handle_image(image_fullpath: str) -> Cell:
    """Собирает и форматирует информацию для занесения в базу данных"""
    image_hash = calculate_hash(image_fullpath)
    
    with Image.open(image_fullpath) as img:
        ext = str(img.format).lower()
        w, h = img.size
    
    weight = getsize(image_fullpath)
    extra = dumps({
        "filename": split(image_fullpath)[1]
    })

    return Cell(CellType.IMAGE, image_hash, ext, w, h, weight, extra)
