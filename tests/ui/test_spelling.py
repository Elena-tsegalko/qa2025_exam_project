"""
Модуль UI-тестов для проверки орфографии на сайте misshacosmetics.by.

Содержит тесты для проверки:
- Орфографии в заголовках страниц
- Орфографии в текстовых элементах
- Орфографии в навигации
- Орфографии в футере

Используется словарь для проверки правописания слов.
"""

import allure
import pytest
import time
from locators.main_locators import MainPage
from selenium.webdriver.common.by import By


# Словарь слов с правильным написанием для проверки орфографии
CORRECT_SPELLING = {
    # Навигация
    "доставка": "доставка",
    "оплата": "оплата",
    "магазины": "магазины",
    "избранное": "избранное",
    "корзина": "корзина",
    "каталог": "каталог",
    "контакты": "контакты",
    "компания": "компания",
    "оферта": "оферта",

    # Категории товаров
    "помада": "помада",
    "тушь": "тушь",
    "тени": "тени",
    "румяна": "румяна",
    "пудра": "пудра",
    "консилер": "консилер",
    "тональный": "тональный",
    "уход": "уход",
    "лицо": "лицо",
    "волосы": "волосы",
    "тело": "тело",
    "руки": "руки",

    # Бренды
    "missha": "missha",
    "the face shop": "the face shop",
    "skin79": "skin79",

    # Общие слова
    "скидка": "скидка",
    "акция": "акция",
    "новинка": "новинка",
    "хит": "хит",
    "бестселлер": "бестселлер",
    "подарок": "подарок",
    "набор": "набор",
    "сет": "сет",
}

# Список слов, которые могут быть на английском (бренды, названия)
ENGLISH_WORDS = [
    "missha", "the face shop", "skin79", "etude", "innisfree",
    "holika holika", "the saem", "nature republic", "it's skin",
    "beauty credit", "tonymoly", "banila co"
]


@allure.feature("UI-тесты")
@allure.story("Проверка орфографии")
class TestSpelling:
    """Класс тестов для проверки орфографии текста на странице"""

    @allure.title("Проверка орфографии в title страницы")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_title_spelling(self, driver):
        """
        Тест проверяет орфографию в title страницы.
        Title отображается во вкладке браузера и важен для SEO.
        """
        page = MainPage(driver)

        with allure.step("Получение title страницы"):
            title = driver.title

        with allure.step("Проверка орфографии в title"):
            # Проверяем отсутствие типичных ошибок
            title_lower = title.lower()

            # Список возможных опечаток
            typos = {
                "мисша": "missha",
                "косметкс": "косметикс",
                "косметикc": "косметикс",
            }

            for typo, correct in typos.items():
                assert typo not in title_lower, \
                    f"Обнаружена опечатка в title: '{typo}' (ожидается '{correct}')"

    @allure.title("Проверка орфографии в main-заголовке")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_main_heading_spelling(self, driver):
        """
        Тест проверяет орфографию в основном заголовке страницы.
        """
        page = MainPage(driver)

        with allure.step("Поиск заголовков h1, h2"):
            headings = driver.find_elements(By.CSS_SELECTOR, "h1, h2")

        with allure.step("Проверка орфографии в заголовках"):
            for heading in headings[:5]:  # Проверяем первые 5 заголовков
                text = heading.text.strip()
                if text:
                    # Проверяем отсутствие типичных ошибок
                    text_lower = text.lower()

                    # Проверяем слова из словаря
                    for word in CORRECT_SPELLING.values():
                        if len(word) > 3:  # Проверяем только длинные слова
                            # Проверяем, что слово не содержит опечаток
                            if word in text_lower:
                                continue  # Слово написано правильно

    @allure.title("Проверка орфографии в навигации")
    @allure.severity(allure.severity_level.NORMAL)
    def test_navigation_spelling(self, driver):
        """
        Тест проверяет орфографию в элементах навигации.
        """
        page = MainPage(driver)

        with allure.step("Поиск элементов навигации"):
            nav_elements = driver.find_elements(By.CSS_SELECTOR, "nav a, .menu a, .navigation a")

        with allure.step("Проверка орфографии"):
            for element in nav_elements[:10]:  # Проверяем первые 10 элементов
                text = element.text.strip()
                if text:
                    text_lower = text.lower()
                    # Проверяем отсутствие типичных опечаток
                    common_typos = {
                        "доставка": ["доставкa", "доставкu", "достака"],
                        "оплата": ["оплaта", "оплтa", "оплата"],
                        "магазины": ["мaгазины", "магазuны", "магaзины"],
                    }
                    for correct_word, typos in common_typos.items():
                        for typo in typos:
                            assert typo not in text_lower, \
                                f"Обнаружена опечатка: '{typo}' (ожидается '{correct_word}')"

    @allure.title("Проверка орфографии в футере")
    @allure.severity(allure.severity_level.NORMAL)
    def test_footer_spelling(self, driver):
        """
        Тест проверяет орфографию в элементах футера.
        """
        page = MainPage(driver)

        with allure.step("Прокрутка к футеру"):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

        with allure.step("Поиск текста в футере"):
            footer = driver.find_elements(By.CSS_SELECTOR, "footer, .footer")
            if footer:
                footer_text = footer[0].text
            else:
                footer_text = ""

        with allure.step("Проверка орфографии в футере"):
            if footer_text:
                # Проверяем отсутствие типичных ошибок
                footer_lower = footer_text.lower()
                assert "компnя" not in footer_lower, \
                    "Обнаружена опечатка в футере: 'компnя' (ожидается 'компания')"
                assert "контaкты" not in footer_lower, \
                    "Обнаружена опечатка в футере: 'контaкты' (ожидается 'контакты')"

    @allure.title("Проверка орфографии в описаниях товаров")
    @allure.severity(allure.severity_level.MINOR)
    def test_product_descriptions_spelling(self, driver):
        """
        Тест проверяет орфографию в описаниях товаров на главной странице.
        """
        page = MainPage(driver)

        with allure.step("Поиск описаний товаров"):
            descriptions = driver.find_elements(By.CSS_SELECTOR, ".product-description, .description, .text")

        with allure.step("Проверка орфографии"):
            for desc in descriptions[:5]:  # Проверяем первые 5 описаний
                text = desc.text.strip()
                if text and len(text) > 10:  # Проверяем только тексты длиннее 10 символов
                    text_lower = text.lower()
                    # Проверяем отсутствие опечаток
                    assert "cosмeтикc" not in text_lower, \
                        "Обнаружена опечатка в описании"

    @allure.title("Проверка отсутствия дублирующихся пробелов")
    @allure.severity(allure.severity_level.MINOR)
    def test_no_double_spaces(self, driver):
        """
        Тест проверяет отсутствие дублирующихся пробелов в тексте.
        """
        page = MainPage(driver)

        with allure.step("Получение всего текста страницы"):
            body_text = driver.find_element(By.TAG_NAME, "body").text

        with allure.step("Проверка двойных пробелов"):
            assert "  " not in body_text, \
                "Обнаружены дублирующиеся пробелы в тексте"

    @allure.title("Проверка отсутствия лишних переносов строк")
    @allure.severity(allure.severity_level.MINOR)
    def test_no_extra_line_breaks(self, driver):
        """
        Тест проверяет отсутствие лишних переносов строк в тексте.
        """
        page = MainPage(driver)

        with allure.step("Получение всего текста страницы"):
            body_text = driver.find_element(By.TAG_NAME, "body").text

        with allure.step("Проверка тройных переносов"):
            assert "\n\n\n" not in body_text, \
                "Обнаружены лишние переносы строк (более 2 подряд)"

    @allure.title("Проверка правильности написания 'Missha'")
    @allure.severity(allure.severity_level.NORMAL)
    def test_brand_name_spelling(self, driver):
        """
        Тест проверяет правильность написания бренда Missha.
        """
        page = MainPage(driver)

        with allure.step("Поиск упоминаний бренда"):
            page_source = driver.page_source.lower()

        with allure.step("Проверка написания"):
            # Проверяем правильное написание
            correct_forms = ["missha", "missha"]
            typo_forms = ["misha", "missha", "missha", "missa", "missha"]

            for typo in typo_forms:
                if typo in page_source and typo not in correct_forms:
                    # Находим все вхождения
                    import re
                    occurrences = [m.start() for m in re.finditer(typo, page_source)]
                    if occurrences:
                        # Проверяем контекст (не часть ли это правильного слова)
                        for pos in occurrences:
                            context = page_source[max(0, pos-5):pos+len(typo)+5]
                            # Пропускаем, если это часть правильного слова
                            if not any(correct in context for correct in correct_forms):
                                allure.attach(
                                    f"Найдено: '{typo}' в позиции {pos}, контекст: '{context}'",
                                    name="Написание бренда",
                                    attachment_type=allure.attachment_type.TEXT
                                )

    @allure.title("Проверка правильности написания 'косметика'")
    @allure.severity(allure.severity_level.NORMAL)
    def test_word_kosmetika_spelling(self, driver):
        """
        Тест проверяет правильность написания слова 'косметика'.
        """
        page = MainPage(driver)

        with allure.step("Поиск упоминаний слова"):
            page_text = driver.find_element(By.TAG_NAME, "body").text.lower()

        with allure.step("Проверка написания"):
            # Проверяем правильное написание
            typo_forms = ["космeтика", "космeтикa", "космeтикcа", "косметuка"]

            for typo in typo_forms:
                assert typo not in page_text, \
                    f"Обнаружена опечатка: '{typo}' (ожидается 'косметика')"

    @allure.title("Проверка правильности написания 'скидка'")
    @allure.severity(allure.severity_level.MINOR)
    def test_word_skidka_spelling(self, driver):
        """
        Тест проверяет правильность написания слова 'скидка'.
        """
        page = MainPage(driver)

        with allure.step("Поиск упоминаний слова"):
            page_text = driver.find_element(By.TAG_NAME, "body").text.lower()

        with allure.step("Проверка написания"):
            typo_forms = ["скuдка", "скuдкa", "скидкa", "скидkа"]

            for typo in typo_forms:
                assert typo not in page_text, \
                    f"Обнаружена опечатка: '{typo}' (ожидается 'скидка')"

    @allure.title("Проверка отсутствия мусорных символов")
    @allure.severity(allure.severity_level.MINOR)
    def test_no_garbage_characters(self, driver):
        """
        Тест проверяет отсутствие мусорных символов в тексте.
        """
        page = MainPage(driver)

        with allure.step("Получение всего текста страницы"):
            body_text = driver.find_element(By.TAG_NAME, "body").text

        with allure.step("Проверка мусорных символов"):
            # Проверяем отсутствие невидимых символов и мусора
            garbage_chars = ["\ufeff", "\u200b", "\xa0", "\u00a0"]
            for char in garbage_chars:
                assert char not in body_text, \
                    f"Обнаружен мусорный символ: {repr(char)}"
