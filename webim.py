#!/usr/bin/env python
#coding: utf-8

"""
python webim client

Overview
========

See U{the WebIM homepage<http://www.github.com/webim>} for more about webim.

Usage summary
=============

This should give you a feel for how this module operates::

    import webim 
    c = webim.Client('domain', 'apikey', host='127.0.0.1', port = 8000)
    c.online('1,2,3', 'grp1, grp2, grp3')
    c.offline()

Detailed Documentation
======================

More detailed documentation is available in the L{Client} class.
"""

__author__    = "Ery Lee <ery.lee@gmail.com>"
__version__ = "4.0.0beta"
__copyright__ = "Copyright (C) 2013 Ery Lee"
__license__   = "Python Software Foundation License"

APIVSN = 'v5'
AVATAR_SIZE = 50
AVATAR_DEFAULT = 'identicon'
GRAVATAR_DEFAULT_URL = 'http://www.gravatar.com/avatar/%s?s={0}&d={1}&f=y'.format(AVATAR_SIZE, AVATAR_DEFAULT)

try:
    import json
except ImportError:
    import simplejson as json

import time
import urllib
import urllib2
import hashlib



# ==============================================================================
# Helpers
# ==============================================================================
def encode_utf8(data_dict):
    for key, value in data_dict.iteritems():
        if isinstance(value, unicode):
            data_dict[key] = value.encode('utf8')
    
    
def gravatar_default(oid):
    return GRAVATAR_DEFAULT_URL % hashlib.sha1(str(oid)).hexdigest()
        
def gravatar_url(email):
    url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
    url += urllib.urlencode({'s':str(AVATAR_SIZE)})
    return url


# ==============================================================================
#  
# ==============================================================================    
class Client:
    
    def __init__(self, user, domain, apikey,
                 ticket=None, host = 'localhost', port=8000, timeout=3):
        """
        Create a new Client object with the given host and port

        @param host: host
        @param port: port
        """
        self.user = user
        self.domain = domain
        self.apikey = apikey
        self.ticket = ticket
        self.host = host
        self.port = port
        self.timeout = timeout

        
    def online(self, buddies, groups, show):
        """
        Client online
        """
        buddy_ids = []
        buddy_dict = {}
        for b in buddies:
            bid = str(b.id)
            buddy_ids.append(bid)
            buddy_dict[bid] = b

        print 'self.user:', self.user
        print 'buddy_dict:', buddy_dict
        
        reqdata = {
            'groups': ','.join(groups),
            'buddies': ','.join(buddy_ids),
            'name': self.user['id'],
            'nick': self.user['nick'],
            'status': self.user['status'],
            'show': show
        }
        #if self.user.is_visitor():
        #    reqdata['visitor'] = True
        
        status, body = self._httpost('/presences/online', reqdata)
        if(status != 200):
            return json.dumps({'success': False, 'error_msg': body})
        else:
            respdata = json.loads(body)
            print 'online.respdata: ', respdata
            print '========='

            conninfo = {
                'domain': self.domain,
                'ticket': respdata['ticket'],
                'mqttd' : respdata['mqttd'],
                # 'websocket': respdata['websocket'],
                'server': respdata['server']
            }

            loaded_buddies = respdata['buddies']
            for b in loaded_buddies:
                uid = b['name']
                b['id'] = uid
                email = buddy_dict[uid].email
                b['status'] = '{}' # FIXME:
                b['pic_url'] = gravatar_url(email)
                b['default_pic_url'] = gravatar_default(uid)
                
            self.ticket = respdata['ticket']
            return json.dumps({'success': True,
                               'connection': conninfo,
                               'buddies': loaded_buddies,
                               'groups': respdata['groups'], #groups
                               'rooms': respdata['groups'],
                               'server_time': int(time.time()*1000), #FIXME:
                               'user': self.user})

    def offline(self):
        """
        Client offline
        """
        status, body = self._httpost('/presences/offline', {})
        return body

    def presence(self, show='available', status = ''):
        """
        Update Presence
        """
        reqdata = {}
        reqdata['nick'] = self.user['nick']
        reqdata['show'] = show
        reqdata['status'] = status
        _status, body = self._httpost('/presences/show', reqdata)
        return body

    def message(self, to, body, style, timestamp, msgtype='chat'):
        """
        Send Message
        """
        reqdata = {}
        reqdata['nick'] = self.user['nick']
        #TODO: fixme later
        reqdata['type'] = msgtype
        reqdata['to'] = to
        reqdata['body'] = body
        reqdata['style'] = style
        reqdata['timestamp'] = timestamp
        _status, body = self._httpost('/messages', reqdata)
        return body

    def status(self, to, show):
        """
        Send Status
        """
        reqdata = {}
        reqdata['nick'] = self.user['nick']
        reqdata['to'] = to
        reqdata['show'] = show
        _status, body = self._httpost('/statuses', reqdata)
        return body

    def members(self, room_id):
        """
        Get group members
        """
        reqdata = {}
        reqdata['group'] = room_id
        status, body = self._httpget('/group/members', reqdata)
        if status == 200:
            respdata = json.loads(body)
            return json.dumps(respdata[room_id])

            
    def join(self, room_id):
        """
        Join Group Chat
        """
        reqdata = {}
        reqdata['nick'] = self.user['nick']
        reqdata['room'] = room_id
        status, body = self._httpost('/group/join', reqdata)
        if status == 200:
            respdata = json.loads(body)
            return json.dumps({'id': room_id, 'count': respdata[room_id]})

            
    def leave(self, room_id):
        """
        Leave Group Chat
        """
        reqdata = {}
        reqdata['nick'] = self.user['nick']
        reqdata['room'] = room_id
        _status, body = self._httpost('/group/leave', reqdata)
        return body
        

    @property
    def reqdata_base(self):
        return {
            'version': APIVSN,
            'domain': self.domain,
            'apikey': self.apikey,
            'ticket': self.ticket
        }

        
    def _httpget(self, path, params=None):
        url = self._apiurl(path)
        
        if params is not None:
            params.update(self.reqdata_base)
            print 'GET.url:', url
            print 'GET.params: ', params
            encode_utf8(params)
            url += "?" + urllib.urlencode(params)
            try:
                if __debug__: print "GET %s" % url
                resp = urllib2.urlopen(url, timeout=self.timeout)
                body = resp.read()
                if __debug__: print body
                return (resp.getcode(), body)
            except urllib2.HTTPError, e:
                raise e

        
    def _httpost(self, path, data):
        url = self._apiurl(path)
        
        try:
            if __debug__: print "POST %s" % url
            data.update(self.reqdata_base)
            print 'POST.url:', url
            print 'POST.data:', data
            encode_utf8(data)
            resp = urllib2.urlopen(url, urllib.urlencode(data), self.timeout)
            body = resp.read()
            if __debug__: print body
            return (resp.getcode(), body)
        except urllib2.HTTPError, e:
            raise e

    def _apiurl(self, path):
        return "http://%s:%d/%s%s" % (self.host, self.port, APIVSN, path)

        
        
    #NOTICE: for test
    def poll(self):
        data = {'domain' : self.domain,
                'ticket': self.ticket,
                'callback': 'alert'}
        return self._httpget("/packets", data)
        
