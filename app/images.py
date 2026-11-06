import os
import hashlib
from PIL import Image
import database as db
from shutil import copy2 as copy_original



MIB = 1024 * 1024

pt = os.path
pwd = os.getcwd()

data_path = pt.abspath(pt.join(pwd, "data"))

import_path = pt.join(data_path, "import")
source_path = pt.join(data_path, "source")
webp_path = pt.join(data_path, "webp")



def _calculate_hash(fullpath: str) -> str:
    result = hashlib.sha256()

    with open(fullpath, "rb") as binary:
        while chunk := binary.read(MIB):
            result.update(chunk)

    return result.hexdigest()



def _import_image(conn: db.Connection, path: str, filename: str):
    fullpath = pt.join(path, filename)

    with Image.open(fullpath) as img:
        img_hash = hashlib.sha256(img.tobytes()).hexdigest()
        ext = str(img.format).lower()
        hash_filename = img_hash + '.' + ext
        
        if not pt.exists( pt.join(source_path, hash_filename)):
            hash_fullpath = pt.join(source_path, hash_filename)

            # TODO
            # db.add_image(conn.cursor(), img_hash, ext, img.width, img.height, pt.getsize(fullpath))
            # copy_original(fullpath, hash_fullpath)
            # print("Added", repr(hash_filename), "by importing", repr(filename))
        else:
            print(filename, "already exists")



def import_all(path):
    conn = db.get_conn()
    path, dirs, files = os.walk(path).__next__()

    files.sort()

    for filename in files:
        _import_image(conn, path, filename)

    db.close_conn()



import_all(import_path)
