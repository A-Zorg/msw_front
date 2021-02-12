from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.webdriver import ActionChains
import time
import os

class CustomDriver():
    def __init__(self, webdriver):
        self.webdriver = webdriver
        self.webdriver.implicitly_wait(10)

    def __get_selector_type(self,selector_type):
        selector_type = selector_type.lower()

        if selector_type == 'xpath':
            return By.XPATH
        elif selector_type == 'css':
            return By.CSS_SELECTOR
        elif selector_type == 'class_name':
            return By.CLASS_NAME
        elif selector_type == 'id':
            return By.ID
        elif selector_type == 'tag':
            return By.TAG_NAME
        elif selector_type == 'name':
            return By.NAME
        elif selector_type == 'link':
            return By.LINK_TEXT
        elif selector_type == 'partial_link':
            return By.PARTIAL_LINK_TEXT
        else:
            raise Exception('selector type is incorrect!')


    def click(self, selector, selector_type = 'xpath'):
        st = self.__get_selector_type(selector_type)
        element = self.webdriver.find_element(st, selector)
        element.click()

    def click_with_wait(self, selector, selector_type = 'xpath'):
        st = self.__get_selector_type(selector_type)

        wait = WebDriverWait(self.webdriver,
                             timeout=10,
                             poll_frequency=1,
                             ignored_exceptions=[
            NoSuchElementException,
            ElementNotVisibleException,
            ElementNotSelectableException
        ])
        element = wait.until(EC.element_to_be_clickable((st, selector)))
        element.click()

    def input_text(self, text, selector, selector_type = 'xpath'):
        st = self.__get_selector_type(selector_type)
        element = self.webdriver.find_element(st, selector)
        element.clear()
        element.send_keys(text)

    def screenshot_of_element(self, file_name, selector, selector_type = 'xpath'):
        st = self.__get_selector_type(selector_type)
        path = os.getcwd()+f'/files/{file_name}.png'

        wait = WebDriverWait(self.webdriver,
                             timeout=10,
                             poll_frequency=1,
                             ignored_exceptions=[
                                 NoSuchElementException,
                                 ElementNotVisibleException,
                                 ElementNotSelectableException
                             ])
        # element = self.webdriver.find_element(st, selector)
        element = wait.until(EC.visibility_of_element_located((st, selector)))
        time.sleep(0.5)
        element.screenshot(path)

    def get_elements(self, selector,selector_type = 'xpath'):
        st = self.__get_selector_type(selector_type)
        elements = self.webdriver.find_elements(st, selector)
        return elements

    def get_atribute(self, selector,attribute='innerHTML', selector_type='xpath'):
        st = self.__get_selector_type(selector_type)
        element = self.webdriver.find_element(st, selector)
        return element.get_attribute(attribute)

    def click_by_coordinates(self, x,y):
        if 'get' in dir(self.webdriver):
            action = ActionChains(self.webdriver)
            action.move_by_offset(int(x), int(y)).click().perform()
        else:
            raise Exception('object is element of page')

    def drug_and_drop(self, selector, selector_type='xpath', x=0,y=0):
        if 'get' in dir(self.webdriver):
            st = self.__get_selector_type(selector_type)
            element = self.webdriver.find_element(st, selector)
            action = ActionChains(self.webdriver)
            action.drag_and_drop_by_offset(element, x, y).perform()
        else:
            raise Exception('object is element of page')

    def move_to_element(self, selector, selector_type='xpath', x=0,y=0):
        if 'get' in dir(self.webdriver):
            st = self.__get_selector_type(selector_type)
            element = self.webdriver.find_element(st, selector)
            action = ActionChains(self.webdriver)
            action.move_to_element(element).perform()
        else:
            raise Exception('object is element of page')
    def get_url(self):
        if 'get' in dir(self.webdriver):
            return self.webdriver.current_url()
        else:
            raise Exception('object is element of page')

    def use_url(self, url):
        if 'get' in dir(self.webdriver):
            self.webdriver.get(url)
        else:
            raise Exception('object is element of page')

    def quit(self):
        if 'get' in dir(self.webdriver):
            self.webdriver.quit()
        else:
            raise Exception('object is element of page')























































