from flask import Flask, Response, g, render_template, url_for, send_from_directory, abort
import app.database as db
import os



pt = os.path
pwd = os.getcwd()

data_path = pt.abspath(pt.join(pwd, "data"))

source_path = pt.join(data_path, "source")
webp_path = pt.join(data_path, "webp")



app = Flask(__name__, static_folder="web", template_folder="templates")
db.get_conn()



@app.route("/")
def main():
    return render_template("index.html", cells=[("path", "alt")])



@app.route("/get/<image_hash>")
def get(image_hash: str) -> Response:
    db.get_conn()

    image_path = db.get_source_by_hash(g.db, image_hash)
    
    if image_path is None:
        abort(404)
    
    return send_from_directory(source_path, image_path)



@app.teardown_appcontext
def close_conn(error) -> None:
    db.close_conn()



app.run(host="127.0.0.1", port=8080, debug=True)
