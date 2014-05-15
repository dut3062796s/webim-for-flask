#!/usr/bin/env python
#coding: utf-8

class Model:

    def __init__(self):
        pass

    def histories(self, uid, to, typ = 'chat', limit = 50):
        return []

    def offline_histories(self, uid, limit = 50):
        return []

    def insert_history(self, message):
        pass

    def clear_histories(self, uid, to):
        pass

    def offline_readed(self, uid):
        pass

    def setting(self, uid, data = None):
        if(data == None): return {} 

    def rooms(self, uid):
        return []

    def rooms_by_ids(self, uid, ids):
        return []

    def members(self, room):
        return []

    def create_room(self, data):
        pass

    def invite_room(self, room, members):
        [self.join_room(room, m['id'], m['nick']) for m in members]

    def join_room(self, room, uid, nick):
        pass

    def leave_room(self, room, uid):
        pass

    def block_room(self, room, uid):
        pass

    def is_room_blocked(self, room, uid):
        return False

    def unblock_room(self, room, uid):
        pass

    def visitor(self):
        return None

    def visitors(self, vids):
        return []

   

