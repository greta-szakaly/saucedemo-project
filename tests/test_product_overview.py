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
    # get products
    products = authenticated_page.get_by_test_id("inventory-item")

    # verify number of items
    expect(products).to_have_count(6)

    # verify visibility of items
    for product in products.all():
        expect(product).to_be_visible()
        
def test_all_products_are_present(authenticated_page):
    # get products
    products = authenticated_page.get_by_test_id("inventory-item")
    
    for i in range(products.count()):
        product = products.nth(i)
        expect(product.get_by_test_id("inventory-item-name")).to_have_text(EXPECTED_PRODUCTS[i])