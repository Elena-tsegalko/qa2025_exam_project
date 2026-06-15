import allure
import pytest
from locators.main_locators import MainPage
from conftest import driver
# ХЕДЕР

def test_header_elements(driver):
    page = MainPage(driver)

    header_elements = [
        (page.header_logo, "Логотип хедера", "/"),
        (page.header_delivery, "Кнопка 'Доставка и оплата'", "/buyers/delivery-payment/"),
        (page.header_shops, "Кнопка 'Магазины'", "/about/contacts/"),
        (page.header_favorites, "Избранное", "/favorite/"),
        (page.header_cart, "Корзина", "/order/")
    ]

    for element, name, expected_url in header_elements:
        with allure.step(f"Проверка элемента хедера: {name}"):
            assert element.is_clickable(), f"Элемент '{name}' не кликабелен"

            element_link = element.get_attribute("href")
            assert element_link is not None, f"У элемента '{name}' отсутствует атрибут href"
            assert expected_url in element_link, f"Неверная ссылка у '{name}'. Ожидалось содержание '{expected_url}', получено:'{element_link}'"

    with allure.step("Проверка поисковой строки"):
        assert page.header_search.is_visible(), "Поисковая строка не отображается"

    with allure.step("Проверка кнопки пользователя"):
        assert page.header_user.is_clickable(), "Кнопка 'Войти' не кликабельна"


# ФУТЕР

def test_footer_elements(driver):
    page = MainPage(driver)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    import time
    time.sleep(1)

    footer_links = [
        (page.footer_logo, "Логотип футера", "/"),
        (page.footer_about_company, "Ссылка 'О компании'", "/about/company/"),
        (page.footer_oferta, "Оферта", "/about/terms/"),
        (page.footer_contacts, "Магазины", "/about/contacts/"),
        (page.footer_delivery, "Доставка и оплата", "/buyers/delivery-payment/")
    ]

    for element, name, expected_url in footer_links:
        with allure.step(f"Проверка элемента футера: {name}"):
            element_link = element.get_attribute("href")
            assert element_link is not None, f"У элемента '{name}' отсутствует href"
            assert expected_url in element_link, f"Неверная ссылка у '{name}'. Ожидалось '{expected_url}', получено '{element_link}'"


    with allure.step("Проверка телефона"):
        assert page.footer_phone.is_clickable(), "Ссылка на телефон не кликабельна"
        phone_href = page.footer_phone.get_attribute("href")
        assert "tel:" in phone_href, f"Некорректный формат телефона: {phone_href}"