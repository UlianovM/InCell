import app.connection as cons
import app.requests as req
from typing import List, Tuple
from flask import Flask, Response, g, render_template, url_for, send_from_directory, abort
from random import shuffle
import os



pt = os.path
pwd = os.getcwd()

data_path = pt.abspath(pt.join(pwd, "data"))

source_path = pt.join(data_path, "source")
thumbnail_path = pt.join(data_path, "thumbnail")



app = Flask(__name__, static_folder="web", template_folder="templates")
cons.init_conn()



@app.route("/")
def main():
    conn = cons.get_conn()
    result = req.gat_cells(conn.cursor())
    shuffle(result)

    return render_template("index.html", cells=result)



@app.route("/source/<image_hash>")
def get_sorce(image_hash: str) -> Response:
    cons.get_conn()

    image_path = req.get_source_ext(g.db, image_hash)
    
    if image_path is None:
        abort(404)
    
    return send_from_directory(source_path, image_path)



@app.route("/thumbnail/<image_hash>")
def get(image_hash: str) -> Response:
    image_path = f"{image_hash}.webp"

    if image_path is None:
        abort(404)
    
    return send_from_directory(thumbnail_path, image_path)



@app.teardown_appcontext
def close_conn(error) -> None:
    cons.close_conn()



app.run(host="127.0.0.1", port=8080, debug=True)
