
from flask import Flask, render_template, jsonify, make_response

from webim.views import webim_view

app = Flask(__name__)
app.config.from_pyfile("setting.cfg")
app.register_blueprint(webim_view, url_prefix='/webim')

@app.route("/")
def index():
	return render_template("index.html");

if __name__ == "__main__":
	app.run()

