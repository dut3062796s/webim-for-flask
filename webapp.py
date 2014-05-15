
from flask import Flask, session, request, render_template, jsonify, make_response

from webim.router import webim_router

app = Flask(__name__)
app.config.from_pyfile("setting.cfg")
app.register_blueprint(webim_router, url_prefix='/webim')

@app.route("/")
def index():
	print request.values.get("id")
	return render_template("index.html");

if __name__ == "__main__":
	app.run()

