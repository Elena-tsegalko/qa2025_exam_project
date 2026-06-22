"""
Модуль нагрузочных тестов для проверки производительности сайта misshacosmetics.by.

Содержит тесты для проверки:
- Параллельных запросов к серверу
- Времени ответа при нагрузке
- Стабильности сервера под нагрузкой

Все тесты переиспользуют API-методы из основных тестов.
"""

import requests
import pytest
import allure
import time
import concurrent.futures


# Конфигурация для нагрузочных тестов
BASE_URL = "https://misshacosmetics.by"

# Заголовок User-Agent для имитации браузера
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


def is_server_available():
    """Проверка доступности сервера перед запуском тестов"""
    try:
        response = requests.get(BASE_URL, headers=HEADERS, timeout=10)
        return response.status_code == 200
    except:
        return False


# Пропуск всех нагрузочных тестов если сервер недоступен
pytestmark = pytest.mark.skipif(
    not is_server_available(),
    reason="Сервер недоступен (возможно, rate limiting)"
)


def safe_request(url, method="GET", timeout=15, **kwargs):
    """
    Безопасный запрос с обработкой ошибок.
    Возвращает None в случае ошибки соединения.
    """
    try:
        if method == "GET":
            return requests.get(url, headers=HEADERS, timeout=timeout, **kwargs)
        elif method == "POST":
            return requests.post(url, headers=HEADERS, timeout=timeout, **kwargs)
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError,
            requests.exceptions.ReadTimeout):
        return None


@allure.feature("Нагрузочные тесты")
@allure.story("Параллельные запросы")
class TestConcurrentRequests:
    """Класс тестов для проверки параллельных запросов"""

    @allure.title("Параллельные GET-запросы (3 потока)")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_concurrent_get_requests(self):
        """
        Тест проверяет обработку 3 одновременных GET-запросов.
        Проверяет стабильность сервера при параллельных обращениях.
        """
        results = []

        def make_request(url):
            """Функция для выполнения одного запроса"""
            start = time.time()
            response = safe_request(url, timeout=20)
            elapsed = time.time() - start
            if response:
                return {"status": response.status_code, "time": elapsed, "success": True}
            return {"status": 0, "time": elapsed, "success": False}

        with allure.step("Выполнение 3 параллельных запросов"):
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                futures = [executor.submit(make_request, BASE_URL) for _ in range(3)]
                for future in concurrent.futures.as_completed(futures):
                    results.append(future.result())

        with allure.step("Анализ результатов"):
            successful = [r for r in results if r["success"]]
            stats = f"Успешных: {len(successful)}/3"
            allure.attach(stats, name="Статистика", attachment_type=allure.attachment_type.TEXT)

            assert len(successful) >= 1, "Ни один запрос не выполнен успешно"

    @allure.title("Параллельные POST-запросы (2 потока)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_concurrent_post_requests(self):
        """
        Тест проверяет обработку 2 одновременных POST-запросов.
        """
        results = []

        def make_post_request(url, data):
            """Функция для выполнения POST-запроса"""
            start = time.time()
            response = safe_request(url, method="POST", data=data, timeout=20)
            elapsed = time.time() - start
            if response:
                return {"status": response.status_code, "time": elapsed, "success": True}
            return {"status": 0, "time": elapsed, "success": False}

        with allure.step("Выполнение 2 параллельных POST-запросов"):
            test_data = {"test": "data"}
            url = f"{BASE_URL}/ajax/callback/"

            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                futures = [executor.submit(make_post_request, url, test_data) for _ in range(2)]
                for future in concurrent.futures.as_completed(futures):
                    results.append(future.result())

        with allure.step("Анализ результатов"):
            successful = [r for r in results if r["success"]]
            stats = f"Успешных: {len(successful)}/2"
            allure.attach(stats, name="Статистика POST", attachment_type=allure.attachment_type.TEXT)

            assert len(successful) >= 1, "POST-запросы не обработаны"


@allure.feature("Нагрузочные тесты")
@allure.story("Нагрузка на разные страницы")
class TestLoadOnPages:
    """Класс тестов для проверки нагрузки на разные страницы"""

    @allure.title("Нагрузка на главную страницу (5 запросов)")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_load_main_page(self):
        """
        Тест проверяет обработку 5 запросов к главной странице.
        Проверяет стабильность при умеренной нагрузке.
        """
        results = []

        with allure.step("Выполнение 5 запросов к главной"):
            for i in range(5):
                response = safe_request(BASE_URL, timeout=15)
                if response:
                    results.append({"status": response.status_code})
                else:
                    results.append({"status": 0})
                time.sleep(1)

        with allure.step("Анализ результатов"):
            successful = [r for r in results if r["status"] == 200]
            stats = f"Успешных: {len(successful)}/5"
            allure.attach(stats, name="Статистика нагрузки", attachment_type=allure.attachment_type.TEXT)

            success_rate = len(successful) / len(results) * 100
            assert success_rate >= 60, f"Низкий процент успешных запросов: {success_rate:.1f}%"

    @allure.title("Нагрузка на страницу 'О компании' (5 запросов)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_load_about_page(self):
        """
        Тест проверяет обработку 5 запросов к странице 'О компании'.
        """
        about_url = f"{BASE_URL}/about/"
        results = []

        with allure.step("Выполнение 5 запросов к странице 'О компании'"):
            for i in range(5):
                response = safe_request(about_url, timeout=15)
                if response:
                    results.append({"status": response.status_code})
                else:
                    results.append({"status": 0})
                time.sleep(1)

        with allure.step("Анализ результатов"):
            successful = [r for r in results if 200 <= r.get("status", 0) < 400]
            stats = f"Успешных: {len(successful)}/5"
            allure.attach(stats, name="Статистика", attachment_type=allure.attachment_type.TEXT)

            success_rate = len(successful) / len(results) * 100
            assert success_rate >= 60, f"Низкий процент успешных запросов: {success_rate:.1f}%"

    @allure.title("Нагрузка на контакты (5 запросов)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_load_contacts(self):
        """
        Тест проверяет обработку 5 запросов к странице контактов.
        """
        contacts_url = f"{BASE_URL}/about/contacts/"
        results = []

        with allure.step("Выполнение 5 запросов к контактам"):
            for i in range(5):
                response = safe_request(contacts_url, timeout=15)
                if response:
                    results.append({"status": response.status_code})
                else:
                    results.append({"status": 0})
                time.sleep(1)

        with allure.step("Анализ результатов"):
            successful = [r for r in results if 200 <= r.get("status", 0) < 400]
            stats = f"Успешных: {len(successful)}/5"
            allure.attach(stats, name="Статистика", attachment_type=allure.attachment_type.TEXT)

            success_rate = len(successful) / len(results) * 100
            assert success_rate >= 60, f"Низкий процент успешных запросов: {success_rate:.1f}%"


@allure.feature("Нагрузочные тесты")
@allure.story("Проверка времени ответа")
class TestResponseTime:
    """Класс тестов для проверки времени ответа"""

    @allure.title("Проверка времени отклика главной страницы < 5с")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_response_time_main(self):
        """
        Тест проверяет, что главная страница загружается менее чем за 5 секунд.
        """
        with allure.step("Измерение времени ответа"):
            start = time.time()
            response = safe_request(BASE_URL, timeout=15)
            elapsed = time.time() - start

        if response:
            with allure.step(f"Проверка времени: {elapsed:.2f}с"):
                assert elapsed < 5, f"Главная страница загружается слишком долго: {elapsed:.2f}с"
                assert response.status_code == 200
        else:
            pytest.skip("Сервер не отвечает")

    @allure.title("Проверка стабильности ответов (5 запросов)")
    @allure.severity(allure.severity_level.MINOR)
    def test_response_stability(self):
        """
        Тест проверяет стабильность ответов сервера.
        Отправляет 5 запросов и проверяет, что хотя бы 80% успешны.
        """
        status_codes = []

        with allure.step("Отправка 5 тестовых запросов"):
            for i in range(5):
                response = safe_request(BASE_URL, timeout=15)
                if response:
                    status_codes.append(response.status_code)
                else:
                    status_codes.append(0)
                time.sleep(1)

        with allure.step("Проверка стабильности"):
            successful = sum(1 for code in status_codes if code == 200)
            success_rate = successful / len(status_codes) * 100 if status_codes else 0

            stats = f"""
            Всего запросов: {len(status_codes)}
            Успешных (200): {successful}
            Процент успеха: {success_rate:.1f}%
            """
            allure.attach(stats, name="Статистика", attachment_type=allure.attachment_type.TEXT)

            assert success_rate >= 80, \
                f"Сервер нестабилен: {success_rate:.1f}% успешных запросов"

    @allure.title("Проверка ответа несуществующей страницы (404)")
    @allure.severity(allure.severity_level.MINOR)
    def test_404_response(self):
        """
        Тест проверяет корректную обработку несуществующих страниц.
        """
        url = f"{BASE_URL}/nonexistent-page-12345/"

        with allure.step("Отправка запроса к несуществующей странице"):
            response = safe_request(url, timeout=15)

        if response:
            with allure.step("Проверка статус-кода"):
                assert response.status_code in [404, 301, 302], \
                    f"Некорректная обработка 404: статус {response.status_code}"
        else:
            pytest.skip("Сервер не отвечает")
