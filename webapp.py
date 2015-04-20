#!/usr/bin/env python
#coding: utf-8

"""
webim demo.
"""

from flask import Flask, session, request, redirect, render_template, url_for, jsonify, make_response

from flask_webim.router import webimbp

app = Flask(__name__)
app.secret_key = "WebimDemoKey"
app.config.from_pyfile("setting.cfg")
app.register_blueprint(webimbp, url_prefix='/webim')

@app.route("/")
def index():
	return render_template("index.html");

@app.route('/login', methods=['POST'])
def login():
    session['uid'] = request.form['uid']
    return redirect(url_for('index'))

if __name__ == "__main__":
	app.run()

