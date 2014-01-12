
from flask import Flask, session, request, render_template, jsonify, make_response

from webim.views import webimbp

app = Flask(__name__)
app.config.from_pyfile("setting.cfg")
app.register_blueprint(webimbp, url_prefix='/webim')

@app.route("/")
def index():
	print request.values.get("id")
	return render_template("index.html");

if __name__ == "__main__":
	app.run()

