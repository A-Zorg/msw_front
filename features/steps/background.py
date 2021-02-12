from behave import *
import configparser

config = configparser.ConfigParser()
config.read("config/selectors.ini")


@step("click on ST button")
def step_impl(context):
    element = eval(config['ST_button']['st'])
    context.driver.click(*element)

