import time
from locators.main_locators import MainPage


def test_catalog_button_click(driver):
    page = MainPage(driver)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    element = page.btn_catalog.find(timeout=5)
    assert element is not None, "Кнопка каталога не найдена"

    driver.execute_script("arguments[0].click();", element)
    time.sleep(2)

    if len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[-1])

    assert "/about/opt/" in driver.current_url, "Не произошёл переход на страницу каталога"
