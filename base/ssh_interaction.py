import paramiko
import requests
import pyotp
from datetime import date, timedelta
import configparser
import time

config = configparser.ConfigParser()
config.read("config/config.ini")

def get_user_account_group_file():
    with open('files/manager_ids.txt','w') as file:
        data_list=[
            config['user_accounts']['accounts'],
            config['user_groups']['groups']
        ]
        for part in data_list:
            file.write(str(part)+'\n')

def upload_server(host,user,secret,port):
    transport = paramiko.Transport((host, int(port)))
    transport.connect(username=user, password=secret)
    sftp = paramiko.SFTPClient.from_transport(transport)
    get_user_account_group_file()

    remotepath = '/home/alex_zatushevkiy/front_msw/manager_ids.txt'
    localpath = 'files/manager_ids.txt'
    sftp.put(localpath, remotepath)

    sftp.close()
    transport.close()

def loader(host,user,secret,port, sec=10):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=secret, port=port)

    stdin, stdout, stderr = client.exec_command('cd /smartteam/msw_server_9999/msw && '
                                                'python3 manage.py shell < /home/alex_zatushevkiy/10/cleaner_super.py &&'
                                                'python3 manage.py shell < /home/alex_zatushevkiy/front_msw/loader_msw.py')
    client.close()
    time.sleep(sec)

