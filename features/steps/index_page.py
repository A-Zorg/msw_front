from behave import *
from base.service_functions import check_image
import configparser
from base64 import b64decode
import time

selectors = configparser.ConfigParser()
selectors.read("config/selectors.ini")

@step("click on the icone: {icon}")
def step_impl(context, icon):
    element = eval(selectors['index_page_icons'][f'icon_{icon}'])
    context.driver.click_with_wait(*element)

@step("make screenshot of the image: {icone}")
def step_impl(context, icone):
    element = eval(selectors['index_page_image'][f'{icone}'])
    context.driver.screenshot_of_element(f'image_{icone}', *element)
    context.driver.click_by_coordinates(0, 0)

@step("get image from api: {icon}")
def step_impl(context, icon):
    url = context.host+f'/api/media/contest/{icon}/image'
    session = context.session
    response = session.get(url)

    image = response.json()['image']
    head, body = image.split(',', 1)

    with open(f'files/image_{icon}_api.png', 'wb') as file:
        file.write(b64decode(body))


"""------------------------------------------------------------------------------"""
@step("make screenshot of the icone: {icon}")
def step_impl(context, icon):
    element = eval(selectors['index_page_icons'][f'icon_{icon}'])
    time.sleep(3)
    context.driver.screenshot_of_element(f'icon_{icon}', *element)

@step("get icone from api: {icon}")
def step_impl(context, icon):
    url = context.host+f'/api/media/contest/{icon}/button'
    session = context.session
    response = session.get(url)

    with open(f'files/icon_{icon}_api.png', 'wb') as file:
        file.write(response.content)

@step("compare {key}s: {icon}")
def step_impl(context, key, icon):
    path_1 = f"files/{key}_{icon}.png"
    path_2 = f"files/{key}_{icon}_api.png"
    assert check_image(path_1, path_2)

"""--------------------------------------------------------------------------------"""

@step("compare current url with expected: {page}")
def step_impl(context, page):
    current_url = context.driver.get_url()
    expected_url = context.host_front+page
    assert current_url == expected_url
