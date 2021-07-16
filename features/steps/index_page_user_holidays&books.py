from behave import *
from base.service_functions import check_image, refine_holidays, \
    mysql_select, pgsql_del, pgsql_select, remove_spaces
import configparser
from base64 import b64decode
import time
import random
import datetime

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

"""---------------------------------------BOOKS------------------------------------------------"""


@step("make general select of books")
def step_impl(context):
    sel = "SELECT b.name, b.author, s.title, s.id FROM books as b JOIN sub_sections as s ON b.sub_section_id=s.id "
    db = config['mysql_db']
    context.general_select = mysql_select(sel, **db)

@step("get all genres")
def step_impl(context):
    genres=set()
    for book in context.general_select:
        genres.add(book[2])
    context.genres = genres


@step("choose category on the Index page")
def step_impl(context):
    genre_list = list(context.genres)
    context.random_category = random.choice(genre_list)

    context.driver.visibility_of_element(*eval(selectors['index_page_books']['marker']))
    context.driver.click_with_wait(*eval(selectors['index_page_books']['category']))
    context.driver.click_element_in_list(context.random_category, *eval(selectors['index_page_books']['category_item']))

@step("make select with chosen {typo}")
def step_impl(context, typo):
    if typo == 'category':
        sel = f"SELECT b.name, b.author, s.title, s.id FROM books as b " \
              f"JOIN sub_sections as s ON b.sub_section_id=s.id " \
              f"WHERE s.title = '{context.random_category}'"
    elif typo == 'search_text':
        sel = f"SELECT b.name, b.author, s.title, s.id " \
              f"FROM books as b JOIN sub_sections as s ON b.sub_section_id=s.id " \
              f"WHERE b.name LIKE '%{context.search_text}%' OR b.author LIKE '%{context.search_text}%'"
    db = config['mysql_db']
    category_select = mysql_select(sel, **db)
    context.result=[]
    for book in category_select:
        context.result.append(str(book[1]+' '+book[0]).upper())

@step("check selected books on the index page")
def step_impl(context):
    time.sleep(3)
    els = context.driver.get_elements(*eval(selectors['index_page_books']['book']))

    for el in els:
        el.location_once_scrolled_into_view
        if el.text not in context.result:
            assert False
    assert True
"""--------------------------"""
@step("get some search random phrase")
def step_impl(context):
    book_names=set()
    for book in context.general_select:
        book_names.add(book[0])
        book_names.add(book[1])
    search_text = random.choice(list(book_names))
    context.search_text = search_text[1:-1]

@step("perform search by the random phrase")
def step_impl(context):
    context.driver.visibility_of_element(*eval(selectors['index_page_books']['marker']))
    context.driver.input_text(context.search_text, *eval(selectors['index_page_books']['search_field']))
    context.driver.click_with_wait(*eval(selectors['index_page_books']['search_button']))

"""----------------------------------------------LIKES-------------------------------------------"""
@step("get {typo} number of likes")
def step_impl(context, typo):
    amount_like = context.driver.get_atribute(*eval(selectors['index_page_news']['outer_like_amount']))
    if typo == 'initial':
        context.initial_like = amount_like
    elif typo == 'intermediate':
        context.intermediate_like = amount_like


@step("click the like button from {locus} page")
def step_impl(context, locus):
    if locus == 'index':
        selector = eval(selectors['index_page_news']['outer_like_button'])
    elif locus == 'news':
        selector = eval(selectors['index_page_news']['inner_like_button'])

    context.driver.click_with_wait(*selector)

@step("open news")
def step_impl(context):
    context.driver.click_with_wait(*eval(selectors['index_page_news']['news_block']))

@step("compare number of likes with {typo} number")
def step_impl(context, typo):
    amount_like = context.driver.get_atribute(*eval(selectors['index_page_news']['inner_like_amount']))
    if typo == 'initial':
        initial_like = amount_like
        assert initial_like == context.initial_like
    elif typo == 'intermediate':
        intermediate_like = amount_like
        assert intermediate_like == context.intermediate_like

@step("Exit the news block")
def step_impl(context):
    context.driver.click_by_coordinates(0, 0)

"""-------------------------------------------VIEWS---------------------------------------------"""

@step("delete all views")
def step_impl(context):
    sel = "DELETE FROM index_postview"
    db = config['pg_db']
    pgsql_del(sel, **db)

@step("get initial number of views")
def step_impl(context):
    context.initial_views = context.driver.get_atribute(*eval(selectors['index_page_news']['outer_view_amount']))

@step("compare number of views with initial number")
def step_impl(context):
    amount_view = context.driver.get_atribute(*eval(selectors['index_page_news']['inner_view_amount']))
    assert int(amount_view) == int(context.initial_views)+1


"""-------------------------------------------NEWS TEXT----------------------------------------------"""

@step("get news from db")
def step_impl(context):
    data_formater = lambda x: '.'.join([part[-2] + part[-1] for part in x.split('-')[::-1]])

    sel = "SELECT * FROM index_news"
    db = config['pg_db']
    news = pgsql_select(sel, **db)

    context.news=[]
    for row in news:
        d = data_formater(str(row[4].date()))
        h_m = str(row[4].time())[0:5]
        context.news.append(remove_spaces(row[1]+row[2]) + h_m + d)
    # with open('C:\\Users\\wsu\\Desktop\\xxx.txt', 'a', encoding='utf-8') as file:
    #     file.write(str(context.news) + '\n')

@step("take text_news from {typo} page")
def step_impl(context, typo):
    time.sleep(3)
    if typo == 'index':
        prefix = 'outer'
    elif typo == 'news':
        prefix = 'inner'

    text = context.driver.get_atribute(*eval(selectors['index_page_news'][f'{prefix}_text']))
    headline = context.driver.get_atribute(*eval(selectors['index_page_news'][f'{prefix}_headline']))
    datum = context.driver.get_atribute(*eval(selectors['index_page_news'][f'{prefix}_datetime']))

    if typo == 'index':
        context.outer_result = remove_spaces(text) + remove_spaces(headline)+remove_spaces(datum)
    elif typo == 'news':
        context.inner_result = remove_spaces(text) + remove_spaces(headline)+remove_spaces(datum)

@step("compare news from index_page and news_page")
def step_impl(context):
    assert context.outer_result == context.inner_result

@step("check that all news are shown on index page")
def step_impl(context):
    for i in range(len(context.news)):
        time.sleep(2)
        headline_selector = selectors['index_page_news']['universal'].format(i+1, 1, '')
        text_selector = selectors['index_page_news']['universal'].format(i+1, 2, '')
        datum_selector = selectors['index_page_news']['universal'].format(i+1, 3, '/div[3]')

        context.driver.show_element(headline_selector)

        headline = context.driver.get_atribute(headline_selector)
        text = context.driver.get_atribute(text_selector)
        datum = context.driver.get_atribute(datum_selector)

        result = remove_spaces(headline) + remove_spaces(text)+remove_spaces(datum)

        if result in context.news:
            context.news.remove(result)
        else:
            assert False
"""------------------------------NEWS IMAGE----------------------------"""
@step("get news from db(image)")
def step_impl(context):
    sel = "SELECT id, title FROM index_news"
    db = config['pg_db']
    context.news = pgsql_select(sel, **db)

@step("get the id of the news being checked")
def step_impl(context):
    headline_selector = selectors['index_page_news']['universal'].format(1, 1, '')
    headline = context.driver.get_atribute(headline_selector)

    for row in context.news:
        if row[1] == headline:
            context.id_news = row[0]
            break
    assert context.id_news

@step("get image from api")
def step_impl(context):
    url = context.host+'/api/media/news/'+str(context.id_news)
    response = context.admin_session.get(url)
    with open('files/image_news_api.png', 'bw') as file:
        file.write(response.content)

@step("make screenshot of the news_image")
def step_impl(context):
    element = eval(selectors['index_page_news']['news_image'])
    context.driver.screenshot_of_element('image_news_msw', *element)
    context.driver.click_by_coordinates(0, 0)

@step("compare news_images")
def step_impl(context):
    path_1 = "files/image_news_api.png"
    path_2 = "files/image_news_msw.png"
    assert check_image(path_1, path_2)
"""-------------------------------------------------------------------------------"""























