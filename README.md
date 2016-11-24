##Host Django 192.168.0.1
###On this node will be Django server with front-end.
###Install packets
```
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
```
###Edit settings in django project.
```
nano /opt/wakeonlan_service/wakeonlan/settings.py
DEBUG = False
ALLOWED_HOSTS = [‘ip-host’]
STATIC_ROOT = os.path.join("/opt/wakeonlan_service/static")

#commend lines bellow
#STATICFILES_DIRS = [
#    os.path.join(BASE_DIR, "static"),
#]
```
###Press CTRL+X and save changes.

###Edit file scripts add path to wakeonlan.conf of django
```
nano /opt/wakeonlan_service/wakeonlanapp/scripts.py
configFilePath = r'/opt/wakeonlan_service/wakeonlanapp/wakeonlan.conf'
```
###Press CTRL+X and save changes.

###Migrate django project
```
./manage.py makemigrations
./manage.py migrate
python manage.py createsuperuser
./manage.py collectstatic
deactivate
```
###Configure apache service
```
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
```
###Press CTRL+X and save changes.

###Add permisions.
```
chown :www-data /opt/wakeonlan_service
```
###Configure wakeonlan.conf add path to remote server.
```
nano /opt/wakeonlan_service/wakeonlanapp/wakeonlan.conf
[general]
key_filename = /root/.ssh/id_rsa
ssh_host = 192.168.0.2
ssh_user = djangouser
place_wakeonlan = /opt/wakeonlandjango/c_wake_on_lan.py
```
###Press CTRL+X and save changes.

###Restart apache service
```
/etc/init.d/apache2 restart
```

##Host with wakeonlan 192.168.0.2 where is scrpits with wakeonlan and database.
###Install packages
```
mkdir /opt/wakeonlandjango
copy all files from remote_files to /opt/wakeonlandjango
apt-get install sqlite3
apt-get install python-pip
apt-get install nmap
pip install python-nmap
pip install netifaces
apt-get install python-paramiko
```
###Edit wakeonlan.conf.
```
nano /opt/wakeonlandjango/wakeonlan.conf
[general]
domain = .eleks-software.local

[database]
name_db = /opt/ wakeonlandjango /mac_db.sqlite3
table_hosts = hosts
tables_gates = gates

[nmap]
range_network = 192.26.1.0/24, 192.5.2.0/24
```
###Press CTRL+X and save changes.

###Add path to config in file c_config_parce.py.
```
nano /opt/wakeonlandjango/c_config_parce.py
configFilePath = r'/opt/wakeonlandjango/wakeonlan.conf'
```
###Press CTRL+X and save changes.

###Run first configurations.
```
/opt/wakeonlandjango/a_first_configuration.py 
/opt/wakeonlandjango/a_update_database_data.py
```
###Add update database of computers to cron
```
crontab -e
* 12 * * * /opt/wakeonlandjango/a_update_database_data.py >> /dev/null 2>&1
```
###Press CTRL+X and save changes.
