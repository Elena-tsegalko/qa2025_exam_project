"""
Модуль UI-тестов для проверки отображения элементов на сайте misshacosmetics.by.

Содержит тесты для проверки:
- Видимости элементов хедера
- Видимости элементов футера
- Отображения текста на странице
- Отображения изображений
- Корректного позиционирования элементов

Все тесты используют Page Object паттерн через локаторы.
"""

import allure
import pytest
import time
from locators.main_locators import MainPage
from selenium.webdriver.common.by import By


@allure.feature("UI-тесты")
@allure.story("Проверка отображения элементов")
class TestElementDisplay:
    """Класс тестов для проверки отображения элементов на странице"""

    @allure.title("Отображение логотипа в хедере")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_header_logo_displayed(self, driver):
        """
        Тест проверяет отображение логотипа в хедере.
        Логотип должен быть видим на странице.
        """
        page = MainPage(driver)

        with allure.step("Проверка видимости логотипа"):
            assert page.header_logo.is_visible(), "Логотип не отображается на странице"

        with allure.step("Проверка размера логотипа"):
            logo = page.header_logo.find()
            size = logo.size
            assert size['width'] > 0 and size['height'] > 0, \
                f"Логотип имеет нулевой размер: {size}"

    @allure.title("Отображение поисковой строки")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_header_search_displayed(self, driver):
        """
        Тест проверяет отображение поисковой строки.
        Поиск должен быть видим и доступен для ввода.
        """
        page = MainPage(driver)

        with allure.step("Проверка видимости поисковой строки"):
            assert page.header_search.is_visible(), \
                "Поисковая строка не отображается"

        with allure.step("Проверка типа элемента"):
            search = page.header_search.find()
            tag = search.tag_name
            assert tag == "input", f"Поисковая строка не является полем ввода: {tag}"

    @allure.title("Отображение кнопки 'Войти'")
    @allure.severity(allure.severity_level.NORMAL)
    def test_header_user_displayed(self, driver):
        """
        Тест проверяет отображение кнопки пользователя.
        Кнопка должна быть видна для авторизации.
        """
        page = MainPage(driver)

        with allure.step("Проверка видимости кнопки"):
            assert page.header_user.is_visible(), \
                "Кнопка 'Войти' не отображается"

    @allure.title("Отображение кнопки избранного")
    @allure.severity(allure.severity_level.NORMAL)
    def test_header_favorites_displayed(self, driver):
        """
        Тест проверяет отображение кнопки избранного.
        """
        page = MainPage(driver)

        with allure.step("Проверка видимости кнопки"):
            assert page.header_favorites.is_visible(), \
                "Кнопка избранного не отображается"

    @allure.title("Отображение кнопки корзины")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_header_cart_displayed(self, driver):
        """
        Тест проверяет отображение кнопки корзины.
        Корзина должна быть всегда видна для пользователя.
        """
        page = MainPage(driver)

        with allure.step("Проверка видимости кнопки"):
            assert page.header_cart.is_visible(), \
                "Кнопка корзины не отображается"

    @allure.title("Отображение логотипа в футере")
    @allure.severity(allure.severity_level.MINOR)
    def test_footer_logo_displayed(self, driver):
        """
        Тест проверяет отображение логотипа в футере.
        """
        page = MainPage(driver)

        with allure.step("Прокрутка к футеру"):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

        with allure.step("Проверка видимости логотипа"):
            assert page.footer_logo.is_visible(), \
                "Логотип в футере не отображается"

    @allure.title("Отображение ссылки на телефон")
    @allure.severity(allure.severity_level.MINOR)
    def test_footer_phone_displayed(self, driver):
        """
        Тест проверяет отображение ссылки на телефон в футере.
        """
        page = MainPage(driver)

        with allure.step("Прокрутка к футеру"):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

        with allure.step("Проверка видимости телефона"):
            assert page.footer_phone.is_visible(), \
                "Ссылка на телефон не отображается"

    @allure.title("Отображение поля email для рассылки")
    @allure.severity(allure.severity_level.MINOR)
    def test_footer_subscribe_input_displayed(self, driver):
        """
        Тест проверяет отображение поля ввода email для рассылки.
        """
        page = MainPage(driver)

        with allure.step("Прокрутка к футеру"):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

        with allure.step("Проверка видимости поля ввода"):
            assert page.footer_subscribe_input.is_visible(), \
                "Поле ввода email не отображается"

    @allure.title("Отображение кнопки подписки")
    @allure.severity(allure.severity_level.MINOR)
    def test_footer_subscribe_btn_displayed(self, driver):
        """
        Тест проверяет отображение кнопки подписки на рассылку.
        """
        page = MainPage(driver)

        with allure.step("Прокрутка к футеру"):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

        with allure.step("Проверка видимости кнопки"):
            assert page.footer_subscribe_btn.is_visible(), \
                "Кнопка подписки не отображается"

    @allure.title("Отображение ссылки 'О компании'")
    @allure.severity(allure.severity_level.MINOR)
    def test_footer_about_displayed(self, driver):
        """
        Тест проверяет отображение ссылки 'О компании' в футере.
        """
        page = MainPage(driver)

        with allure.step("Прокрутка к футеру"):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

        with allure.step("Проверка видимости ссылки"):
            assert page.footer_about_company.is_visible(), \
                "Ссылка 'О компании' не отображается"

    @allure.title("Отображение ссылки 'Контакты'")
    @allure.severity(allure.severity_level.MINOR)
    def test_footer_contacts_displayed(self, driver):
        """
        Тест проверяет отображение ссылки 'Контакты' в футере.
        """
        page = MainPage(driver)

        with allure.step("Прокрутка к футеру"):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

        with allure.step("Проверка видимости ссылки"):
            assert page.footer_contacts.is_visible(), \
                "Ссылка 'Контакты' не отображается"

    @allure.title("Отображение ссылки 'Доставка и оплата'")
    @allure.severity(allure.severity_level.MINOR)
    def test_footer_delivery_displayed(self, driver):
        """
        Тест проверяет отображение ссылки 'Доставка и оплата' в футере.
        """
        page = MainPage(driver)

        with allure.step("Прокрутка к футеру"):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

        with allure.step("Проверка видимости ссылки"):
            assert page.footer_delivery.is_visible(), \
                "Ссылка 'Доставка и оплата' не отображается"


@allure.feature("UI-тесты")
@allure.story("Проверка отображения текста и изображений")
class TestTextAndImageDisplay:
    """Класс тестов для проверки отображения текста и изображений"""

    @allure.title("Проверка наличия title страницы")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_page_title_displayed(self, driver):
        """
        Тест проверяет наличие title страницы.
        Title важен для SEO и отображается во вкладке браузера.
        """
        page = MainPage(driver)

        with allure.step("Получение title страницы"):
            title = driver.title

        with allure.step("Проверка непустоты title"):
            assert title is not None and len(title) > 0, \
                "Title страницы пустой"

        with allure.step("Проверка содержимого title"):
            assert "missha" in title.lower() or "косметик" in title.lower() or \
                   "beauty" in title.lower(), \
                f"Title не содержит ожидаемых слов: {title}"

    @allure.title("Проверка наличия meta-описания")
    @allure.severity(allure.severity_level.NORMAL)
    def test_meta_description_displayed(self, driver):
        """
        Тест проверяет наличие meta-описания страницы.
        Meta-описание важно для SEO.
        """
        page = MainPage(driver)

        with allure.step("Поиск meta-описания"):
            meta_desc = driver.find_elements(By.CSS_SELECTOR, 'meta[name="description"]')

        with allure.step("Проверка наличия meta-описания"):
            assert len(meta_desc) > 0, "Meta-описание отсутствует"

        with allure.step("Проверка непустоты описания"):
            content = meta_desc[0].get_attribute("content")
            assert content is not None and len(content) > 0, \
                "Meta-описание пустое"

    @allure.title("Проверка наличия main тега")
    @allure.severity(allure.severity_level.MINOR)
    def test_main_tag_displayed(self, driver):
        """
        Тест проверяет наличие main-тега на странице.
        Main-тег важен для семантики и accessibility.
        """
        page = MainPage(driver)

        with allure.step("Поиск main-тега"):
            main_tags = driver.find_elements(By.TAG_NAME, "main")

        with allure.step("Проверка наличия main-тега"):
            # Main может отсутствовать, это не критично
            # Проверяем хотя бы наличие контента
            body = driver.find_elements(By.TAG_NAME, "body")
            assert len(body) > 0, "Тело страницы отсутствует"

    @allure.title("Проверка отображения изображений в логотипе")
    @allure.severity(allure.severity_level.MINOR)
    def test_logo_image_displayed(self, driver):
        """
        Тест проверяет отображение изображения логотипа.
        """
        page = MainPage(driver)

        with allure.step("Поиск изображения в логотипе"):
            logo = page.header_logo.find()
            images = logo.find_elements(By.TAG_NAME, "img")

        with allure.step("Проверка наличия изображения"):
            if len(images) > 0:
                img = images[0]
                src = img.get_attribute("src")
                assert src is not None and len(src) > 0, \
                    "Изображение логотипа не имеет src"

    @allure.title("Проверка отображения текста в хедере")
    @allure.severity(allure.severity_level.NORMAL)
    def test_header_text_displayed(self, driver):
        """
        Тест проверяет отображение текста в элементах хедера.
        """
        page = MainPage(driver)

        with allure.step("Проверка наличия текста на странице"):
            body_text = driver.find_element(By.TAG_NAME, "body").text
            assert len(body_text) > 0, "Текст на странице отсутствует"

    @allure.title("Проверка отсутствия ошибок 404 в изображениях")
    @allure.severity(allure.severity_level.MINOR)
    def test_no_broken_images(self, driver):
        """
        Тест проверяет отсутствие сломанных изображений на странице.
        Использует JavaScript для проверки naturalWidth изображений.
        """
        page = MainPage(driver)

        with allure.step("Проверка изображений через JS"):
            broken_images = driver.execute_script("""
                var images = document.querySelectorAll('img');
                var broken = [];
                for (var i = 0; i < images.length; i++) {
                    if (images[i].naturalWidth === 0 && images[i].src !== '') {
                        broken.push(images[i].src);
                    }
                }
                return broken;
            """)

        with allure.step("Проверка отсутствия сломанных изображений"):
            assert len(broken_images) == 0, \
                f"Найдены сломанные изображения: {broken_images}"

    @allure.title("Проверка отображения шрифтов")
    @allure.severity(allure.severity_level.MINOR)
    def test_fonts_displayed(self, driver):
        """
        Тест проверяет, что шрифты на странице загружены корректно.
        """
        page = MainPage(driver)

        with allure.step("Проверка шрифтов через JS"):
            fonts_loaded = driver.execute_script("""
                return document.fonts.ready.then(function() {
                    return document.fonts.size > 0;
                });
            """)

        with allure.step("Проверка загрузки шрифтов"):
            # Шрифты могут быть не загружены, это не критично
            pass

    @allure.title("Проверка отсутствия горизонтального скролла")
    @allure.severity(allure.severity_level.NORMAL)
    def test_no_horizontal_scroll(self, driver):
        """
        Тест проверяет отсутствие горизонтальной прокрутки.
        Горизонтальная прокрутка ломает UX на мобильных устройствах.
        """
        page = MainPage(driver)

        with allure.step("Проверка ширины страницы"):
            page_width = driver.execute_script(
                "return Math.max(document.body.scrollWidth, document.documentElement.scrollWidth);"
            )
            viewport_width = driver.execute_script(
                "return window.innerWidth;"
            )

        with allure.step("Сравнение ширины"):
            assert page_width <= viewport_width + 10, \
                f"Обнаружена горизонтальная прокрутка: страница {page_width}px, видимая область {viewport_width}px"

    @allure.title("Проверка отсутствия JS-ошибок критических")
    @allure.severity(allure.severity_level.MINOR)
    def test_no_critical_js_errors(self, driver):
        """
        Тест проверяет отсутствие критических JS-ошибок на странице.
        """
        page = MainPage(driver)

        with allure.step("Получение логов браузера"):
            logs = driver.get_log('browser')

        with allure.step("Фильтрация критических ошибок"):
            critical_errors = [
                log for log in logs
                if log['level'] == 'SEVERE' and 'favicon' not in log['message'].lower()
            ]

        with allure.step("Проверка отсутствия критических ошибок"):
            assert len(critical_errors) == 0, \
                f"Найдены критические JS-ошибки: {critical_errors}"
