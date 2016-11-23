#!/usr/bin/python
import sqlite3
import nmap
import logging
import paramiko
from c_network import NetworkInformation
from c_patterns import Patterns
from c_config_parce import GetConfig
__author__ = 'oleh.hrebchuk'


class ScannCopmputers(GetConfig):
    def get_detail_computers(self,network):
        detail_hosts = {}
        nm = nmap.PortScanner()
        scann = nm.scan(hosts=network, arguments='-sP')
        print scann
        try:
            for key in scann['scan'].keys():
                if 'VMware' not in scann['scan'][key]['vendor'].values():
                    if scann['scan'][key]['hostnames'][0]['name'] != '':
                        detail_hosts[key] = {}
                        detail_hosts[key]['hostname'] = scann['scan'][key]['hostnames'][0]['name']
                        detail_hosts[key]['mac'] = scann['scan'][key]['addresses']['mac']
                        detail_hosts[key]['ip'] = scann['scan'][key]['addresses']['ipv4']
        except Exception as e:
            print e
        return detail_hosts
