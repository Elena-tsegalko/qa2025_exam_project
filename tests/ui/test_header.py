import allure

from conftest import driver
from selenium.webdriver.common.by import By


def test_links2(driver):
    driver.get("https://misshacosmetics.by/")
    elements = [
        (driver.find_element(By.XPATH, "(//a[contains(text(), 'Магазины')])[1]"), "кнопка Хедара 'Магазины'"),
        (driver.find_element(By.XPATH, "(//a[contains(text(), 'Доставка и оплата')])[1]"), "кнопка Хедара 'Доставка и оплата'")
    ]
    for element, text_element in elements:
        with allure.step(f'Проверка кликабельности{text_element}'):
            assert element.is_enabled(), f'{text_element} не кликабельна'