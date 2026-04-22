import pytest
from playwright.sync_api import Page, expect

@pytest.fixture
def authenticated_page(authenticated_context):
    page = authenticated_context.new_page()
    page.goto("https://www.saucedemo.com/inventory.html")
    yield(page)
    page.close()

def test_add_one_product_to_cart_from_overview(authenticated_page):
    cartBadge = authenticated_page.get_by_test_id("shopping-cart-badge")
    #addedProductAmount = cartBadge.text_content()

    firstProduct = authenticated_page.get_by_test_id("inventory-item").nth(0)
    firstProductAddToCartButton = firstProduct.get_by_role("button", name="Add to cart")
    firstProductRemoveButton = firstProduct.get_by_role("button", name="Remove")

    expect(firstProductAddToCartButton).to_be_enabled()
    
    firstProductAddToCartButton.click()
    #addedProductAmount += 1
    
    expect(firstProductRemoveButton).to_be_enabled()
    expect(cartBadge).to_have_text("1")

def test_add_one_product_to_cart_from_detail(authenticated_page):
    addToCartButton = authenticated_page.get_by_role("button", name="Add to cart")
    removeButton = authenticated_page.get_by_role("button", name="Remove")
    cartBadge = authenticated_page.get_by_test_id("shopping-cart-badge")

    authenticated_page.get_by_test_id("inventory-item-name").nth(0).click()
    expect(addToCartButton).to_be_enabled()

    addToCartButton.click()
    expect(cartBadge).to_have_text("1")
    expect(removeButton).to_be_enabled()
    
def test_add_multiple_products_to_cart_from_overview(authenticated_page):
    cartBadge = authenticated_page.get_by_test_id("shopping-cart-badge")
    products = authenticated_page.get_by_test_id("inventory-item")

    for product in products.all():
        product.get_by_role("button", name="Add to cart").click()
        expect(product.get_by_role("button", name="Remove")).to_be_enabled()

    expect(cartBadge).to_have_text("6")

def test_remove_one_product_from_cart_from_overview(authenticated_page):
    authenticated_page.evaluate("localStorage.setItem('cart-contents', '[0]')")
    authenticated_page.reload()

    cartBadge = authenticated_page.get_by_test_id("shopping-cart-badge")
    expect(cartBadge).to_have_text("1")

    authenticated_page.get_by_role("button", name="Remove").click()
    expect(cartBadge).to_have_count(0) # expect this element to not exist


def test_remove_one_product_from_cart_from_detail(authenticated_page):
    authenticated_page.evaluate("localStorage.setItem('cart-contents', '[0]')")
    authenticated_page.goto("https://www.saucedemo.com/inventory-item.html?id=0")

    cartBadge = authenticated_page.get_by_test_id("shopping-cart-badge")
    expect(cartBadge).to_have_text("1")

    authenticated_page.get_by_role("button", name="Remove").click()
    expect(cartBadge).to_have_count(0) # expect this element to not exist
