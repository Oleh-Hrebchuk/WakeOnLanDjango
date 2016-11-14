import ConfigParser
import ast
import paramiko
__author__ = 'oleh.hrebchuk'


class GetConfig(object):
    def get_value_confing(self, section, key):
        configParser = ConfigParser.RawConfigParser()
        configFilePath = r'wakeonlan.conf'
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
        
    def create_ssh_connection(self, host, user, key_filename):
        """
        Frame of ssh conection
        :param host: to connect
        :param user: user
        :return: return ssh_conect
        """
        try:
            ssh = paramiko.SSHClient()
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, 22, username=user, key_filename=key_filename)
            return ssh
        except Exception as e:
            self.add_to_file(self.path_error_log, str(self.date_log()) + ' ' + str(e) + ' ' + host + '\n')
            self.send_mail('Trigger: Script execution error', 'Current provider: {}\n'.
                           format(str(e)))

    def ssh_copy_file(self, host, src_dir, dst_dir, key_filename, login):
        """
        This method replace copy file to remote host
        :param host: host
        :param src_dir: source file
        :param dst_dir: destination file
        :return: None
        """
        try:
            ssh_connect = self.create_ssh_connection(host, login, key_filename)
            sftp = ssh_connect.open_sftp()
            # backup tcrules
            with sftp.open(dst_dir, 'r')as f:
                data = f.read()
            if 'tc-rulses-core' in data:
                sftp.get(dst_dir, '/opt/template-vpn/tcrules')
            sftp.put(src_dir, dst_dir)
            sftp.close()
        except Exception as e:
            self.add_to_file(self.path_error_log, str(self.date_log()) + ' ' + str(e) + ' ' + host + '\n')
            self.send_mail('Trigger: Script execution error', 'Current provider: {}\n'.
                           format(str(e)))
        finally:
            if ssh_connect:
                ssh_connect.close()

    def ssh_rem_comand(self, host, name_service, check, key_filename, login):
        """
            This could restart shorewall via ssh with check (check:'yes') and other services without check service.
            :param host: host
            :param name_service: service of linux(ipsec or shorewall)
            :param check: use 'yes' for check shorewall
            :return: None
        """
        try:
            ssh_connect = self.create_ssh_connection(host, login, key_filename)
            if check == 'yes':
                stdin, stdout, stderr = ssh_connect.exec_command('/etc/init.d/{} check'.format(name_service))
                if 'Shorewall configuration verified' in stdout.read():
                    ssh_connect.exec_command('/etc/init.d/{} restart'.format(name_service))
            else:
                ssh_connect.exec_command('/etc/init.d/{} restart'.format(name_service))
        except Exception as e:
            self.add_to_file(self.path_error_log, str(self.date_log()) + ' ' + str(e) + ' ' + host + '\n')
            self.send_mail('Trigger: Script execution error', 'Current provider: {}\n'.
                           format(str(e)))
        finally:
            if ssh_connect:
                ssh_connect.close()