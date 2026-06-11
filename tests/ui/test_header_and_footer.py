import allure
import pytest
from locators.main_locators import MainPage

# ХЕДЕР

def test_header_elements(driver):
    page = MainPage(driver)

    header_elements = [
        (page.header_logo, "Логотип хедера", "misshacosmetics.by"),
        (page.header_shops, "Кнопка 'Магазины'", "shops" or "contacts"),
        (page.header_delivery, "Кнопка 'Доставка и оплата'", "delivery"),
        (page.header_cart, "Корзина", "cart")
    ]

    for element, name, expected_url in header_elements:
        with allure.step(f"Проверка элемента хедера: {name}"):

            #assert element.is_displayed(), f"Элемент '{name}' не отображается в хедере"


            assert element.is_clickable(), f"Элемент '{name}' не кликабелен"


            element_link = element.get_attribute("href")
            assert element_link is not None, f"У элемента '{name}' отсутствует атрибут href"
            assert expected_url in element_link, f"Неверная ссылка у '{name}'. Ожидалось содержание '{expected_url}', получено:'{element_link}'"


# ФУТЕР

def test_footer_elements(driver):
    page = MainPage(driver)

    footer_elements = [
        (page.footer_instagram, "Ссылка Instagram", "instagram.com"),
        (page.footer_oferta, "Ссылка на оферту/правила", "oferta"),
        (page.footer_about, "Ссылка 'О компании'", "about")
    ]

    for element, name, expected_url in footer_elements:
        with allure.step(f"Проверка элемента футера: {name}"):

            #assert element.is_displayed(), f"Элемент '{name}' не отображается в футере"


            assert element.is_clickable(), f"Элемент '{name}' не кликабелен"


            element_link = element.get_attribute("href")
            assert element_link is not None, f"У элемента '{name}' в футере нет ссылки"
            assert expected_url in element_link, f"Элемент '{name}' ведет на некорректный URL: {element_link}"