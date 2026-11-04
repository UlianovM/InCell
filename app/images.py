import os
import hashlib
from PIL import Image
import database



pt = os.path
pwd = os.getcwd()

data_path = pt.abspath(pt.join(pwd, "data"))

import_path = pt.join(data_path, "import")
source_path = pt.join(data_path, "source")
webp_path = pt.join(data_path, "webp")



def _import_image(conn: database.Connection, path: str, filename: str):
    fullpath = pt.join(path, filename)
    img = Image.open(fullpath)
    img_hash = hashlib.sha256(img.tobytes()).hexdigest()
    hash_filename = img_hash + '.' + str(img.format).lower()
    
    if not pt.exists( pt.join(source_path, hash_filename)):
        ext = pt.splitext(filename)[1]
        hash_fullpath = pt.join(source_path, hash_filename)

        database.add_image(conn.cursor(), img_hash, ext, img.width, img.height, pt.getsize(fullpath))
        img.save(hash_fullpath)
        print("Added", repr(hash_filename), "by importing", repr(filename))
    else:
        print(filename, "already exists")



def import_all(path):
    conn = database.connect()
    path, dirs, files = os.walk(path).__next__()

    files.sort()

    for filename in files:
        _import_image(conn, path, filename)



import_all(import_path)
