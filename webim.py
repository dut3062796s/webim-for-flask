#!/usr/bin/env python
#coding: utf-8

"""
python webim client

Overview
========

See U{the Webim homepage<http://www.github.com/webim>} for more about webim.

Usage summary
=============

This should give you a feel for how this module operates::

    import webim 
    endpoint = webim.Endpoint("uid1", "user1")
    c = webim.Client(endpoint, 'domain', 'apikey', host='127.0.0.1', port = 8000)
    c.online(['uid1','uid2','uid3'], ['grp1','grp2','grp3'])
    c.offline()

Detailed Documentation
======================

More detailed documentation is available in the L{Client} class.
"""

__author__    = "Ery Lee <ery.lee@gmail.com>"
__version__ = "5.2"
__copyright__ = "Copyright (C) 2014 Ery Lee"
__license__   = "Python Software Foundation License"

APIVSN = 'v5'
#AVATAR_SIZE = 50
#AVATAR_DEFAULT = 'identicon'
#GRAVATAR_DEFAULT_URL = 'http://www.gravatar.com/avatar/%s?s={0}&d={1}&f=y'.format(AVATAR_SIZE, AVATAR_DEFAULT)

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
    return data_dict
    
#def gravatar_default(oid):
#    return GRAVATAR_DEFAULT_URL % hashlib.sha1(str(oid)).hexdigest()
        
#def gravatar_url(email):
#    url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
#    url += urllib.urlencode({'s':str(AVATAR_SIZE)})
#    return url

# ==============================================================================
# Endpoint 
# ==============================================================================    
class Endpoint:

    def __init__(self, id, nick, presence="offline", show="unavailable", status="", status_time="", url="", pic_url = ""):
        """
        Endpoint

        @param id: endpoint id
        @param nick: endpoint nick
        """
        self.id = id
        self.nick = nick
        self.presence = presence
        self.show = show
        self.status = status
        self.status_time = status_time
        self.url = url
        self.pic_url = pic_url

class Message:

    def __init__(self, to, nick, body, timestamp, type = "chat", style = ""):
        self.to = to
        self.nick = nick
        self.body = body
        self.timestamp = timestamp
        self.type = type
        self.style = style

class Presence:

    def __init__(self, type = "online", show = "available", status = ""):
        self.type = type
        self.show = show
        self.status = status

class Status:

    def __init__(self, to, show, status):
        self.to = to
        self.show = show
        self.status = status

# ==============================================================================
# Client
# ==============================================================================    
class Client:
    
    def __init__(self, endpoint, domain, apikey,
                 ticket=None, host = 'localhost', port=8000, timeout=10):
        """
        Create a new Client object with the given host and port

        @param endpoint: endpoint
        @param host: host
        @param port: port
        """
        self.endpoint = endpoint
        self.domain = domain
        self.apikey = apikey
        self.ticket = ticket
        self.host = host
        self.port = port
        self.timeout = timeout
        
    def online(self, buddies, groups):

        """
        Client online
        """
        reqdata = self._reqdata
        reqdata.update({
            'buddies': ','.join(buddies),
            'groups': ','.join(groups),
            'name': self.endpoint.id,
            'nick': self.endpoint.nick,
            'show': self.endpoint.show,
            'status': self.endpoint.status
        })
        status, body = self._httpost('/presences/online', reqdata)
        respdata = json.loads(body)
        print 'online.respdata: ', respdata
        if(status == 200): self.ticket = respdata['ticket']
        return (status, respdata)

    def offline(self):
        """
        Client offline
        """
        reqdata = self._reqdata
        status, body = self._httpost('/presences/offline', reqdata)
        respdata = json.loads(body)
        return (status, respdata)

    def presence(self, presence):
        """
        Send Presence
        """
        reqdata = self._reqdata
        reqdata.update({
            'nick': self.endpoint.nick,   
            'show': presence.show,
            'status': presence.status 
        })
        status, body = self._httpost('/presences/show', reqdata)
        return (status, json.loads(body))

    def message(self, message):
        """
        Send Message
        """
        reqdata = self._reqdata
        reqdata.update({
            'nick': self.endpoint.nick,
            'type': message.type,
            'to': message.to,
            'body': message.body,
            'style': message.style,
            'timestamp': message.timestamp
        })
        status, body = self._httpost('/messages', reqdata)
        return (status, json.loads(body))

    #TODO: refactor later
    def push(self, from1, message):
        """
        Push Message
        """
        reqdata = self._reqdata
        reqdata.update({
            'from': from1,
            'nick': self.endpoint.nick,
            'type': message.type,
            'to': message.to,
            'body': message.body,
            'style': message.style,
            'timestamp': message.timestamp
        })
        status, body = self._httpost('/messages', reqdata)
        return (status, json.loads(body))

    def status(self, status):
        """
        Send Status
        """
        reqdata = self._reqdata
        reqdata.update({
            'nick': self.endpoint.nick,
            'to': status.to,
            'show': status.show
        })
        status, body = self._httpost('/statuses', reqdata)
        return (status, json.loads(body))

    def presences(self, ids):
        """
        Read presences
        """
        reqdata = self._reqdata
        reqdata.update({
            'ids': ",".join(ids)
        })
        status, body = self._httpget("/presences", reqdata)
        return (status, json.loads(body))

    def members(self, gid):
        """
        Read group members
        """
        reqdata = self._reqdata
        reqdata.update({
            'group': gid
        })
        status, body = self._httpget('/group/members', reqdata)
        return (status, json.loads(body))
            
    def join(self, gid):
        """
        Join group 
        """
        reqdata = self._reqdata
        reqdata.update({
            'nick': self.endpoint.nick,
            'group': gid
        })
        status, body = self._httpost('/group/join', reqdata)
        return (status, json.loads(body))
            
    def leave(self, gid):
        """
        Leave group
        """
        reqdata = self._reqdata
        reqdata.update({
            'nick': self.endpoint.nick,
            'group': gid
        })
        status, body = self._httpost('/group/leave', reqdata)
        return (status, json.loads(body))
        
    @property
    def _reqdata(self):
        data = {
            'version': __version__,
            'apikey': self.apikey, 
            'domain': self.domain
        }
        if self.ticket is not None: 
            data['ticket'] = self.ticket
        return data

    def _httpget(self, path, params=None):
        """
        Http Get
        """
        url = self._apiurl(path)
        
        if params is not None:
            print 'GET.url:', url
            print 'GET.params: ', params
            url += "?" + urllib.urlencode(encode_utf8(params))
            try:
                if __debug__: print "GET %s" % url
                resp = urllib2.urlopen(url, timeout=self.timeout)
                body = resp.read()
                if __debug__: print body
                return (resp.getcode(), body)
            except urllib2.HTTPError, e:
                raise e
        
    def _httpost(self, path, data):
        """
        Http Post
        """
        url = self._apiurl(path)
        try:
            if __debug__: print "POST %s" % url
            print 'POST.url:', url
            print 'POST.data:', data
            resp = urllib2.urlopen(url, urllib.urlencode(encode_utf8(data)), self.timeout)
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
