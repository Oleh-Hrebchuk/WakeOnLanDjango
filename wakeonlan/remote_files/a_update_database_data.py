from b_database_manager import *
from c_config_parce import GetConfig
__author__ = 'oleh.hrebchuk'

c = GetConfig()
name_db = c.get_value_confing('database','name_db')

h = ManageHostsTable('hosts')
g = ManageGatesTable('gates')

h.update_table_hosts()
g.update_table_gates()