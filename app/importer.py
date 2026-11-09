from .connection import get_raw_conn, Cursor, Connection
from .images import WHITELIST as IMGS_WHITELIST
from .images import handle_image, generate_thumbnail, validate_image_file
from .requests import add_cell
from typing import List
from os import getcwd, walk
from os import path as pt
from shutil import copy2 as copy_with_meta



PWD = getcwd()
DATA_PATH = pt.abspath(pt.join(PWD, "data"))
SOURCE_PATH = pt.join(DATA_PATH, "source")
THUMBNAIL_PATH = pt.join(DATA_PATH, "thumbnail")
IMPORT_PATH = pt.join(DATA_PATH, "import")



def _files_in_dir(path: str) -> List[str]:
    return sorted(walk(path).__next__()[2])

def _file_ext(filename: str) -> str|None:
    return pt.splitext(filename)[1].replace(".", "")



def _import_image(cursor: Cursor | Connection, fullpath: str) -> None:
    cell = handle_image(fullpath)
    source_path = pt.join(SOURCE_PATH, f"{cell.hash}.{cell.ext}")
    thumbnail_filename = f"{cell.hash}.webp"
    thumbnail_path = pt.join(THUMBNAIL_PATH, thumbnail_filename)
    
    thumbnail = generate_thumbnail(fullpath)

    # TODO check is hash in source/ and thumbnail/

    copy_with_meta(fullpath, source_path)
    thumbnail.save(thumbnail_path, format="webp", quality=75)
    
    add_cell(cursor, cell)



def import_files(dir_path: str) -> ...:
    """Импортирует все файлы из указанной директории. Игнорирует дочерние папки"""
    conn = get_raw_conn()
    files = _files_in_dir(dir_path)
    
    for filename in files:
        fullpath = pt.join(dir_path, filename)
        ext = _file_ext(filename)

        if not ext:
            print(f"The file extension is not specified; File: \"{filename}\"")
            continue

        if ext in IMGS_WHITELIST:
            if not validate_image_file(fullpath):
                print(f"The file extension is specified incorrectly; File: \"{filename}\"")
                continue

            _import_image(conn, fullpath)
        # elif ext in ward.animated.WHITELIST:
        #     ...
        # elif ext in ward.text.WHITELIST:
        #     ...
        else:
            print(f"Unsupported file type: {ext}; File: \"{filename}\"")

    conn.close()



import_files(IMPORT_PATH)
