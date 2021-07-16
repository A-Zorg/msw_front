import paramiko
import requests
import pyotp
from datetime import date, timedelta, datetime
import configparser
import time
from base.db_interactions.index import User, UserGroup, Group
from base.db_interactions.accounting_system import UserBillType, UserBill, HistoryUserBill

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


def prepare_data(context):
    now = datetime.now()

    users = {
        'manager_1': User.get(username=config['manager_1']['username']),
        'manager_2': User.get(username=config['manager_2']['username'])
    }

    bill_types = UserBillType.all()
    for bill_type in bill_types:
        for user in users.values():
            is_exist = UserBill.get(
                user_id=user,
                bill_id=bill_type
            )

            if not is_exist:
                bill = UserBill.create(
                    user_id=user,
                    bill_id=bill_type,
                    amount=0
                )

                HistoryUserBill.create(
                    model_id=bill,
                    history_date=now-timedelta(days=90),
                    history_type='+',
                    history_created=now,
                    amount=0,
                    bill_id=bill_type,
                    user_id=user
                )

    for user in users.values():
        UserGroup.filter(customuser_id=user).delete()
        UserGroup.create(
            customuser_id=user,
            group_id=Group.get(name='OPS')
        )

    superuser = User.get(username=config['super_user']['username'])
    UserGroup.filter(customuser_id=superuser).delete()
    for group in ['RISK', 'FIN ENTRIES', 'FIN']:
        UserGroup.create(
            customuser_id=superuser,
            group_id=Group.get(name=group)
        )

























