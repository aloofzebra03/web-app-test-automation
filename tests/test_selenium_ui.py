import pytest

selenium = pytest.importorskip("selenium")
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    browser = webdriver.Chrome(options=options)
    yield browser
    browser.quit()


@pytest.mark.selenium
def test_profile_minimum_age_boundary(base_url, driver):
    driver.get(base_url)

    username = driver.find_element(By.ID, "username")
    age = driver.find_element(By.ID, "age")

    username.clear()
    username.send_keys("tester")
    age.clear()
    age.send_keys("18")
    driver.find_element(By.ID, "profile-btn").click()

    status = WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element(
            (By.ID, "profile-status"), "Profile created for tester"
        )
    )
    assert status


@pytest.mark.selenium
def test_profile_below_minimum_age_is_rejected(base_url, driver):
    driver.get(base_url)

    age = driver.find_element(By.ID, "age")
    age.clear()
    age.send_keys("17")
    driver.find_element(By.ID, "profile-btn").click()

    WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element(
            (By.ID, "profile-status"), "Validation failed"
        )
    )
    assert driver.find_element(By.ID, "profile-status").text == "Validation failed"
