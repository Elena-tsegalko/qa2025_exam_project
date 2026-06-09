import os
from pages.elements import WebElement, ManyWebElements
from pages.base_page import WebPage

class MainPage(WebPage):
    def __init__(self, web_driver, url=''):
        if not url:
            url = os.getenv("MAIN_PAGE") or 'https://misshacosmetics.by/'

        super().__init__(web_driver, url)

    btn_catalog = WebElement(xpath='//*[@class="page-footer-menu"]//a[@href="/about/opt/"]')

