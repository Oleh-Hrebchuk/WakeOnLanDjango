#!/usr/bin/python

import socket
import struct
from sys import argv
__author__ = 'oleh.hrebchuk'


class WakeOnLan(object):
    def __init__(self, *args):
        try:
            if len(args) == 0:
                self.macaddress = str(argv[1])
                self.eth = str(argv[2])
                self.broadcast = str(argv[3])
            else:
                self.macaddress = str(args[0])
                self.eth = str(args[1])
                self.broadcast = str(args[2])
        except Exception as e:
            print e

    def wake_on_lan(self):
        # check mac address
        print self.macaddress,self.eth,self.broadcast
        if len(self.macaddress) == 12:
            pass
        elif len(self.macaddress) == 17:
            self.macaddress = self.macaddress.replace(':', '')
        else:
            raise ValueError('Invalid MAC format')
        # sync
        data = ''.join(['FFFFFFFFFFFF', self.macaddress * 20])
        send_data = b''
        # split hex values
        for i in range(0, len(data), 2):
            send_data += struct.pack('B', int(data[i: i + 2], 16))
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, self.eth + '\0')
        sock.sendto(send_data, (self.broadcast, 7))