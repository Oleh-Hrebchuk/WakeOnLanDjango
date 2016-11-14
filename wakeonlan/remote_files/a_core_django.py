#!/usr/bin/python
from sys import argv
from b_database_manager import *
from c_wake_on_lan import WakeOnLan
from c_ssh_manager import SSHManage
from c_patterns import Patterns
from c_config_parce import GetConfig
from c_logging import LoggingData

__author__ = 'oleh.hrebchuk'


class Manager(SSHManage, Patterns, WakeOnLan, ManageGatesTable, ManageHostsTable, GetConfig, LoggingData):
    c = GetConfig()
    name_db = c.get_value_confing('database', 'name_db')
    h = ManageHostsTable('hosts')
    g = ManageGatesTable('gates')

    def __init__(self, *args):
        self.host = str(argv[1])
        self.name_db = self.get_value_confing('database', 'name_db')
        self.key_filename = self.get_value_confing('general', 'key_filename')
        self.domain = self.get_value_confing('general', 'domain')
        WakeOnLan.__init__(self)

    def call_wakeonlan(self):
        """
        this method read mail from remote host "subject:"
        and call wakeonlan script for turn on pc
        """
        try:
            get_host = self.host
            if self.regex_ip(get_host):
                self.macaddress = self.get_mac_via_ip(get_host)
                self.broadcast = self.get_broadcast(get_host)
                self.eth = self.g.get_eth_via_brod(self.get_broadcast(get_host))[0][0]
                self.wake_on_lan()
            else:
                if self.host.endswith(self.domain):
                    self.macaddress = self.get_mac_via_hostname(get_host.lower())[0][0]
                    ip = self.get_ip_via_hostname(get_host.lower())[0][0]
                    self.broadcast = self.get_broadcast(ip)
                    self.eth = self.g.get_eth_via_brod(self.get_broadcast(ip))[0][0]
                    self.wake_on_lan()
                else:
                    host = get_host + self.domain
                    self.macaddress = self.get_mac_via_hostname(host.lower())[0][0]
                    ip = self.get_ip_via_hostname(host)[0][0]
                    self.broadcast = self.get_broadcast(ip)
                    self.eth = self.g.get_eth_via_brod(self.get_broadcast(ip))[0][0]
                    self.wake_on_lan()
        except Exception as e:
            self.loger(e, 'info')


c = Manager()
c.call_wakeonlan()
