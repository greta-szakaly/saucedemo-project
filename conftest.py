import pytest
from pageobjects.LoginPage import LoginPage

@pytest.fixture(scope="session")
def ensure_logged_in_state(browser):
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://saucedemo.com/")

    loginPage = LoginPage(page)
    loginPage.login("standard_user", "secret_sauce")

    page.wait_for_load_state("networkidle")

    context.storage_state(path="state.json")

    context.close()

@pytest.fixture
def authenticated_context(browser, ensure_logged_in_state):
    context = browser.new_context(storage_state="state.json")
    yield context
    context.close()