from behave import *
from base.service_functions import check_image, refine_holidays
import configparser
from base64 import b64decode
import time

config = configparser.ConfigParser()
config.read("config/config.ini")

selectors = configparser.ConfigParser()
selectors.read("config/selectors.ini")
"""------------------------------------------Holidays------------------------------------------------------"""
@step("get next 5 holidays")
def step_impl(context):
    context.holidays = refine_holidays(config['holidays_api'])


@step("compare actual holidays name_list with expected")
def step_impl(context):
    holidays = context.holidays
    for i in range(len(holidays)):
        name_expected = str(holidays[i][0])

        selelector_list = eval(selectors['index_page_holidays']['name'])
        selector = selelector_list[0].format(i + 2)
        name_actual = context.driver.get_atribute(selector=selector)

        assert name_actual == name_expected


@step("compare actual holidays date_list with expected")
def step_impl(context):
    holidays = context.holidays
    formating = lambda part: '-'.join(part.split('.')[::-1])
    for i in range(len(holidays)):
        date_expected = str(holidays[i][1])


        selelector_list = eval(selectors['index_page_holidays']['date'])
        selector = selelector_list[0].format(i+2)
        date_actual = context.driver.get_atribute(selector=selector)
        date_actual = formating(date_actual)

        assert date_actual == date_expected

"""-----------------------------------SERV and COMP-------------------------------------------------------"""

@step("check sevices field")
def step_impl(context):
    service = eval(selectors['index_page_serv&comp']['serv_name'])
    result_1 = context.driver.check_el_text('SERV', *service)

    service_amount = eval(selectors['index_page_serv&comp']['serv_amount'])
    result_2 = context.driver.check_el_text("-100", *service_amount)

    assert result_1==result_2==True
    # with open('C:\\Users\\wsu\\Desktop\\xxx.txt', 'a') as file:
    #     file.write(str(result_2) + '\n')
    # with open('C:\\Users\\wsu\\Desktop\\xxx.txt', 'a') as file:
    #     file.write(str(result_1) + '\n')

@step("check compensations field")
def step_impl(context):
    compensation = eval(selectors['index_page_serv&comp']['comp_name'])
    result_1 = context.driver.check_el_text('COMP', *compensation)

    compensation_amount = eval(selectors['index_page_serv&comp']['comp_amount'])
    result_2 = context.driver.check_el_text("200", *compensation_amount)

    assert result_1 == result_2 == True

@step("check total")
def step_impl(context):
    total = eval(selectors['index_page_serv&comp']['total'])
    result = context.driver.check_el_text('100', *total)


    assert result == True