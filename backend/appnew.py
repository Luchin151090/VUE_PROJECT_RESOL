from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
from flask_cors import CORS #para que no genere errores en las peticiones

from blueprint.blueprint import blue_print


app = Flask(__name__,
    static_folder="./frontend/dist/static",
    template_folder="./frontend/dist")

app.register_blueprint(blue_print)
CORS(app, methods=["GET", "POST", "PUT", "DELETE"])

@app.route('/',defaults={'path':''})
@app.route('/<path:path>')
def dender_vue(path):
    return render_template("index.html")

if __name__=="__main__":
    app.run(debug=True)
