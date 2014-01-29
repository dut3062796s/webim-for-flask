#!/usr/bin/env python
#coding: utf-8

# ==============================================================================
# Webim User
# ==============================================================================    
def new_user(id, nick, presence="offline", show="unavailable", status="",
    status_time="", url="#", pic_url = "/static/webim/images/chat.png"):
    return {
       'id': id,
       'nick': nick,
       'presence': presence,
       'show': show,
       'status': status,
       'status_time': status_time,
       'url': url,
       'pic_url': pic_url
    }

# ==============================================================================
# Webim Group
# ==============================================================================    
def new_group(id, nick, url = '#', pic_url = '/static/webim/images/chat.png'):
    return {
        'id': id,
        'nick': nick,
        'count': 0,
        'url': url,
        'pic_url': pic_url
    }

# ==============================================================================
# Webim Message
# ==============================================================================    
def new_message(to, nick, body, timestamp, type = "chat", style = ""):
    return {
        'to': to,
        'nick': nick,
        'body': body,
        'timestamp': timestamp,
        'type': type,
        'style': style
    }

# ==============================================================================
# Presence
# ==============================================================================    
def new_presence(type = "online", show = "available", status = ""):
    return {
        'type': type,
        'show':  show,
        'status': status
    }

# ==============================================================================
# Status
# ==============================================================================    
def new_status(to, show, status):
    return {
        'to': to,
        'show': show,
        'status': status
    }

class WebimBuddy:
    pass

class WebimGroup:
    pass

class WebimSetting(db.Model):
    pass

class WebimHistory(db.Model):
    pass

class WebimModel:

    def buddies(self, uid):
        return [new_user('uid1', 'uid1'), new_user('uid2', 'uid2')]

    def groups(self, uid):
        return [new_group('gid1', 'group1')]

    def group(self, gid):
        return new_group(gid, gid)

    def buddies_by_ids(self, ids):
        return [new_user(id, id) for id in ids]

    def notifications(self, uid):
        return [{'text': 'notification', 'link': '#'}, {'text' : 'notification2', 'link': '#'}]

