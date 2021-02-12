from behave import *
from base.service_functions import check_image
import configparser
from base64 import b64decode
import time

config = configparser.ConfigParser()
config.read("config/selectors.ini")


@step("click on the icone: {icone}")
def step_impl(context, icone):
    element = eval(config['index_page_icons'][f'icon_{icone}'])
    context.driver.click_with_wait(*element)

@step("make screenshot of the image: {icone}")
def step_impl(context, icone):
    element = eval(config['index_page_image'][f'{icone}'])
    context.driver.screenshot_of_element(f'image_{icone}', *element)
    context.driver.click_by_coordinates(0,0)

@step("get image from api: {icone}")
def step_impl(context, icone):
    url = context.host+f'/api/media/contest/{icone}/image'
    session = context.session
    response = session.get(url)

    image = response.json()['image']
    head, body = image.split(',', 1)

    with open(f'files/image_{icone}_api.png','wb') as file:
        file.write(b64decode(body))


"""------------------------------------------------------------------------------"""
@step("make screenshot of the icone: {icone}")
def step_impl(context, icone):
    element = eval(config['index_page_icones'][f'icone_{icone}'])
    context.driver.screenshot_of_element(f'icone_{icone}', *element)

@step("get icone from api: {icone}")
def step_impl(context, icone):
    url = context.host+f'/api/media/contest/{icone}/button'
    session = context.session
    response = session.get(url)

    with open(f'files/icone_{icone}_api.png','wb') as file:
        file.write(response.content)

@step("compare {key}s: {icone}")
def step_impl(context, key, icone):
    path_1 = f"files/{key}_{icone}.png"
    path_2 = f"files/{key}_{icone}_api.png"
    assert check_image(path_1, path_2)

"""--------------------------------------------------------------------------------"""

@step("compare {key}s: {icone}")
def step_impl(context, key, icone):
    part = context.driver.get_url()
    path_2 = f"files/{key}_{icone}_api.png"
    assert check_image(path_1, path_2)
