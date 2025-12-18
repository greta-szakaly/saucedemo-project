import pytest
from playwright.sync_api import Page, expect
from pageobjects.LoginPage import LoginPage

@pytest.fixture
def authenticated_page(authenticated_context):
    page = authenticated_context.new_page()
    page.goto("https://www.saucedemo.com/inventory.html")
    yield page
    page.close()

def test_logout_with_standard_user(authenticated_page):
    loginPage = LoginPage(authenticated_page)
    # loginPage.login("standard_user", "secret_sauce")
    authenticated_page.get_by_role("button", name="Open Menu").click()
    authenticated_page.get_by_role("link", name="Logout").click()
    expect(authenticated_page).to_have_url("https://www.saucedemo.com/")
    expect(loginPage.login_button).to_be_enabled()