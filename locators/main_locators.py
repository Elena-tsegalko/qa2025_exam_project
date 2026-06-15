import os
from pages.elements import WebElement, ManyWebElements
from pages.base_page import WebPage

class MainPage(WebPage):
    def __init__(self, web_driver, url=''):
        if not url:
            url = os.getenv("MAIN_PAGE") or 'https://misshacosmetics.by/'

        super().__init__(web_driver, url)

    btn_catalog = WebElement(xpath='//*[@class="page-footer-menu"]//a[@href="/about/opt/"]')

    header_logo = WebElement(xpath="//a[contains(@class, 'page-header-logo')]")
    header_search = WebElement(xpath="//input[contains(@class, 'field-input--search')]")
    header_delivery = WebElement(xpath='//a[@title="Доставка и оплата"]')
    header_shops = WebElement(xpath='//a[@title="Магазины"]')
    header_user = WebElement(xpath="//button[contains(@class, 'user-login__toggle')]")
    header_favorites = WebElement(xpath="//a[@href='/favorite/']")
    header_cart = WebElement(xpath="//a[@href='/order/']")

    footer_logo = WebElement(xpath="//a[contains(@class, 'page-header-logo--footer')]")
    footer_subscribe_input = WebElement(xpath="//input[contains(@class, 'field-input--email')]")
    footer_subscribe_btn = WebElement(xpath="//button[contains(@class, 'subscription-form__btn')]")
    footer_phone = WebElement(xpath="//a[contains(@href, 'tel:')]")

    footer_about_company = WebElement(xpath='//a[@href="/about/company/"]')
    footer_oferta = WebElement(xpath='//a[@href="/about/terms/"]')
    footer_contacts = WebElement(xpath='//a[@href="/about/contacts/"]')
    footer_delivery = WebElement(xpath='//a[@href="/buyers/delivery-payment/"]')

