#!/usr/bin/env python
#coding: utf-8

"""
webim router.
"""

from flask import Blueprint, g, session, request, render_template, jsonify, current_app, make_response

import time, webim

from .model import Model
from .plugin import Plugin

webimbp = Blueprint('webim_view', __name__)

@webimbp.before_request
def init_webim():
   CFG = current_app.config['WEBIM']
   g.model = Model()
   g.plugin = Plugin()
   if 'uid' in session:
       g.user = g.plugin.user(session['uid'])
   else:
       g.user = g.plugin.visitor(request)
   ticket = request.values.get('ticket', None)
   g.client = webim.Client(g.user, CFG['domain'], CFG['apikey'], 
         ticket=ticket, host=CFG['host'], port=CFG['port'])

@webimbp.route("/boot")
def boot():
    setting = g.model.setting(g.user['id'])
    #WebIM config
    config = current_app.config['WEBIM']
    config['is_visitor'] = g.user['role'] == 'visitor'
    config['setting'] = setting
    config['jsonp'] = False
    response = make_response(render_template('/webim/boot.js', WEBIM_CFG=config))
    response.headers['Content-Type'] = 'text/javascript'
    return response

@webimbp.route("/online", methods=['POST', 'GET'])
def online():
    IMC = current_app.config['WEBIM']
    uid = g.user['id']
    buddies = g.plugin.buddies(uid)
    rooms = g.plugin.rooms(uid)

    buddy_ids = [buddy['id'] for buddy in buddies]
    room_ids = [room['id'] for room in rooms]

    data = g.client.online(buddy_ids, room_ids)

    presences = data['presences']

    for buddy in buddies:
        if buddy['id'] in presences:
            buddy['presence'] = 'online'
            buddy['show'] = presences[buddy['id']]

    data = {
        'success': True,
        'connection': data['connection'],
        'presences': data['presences'],
        'buddies': buddies,
        'rooms': rooms,
        'server_time': time.time()*1000,
        'user': g.user
    }
    return jsonify(data)

@webimbp.route("/offline", methods=['POST'])
def offline():
    g.client.offline()
    return "ok"

@webimbp.route("/refresh", methods=['POST'])
def deactivate():
    g.client.offline()
    return "ok"

@webimbp.route("/buddies")
def buddies():
    ids = request.values.get('ids').split(',')
    buddies = g.plugin.buddies_by_ids(ids)
    return jsonify(buddies)

@webimbp.route("/message", methods=['POST'])
def message():
    req = request.values
    type = req.get('type')
    offline = req.get('offline')
    to = req.get('to')
    body = req.get('body')
    style = req.get('style', '')
    send = 0 if offline == 'true' else 1
    timestamp = time.time() * 1000
    message = {
        'to':   to,
        'type': type,
        'body': body,
        'style': style,
        'timestamp': timestamp
    }
    if send == 1:
        g.client.message(message) 
    if not body.startswith('webim-event:'): 
        g.model.insert_history(
            message.update({
                'send': send,
                'from': g.user['id'],
                'nick': g.user['nick']
            })
        )
    return "ok"

@webimbp.route("/presence", methods=['POST'])
def presence():
    req = request.values
    show = req.get('show')
    status = req.get('status')
    g.client.presence({
        'show': show, 
        'status': status
    })
    return "ok"

@webimbp.route("/status", methods=['POST'])
def status():
    req = request.values
    to = req.get('to')
    show = req.get('show')
    g.client.status({'to': to, 'show': show})
    return "ok"

@webimbp.route("/history")
def history():
    to = request.values.get('id')
    type = request.values.get('type')
    histories = g.model.histories(g.user['id'], to, type)
    return jsonify(histories)

@webimbp.route("/history/clear", methods=['POST'])
def clear_history():
    g.model.clear_histories(g.user['id'], request.values.post("id"))
    return "ok"

@webimbp.route("/history/download", methods=['POST'])
def download_history():
    id = request.values.get('id')
    type = request.values.get('type')
    histories = g.model.histories(g.user['id'], id, type, 1000)
    response = make_response(render_template('/webim/download_history', histories=histories))
    response.headers['Content-Type'] = 'text/html;charset=utf-8'
    response.headers['Content-Disposition'] = "attachment; filename=\"histories-%d.html\"" % time.time()
    return response

@webimbp.route("/chatbox/<uid>")
def chatbox(uid):
    buddy = g.plugin.user(uid)
    return render_template("webim/chatbox.html", buddy = buddy)

@webimbp.route("/rooms")
def rooms():
    ids = request.values.get('ids').split(',')
    persist_rooms = g.plugin.rooms_by_ids(g.user['id'], ids)
    temporary_rooms = g.model.rooms_by_ids(g.user['id'], ids)
    return jsonify(persist_rooms+temporary_rooms)

@webimbp.route("/room/invite")
def invite():
    #TODO:
    return "ok"

@webimbp.route("/room/join")
def join_room():
    #TODO:
    room_id = request.values.get('id')
    nick = request.values.get('nick', '')
    g.client.join(room_id)
    return jsonify({})

@webimbp.route("/room/leave")
def leave_room():
    room_id = request.values.get('id')
    g.client.leave(room_id)
    g.model.leave_room(room_id, g.user['id'])
    return "ok"

@webimbp.route("/room/members")
def members():
    #TODO:
    room_id = request.values.get('id')
    #room = find_room(room_id)
    presences = g.client.members(room_id)
    return jsonify([])

@webimbp.route("/setting", methods=['POST'])
def setting():
    data = request.values.get('data')
    g.model.setting(g.user['id'], data)
    return "ok"

@webimbp.route("/notifications")
def notifications():
    return jsonify(g.plugin.notifications(g.user['id']))

def _v(k):
    return request.values.get(k)

def _v(k, v):
    return reqeust.values.get(k, v)

