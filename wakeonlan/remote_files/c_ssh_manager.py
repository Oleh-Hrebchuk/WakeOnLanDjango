import paramiko
import logging


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