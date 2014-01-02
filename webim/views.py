from flask import Blueprint, render_template, jsonify, current_app, make_response

webim_view = Blueprint('webim_view', __name__)

@webim_view.route("/boot")
def boot():
	#WebIM config
	WEBIM_CFG = current_app.config['WEBIM']
	#TODO:
	urlpath = "http://localhost:5000"
	response = make_response(render_template('/webim/boot.js', urlpath=urlpath, WEBIM_CFG=WEBIM_CFG))
	response.headers['Content-Type'] = 'text/javascript'
	return response

@webim_view.route("/online", methods=['POST'])
def online():
	#TODO: 5.2 update
	return jsonify({'success':False})

@webim_view.route("/offline", methods=['POST'])
def offline():
	return jsonify("ok")

@webim_view.route("/refresh", methods=['POST'])
def deactivate():
	return jsonify("ok")

@webim_view.route("/message", methods=['POST'])
def message():
	return jsonify("ok")

@webim_view.route("/presence", methods=['POST'])
def presence():
	return jsonify("ok")

@webim_view.route("/status", methods=['POST'])
def status():
	return jsonify("ok")

@webim_view.route("/setting", methods=['POST'])
def setting():
	return "ok"
	
@webim_view.route("/history")
def history():
	return jsonify("ok")

@webim_view.route("/history/clear", methods=['POST'])
def clear_history():
	return jsonify("ok")

@webim_view.route("/history/download", methods=['POST'])
def download_history():
	return jsonify("ok")

@webim_view.route("/members")
def members():
	#TODO: 5.2 change
	return jsonify("ok")

@webim_view.route("/group/join")
def join_group():
	return jsonify("ok")

@webim_view.route("/group/leave")
def leave_group():
	return jsonify("ok")

@webim_view.route("/buddies")
def buddies():
	return jsonify("ok")

@webim_view.route("/notifications")
def notifications():
	return jsonify([])
