import pytest

pytest.importorskip("playwright.sync_api")
from playwright.sync_api import sync_playwright


@pytest.mark.playwright
def test_valid_login_shows_success_message(base_url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(base_url)

        page.locator("#email").fill("qa@example.com")
        page.locator("#password").fill("Password123")
        page.locator("#login-btn").click()

        assert page.locator("#login-status").inner_text() == "Login successful"
        browser.close()


@pytest.mark.playwright
def test_invalid_login_shows_error_message(base_url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(base_url)

        page.locator("#email").fill("qa@example.com")
        page.locator("#password").fill("wrong")
        page.locator("#login-btn").click()

        assert page.locator("#login-status").inner_text() == "Invalid credentials"
        browser.close()


@pytest.mark.playwright
@pytest.mark.parametrize(
    "query,expected",
    [
        ("mouse", ["Mouse"]),
        ("USB", ["USB Cable"]),
    ],
)
def test_search_filters_results(base_url, query, expected):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(base_url)

        page.locator("#search").fill(query)
        page.locator("#search-btn").click()

        items = page.locator("#results li").all_inner_texts()
        assert items == expected
        browser.close()
