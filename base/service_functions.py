import pyotp
import requests
import cv2
from mysql.connector import connection
import psycopg2
import re

def login(driver, username, password, totp):
    driver.use_url('https://mytest.sg.com.ua:9999/login')
    driver.input_text(username, '//*[@id="input-12"]')
    driver.input_text(password, '//*[@id="input-16"]')
    driver.click_with_wait('/html/body/div/div/div/main/div/div/div/div/div/div/form/div[3]/button[1]/span')

    totp_object = pyotp.TOTP(totp)
    driver.input_text(totp_object.now(), '//*[@id="input-30"]')
    driver.click_with_wait('/html/body/div/div/div/main/div/div/div/div/div/div/form/div[2]/button/span')


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
    resized = cv2.resize(image, (16,16), interpolation=cv2.INTER_AREA)

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
    with open('C:\\Users\\wsu\\Desktop\\xxx.txt', 'a') as file:
        file.write(str(_hash)+'\n')
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
    result = CompareHash(hash1,hash2)
    with open('C:\\Users\\wsu\\Desktop\\xxx.txt', 'a') as file:
        file.write(str(result)+'\n')
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

      return response

def pgsql_select(request, user,password, port, host, database):
  with psycopg2.connect(user=user, host=host, port=port,password=password,database=database,) as connect:
    cursor = connect.cursor()
    if request.startswith('SELECT'):
      cursor.execute(request)
      response = cursor.fetchall()

      return response

def pgsql_del(request, user,password, port, host, database):
  with psycopg2.connect(user=user, host=host, port=port,password=password,database=database,) as connect:
    cursor = connect.cursor()
    if request.startswith('DELETE'):
      cursor.execute(request)
      connect.commit()
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



















































