import time


class ASModel:
    as_sidebar = {'selector': 'div[class="as-buttons"]', 'selector_type': 'css'}
    accounting_tab = {'selector': '//span[contains(text(),"Accounting")]', 'selector_type': 'xpath'}
    create_transaction_tab = {'selector': '//span[contains(text(),"Create transaction")]', 'selector_type': 'xpath'}
    transactions_tab = {'selector': '//span[contains(text(),"Transactions")]', 'selector_type': 'xpath'}
    reports_tab = {'selector': '//span[contains(text(),"Reports")]', 'selector_type': 'xpath'}
    burger_button = {'selector': 'button.menu-icon>span>i', 'selector_type': 'css'}
    accounting_table = {'selector': 'table.accounting--table', 'selector_type': 'css'}
    accounting_user_select = {'selector': 'input[id^="input"]', 'selector_type': 'css'}
    general_input = {'selector': '[id^="input"]', 'selector_type': 'css'}
    transaction_type = {'selector': '//div[@class="v-list-item__content"]/div[text()="{}"]', 'selector_type': 'xpath'}

    def __init__(self, webdriver):
        self.webdriver = webdriver

    def click_accounting_tab(self, button_name):
        for i in range(2):
            self.webdriver.move_to_element(**self.as_sidebar)
            self.webdriver.click_with_wait(**getattr(self, button_name))
            # time.sleep(5)

        # self.webdriver.click(**{'selector': 'i.mdi-view-split-horizontal', 'selector_type': 'css'})
        # self.webdriver.move_to_element(**self.burger_button)

    def get_create_transactions_inputs(self):
        inputs_names_list = [
            'effective_date',
            'transaction_type',
            'affected_user',
            'from_account',
            'to_account',
            'amount',
            'currency',
            'approver',
            'comment',
        ]
        elements = self.webdriver.get_elements(**self.general_input)

        inputs_names_dict = {}
        for index, element in enumerate(elements):
            inputs_names_dict[inputs_names_list[index]] = element

        return inputs_names_dict

    def choose_transaction_type(self, transaction_type, element):
        self.webdriver.click_with_wait(element=self.webdriver.get_element(selector='..', element=element))
        self.webdriver.click_with_wait(
            selector=self.transaction_type['selector'].format(transaction_type),
            selector_type=self.transaction_type['selector_type']
        )

    def write_data(self, text, element):
        self.webdriver.click_with_wait(element=self.webdriver.get_element(selector='..', element=element))
        self.webdriver.input_text(text=text, element=element)

    def write_data_and_select(self, text, element):
        self.webdriver.click_with_wait(element=self.webdriver.get_element(selector='..', element=element))
        self.webdriver.input_text(text=text, element=element)
        self.webdriver.click_with_wait(selector=f'//span[contains(text(),"{text}")]')

    def select_data(self, text, element):
        self.webdriver.click_with_wait(element=self.webdriver.get_element(selector='..', element=element))
        self.webdriver.click_with_wait(selector=f'//div[text()="{text}"]')

    def multiple_select(self, managers, amount):
        qty_row = len(self.webdriver.get_elements(
            selector='form > div.ps.ps--active-y > div',
            selector_type='css')
        )
        for row_number in range(1, qty_row - 1):
            row = self.webdriver.get_element(
                selector=f'form > div.ps.ps--active-y > div:nth-child({row_number})',
                selector_type='css'
            )
            user_input = self.webdriver.get_element(selector=f'input[type="text"]', selector_type='css', element=row)
            user = self.webdriver.get_atribute(element=user_input, attribute='value')
            if (managers[0] in user) or (managers[1] in user):
                amount_input = self.webdriver.get_element(selector=f'input[type="number"]', selector_type='css', element=row)
                self.webdriver.input_text(text=amount, element=amount_input)
