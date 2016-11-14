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


class SSHManage(object):
    def create_ssh_connection(self, host, user, key_filename):
        try:
            ssh = paramiko.SSHClient()
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, 22, username=user, key_filename=key_filename)
            return ssh
        except Exception as e:
            logging.INFO(e)

    def ssh_read_data(self, host, path_file, key_filename, login):
        try:
            ssh_connect = self.create_ssh_connection(host, login, key_filename)
            sftp = ssh_connect.open_sftp()
            with sftp.open('{}'.format(path_file), 'r')as file_edit:
                text_data = file_edit.read()
            sftp.close()
        except Exception as e:
            logging.INFO(e)
        finally:
            if ssh_connect:
                ssh_connect.close()
        return text_data


class DB(SSHManage, Patterns, ScannCopmputers):
    def __init__(self, db_path, table_name, ):
        self.db_path = db_path
        self.table_name = table_name

    def db_connect(self):
        con = sqlite3.connect(self.db_path)
        return con

    def create_table_hosts(self):
        cur = self.db_connect().cursor()
        cur.execute('''CREATE TABLE {} (id INTEGER PRIMARY KEY AUTOINCREMENT,'''.format(self.table_name))

    def add_columns(self, *args):
        print args
        cur = self.db_connect().cursor()
        # cur.execute('''CREATE TABLE {} (id INTEGER PRIMARY KEY AUTOINCREMENT,'''.format(self.table_name))

        for i in args:
            cur.execute("ALTER TABLE {} ADD COLUMN {} INTEGER".format(self.table_name, i))
        self.db_connect().commit()
        self.db_connect().close()

    def insert_data(self, hostname, ip, mac):
        con = self.db_connect()
        cur = con.cursor()
        cur.execute("INSERT INTO {}(hostname, ip, mac) VALUES(?, ?, ?)".
                    format(self.table_name), (hostname, ip, mac))
        con.commit()
        con.close()

    def update_row(self, hostname, ip, mac):
        con = self.db_connect()
        cur = con.cursor()
        cur.execute("UPDATE {} SET  hostname= ? ,mac = ? WHERE ip= ?".
                    format(self.table_name), (hostname, mac, ip))
        con.commit()
        con.close()

    def get_hostname(self, key):
        con = self.db_connect()
        cur = con.cursor()
        return cur.execute("SELECT hostname FROM {} WHERE ip=:ips".
                           format(self.table_name), {'ips': key}).fetchall()[0][0]

    def get_ip(self, key):
        cur = self.db_connect().cursor()
        return cur.execute("SELECT ip FROM {} WHERE ip=:ips".
                           format(self.table_name), {'ips': key}).fetchall()

    def get_mac_via_ip(self, key):
        cur = self.db_connect().cursor()
        return cur.execute("SELECT mac FROM {} WHERE ip=:ips".
                           format(self.table_name), {'ips': key}).fetchall()[0][0]

    def get_mac_via_hostname(self, key):
        cur = self.db_connect().cursor()
        return cur.execute("SELECT mac FROM {} WHERE hostname=:hostname".
                           format(self.table_name), {'hostname': key}).fetchall()

    def get_ip_via_hostname(self, key):
        cur = self.db_connect().cursor()
        return cur.execute("SELECT ip FROM {} WHERE hostname=:hostnames".
                           format(self.table_name), {'hostnames': key}).fetchall()

    def update_table_hosts(self):
        get_data = self.get_detail_computers()
        for key in get_data.keys():
            if len(self.get_ip(key)) != 0:
                if self.get_ip(key)[0][0] == key:
                    # check if hostname doesn't change
                    if get_data[key]['hostname'].lower() != self.get_hostname(key)[0][0] or \
                                    get_data[key]['mac'] != self.get_mac_via_hostname(key)[0][0]:
                        # update mac and hostname
                        self.update_row(get_data[key]['hostname'].lower(), get_data[key]['ip'], get_data[key]['mac'])
            else:
                self.insert_data(get_data[key]['hostname'].lower(), get_data[key]['ip'], get_data[key]['mac'])

    def get_broadcast(self, host):
        broad = ''
        i = 0
        for line in host.split('.'):

            if i < 3:
                broad += line + '.'
            i += 1
        broad += '255'
        return broad

    def read_fetchmail(self):
        sbj = 'Subject: '
        try:
            for host in self.ssh_read_data('172.25.0.196', '/var/spool/mail/wakeonlan', '/root/.ssh/id_rsa',
                                           'root').split('\n'):
                if host.startswith(sbj):
                    print repr(host)
                    get_host = host[len(sbj):]
                    print get_host
                    if self.regex_ip(get_host):
                        print 'Turn up via IP'
                        ip_broadcast = get_host[:len(get_host) - 2] + '255'
                    else:
                        if host.endswith('.eleks-software.local'):
                            print 'Turn up via hostname'
                            get_ip = self.get_ip_via_hostname(get_host.lower())
                            ip_broadcast = self.get_broadcast(get_ip[0][0])
                        else:
                            print 'Turn up via ADDhostname'
                            host = get_host + '.eleks-software.local'
                            get_host = self.get_ip_via_hostname(host)[0][0]
                            ip_broadcast = self.get_broadcast(get_host)
                else:
                    pass
        except Exception as e:
            print e


class DBGATES(DB, NetworkInformation):
    def insert_data(self, eth, broadcast, addr):
        con = self.db_connect()
        cur = con.cursor()
        cur.execute("INSERT INTO {}(eth, broadcast, addr) VALUES(?, ?, ?)".
                    format(self.table_name), (eth, broadcast, addr))
        con.commit()
        con.close()

    def get_broadcast_table(self, key):
        cur = self.db_connect().cursor()
        return cur.execute("SELECT broadcast FROM {} WHERE broadcast=:ips".
                           format(self.table_name), {'ips': key}).fetchall()

    def get_eth_via_brod(self, key):
        cur = self.db_connect().cursor()
        return cur.execute("SELECT eth FROM {} WHERE broadcast=:ips".
                           format(self.table_name), {'ips': key}).fetchall()

    def update_table(self):
        print self.get_net_add()
        for line in self.get_net_add():
            print line['addr']
            print self.get_broadcast_table(line['broadcast'])
            if len(self.get_broadcast_table(line['broadcast'])) !=0:
                    print 'ok'
            else:
                self.insert_data(line['eth'],line['broadcast'], line['addr'])
