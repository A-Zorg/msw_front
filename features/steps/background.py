from behave import *
import configparser
import time

config = configparser.ConfigParser()
config.read("config/selectors.ini")


@step("click on ST button")
def step_impl(context):
    element = eval(config['ST_button']['st'])
    context.driver.click_with_wait(*element)

@step("refresh index page")
def step_impl(context):
    context.driver.webdriver.refresh()

@step("pause {t} sec")
def step_impl(context, t):
    time.sleep(int(t))







