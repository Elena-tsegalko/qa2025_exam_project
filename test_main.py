import requests
import pytest
from urls import links


@pytest.mark.parametrize("url", links)
def test_get_request(url):
    response = requests.get(url)
    assert response.status_code == 200, "Неверный статус код. Ожидался 200"