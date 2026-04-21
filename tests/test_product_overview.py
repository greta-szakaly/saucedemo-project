import pytest
from playwright.sync_api import Page, expect
import json

EXPECTED_PRODUCTS = [
    "Sauce Labs Backpack",
    "Sauce Labs Bike Light",
    "Sauce Labs Bolt T-Shirt",
    "Sauce Labs Fleece Jacket",
    "Sauce Labs Onesie",
    "Test.allTheThings() T-Shirt (Red)"
]

@pytest.fixture
def authenticated_page(authenticated_context):
    page = authenticated_context.new_page()
    page.goto("https://www.saucedemo.com/inventory.html")
    yield(page)
    page.close()

def test_product_list_is_visible(authenticated_page):
    products = authenticated_page.get_by_test_id("inventory-item")

    expect(products).to_have_count(6)

    for product in products.all():
        expect(product).to_be_visible()
        
def test_all_products_are_present(authenticated_page):
    products = authenticated_page.get_by_test_id("inventory-item")
    
    for i in range(products.count()):
        product = products.nth(i)
        expect(product.get_by_test_id("inventory-item-name")).to_have_text(EXPECTED_PRODUCTS[i])

def test_all_product_images_are_clickable(authenticated_page):
    products = authenticated_page.get_by_test_id("inventory-item")

    for product in products.all():
        productImage = product.get_by_role("img")
        productImage.click()
        expect(authenticated_page.get_by_role("button", name="Back to products")).to_be_visible()

        authenticated_page.goto("https://www.saucedemo.com/inventory.html")

def test_all_product_names_are_clickable(authenticated_page):
    productNames = authenticated_page.get_by_test_id("inventory-item-name")

    for productName in productNames.all():
        productName.click()
        expect(authenticated_page.get_by_role("button", name="Back to products")).to_be_visible()

        authenticated_page.goto("https://www.saucedemo.com/inventory.html")
        

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