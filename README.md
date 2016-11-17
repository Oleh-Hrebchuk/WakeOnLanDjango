#Host django 192.168.0.1
sudo apt-get update
apt-get install python-pip apache2 libapache2-mod-wsgi
pip install virtualenv
mkdir /opt/wakeonlan_service
cd /opt/wakeonlan_service
virtualenv wakeonlanenv
source wakeonlanenv/bin/activate
pip install django

pip install django-bootstrap3

apt-get install python-paramiko
nano /opt/wakeonlan_service/wakeonlan/settings.py
DEBUG = False
ALLOWED_HOSTS = [‘ip-host’]
STATIC_ROOT = os.path.join("/opt/wakeonlan_service/static")
#Save it.
nano /opt/wakeonlan_service/wakeonlanapp/scripts.py
configFilePath = r'/opt/wakeonlan_service/wakeonlanapp/wakeonlan.conf'
#save it
./manage.py makemigrations
./manage.py migrate
python manage.py createsuperuser
./manage.py collectstatic
./manage.py runserver 0.0.0.0:8000
#Check if frontend up.
deactivate
nano /etc/apache2/sites-enabled/000-default.conf
<VirtualHost *:80>

Alias /static/ /opt/wakeonlan_service/static/
<Directory /opt/wakeonlan_service/static>
Require all granted
</Directory>
WSGIScriptAlias / /opt/wakeonlan_service/wakeonlan/wsgi.py
<Directory /opt/wakeonlan_service/wakeonlan/>
<Files wsgi.py>
Require all granted
</Files>
</Directory>
</VirtualHost>
#save it.
chown :www-data /opt/wakeonlan_service

nano /opt/wakeonlan_service/wakeonlanapp/wakeonlan.conf
[general]
key_filename = /root/.ssh/id_rsa
ssh_host = 192.168.0.2
ssh_user = djangouser
place_wakeonlan = /opt/wakeonlandjango/c_wake_on_lan.py


#Host with wakeonlan 192.168.0.2
mkdir /opt/wakeonlandjango
copy all files from remote_files to /opt/wakeonlandjango
apt-get install sqlite3
apt-get install python-pip
pip install nmap
pip install netifaces
apt-get install python-paramiko

nano /opt/wakeonlandjango/wakeonlan.conf
[general]
domain = .eleks-software.local

[database]
name_db = /opt/ wakeonlandjango /mac_db.sqlite3
table_hosts = hosts
tables_gates = gates

[nmap]
range_network = 192.26.1.0/24, 192.5.2.0/24
#save it
nano /opt/wakeonlandjango/c_config_parce.py
configFilePath = r'/opt/wakeonlandjango/wakeonlan.conf'
#run configurations
/opt/wakeonlandjango/a_first_configuration.py 
/opt/wakeonlandjango/a_update_database_data.py



