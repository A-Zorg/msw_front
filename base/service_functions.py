import pyotp
import requests
import cv2
from mysql.connector import connection
import psycopg2
import re
import datetime
import time

def login(driver, username, password, totp):
    driver.use_url('https://mytest.sg.com.ua:9999/login')
    driver.input_text(username, '//*[@id="input-11"]')
    driver.input_text(password, '//*[@id="input-15"]')
    driver.click_with_wait(selector='button[type="submit"]', selector_type='css')
    totp_object = pyotp.TOTP(totp).now()
    driver.input_text(totp_object, '//*[@id="input-29"]')
    driver.click_with_wait(selector='button[type="submit"]', selector_type='css')

    if 'twofa' in driver.get_url():
        while True:
            totp_object_next = pyotp.TOTP(totp).now()
            if totp_object_next != totp_object:
                driver.input_text(totp_object_next, '//*[@id="input-29"]')
                driver.click_with_wait(selector='button[type="submit"]', selector_type='css')

                break


def logout(driver):
    driver.click('/html/body/div/div/div/header/div/button/span/i')
    driver.click('/html/body/div/div/div[2]/aside/div[1]/div/div/div[2]/div')

def create_user_session(username, password, totp):
    start = 'https://mytest-server.sg.com.ua:9999/admin/'
    end = 'https://mytest-server.sg.com.ua:9999/admin/login/?next=/admin/'
    session = requests.Session()
    totp_code = pyotp.TOTP(totp)

    session.get(start)
    request_dict = {'username': username, 'password': password, 'next': '/admin/'}
    request_dict['csrfmiddlewaretoken'] = session.cookies['csrftoken']
    request_dict['otp_token'] = totp_code.now()
    session.post(end, data=request_dict, headers={"Referer": end})
    return session


"""--------------------------------CHECK PICTURES-------------------------------------"""
def CalcImageHash(FileName):
    image = cv2.imread(FileName)
    resized = cv2.resize(image, (16, 16), interpolation=cv2.INTER_AREA)

    gray_image = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    avg = gray_image.mean()

    ret, threshold_image = cv2.threshold(gray_image, avg, 255, 0)
    _hash = ""
    for x in range(16):
        for y in range(16):
            val = threshold_image[x, y]
            if val == 255:
                _hash = _hash + "1"
            else:
                _hash = _hash + "0"
    return _hash

def CompareHash(hash1, hash2):
    l = len(hash1)
    i = 0
    count = 0
    while i < l:
        if hash1[i] != hash2[i]:
            count = count + 1
        i = i + 1
    return count

def check_image(img1, img2):
    hash1 = CalcImageHash(img1)
    hash2 = CalcImageHash(img2)
    result = CompareHash(hash1, hash2)
    if result > 20:
        return False
    else:
        return True

"""---------------------------------------------SQL--------------------------------------------"""
def mysql_select(request, user,password, port, host, database):
    with connection.MySQLConnection(user=user, host=host, port=port,password=password,database=database) as connect:
        cursor = connect.cursor()
        if request.startswith('SELECT'):
            cursor.execute(request)
            response = cursor.fetchall()
            time.sleep(1)
            return response

def pgsql_select(request, user,password, port, host, database):
    with psycopg2.connect(user=user, host=host, port=port,password=password,database=database,) as connect:
        cursor = connect.cursor()
        if request.startswith('SELECT'):
            cursor.execute(request)
            response = cursor.fetchall()
            time.sleep(1)
            return response

def pgsql_del(request, user,password, port, host, database):
    with psycopg2.connect(user=user, host=host, port=port,password=password,database=database,) as connect:
        cursor = connect.cursor()
        if request.startswith('DELETE'):
          cursor.execute(request)
          connect.commit()
          time.sleep(1)
          return True
        else:
            return False

"""----------------------------------------work with UserData table------------------------------------------"""

def get_token(session, url, key='csrftoken'):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,'
                  'image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    }
    html = session.get(url, headers=headers)
    if key == 'csrftoken':
        token = re.findall('name="csrfmiddlewaretoken" value="([a-zA-Z0-9]*)">', html.text)[0]
    elif key == 'X-CSRFToken':
        token = re.findall('csrfToken: "([a-zA-Z0-9]*)"', html.text)[0]
    return token

def get_userdata_page(session, hr_id):
    url = 'https://mytest-server.sg.com.ua:9999/admin/reconciliation/userdata/'
    response = session.get(url)
    html = response.text
    url_part = re.findall(r'<a href="([a-z0-9/]*)">{0}</a>'.format(hr_id), html)[0]
    return url_part

def modify_userdata(session, host, id, hr_id, prev_m_n, acc_amount):
    url = host + get_userdata_page(session, hr_id)
    token = get_token(session, url)
    data = {'user': id,
            'csrfmiddlewaretoken': token,
            'prev_month_net': prev_m_n,
            'account': acc_amount,
            'qty_of_reconciliations': '0',
            '_save': 'Save',
            }

    response = session.post(url, data=data, headers={"Referer": url})
    return response.ok

"""--------------------------HOLIDAYS-------------------------------------"""


def get_holidays(config):
    countries = ['US', 'GB']
    holidays = {
        'New Year\'s Day': '',
        'Martin Luther King, Jr. Day': '',
        'Washington\'s Birthday': '',
        'Memorial Day': '',
        'Independence Day': '',
        'Labour Day': '',
        'Thanksgiving Day': '',
        'Christmas Day': '',
        'Good Friday': '',
                }
    for country in countries:
        url = f"https://public-holiday.p.rapidapi.com/2021/{country}"

        headers = {
            'x-rapidapi-key': config['x-rapidapi-key'],
            'x-rapidapi-host': config['x-rapidapi-host']
        }

        response = requests.get(
            url=url,
            headers= headers
        )
        for i in response.json():
            if holidays.get(i['name']) == '':
                holidays[i['name']] = datetime.date.fromisoformat(i['date'])
    holidays['Labor Day'] = holidays['Labour Day']
    del holidays['Labour Day']

    return holidays

def refine_holidays(config):
    holidays = get_holidays(config)
    now = datetime.date.today()
    ref_hol = []
    for key, value in holidays.items():
        if value >= now:
            ref_hol.append([key, value])
    ref_hol = sorted(ref_hol, key=lambda lis: lis[1])

    return ref_hol[:5]


"""----------------------------------------------MINOR functions-------------------------------------------------"""
def remove_spaces(text):
    text = text.replace(' ', '')
    text = text.replace('\n', '')
    text = text.replace('\t', '')
    text = text.replace('\r', '')
    return text


"""--------------------------------------------------------------------------------------------------"""













































