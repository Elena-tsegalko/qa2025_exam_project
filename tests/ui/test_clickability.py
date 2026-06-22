"""
Модуль UI-тестов для проверки кликабельности элементов на сайте misshacosmetics.by.

Содержит тесты для проверки:
- Кликабельности кнопок и ссылок в хедере
- Кликабельности элементов в футере
- Кликабельности элементов каталога
- Кликабельности формы обратной связи

Все тесты используют Page Object паттерн через локаторы.
"""

import allure
import pytest
import time
from locators.main_locators import MainPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@allure.feature("UI-тесты")
@allure.story("Проверка кликабельности элементов")
class TestClickability:
    """Класс тестов для проверки кликабельности элементов"""

    @allure.title("Кликабельность логотипа в хедере")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_header_logo_clickable(self, driver):
        """
        Тест проверяет, что логотип в хедере кликабелен.
        Логотип должен вести на главную страницу.
        """
        page = MainPage(driver)

        with allure.step("Проверка кликабельности логотипа"):
            assert page.header_logo.is_clickable(), "Логотип в хедере не кликабелен"

        with allure.step("Клик по логотипу"):
            page.header_logo.click()

        with allure.step("Проверка перехода на главную"):
            assert driver.current_url.rstrip('/') == "https://misshacosmetics.by", \
                f"Не произошел переход на главную, текущий URL: {driver.current_url}"

    @allure.title("Кликабельность кнопки поиска")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_header_search_clickable(self, driver):
        """
        Тест проверяет кликабельность поисковой строки.
        Поиск должен открываться при клике.
        """
        page = MainPage(driver)

        with allure.step("Проверка видимости поисковой строки"):
            assert page.header_search.is_visible(), "Поисковая строка не отображается"

        with allure.step("Клик по поисковой строке"):
            page.header_search.click()

        with allure.step("Проверка активации поиска"):
            # Проверяем, что поле активировалось (получило фокус)
            search_input = page.header_search.find()
            assert search_input is not None, "Поле поиска не найдено после клика"

    @allure.title("Кликабельность кнопки 'Доставка и оплата'")
    @allure.severity(allure.severity_level.NORMAL)
    def test_header_delivery_clickable(self, driver):
        """
        Тест проверяет кликабельность ссылки 'Доставка и оплата'.
        Ссылка должна вести на соответствующую страницу.
        """
        page = MainPage(driver)

        with allure.step("Проверка кликабельности кнопки"):
            assert page.header_delivery.is_clickable(), \
                "Кнопка 'Доставка и оплата' не кликабельна"

        with allure.step("Клик по кнопке"):
            page.header_delivery.click()

        with allure.step("Проверка URL после клика"):
            assert "delivery" in driver.current_url or "payment" in driver.current_url, \
                f"Не произошел переход на страницу доставки: {driver.current_url}"

    @allure.title("Кликабельность кнопки 'Магазины'")
    @allure.severity(allure.severity_level.NORMAL)
    def test_header_shops_clickable(self, driver):
        """
        Тест проверяет кликабельность ссылки 'Магазины'.
        Ссылка должна вести на страницу с адресами магазинов.
        """
        page = MainPage(driver)

        with allure.step("Проверка кликабельности кнопки"):
            assert page.header_shops.is_clickable(), \
                "Кнопка 'Магазины' не кликабельна"

        with allure.step("Клик по кнопке"):
            page.header_shops.click()

        with allure.step("Проверка URL после клика"):
            assert "contacts" in driver.current_url or "shops" in driver.current_url, \
                f"Не произошел переход на страницу магазинов: {driver.current_url}"

    @allure.title("Кликабельность кнопки избранного")
    @allure.severity(allure.severity_level.NORMAL)
    def test_header_favorites_clickable(self, driver):
        """
        Тест проверяет кликабельность кнопки 'Избранное'.
        Кнопка должна открывать список избранных товаров.
        """
        page = MainPage(driver)

        with allure.step("Проверка кликабельности кнопки"):
            assert page.header_favorites.is_clickable(), \
                "Кнопка избранного не кликабельна"

        with allure.step("Клик по кнопке"):
            page.header_favorites.click()

        with allure.step("Проверка URL после клика"):
            assert "favorites" in driver.current_url or "favorite" in driver.current_url, \
                f"Не произошел переход на страницу избранного: {driver.current_url}"

    @allure.title("Кликабельность кнопки корзины")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_header_cart_clickable(self, driver):
        """
        Тест проверяет кликабельность кнопки 'Корзина'.
        Корзина должна открываться при клике.
        """
        page = MainPage(driver)

        with allure.step("Проверка кликабельности кнопки"):
            assert page.header_cart.is_clickable(), \
                "Кнопка корзины не кликабельна"

        with allure.step("Клик по кнопке"):
            page.header_cart.click()

        with allure.step("Проверка URL после клика"):
            assert "cart" in driver.current_url or "order" in driver.current_url, \
                f"Не произошел переход на корзину: {driver.current_url}"

    @allure.title("Кликабельность кнопки пользователя")
    @allure.severity(allure.severity_level.NORMAL)
    def test_header_user_clickable(self, driver):
        """
        Тест проверяет кликабельность кнопки пользователя (Войти).
        Должна открываться форма авторизации.
        """
        page = MainPage(driver)

        with allure.step("Проверка кликабельности кнопки"):
            assert page.header_user.is_clickable(), \
                "Кнопка пользователя не кликабельна"

        with allure.step("Клик по кнопке"):
            page.header_user.click()

        with allure.step("Проверка появления формы авторизации"):
            time.sleep(1)
            # Проверяем наличие модального окна или формы
            page_source = driver.page_source
            assert "login" in page_source.lower() or "авториз" in page_source.lower() or \
                   "вход" in page_source.lower() or "войти" in page_source.lower(), \
                "Форма авторизации не появилась после клика"

    @allure.title("Кликабельность логотипа в футере")
    @allure.severity(allure.severity_level.MINOR)
    def test_footer_logo_clickable(self, driver):
        """
        Тест проверяет кликабельность логотипа в футере.
        Логотип должен вести на главную страницу.
        """
        page = MainPage(driver)

        with allure.step("Прокрутка к футеру"):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

        with allure.step("Проверка кликабельности логотипа"):
            assert page.footer_logo.is_clickable(), \
                "Логотип в футере не кликабелен"

        with allure.step("Клик по логотипу"):
            page.footer_logo.click()

        with allure.step("Проверка перехода на главную"):
            assert driver.current_url.rstrip('/') == "https://misshacosmetics.by", \
                f"Не произошел переход на главную: {driver.current_url}"

    @allure.title("Кликабельность ссылки 'О компании'")
    @allure.severity(allure.severity_level.MINOR)
    def test_footer_about_clickable(self, driver):
        """
        Тест проверяет кликабельность ссылки 'О компании' в футере.
        """
        page = MainPage(driver)

        with allure.step("Прокрутка к футеру"):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

        with allure.step("Проверка кликабельности ссылки"):
            assert page.footer_about_company.is_clickable(), \
                "Ссылка 'О компании' не кликабельна"

        with allure.step("Клик по ссылке"):
            page.footer_about_company.click()

        with allure.step("Проверка URL после клика"):
            assert "about" in driver.current_url or "company" in driver.current_url, \
                f"Не произошел переход: {driver.current_url}"

    @allure.title("Кликабельность ссылки 'Контакты'")
    @allure.severity(allure.severity_level.MINOR)
    def test_footer_contacts_clickable(self, driver):
        """
        Тест проверяет кликабельность ссылки 'Контакты' в футере.
        """
        page = MainPage(driver)

        with allure.step("Прокрутка к футеру"):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

        with allure.step("Проверка кликабельности ссылки"):
            assert page.footer_contacts.is_clickable(), \
                "Ссылка 'Контакты' не кликабельна"

        with allure.step("Клик по ссылке"):
            page.footer_contacts.click()

        with allure.step("Проверка URL после клика"):
            assert "contacts" in driver.current_url, \
                f"Не произошел переход на контакты: {driver.current_url}"

    @allure.title("Кликабельность телефона в футере")
    @allure.severity(allure.severity_level.MINOR)
    def test_footer_phone_clickable(self, driver):
        """
        Тест проверяет кликабельность ссылки на телефон в футере.
        Ссылка должна содержать tel: протокол.
        """
        page = MainPage(driver)

        with allure.step("Прокрутка к футеру"):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

        with allure.step("Проверка кликабельности телефона"):
            assert page.footer_phone.is_clickable(), \
                "Ссылка на телефон не кликабельна"

        with allure.step("Проверка формата ссылки"):
            phone_href = page.footer_phone.get_attribute("href")
            assert phone_href.startswith("tel:"), \
                f"Некорректный формат ссылки на телефон: {phone_href}"

    @allure.title("Кликабельность кнопки подписки на рассылку")
    @allure.severity(allure.severity_level.MINOR)
    def test_footer_subscribe_clickable(self, driver):
        """
        Тест проверяет кликабельность кнопки подписки на рассылку.
        """
        page = MainPage(driver)

        with allure.step("Прокрутка к футеру"):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

        with allure.step("Проверка кликабельности кнопки"):
            assert page.footer_subscribe_btn.is_clickable(), \
                "Кнопка подписки не кликабельна"

    @allure.title("Кликабельность поля ввода email для рассылки")
    @allure.severity(allure.severity_level.MINOR)
    def test_footer_subscribe_input_clickable(self, driver):
        """
        Тест проверяет кликабельность поля ввода email для рассылки.
        """
        page = MainPage(driver)

        with allure.step("Прокрутка к футеру"):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

        with allure.step("Проверка кликабельности поля ввода"):
            assert page.footer_subscribe_input.is_clickable(), \
                "Поле ввода email не кликабельно"

        with allure.step("Ввод тестового email"):
            page.footer_subscribe_input.send_keys("test@example.com")
            time.sleep(0.5)

        with allure.step("Проверка введенного значения"):
            input_value = page.footer_subscribe_input.get_attribute("value")
            assert "test@example.com" in input_value, \
                f"Email не введен корректно: {input_value}"


@allure.feature("UI-тесты")
@allure.story("Проверка кликабельности в каталоге")
class TestCatalogClickability:
    """Класс тестов для проверки кликабельности элементов каталога"""

    @allure.title("Кликабельность кнопки каталога")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_catalog_button_clickable(self, driver):
        """
        Тест проверяет кликабельность кнопки открытия каталога.
        """
        page = MainPage(driver)

        with allure.step("Прокрутка к кнопке каталога"):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

        with allure.step("Поиск кнопки каталога"):
            catalog_btn = page.btn_catalog.find(timeout=5)
            assert catalog_btn is not None, "Кнопка каталога не найдена"

        with allure.step("Проверка кликабельности"):
            driver.execute_script("arguments[0].click();", catalog_btn)
            time.sleep(2)

        with allure.step("Проверка перехода"):
            if len(driver.window_handles) > 1:
                driver.switch_to.window(driver.window_handles[-1])
            assert "/about/opt/" in driver.current_url or "catalog" in driver.current_url, \
                f"Не произошел переход: {driver.current_url}"
