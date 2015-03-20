#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from sleekxmpp import ClientXMPP
from collections import deque

class XmppClient(ClientXMPP):
    def __init__(self, jid, password, room, nick):
        ClientXMPP.__init__(self, jid, password)

        self.room = room.lower()
        self.nick = nick

        self.add_event_handler("session_start", self.session_start)

        self.add_event_handler("muc::%s::message" % self.room,
                               self.muc_message)
        self.add_event_handler("muc::%s::got_online" % self.room,
                               self.muc_online)

        self.add_event_handler("socket_error", self.on_socket_error)
        
        self.register_plugin('xep_0045')

        self.msg_queue = deque()
        self.ready_to_send = False

    def on_socket_error(self, args):
        print("socket error %s" % args)
        self.stop.set()

    def session_start(self, event):
        self.get_roster()
        self.send_presence()
        self.plugin['xep_0045'].joinMUC(self.room, self.nick, wait=True)

    def muc_message(self, msg):
        logging.debug("MUC MESSAGE RECEIVED! FROM %s" % msg['from'].bare)

    def muc_online(self, presence):
        if presence['muc']['nick'] == self.nick:
            logging.log(logging.DEBUG, "GOT MY OWN PRESENCE!!!!")
            self.ready_to_send = True

            # If we have messages in the queue, send them
            if self.msg_queue:
                logging.debug("Sending queued messages...")
                for m in self.msg_queue:
                    self.send_message(mto=self.room,
                                      mbody=m,
                                      mtype='groupchat')

                self.msg_queue.clear()

    def send_muc_message(self, msg):
        if self.ready_to_send:
            self.send_message(mto=self.room, mbody=msg, mtype='groupchat')
        else:
            logging.debug("Message added to the queue")
            self.msg_queue.append(msg)
