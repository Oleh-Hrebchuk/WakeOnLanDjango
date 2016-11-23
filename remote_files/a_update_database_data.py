#!/usr/bin/python
from b_database_manager import *
from c_config_parce import GetConfig
__author__ = 'oleh.hrebchuk'

c = GetConfig()
name_db = c.get_value_confing('database','name_db')

g = ManageGatesTable('gates')
h = ManageHostsTable('hosts')

g.update_table_gates()
h.update_table_hosts()
