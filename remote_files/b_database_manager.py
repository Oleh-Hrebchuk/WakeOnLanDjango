import sqlite3
from b_get_computer_info import ScannCopmputers
from c_network import NetworkInformation
from c_config_parce import GetConfig
from c_logging import LoggingData

__author__ = 'oleh.hrebchuk'


class ManageDB(GetConfig, LoggingData):
    def __init__(self, table_name):
        self.name_db = self.get_value_confing('database', 'name_db')
        self.table_name = table_name

    def db_connect(self):
        con = sqlite3.connect(self.name_db)
        return con

    def create_table(self):
        cur = self.db_connect().cursor()
        cur.execute('''CREATE TABLE {} (id INTEGER PRIMARY KEY AUTOINCREMENT)'''.format(self.table_name))

    def add_columns(self, *args):
        cur = self.db_connect().cursor()
        for i in args:
            cur.execute("ALTER TABLE {} ADD COLUMN {} INTEGER".format(self.table_name, i))
        self.db_connect().commit()
        self.db_connect().close()


class ManageHostsTable(ManageDB, ScannCopmputers):
    def insert_data(self, hostname, ip, mac):
        try:
            con = self.db_connect()
            cur = con.cursor()
            cur.execute("INSERT INTO hosts(hostname, ip, mac) VALUES(?, ?, ?)", (hostname, ip, mac))
            con.commit()
            con.close()
        except Exception as e:
            self.loger(e, 'error')

    def update_row(self, hostname, ip, mac):
        con = self.db_connect()
        cur = con.cursor()
        cur.execute("UPDATE hosts SET  hostname= ? ,mac = ? WHERE ip= ?", (hostname, mac, ip))
        con.commit()
        con.close()

    def get_hostname(self, key):
        con = self.db_connect()
        cur = con.cursor()
        return cur.execute("SELECT hostname FROM hosts WHERE ip=:ips", {'ips': key}).fetchall()[0][0]

    def get_ip(self, key):
        cur = self.db_connect().cursor()
        return cur.execute("SELECT ip FROM hosts WHERE ip=:ips", {'ips': key}).fetchall()

    def get_mac_via_ip(self, key):
        cur = self.db_connect().cursor()
        return cur.execute("SELECT mac FROM hosts WHERE ip=:ips", {'ips': key}).fetchall()[0][0]

    def get_mac_via_hostname(self, key):
        cur = self.db_connect().cursor()
        return cur.execute("SELECT mac FROM hosts WHERE hostname=:hostname", {'hostname': key}).fetchall()

    def get_ip_via_hostname(self, key):
        cur = self.db_connect().cursor()
        return cur.execute("SELECT ip FROM hosts WHERE hostname=:hostnames", {'hostnames': key}).fetchall()

    def update_table_hosts(self):
        for net in self.get_list_config('nmap', 'range_network'):
            print net
            try:
                get_data = self.get_detail_computers(net)
                for key in get_data.keys():
                    try:
                        if len(self.get_ip(key)) != 0:
                            if self.get_ip(key)[0][0] == key:
                                # check if hostname doesn't change
                                if get_data[key]['hostname'].lower() != self.get_hostname(key)[0][0] or \
                                                get_data[key]['mac'] != self.get_mac_via_hostname(key)[0][0]:
                                    # update mac and hostname
                                    self.update_row(get_data[key]['hostname'].lower(), get_data[key]['ip'],
                                                    get_data[key]['mac'])
                        else:
                            print get_data[key]['hostname'].lower(), get_data[key]['ip'], get_data[key]['mac']
                            self.insert_data(get_data[key]['hostname'].lower(), get_data[key]['ip'], get_data[key]['mac'])

                    except Exception as e:
                        self.loger(e, 'error')
                        continue

            except Exception as e:
                        self.loger(e, 'error')
                        continue

class ManageGatesTable(ManageDB, NetworkInformation):
    def insert_data(self, eth, broadcast, addr):
        con = self.db_connect()
        cur = con.cursor()
        cur.execute("INSERT INTO gates(eth, broadcast, addr) VALUES(?, ?, ?)", (eth, broadcast, addr))
        con.commit()
        con.close()

    def get_broadcast_table(self, key):
        cur = self.db_connect().cursor()
        return cur.execute("SELECT broadcast FROM gates WHERE broadcast=:ips", {'ips': key}).fetchall()

    def get_eth_via_brod(self, key):
        cur = self.db_connect().cursor()
        return cur.execute("SELECT eth FROM gates WHERE broadcast=:ips", {'ips': key}).fetchall()

    def update_table_gates(self):
        for line in self.get_net_add():
            if len(self.get_broadcast_table(line['broadcast'])) != 0:
                pass
            else:
                self.insert_data(line['eth'], line['broadcast'], line['addr'])
