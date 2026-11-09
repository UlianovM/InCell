import app.connection as cons
import app.requests as req
from flask import Flask, Response, g, render_template, url_for, send_from_directory, abort
import os



pt = os.path
pwd = os.getcwd()

data_path = pt.abspath(pt.join(pwd, "data"))

source_path = pt.join(data_path, "source")
webp_path = pt.join(data_path, "webp")



app = Flask(__name__, static_folder="web", template_folder="templates")
cons.init_conn()



@app.route("/")
def main():
    return render_template("index.html", cells=[("path", "alt")])



@app.route("/get/<image_hash>")
def get(image_hash: str) -> Response:
    cons.get_conn()

    image_path = req.get_source_ext(g.db, image_hash)
    
    if image_path is None:
        abort(404)
    
    return send_from_directory(source_path, image_path)



@app.teardown_appcontext
def close_conn(error) -> None:
    cons.close_conn()



app.run(host="127.0.0.1", port=8080, debug=True)
