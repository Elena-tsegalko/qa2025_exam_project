from locators.main_locators import MainPage


def test_missha(driver):
    page = MainPage(driver)
    print(page.btn_catalog.get_text())
    #page.btn_accept_popup.click()
    #page.input_domain_name.send_keys('Take_me_home_country_roads')
    #page.btn_found_domain.click()
    #time.sleep(10)
