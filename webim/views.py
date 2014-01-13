from flask import Blueprint, g, request, render_template, jsonify, current_app, make_response

import time, webim

from models import new_user, new_status, new_message, WebimModel

#def gravatar_default(oid):
#    return GRAVATAR_DEFAULT_URL % hashlib.sha1(str(oid)).hexdigest()
        
#def gravatar_url(email):
#    url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
#    url += urllib.urlencode({'s':str(AVATAR_SIZE)})
#    return url

webimbp = Blueprint('webim_view', __name__)

def current_uid():
   return request.values.get('uid', 'uid1')

@webimbp.before_request
def init_client():
   CFG = current_app.config['WEBIM']
   uid = request.values.get('uid', 'uid1')
   ticket = request.values.get('ticket', None)
   g.user = new_user(uid, uid, presence="online", show="available")
   g.client = webim.Client(g.user, CFG['DOMAIN'], CFG['APIKEY'], 
         ticket=ticket, host=CFG['HOST'], port=CFG['PORT'])

@webimbp.route("/boot")
def boot():
   print g
   #WebIM config
   WEBIM_CFG = current_app.config['WEBIM']
   #TODO:
   urlpath = "http://localhost:5000"
   response = make_response(render_template('/webim/boot.js', urlpath=urlpath, WEBIM_CFG=WEBIM_CFG))
   response.headers['Content-Type'] = 'text/javascript'
   return response

@webimbp.route("/online", methods=['POST', 'GET'])
def online():
   uid = current_uid()
   model = WebimModel()
   buddies = model.buddies(uid)
   groups = model.groups(uid)

   buddy_ids = [buddy['id'] for buddy in buddies]
   group_ids = [group['id'] for group in groups]

   status, json = g.client.online(buddy_ids, group_ids)
   if status != 200:
      return jsonify({'success':False, 'error_msg': str(json)})
   conn = {
      'ticket': json['ticket'],
      'domain': g.client.domain,
      'server': json['server'],
      'jsonpd': json['jsonpd'],
      'websocket': json['websocket']
   }

   print json['buddies']
   for buddy in buddies:
       bid = buddy['id']
       if bid in json['buddies']:
           buddy['presence'] = 'online'
           buddy['show'] = json['buddies'][bid]

   data = {
      'success': True,
      'connection': conn,
      'buddies': buddies,
      'rooms': groups,
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
   g.client.offline
   return "ok"

@webimbp.route("/message", methods=['POST'])
def message():
   type = request.values.get('type')
   offline = request.values.get('offline')
   to = request.values.get('to')
   body = request.values.get('body')
   style = request.values.get('style', '')
   send = 0 if offline == 'true' else 1
   print send
   timestamp = time.time() * 1000
   #TODO: insert into history table
   message = new_message(to, g.user['nick'], body, timestamp, type, style)
   if send == 1:
       g.client.message(message) 
   return "ok"

@webimbp.route("/presence", methods=['POST'])
def presence():
   show = request.values.get('show')
   status = request.values.get('status')
   g.client.presence(webim.Presence(show, status))
   return "ok"

@webimbp.route("/status", methods=['POST'])
def status():
   to = request.values.get('to')
   show = request.values.get('show')
   status = request.values.get('status')
   g.client.status(new_status(to, show, status))
   return "ok"

@webimbp.route("/setting", methods=['POST'])
def setting():
   data = request.values.get('data')
   #TODO:
   return "ok"
   
@webimbp.route("/history")
def history():
   #TODO
   histories = []
   return jsonify(histories)

@webimbp.route("/history/clear", methods=['POST'])
def clear_history():
   #TODO
   WebimHistory.clear(request.values.get("id"))
   return "ok"

@webimbp.route("/history/download", methods=['POST'])
def download_history():
   uid = current_uid()
   id = request.values.get('id')
   type = request.values.get('type')
   #TODO: NOW
   date = request.values.get('date', '') 
   histories = WebimHistory.recent(uid, id, type, 1000)
   return render_tempate('/webim/download_history', histories=histories)

#TODO: FIXME
@webimbp.route("/members")
def members():
   gid = request.values.get('id')
   group = WebimModel().group(gid)
   status, json = g.client.members(gid)
   if status != 200:
      return "Not Found"
   return str(json)

@webimbp.route("/group/join")
def join_group():
   gid = request.values.get('id')
   group = WebimMode.group(gid)
   status, json = g.client.join(gid)
   if status != 200:
      return "Error...."
   group.count = json['count']
   return jsonify(group)

@webimbp.route("/group/leave")
def leave_group():
   gid = _g('id')
   g.client.leave(gid)
   return "ok"

@webimbp.route("/buddies")
def buddies():
   buddies = WebimModel().buddies_by_ids(_g('ids').split(','))
   return jsonify(buddies)

@webimbp.route("/rooms")
def rooms():
   rooms = WebimModel().groups_by_ids(_g('ids').split(','))
   return jsonify(rooms)

@webimbp.route("/notifications")
def notifications():
   return jsonify(WebimModel().notifications(current_uid()))

def _g(k):
   return request.values.get(k)

def _g(k, v):
   return reqeust.values.get(k, v)





