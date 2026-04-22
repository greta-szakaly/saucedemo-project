import pytest
from playwright.sync_api import Page, expect

@pytest.fixture
def authenticated_page(authenticated_context):
    page = authenticated_context.new_page()
    page.goto("https://www.saucedemo.com/inventory.html")
    yield(page)
    page.close()

def test_product_information_is_consistent(authenticated_page):
    products = authenticated_page.get_by_test_id("inventory-item")

    for product in products.all():
        productName = product.get_by_test_id("inventory-item-name").text_content()
        productDescription = product.get_by_test_id("inventory-item-desc").text_content()
        productPrice = product.get_by_test_id("inventory-item-price").text_content()
        
        product.get_by_role("img").click()

        expect(authenticated_page.get_by_test_id("inventory-item-name")).to_have_text(productName)
        expect(authenticated_page.get_by_test_id("inventory-item-desc")).to_have_text(productDescription)
        expect(authenticated_page.get_by_test_id("inventory-item-price")).to_have_text(productPrice)

        authenticated_page.goto("https://www.saucedemo.com/inventory.html")

def test_back_to_products_navigation(authenticated_page):
    authenticated_page.get_by_test_id("inventory-item-name").nth(0).click()

    backToProductsButton = authenticated_page.get_by_role("button", name="Back to products")
    expect(backToProductsButton).to_be_enabled()

    backToProductsButton.click()
    expect(authenticated_page).to_have_url("https://www.saucedemo.com/inventory.html")
