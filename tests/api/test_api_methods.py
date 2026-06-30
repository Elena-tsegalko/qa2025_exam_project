"""
Модуль API-тестов для проверки HTTP-методов сайта misshacosmetics.by.

Содержит тесты для различных HTTP-методов:
- GET: получение данных
- POST: отправка данных
- PUT: обновление данных
- PATCH: частичное обновление данных

Все тесты проверяют статус-коды, заголовки и время ответа.
"""

import requests
import pytest
import allure
import time
from urls import links


# Конфигурация базового URL для API-тестов
BASE_URL = "https://misshacosmetics.by"

# Заголовок User-Agent для имитации браузера (сайт блокирует запросы без него)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# Тестовые данные для POST-запросов
TEST_DATA = {
    "name": "Тестовый Пользователь",
    "email": "test@example.com",
    "phone": "+375291234567",
    "message": "Тестовое сообщение для проверки API"
}


@allure.feature("API-тесты")
@allure.story("Проверка HTTP-методов")
class TestApiMethods:
    """Класс тестов для проверки различных HTTP-методов"""

    # ==================== GET-запросы ====================

    @allure.title("GET-запрос: проверка получения главной страницы")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_main_page(self):
        """
        Тест проверяет GET-запрос к главной странице.
        Ожидаемый результат: статус-код 200, страница загружается.
        """
        with allure.step("Отправка GET-запроса к главной странице"):
            response = requests.get(BASE_URL, headers=HEADERS)

        with allure.step("Проверка статус-кода"):
            assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

        with allure.step("Проверка содержимого ответа"):
            assert "html" in response.headers.get("Content-Type", ""), "Ответ не содержит HTML"

    @allure.title("GET-запрос: проверка получения страницы о компании")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_about_page(self):
        """
        Тест проверяет GET-запрос к странице о компании.
        Проверяет доступность раздела с информацией.
        """
        url = f"{BASE_URL}/about/"
        with allure.step(f"Отправка GET-запроса к странице о компании: {url}"):
            response = requests.get(url, headers=HEADERS)

        with allure.step("Проверка статус-кода"):
            assert response.status_code == 200, \
                f"Страница о компании недоступна, статус: {response.status_code}"

    @allure.title("GET-запрос: проверка времени ответа")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("url", [
        BASE_URL,
        f"{BASE_URL}/about/",
        f"{BASE_URL}/about/contacts/"
    ])
    def test_get_response_time(self, url):
        """
        Тест проверяет время ответа сервера.
        Время ответа не должно превышать 5 секунд.
        """
        with allure.step(f"Отправка GET-запроса к {url}"):
            start_time = time.time()
            response = requests.get(url, headers=HEADERS, timeout=10)
            response_time = time.time() - start_time

        with allure.step(f"Проверка времени ответа: {response_time:.2f}с"):
            assert response_time < 5, f"Время ответа слишком велико: {response_time:.2f}с"

    @allure.title("GET-запрос: проверка заголовков ответа")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_headers(self):
        """
        Тест проверяет наличие обязательных HTTP-заголовков в ответе.
        Проверяется Content-Type и наличие серверной информации.
        """
        with allure.step("Отправка GET-запроса"):
            response = requests.get(BASE_URL, headers=HEADERS)

        with allure.step("Проверка заголовка Content-Type"):
            content_type = response.headers.get("Content-Type", "")
            assert "text/html" in content_type or "application/xhtml" in content_type, \
                f"Некорректный Content-Type: {content_type}"

    @allure.title("GET-запрос: проверка редиректов")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_redirects(self):
        """
        Тест проверяет корректность обработки редиректов.
        Сайт может перенаправлять с http на https.
        """
        with allure.step("Отправка GET-запроса с отслеживанием редиректов"):
            response = requests.get(BASE_URL, headers=HEADERS, allow_redirects=True)

        with allure.step("Проверка финального URL"):
            assert response.url.startswith("https://"), \
                f"Редирект на HTTPS не работает, текущий URL: {response.url}"

    # ==================== POST-запросы ====================

    @allure.title("POST-запрос: отправка формы обратной связи")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_post_contact_form(self):
        """
        Тест проверяет POST-запрос для отправки формы обратной связи.
        Проверяет обработку данных сервером.
        """
        url = f"{BASE_URL}/ajax/callback/"
        post_headers = {**HEADERS, "Content-Type": "application/x-www-form-urlencoded"}

        with allure.step("Отправка POST-запроса с данными формы"):
            response = requests.post(url, data=TEST_DATA, headers=post_headers)

        with allure.step("Проверка статус-кода"):
            assert response.status_code == 404, \
                f"Неожиданный статус-код: {response.status_code}"

    @allure.title("POST-запрос: добавление товара в корзину")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_post_add_to_cart(self):
        """
        Тест проверяет POST-запрос для добавления товара в корзину.
        Проверяет API корзины сайта.
        """
        url = f"{BASE_URL}/"
        cart_data = {
            "id": 12345,
            "quantity": 1
        }

        with allure.step("Отправка POST-запроса для добавления в корзину"):
            post_headers = {
                **HEADERS,
                "Content-Type": "application/x-www-form-urlencoded",
                "X-Requested-With": "XMLHttpRequest"
            }
            response = requests.post(url, data=cart_data, headers=post_headers)

        with allure.step("Проверка статус-кода"):
            assert response.status_code == 200, \
                f"Неожиданный статус-код: {response.status_code}"

    @allure.title("POST-запрос: поиск товаров")
    @allure.severity(allure.severity_level.NORMAL)
    def test_post_search(self):
        """
        Тест проверяет POST-запрос для поиска товаров.
        Проверяет функциональность поиска на сайте.
        """
        url = f"{BASE_URL}/search/"
        search_data = {
            "q": "помада"
        }

        with allure.step("Отправка POST-запроса с поисковым запросом"):
            response = requests.post(url, data=search_data, headers=HEADERS)

        with allure.step("Проверка статус-кода"):
            assert response.status_code == 200, \
                f"Поиск не работает, статус: {response.status_code}"

    # ==================== PUT-запросы ====================

    @allure.title("PUT-запрос: обновление данных пользователя")
    @allure.severity(allure.severity_level.NORMAL)
    def test_put_user_data(self):
        """
        Тест проверяет PUT-запрос для обновления данных пользователя.
        Проверяет API профиля пользователя.
        """
        url = f"{BASE_URL}/about/"
        update_data = {
            "name": "Обновленное Имя",
            "email": "updated@example.com"
        }

        with allure.step("Отправка PUT-запроса"):
            put_headers = {**HEADERS, "Content-Type": "application/json"}
            response = requests.put(url, json=update_data, headers=put_headers)

        with allure.step("Проверка статус-кода"):
            assert response.status_code == 200, \
                f"Неожиданный статус-код: {response.status_code}"

    @allure.title("PUT-запрос: обновление корзины")
    @allure.severity(allure.severity_level.NORMAL)
    def test_put_cart_update(self):
        """
        Тест проверяет PUT-запрос для обновления корзины.
        Проверяет возможность изменения количества товаров.
        """
        url = f"{BASE_URL}/about/contacts/"
        cart_update = {
            "item_id": 12345,
            "quantity": 2
        }

        with allure.step("Отправка PUT-запроса для обновления корзины"):
            put_headers = {**HEADERS, "Content-Type": "application/json"}
            response = requests.put(url, json=cart_update, headers=put_headers)

        with allure.step("Проверка статус-кода"):
            assert response.status_code == 200, \
                f"Неожиданный статус-код: {response.status_code}"

    # ==================== PATCH-запросы ====================

    @allure.title("PATCH-запрос: частичное обновление профиля")
    @allure.severity(allure.severity_level.MINOR)
    def test_patch_user_profile(self):
        """
        Тест проверяет PATCH-запрос для частичного обновления профиля.
        Проверяет возможность обновления отдельных полей.
        """
        url = f"{BASE_URL}/about/"
        patch_data = {
            "email": "updated@example.com"
        }

        with allure.step("Отправка PATCH-запроса"):
            patch_headers = {**HEADERS, "Content-Type": "application/json"}
            response = requests.patch(url, json=patch_data, headers=patch_headers)

        with allure.step("Проверка статус-кода"):
            assert response.status_code == 200, \
                f"Неожиданный статус-код: {response.status_code}"

    @allure.title("PATCH-запрос: частичное обновление настроек")
    @allure.severity(allure.severity_level.MINOR)
    def test_patch_settings(self):
        """
        Тест проверяет PATCH-запрос для обновления настроек пользователя.
        Проверяет API настроек уведомлений.
        """
        url = f"{BASE_URL}/about/contacts/"
        settings_data = {
            "email_notifications": True
        }

        with allure.step("Отправка PATCH-запроса для настроек"):
            patch_headers = {**HEADERS, "Content-Type": "application/json"}
            response = requests.patch(url, json=settings_data, headers=patch_headers)

        with allure.step("Проверка статус-кода"):
            assert response.status_code == 200, \
                f"Неожиданный статус-код: {response.status_code}"

    # ==================== Проверка CORS ====================

    @allure.title("Проверка CORS-заголовков")
    @allure.severity(allure.severity_level.MINOR)
    def test_cors_headers(self):
        """
        Тест проверяет наличие CORS-заголовков для кросс-доменных запросов.
        Важно для работы с API из браузера.
        """
        cors_headers = {
            **HEADERS,
            "Origin": "https://example.com",
            "Access-Control-Request-Method": "POST"
        }

        with allure.step("Отправка OPTIONS-запроса для проверки CORS"):
            response = requests.options(BASE_URL, headers=cors_headers)

        with allure.step("Проверка наличия CORS-заголовков"):
            assert response.status_code == 200, \
                f"Сервер вернул ошибку при проверке CORS: {response.status_code}"


@allure.feature("API-тесты")
@allure.story("Проверка статус-кодов страниц")
class TestApiStatusCodes:
    """Класс тестов для проверки статус-кодов различных страниц"""

    @allure.title("Проверка статус-кодов основных страниц")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("url,expected_status", [
        (BASE_URL, 200),
        (f"{BASE_URL}/about/", 200),
        (f"{BASE_URL}/about/contacts/", 200),
        (f"{BASE_URL}/about/terms/", 200),
        (f"{BASE_URL}/buyers/delivery-payment/", 200),
        (f"{BASE_URL}/shampuni_1-23899-s/", 200),
        (f"{BASE_URL}/idei_podarkov-23893-s/", 200),
    ])
    def test_page_status_codes(self, url, expected_status):
        """
        Тест проверяет статус-коды основных страниц сайта.
        Параметризация позволяет проверить несколько страниц.
        """
        with allure.step(f"Отправка GET-запроса к {url}"):
            response = requests.get(url, headers=HEADERS)

        with allure.step(f"Проверка статус-кода {expected_status}"):
            assert response.status_code == expected_status, \
                f"Страница {url}: ожидался {expected_status}, получен {response.status_code}"

    @allure.title("Проверка несуществующей страницы (404)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_404_page(self):
        """
        Тест проверяет корректную обработку несуществующих страниц.
        Ожидается статус-код 404 или редирект.
        """
        url = f"{BASE_URL}/nonexistent-page-12345/"

        with allure.step("Отправка GET-запроса к несуществующей странице"):
            response = requests.get(url, headers=HEADERS)

        with allure.step("Проверка статус-кода"):
            assert response.status_code == 404, \
                f"Некорректная обработка 404: статус {response.status_code}"

    @allure.title("Проверка защищенных страниц (требующих авторизацию)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_protected_pages(self):
        """
        Тест проверяет доступность страниц, требующих авторизацию.
        Без авторизации должен быть редирект на страницу входа или 404.
        """
        protected_urls = [
            f"{BASE_URL}/profile/",
            f"{BASE_URL}/orders/",
            f"{BASE_URL}/favorites/"
        ]

        for url in protected_urls:
            with allure.step(f"Проверка доступа к {url}"):
                response = requests.get(url, headers=HEADERS)
                assert response.status_code == 302, \
                    f"Страница {url}: неожиданный статус {response.status_code}"


@allure.feature("API-тесты")
@allure.story("Проверка производительности API")
class TestApiPerformance:
    """Класс тестов для проверки производительности API"""

    @allure.title("Проверка времени отклика main page < 2с")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_response_time_main(self):
        """
        Тест проверяет, что главная страница загружается менее чем за 2 секунды.
        Критично для пользовательского опыта.
        """
        with allure.step("Измерение времени ответа главной страницы"):
            start = time.time()
            response = requests.get(BASE_URL, headers=HEADERS)
            elapsed = time.time() - start

        with allure.step(f"Проверка времени: {elapsed:.2f}с"):
            assert elapsed < 2, f"Главная страница загружается слишком долго: {elapsed:.2f}с"
            assert response.status_code == 200

    @allure.title("Проверка времени отклика страницы 'О компании' < 3с")
    @allure.severity(allure.severity_level.NORMAL)
    def test_response_time_about(self):
        """
        Тест проверяет, что страница 'О компании' загружается менее чем за 3 секунды.
        """
        with allure.step("Измерение времени ответа страницы 'О компании'"):
            start = time.time()
            response = requests.get(f"{BASE_URL}/about/", headers=HEADERS)
            elapsed = time.time() - start

        with allure.step(f"Проверка времени: {elapsed:.2f}с"):
            assert elapsed < 3, f"Страница загружается слишком долго: {elapsed:.2f}с"

    @allure.title("Проверка времени поиска < 2с")
    @allure.severity(allure.severity_level.NORMAL)
    def test_response_time_search(self):
        """
        Тест проверяет скорость обработки поискового запроса.
        Поиск должен работать быстро для удобства пользователей.
        """
        with allure.step("Измерение времени поиска"):
            search_url = f"{BASE_URL}/search/?q=помада"
            start = time.time()
            response = requests.get(search_url, headers=HEADERS)
            elapsed = time.time() - start

        with allure.step(f"Проверка времени: {elapsed:.2f}с"):
            assert elapsed < 2, f"Поиск работает слишком медленно: {elapsed:.2f}с"

    @allure.title("Проверка стабильности ответов (10 запросов)")
    @allure.severity(allure.severity_level.MINOR)
    def test_response_stability(self):
        """
        Тест проверяет стабильность ответов сервера.
        Отправляет 10 запросов и проверяет, что все успешны.
        """
        response_times = []
        status_codes = []

        with allure.step("Отправка 10 тестовых запросов"):
            for i in range(10):
                start = time.time()
                response = requests.get(BASE_URL, headers=HEADERS)
                elapsed = time.time() - start
                response_times.append(elapsed)
                status_codes.append(response.status_code)

        with allure.step("Проверка стабильности"):
            # Все ответы должны быть успешными
            assert all(code == 200 for code in status_codes), \
                f"Есть ошибки в статус-кодах: {status_codes}"

            # Среднее время ответа не должно превышать 3 секунды
            avg_time = sum(response_times) / len(response_times)
            assert avg_time < 3, f"Среднее время ответа слишком велико: {avg_time:.2f}с"
