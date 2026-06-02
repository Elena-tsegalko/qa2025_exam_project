import requests
import pytest
import allure


@allure.feature("Тесты API")
@allure.story("Проверка статус кода")
class TestApiV1Activities():
    @pytest.mark.parametrize("status_code, name_site, url", [
                             (200, "Главная страница", "https://misshacosmetics.by/"),
                             (200, "Шампуни", "https://misshacosmetics.by/shampuni_1-23899-s/"),
                             (200, "Идеи подарков", "https://misshacosmetics.by/idei_podarkov-23893-s/")
    ])
    @allure.title("Проверка статус кода страниц на экране main")
    def test_api_v1_activities(self, status_code, name_site, url):
        with allure.step("Вызов ручки /api/v1/Activities/"):
            response = requests.get(url=url)

        with allure.step(f"Проверка статус кода страницы {name_site}"):
            assert response.status_code == status_code