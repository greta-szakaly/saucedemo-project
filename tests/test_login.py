import pytest
from playwright.sync_api import Page, expect
from pageobjects.LoginPage import LoginPage

@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page):
    page.goto("/")
    yield
    # logout? probs not necessary here, new browser is opened each time

def test_navigation_to_login_page(page: Page):
    expect(page).to_have_url("https://www.saucedemo.com/")
    expect(page).to_have_title("Swag Labs")

def test_username_input_field_is_editable(page: Page):
    loginPage = LoginPage(page)
    loginPage.username_field.click()
    expect(loginPage.username_field).to_be_editable()

def test_password_input_field_is_editable(page: Page):
    loginPage = LoginPage(page)
    loginPage.password_field.click()
    expect(loginPage.password_field).to_be_editable()

def test_login_button_is_enabled(page: Page):
    loginPage = LoginPage(page)
    expect(loginPage.login_button).to_be_enabled()

def test_login_with_valid_credentals(page: Page):
    loginPage = LoginPage(page)
    loginPage.login("standard_user", "secret_sauce")
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

def test_login_with_no_username_and_no_password(page: Page):
    loginPage = LoginPage(page)
    loginPage.login("", "")
    expect(page).to_have_url("https://www.saucedemo.com/")
    expect(loginPage.login_error_message).to_have_text("Epic sadface: Username is required")

def test_login_with_no_username(page: Page):
    loginPage = LoginPage(page)
    loginPage.login("", "test")
    expect(page).to_have_url("https://www.saucedemo.com/")
    expect(loginPage.login_error_message).to_have_text("Epic sadface: Username is required")

def test_login_with_no_password(page: Page):
    loginPage = LoginPage(page)
    loginPage.login("test", "")
    expect(page).to_have_url("https://www.saucedemo.com/")
    expect(loginPage.login_error_message).to_have_text("Epic sadface: Password is required")

def test_login_with_invalid_credentials(page: Page):
    loginPage = LoginPage(page)
    loginPage.login("invalid", "invalid")
    expect(page).to_have_url("https://www.saucedemo.com/")
    expect(loginPage.login_error_message).to_have_text("Epic sadface: Username and password do not match any user in this service")

def test_login_with_locked_out_user_credentials(page: Page):
    loginPage = LoginPage(page)
    loginPage.login("locked_out_user", "secret_sauce")
    expect(page).to_have_url("https://www.saucedemo.com/")
    expect(loginPage.login_error_message).to_have_text("Epic sadface: Sorry, this user has been locked out.")
    # this is mainly design, better separately, the login details are not removed by clicking it anyway
    # expect(page.locator("[data-test='error-button']")).to_be_enabled()
