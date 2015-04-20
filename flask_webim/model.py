#!/usr/bin/env python
#coding: utf-8

class Model:

    def __init__(self):
        pass

    def histories(self, uid, to, typ = 'chat', limit = 100):
        """
        读取与with用户聊天记录.

        @param uid: 当前用户id
        @param with: 对方id，可根据需要转换为long
        @param type: 记录类型：chat | grpchat

        @param limit: 记录条数
        @return 聊天记录
        
        MySQL查询逻辑:

        <pre>
            if (type == "chat")
              {
                  
                  "SELECT * FROM webim_Histories WHERE `type` = 'chat' 
                  AND ((`to`=%s AND `from`=%s AND `fromdel` != 1) 
                  OR (`send` = 1 AND `from`=%s AND `to`=%s AND `todel` != 1))  
                  ORDER BY timestamp DESC LIMIT %d", $with, $uid, $with, $uid, $limit );
                  
              }
              else
              {
                  
                  "SELECT * FROM  webim_histories 
                      WHERE `to`=%s AND `type`='grpchat' AND send = 1 
                      ORDER BY timestamp DESC LIMIT %d", , $with, $limit);
                  
              }
        </pre>
        """
        return []


    def offline_histories(self, uid, limit = 100):
        """
        读取用户的离线消息.

        @param uid: 用户uid
        @return: 返回离线消息

        MySQL脚本:

        SELECT * FROM  webim_histories WHERE `to` = ? and send != 1 ORDER BY timestamp DESC LIMIT limit
        """
        return []

    def insert_history(self, message):
        """
        插入一条历史消息记录.

        insert into webim_histories(
            send,
            msg_type,
            to_user,
            from_user,
            nick,
            body,
            style,
            timestamp
        ) values(
            message.send,
            message.type,
            message.to,
            message.from,
            message.nick,
            message.body,
            message.style,
            message.timestamp
        )
        """
        pass

    def clear_histories(self, uid, to):
        """
        清除与with用户聊天记录.

        @param uid: 用户uid
        @param with: 对方id,可根据需要转换为long

        MySQL脚本:

        UPDATE webim_histories SET fromdel = 1 Where from = uid and to = to and type = 'chat';
        UPDATE webim_histories SET todel = 1 Where to = uid and from = to and type = 'chat';
        DELETE FROM webim_histories WHERE fromdel = 1 AND todel = 1;
        """
        pass

    def offline_readed(self, uid):
        pass

    def setting(self, uid, data = None):
        """
        @param uid: 用户uid
        @return JSON格式配置数据，

        if data == None: 
            读取用户配置数据，MySQL数据库查询SQL脚本:
            select data from webim_settings where uid = ?
            返回查询data, 或"{}"
        else:
            设置用户配置数据，MySQL数据库脚本: 
            update webim_settings set data = ?  where uid = ?" 
            应该先读取配置检查是否存在，不存在插入，否则更新。
        """
        if(data == None):
            #select data from webim_settings where uid = ?
            return {} 
        else:
            # update webim_settings set data = ?  where uid = ?
            # or 
            # insert into webim_settings(uid, data) values (?, ?)
            pass

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

    def visitor(self, vid):
        return None

    def visitors(self, vids):
        return []

