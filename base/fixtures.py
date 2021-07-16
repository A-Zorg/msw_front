from selenium import webdriver
from behave import fixture
import os
import datetime
from selenium.webdriver.chrome.options import Options
from msedge.selenium_tools import Edge, EdgeOptions
from base.custom_driver import CustomDriver
import configparser
from base.service_functions import create_user_session

config = configparser.ConfigParser()
config.read("config/config.ini")


def txt_writer(message):
    with open('./xxx.txt', 'a') as file:
        file.write(f'date:{datetime.datetime.now()}: {message} \n')

def firefox():

    directory = os.getcwd() + '\\files'

    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", directory)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/vnd.ms-excel")
    profile.update_preferences()

    path = os.getcwd() + '/drivers/geckodriver.exe'
    os.environ['webdriver.gecko.driver'] = path

    driver = webdriver.Firefox(executable_path=path, firefox_profile=profile)
    return driver


def chrome():

    directory = os.getcwd() + '/files'

    options = Options()
    options.add_experimental_option("prefs", {
        "download.default_directory": directory,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    path = os.getcwd() + '/drivers/chromedriver.exe'
    os.environ['webdriver.chrome.driver'] = path

    driver = webdriver.Chrome(executable_path=path, options=options)
    return driver


def edge():

    directory = os.getcwd() + '/files'

    options = EdgeOptions()
    options.add_experimental_option("prefs", {
        "download.default_directory": directory,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    options.use_chromium = True

    path = os.getcwd() + '/drivers/msedgedriver.exe'
    os.environ['webdriver.msedge.driver'] = path

    driver = Edge(executable_path=path, options=options)
    return driver


@fixture
def browser(context, name='chrome'):
    """browser"""
    driver = eval(name)()
    context.driver = CustomDriver(driver)
    """requests session"""
    context.admin_session = create_user_session(**config['super_user'])
    context.manger_session = create_user_session(**config['manager_1'])
    """define host"""
    context.host = config['host']['host_api']
    context.host_front = config['host']['host_front']
    context.txt_writer = txt_writer

    yield

    context.driver.quit()
    context.admin_session.close()





















