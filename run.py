from flask import Flask, render_template, url_for



app = Flask(__name__, static_folder="web", template_folder="templates")



@app.route("/")
def main():
    return render_template("index.html", cells=[("path", "alt")])



app.run(host="127.0.0.1", port=8080, debug=True)
