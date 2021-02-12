import logging
from datetime import datetime, timedelta
import pandas
from django_otp.plugins.otp_totp.models import TOTPDevice
from index.models import CustomUser
from reconciliation.models import UserData, ReconciliationUserPropAccount, Service, SmartRiskMyAccount, ServicesAndCompensationUpdate, ImportHRUpdate,PropreportsUpdate
from accounting_system.models import UserMainData, UserBillTypes, \
    UserBill,CompanyBill, HistoryCompanyBill, HistoryUserBill, Transaction, AccountType, Broker
from accounting.models import UserAccData
from django.contrib.auth.models import Group
import time
import re

logging.basicConfig(
                    filename="dataset_log.log",
                    format='%(asctime)s (%(filename)s:%(lineno)d  %(threadName)s) %(name)s - %(levelname)s: %(message)s'
                   )
logger=logging.getLogger()
logger.setLevel(logging.INFO)

logger.info('start creation of datasets')

def check_bool(b):
    if type(b) == bool:
        return b
    elif b in ['True', 'true']:
        return True
    elif b in ['False', 'false']:
        return False
    else:
        raise Exception ('Value is not boolean!')

def check_date(d):
    if not d:
        return None
    elif type(d) in [datetime, pandas.Timestamp]:
        return d
    else:
        try:
            # date = datetime.fromisoformat(d)
            return d
        except:
            raise Exception('Incorrect date')

def check_recon_quantity(q):
    if not q:
        return 0
    else:
        return q

def clean_history(set_element):
    for i in range(1,len(set_element)):
        set_element[i].delete()


"""Create user bills types and compamy bills"""
user_bills_type = ['Investments','SmartPoints','Withdrawal',
                   'Account','Cash hub','Current Net balance']
try:
    for b_type in user_bills_type:
        bill_type = UserBillTypes.objects.create(name=b_type)
        bill_type.save()
    logger.info('company bills are created')
except:
    logger.error('types bill were created')
# ---------------------
company_bills_type = ['Company ServComp','Company Office Fees','Company Net Income',
                   'Company Social Fund','Company Daily Net']
try:
    HistoryCompanyBill.objects.all().delete()
    for c_type in company_bills_type:
        company_bill= CompanyBill.objects.get(name=c_type)
        company_bill.amount = 10000
        company_bill.save()
    logger.info('company bills are created')
except:
    logger.error('company bills were created')
"""----------------------------------------------------"""
tod_ay = datetime.today()
month = (tod_ay-timedelta(tod_ay.day+1)).month
year = (tod_ay - timedelta(tod_ay.day+1)).year
back_date = datetime(year, month, 28, 0, 0, 0, 00000)
"""-------------------------------manager configurations-------------------------------"""

with open('/home/alex_zatushevkiy/front_msw/manager_ids.txt', 'r') as file:
    user_account_list = file.readline()
    user_list = file.readline()

user_list = eval(user_list[:-1])
for username, groups in user_list.items():
    user = CustomUser.objects.get(username=username)
    user.groups.clear()
    for gr in Group.objects.filter(name__in=groups):
        user.groups.add(gr)

user_dict = eval(user_account_list[:-1])
for username in user_dict.keys():
    user = CustomUser.objects.get(username=username)

    UserAccData.objects.filter(user=user).delete()
    Service.objects.filter(user=user).delete()

    Service.objects.create(user=user,
                           name='SERV',
                           service_type='service',
                           amount=-100,
                           effective_datetime=back_date
                           ).save()
    Service.objects.create(user=user,
                           name='COMP',
                           service_type='compensation',
                           amount=200,
                           effective_datetime=back_date
                           ).save()
    Service.objects.create(user=user,
                           name='FEE',
                           service_type='fee',
                           amount=-50,
                           effective_datetime=back_date
                           ).save()

    ReconciliationUserPropAccount.objects.filter(user=user).delete()
    account_user = user_dict[username]
    acc_types = AccountType.objects.all()
    for acc_type in acc_types:
        regexp = acc_type.account_regexp
        if re.search(regexp, account_user):
            ReconciliationUserPropAccount.objects.create(user=user,
                                                         account=account_user,
                                                         account_type=acc_type,
                                                         month_adj_net=0.01,
                                                         ).save()


    UserBill.objects.filter(user=user).delete()
    HistoryUserBill.objects.filter(user=user).delete()
    for bill_type in UserBillTypes.objects.all():
        UserBill.objects.create(user=user,bill=bill_type, amount=0).save()


    userdata_object = UserData.objects.get(user=user)
    userdata_object.prev_month_net=0
    userdata_object.podushka=0
    userdata_object.account=0
    userdata_object.account_plus_minus=0
    userdata_object.cash=0
    userdata_object.social=0
    userdata_object.save()

    for bill_type in UserBillTypes.objects.all():
        query_set = HistoryUserBill.objects.filter(user=user, bill=bill_type)
        clean_history(query_set)

for bill in company_bills_type:
    query_set = HistoryCompanyBill.objects.filter(name=bill)
    clean_history(query_set)

"--------------------------------------------------------------"

for history_bill in HistoryUserBill.objects.all():
    history_bill.history_date = back_date- timedelta(30)
    history_bill.save()

for history_comp_bill in HistoryCompanyBill.objects.all():
    history_comp_bill.history_date = back_date- timedelta(30)
    history_comp_bill.save()
"""------------------------clear tables form prev month-----------------------------"""
from_date = datetime(year, month, 1, 0, 0, 0)
PropreportsUpdate.objects.filter(date_uploaded__gte=from_date).delete()
ServicesAndCompensationUpdate.objects.filter(date_uploaded__gte=from_date).delete()
ImportHRUpdate.objects.filter(date_uploaded__gte=from_date).delete()
SmartRiskMyAccount.objects.filter(date_uploaded__gte=from_date).delete()


logger.info('finish creation of datasets')





























