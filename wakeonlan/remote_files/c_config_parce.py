import ConfigParser
import ast
__author__ = 'oleh.hrebchuk'


class GetConfig(object):
    def get_value_confing(self, section, key):
        configParser = ConfigParser.RawConfigParser()
        configFilePath = r'/root/repwakeonlan/wakeonlan.conf'
        configParser.read(configFilePath)
        value = configParser.get(section, key)
        return value

    def get_dict_config(self, section, key):
        return ast.literal_eval(self.get_value_confing(section, key))

    def get_list_config(self, section, key):
        return [val.strip() for val in self.get_value_confing(section, key).split(',')]
