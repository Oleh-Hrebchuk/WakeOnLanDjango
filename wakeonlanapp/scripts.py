import ConfigParser
import ast
import paramiko
__author__ = 'oleh.hrebchuk'


class GetConfig(object):
    def get_value_confing(self, section, key):
        configParser = ConfigParser.RawConfigParser()
        configFilePath = r'/opt/wakeonlan_service/wakeonlanapp/wakeonlan.conf'
        configParser.read(configFilePath)
        value = configParser.get(section, key)
        return value

    def get_dict_config(self, section, key):
        return ast.literal_eval(self.get_value_confing(section, key))

    def get_list_config(self, section, key):
        return [val.strip() for val in self.get_value_confing(section, key).split(',')]


class SSHManager(GetConfig):
    def __init__(self):
        self.ssh_user = self.get_value_confing('general', 'ssh_user')
        self.key_filename = self.get_value_confing('general','key_filename')
        self.ssh_host = self.get_value_confing('general','ssh_host')
        self.place_wakeonlan = self.get_value_confing('general','place_wakeonlan')
        self.ssh_pass = self.get_value_confing('general','ssh_pass')
	
    def create_ssh_connection(self):
        """
        Frame of ssh conection
        :param host: to connect
        :param user: user
        :return: return ssh_conect
        """
        try:
            ssh = paramiko.SSHClient()
            #ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.ssh_host, 22, password=self.ssh_pass, username=self.ssh_user)
            return ssh
        except Exception as e:
            print(e)

    def ssh_rem_comand(self, name_cp):
        """
            This could restart shorewall via ssh with check (check:'yes') and other services without check service.
            :param host: host
            :param name_service: service of linux(ipsec or shorewall)
            :param check: use 'yes' for check shorewall
            :return: None
        """
        try:
            ssh_connect = self.create_ssh_connection()
            stdin, stdout, stderr = ssh_connect.exec_command('/opt/wakeonlandjango/a_core_django.py {}'.format(name_cp))
        except Exception as e:
            print(e)
        finally:
            if ssh_connect:
                ssh_connect.close()


