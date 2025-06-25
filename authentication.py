from playwright.sync_api import sync_playwright
from tests.pageobjects.LoginPage import LoginPage

def save_storage_state():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://saucedemo.com/")

        loginPage = LoginPage(page)
        loginPage.login("standard_user", "secret_sauce")

        page.wait_for_load_state("networkidle")

        context.storage_state(path="state.json")

        browser.close()

save_storage_state()