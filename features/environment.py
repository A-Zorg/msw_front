from behave import use_fixture
from base.fixtures import browser
from base.ssh_interaction import upload_server, loader, prepare_data
import configparser
from base.service_functions import logout, login, modify_userdata, pgsql_select, refine_holidays

config = configparser.ConfigParser()
config.read("config/config.ini")

selectors = configparser.ConfigParser()
selectors.read("config/selectors.ini")

def before_all(context):
    """determinating of the browser"""
    browser_type = 'chrome'
    if context.config.userdata.get('browser'):
        browser_type = context.config.userdata['browser']
    use_fixture(browser, context, browser_type)
    """perform configurations"""
    # prepare_data(context)
    # upload_server(**config['server'])
    # loader(**config['server'])
    """"""


def before_feature(context, feature):
    if feature.tags:
        tag = feature.tags[0]
        login(context.driver, **config[tag])

def after_feature(context, feature):
    if feature.tags:
        logout(context.driver)













    # asd = pgsql_select("SELECT id, hr_id FROM index_customuser WHERE username= 'Lantern'",**config['pg_db'])
    # print(asd)
    # modify_userdata(context.session,
    #                 context.host,
    #                 asd[0][0],
    #                 asd[0][1],
    #                 134,
    #                 434
    #     )