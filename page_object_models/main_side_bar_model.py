

class MainSideBar:
    logo = {'selector': '.logo', 'selector_type': 'css'}
    burger_button = {'selector': 'button.menu-icon>span>i', 'selector_type': 'css'}
    main_page_button = {'selector': '//div[contains(text(),"Main page")]', 'selector_type': 'xpath'}
    daily_review_button = {'selector': '//div[contains(text(),"Daily review")]', 'selector_type': 'xpath'}
    reconciliation_button = {'selector': '//div[contains(text(),"Reconciliation")]', 'selector_type': 'xpath'}
    as_button = {'selector': '//div[contains(text(),"Accounting system")]', 'selector_type': 'xpath'}
    trader_profile_button = {'selector': '//div[contains(text(),"Trader profile)]', 'selector_type': 'xpath'}
    podcast_button = {'selector': '//div[contains(text(),"After close (podcast)")]', 'selector_type': 'xpath'}
    logout_button = {'selector': '//div[contains(text(),"Log out")]', 'selector_type': 'xpath'}



    def __init__(self, webdriver):
        self.webdriver = webdriver

    def click_logo(self):
        self.webdriver.click_with_wait(**self.logo)

    def click_burger(self):
        self.webdriver.click_with_wait(**self.burger_button)

    def click_main_page(self):
        self.webdriver.click_with_wait(**self.main_page_button)

    def click_daily_review(self):
        self.webdriver.click_with_wait(**self.daily_review_button)

    def click_reconciliation(self):
        self.webdriver.click_with_wait(**self.reconciliation_button)

    def click_accounting_system(self):
        self.webdriver.click_with_wait(**self.as_button)

    def click_trader_profile(self):
        self.webdriver.click_with_wait(**self.trader_profile_button)

    def click_podcast(self):
        self.webdriver.click_with_wait(**self.podcast_button)

    def click_logout(self):
        self.webdriver.click_with_wait(**self.logout_button)
