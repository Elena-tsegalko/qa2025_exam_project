import os
from pages.elements import WebElement, ManyWebElements
from pages.base_page import WebPage

class MainPage(WebPage):
    def __init__(self, web_driver, url=''):
        if not url:
            url = os.getenv("MAIN_PAGE") or 'https://misshacosmetics.by/'

        super().__init__(web_driver, url)

    btn_catalog = WebElement(xpath='//*[@class="page-footer-menu"]//a[@href="/about/opt/"]')
    header_logo = WebElement(xpath="//header//a[contains(@class, 'logo')]")
    header_shops = WebElement(xpath='//a[@title="Магазины"]')
    header_delivery = WebElement(xpath="(//header//a[contains(text(), 'Доставка и оплата')])")
    header_cart = WebElement(xpath="//header//a[contains(@href, 'cart') or contains(@class, 'cart')]")
    footer_instagram = WebElement(xpath="//footer//a[contains(@href, 'instagram.com')]")
    footer_oferta = WebElement(xpath="//footer//a[contains(@href, 'oferta')]")
    footer_about = WebElement(xpath="//footer//a[contains(@href, 'about') or contains(text(), 'О компании')]")

