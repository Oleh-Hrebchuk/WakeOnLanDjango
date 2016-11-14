import os
from b_database_manager import *
from c_config_parce import GetConfig
__author__ = 'oleh.hrebchuk'

c = GetConfig()
name_db = c.get_value_confing('database','name_db')

h = ManageHostsTable('hosts')
g = ManageGatesTable('gates')

if os.path.exists(name_db) is False:
    with open(name_db, 'w+')as f:
        f.write('')

h.create_table()
h.add_columns('hostname', 'ip', 'mac')

g.create_table()
g.add_columns('eth', 'broadcast', 'addr')
