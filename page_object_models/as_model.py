import time


class ASModel:
    as_sidebar = {'selector': 'div[class="as-buttons"]', 'selector_type': 'css'}
    accounting_tab = {'selector': '//span[contains(text(),"Accounting")]', 'selector_type': 'xpath'}
    transactions_tab = {'selector': '//span[contains(text(),"Transactions")]', 'selector_type': 'xpath'}
    reports_tab = {'selector': '//span[contains(text(),"Reports")]', 'selector_type': 'xpath'}
    burger_button = {'selector': 'button.menu-icon>span>i', 'selector_type': 'css'}
    accounting_table = {'selector': 'table.accounting--table', 'selector_type': 'css'}

    def __init__(self, webdriver):
        self.webdriver = webdriver

    def click_accounting_tab(self):
        for i in range(2):
            self.webdriver.move_to_element(**self.as_sidebar)
            self.webdriver.click_with_wait(**self.accounting_tab)
            # time.sleep(5)

        # self.webdriver.click(**{'selector': 'i.mdi-view-split-horizontal', 'selector_type': 'css'})
        # self.webdriver.move_to_element(**self.burger_button)

