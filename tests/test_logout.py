import pytest
from playwright.sync_api import Page, expect
from pageobjects.LoginPage import LoginPage

@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page):
    page.goto("/")
    yield

def test_logout_with_standard_user(page: Page):
    loginPage = LoginPage(page)
    loginPage.login("standard_user", "secret_sauce")
    page.get_by_role("button", name="Open Menu").click()
    page.get_by_role("link", name="Logout").click()
    expect(page).to_have_url("https://www.saucedemo.com/")
    expect(loginPage.login_button).to_be_enabled()