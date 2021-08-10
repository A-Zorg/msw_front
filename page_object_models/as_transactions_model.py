
class ASTransactionsModel:
    as_sidebar = {'selector': 'div[class="as-buttons"]', 'selector_type': 'css'}
    accounting_tab = {'selector': '//span[contains(text(),"Accounting")]', 'selector_type': 'xpath'}
    create_transaction_tab = {'selector': '//span[contains(text(),"Create transaction")]', 'selector_type': 'xpath'}
    transactions_tab = {'selector': '//span[contains(text(),"Transactions")]', 'selector_type': 'xpath'}
    reports_tab = {'selector': '//span[contains(text(),"Reports")]', 'selector_type': 'xpath'}
    burger_button = {'selector': 'button.menu-icon>span>i', 'selector_type': 'css'}
    accounting_table = {'selector': 'table.accounting--table', 'selector_type': 'css'}
    accounting_user_select = {'selector': 'input[id^="input"]', 'selector_type': 'css'}

    general_input = {'selector': '[id^="input"]', 'selector_type': 'css'}

    def __init__(self, webdriver):
        self.webdriver = webdriver

    def get_transactions_inputs(self):
        inputs_names_list = [
            'user',
            'account',
            'side',
            'broker',
            'company',
            'clearing',
            'date_from',
            'date_to',
            'pagination',
        ]
        elements = self.webdriver.get_elements(**self.general_input)

        inputs_names_dict = {}
        for index, element in enumerate(elements):
            inputs_names_dict[inputs_names_list[index]] = element

        return inputs_names_dict

    def write_data_and_select(self, text, element):
        self.webdriver.click_with_wait(
            element=self.webdriver.get_element(selector='..', element=element)
        )
        self.webdriver.input_text(
            text=text,
            element=element
        )
        self.webdriver.click_with_wait(selector=f'//div[contains(text(),"{text}")]')

    def select_data(self, text, element):
        self.webdriver.click_with_wait(
            element=self.webdriver.get_element(selector='..', element=element)
        )
        self.webdriver.click_with_wait(selector=f'//div[text()="{text}"]')