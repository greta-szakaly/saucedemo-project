import pytest
from playwright.sync_api import Page, expect
from pageobjects.ProductsPage import ProductsPage
from pageobjects.ProductDetailPage import ProductDetailPage
from components.ProductComponent import ProductComponent

@pytest.fixture
def authenticated_page(authenticated_context):
    page = authenticated_context.new_page()
    page.goto("https://www.saucedemo.com/inventory.html")
    yield(page)
    page.close()

def test_add_one_product_to_cart_from_overview(authenticated_page):
    productsPage = ProductsPage(authenticated_page)

    firstProductComponent = productsPage.get_all_product_components()[0]

    expect(firstProductComponent.add_to_cart_button_locator).to_be_enabled()
    
    firstProductComponent.add_to_cart()
    
    expect(firstProductComponent.remove_from_cart_button_locator).to_be_enabled()
    expect(productsPage.cart_badge_locator).to_have_text("1")

def test_add_one_product_to_cart_from_detail(authenticated_page):
    productsPage = ProductsPage(authenticated_page)
    productDetailPage = ProductDetailPage(authenticated_page)

    productsPage.get_all_product_components()[0].click_image()

    productComponent = productDetailPage.get_product_detail_component()

    expect(productComponent.add_to_cart_button_locator).to_be_enabled()

    productComponent.add_to_cart()

    expect(productDetailPage.cart_badge_locator).to_have_text("1")
    expect(productComponent.remove_from_cart_button_locator).to_be_enabled()
    
def test_add_multiple_products_to_cart_from_overview(authenticated_page):
    productsPage = ProductsPage(authenticated_page)

    productComponents = productsPage.get_all_product_components()

    for productComponent in productComponents:
        productComponent.add_to_cart()
        expect(productComponent.remove_from_cart_button_locator).to_be_enabled()

    expect(productsPage.cart_badge_locator).to_have_text("6")

def test_remove_one_product_from_cart_from_overview(authenticated_page):
    productsPage = ProductsPage(authenticated_page)

    authenticated_page.evaluate("localStorage.setItem('cart-contents', '[0]')")
    authenticated_page.reload()

    while productsPage.get_added_product_components():
        productsPage.get_added_product_components()[0].remove_from_cart()

    expect(productsPage.cart_badge_locator).to_have_count(0) # expect this element to not exist

def test_remove_one_product_from_cart_from_detail(authenticated_page):
    productDetailPage = ProductDetailPage(authenticated_page)

    authenticated_page.evaluate("localStorage.setItem('cart-contents', '[0]')")
    authenticated_page.goto("https://www.saucedemo.com/inventory-item.html?id=0")

    productComponent = productDetailPage.get_product_detail_component()
    productComponent.remove_from_cart()

    expect(productDetailPage.cart_badge_locator).to_have_count(0) # expect this element to not exist

def test_remove_multiple_products_from_cart_from_overview(authenticated_page):
    productsPage = ProductsPage(authenticated_page)

    authenticated_page.evaluate("localStorage.setItem('cart-contents', '[0, 4]')")
    authenticated_page.reload()

    while productsPage.get_added_product_components():
        productsPage.get_added_product_components()[0].remove_from_cart()

    expect(productsPage.cart_badge_locator).to_have_count(0) # expect this element to not exist
