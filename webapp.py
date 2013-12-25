
from flask import Flask, render_template, jsonify, make_response

app = Flask(__name__)
app.config.from_pyfile("setting.cfg")

#config from setting.py

@app.route("/")
def index():
	return render_template("index.html");

@app.route("/webim/boot")
def boot():
	urlpath = "http://localhost:5000"
	response = make_response(render_template('/webim/boot.js', urlpath=urlpath))
	response.headers['Content-Type'] = 'text/javascript'
	return response

@app.route("/webim/online", methods=['POST'])
def online():
	return jsonify({'success':False})

@app.route("/webim/offline", methods=['POST'])
def offline():
	return jsonify("ok")

@app.route("/webim/refresh", methods=['POST'])
def deactivate():
	return jsonify("ok")

@app.route("/webim/message", methods=['POST'])
def message():
	return jsonify("ok")

@app.route("/webim/presence", methods=['POST'])
def presence():
	return jsonify("ok")

@app.route("/webim/status", methods=['POST'])
def status():
	return jsonify("ok")

@app.route("/webim/setting", methods=['POST'])
def setting():
	return "ok"
	
@app.route("/webim/history")
def history():
	return jsonify("ok")

@app.route("/webim/history/clear", methods=['POST'])
def clear_history():
	return jsonify("ok")

@app.route("/webim/history/download", methods=['POST'])
def download_history():
	return jsonify("ok")

@app.route("/webim/members")
def members():
	return jsonify("ok")

@app.route("/webim/group/join")
def join_group():
	return jsonify("ok")

@app.route("/webim/group/leave")
def leave_group():
	return jsonify("ok")

@app.route("/webim/buddies")
def buddies():
	return jsonify("ok")

@app.route("/webim/notifications")
def notifications():
	return jsonify([])

if __name__ == "__main__":
	app.run()

