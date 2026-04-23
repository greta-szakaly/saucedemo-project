import pytest
from playwright.sync_api import Page, expect
from data.products import ALL_PRODUCTS
from pageobjects.ProductsPage import ProductsPage
from pageobjects.ProductDetailPage import ProductDetailPage
from components.ProductComponent import ProductComponent

@pytest.fixture
def authenticated_page(authenticated_context):
    page = authenticated_context.new_page()
    page.goto("https://www.saucedemo.com/inventory.html")
    yield(page)
    page.close()

def test_product_list_is_visible(authenticated_page):
    productsPage = ProductsPage(authenticated_page)

    productLocators = productsPage.product_locators

    expect(productLocators).to_have_count(6)

    for productLocator in productLocators.all():
        expect(productLocator).to_be_visible()
        
def test_all_products_are_present(authenticated_page):
    productsPage = ProductsPage(authenticated_page)

    productComponents = productsPage.get_product_components()
    
    for i in range(len(productComponents)):
        productComponent = productComponents[i]
        expect(productComponent.name_locator).to_have_text(ALL_PRODUCTS[i].name)

def test_all_product_images_are_clickable(authenticated_page):
    productsPage = ProductsPage(authenticated_page)
    productDetailPage = ProductDetailPage(authenticated_page)

    productComponents = productsPage.get_product_components()

    for productComponent in productComponents:
        productComponent.click_image()

        expect(productDetailPage.back_to_products_button_locator).to_be_visible()

        productsPage.goto()

def test_all_product_names_are_clickable(authenticated_page):
    productsPage = ProductsPage(authenticated_page)
    productDetailPage = ProductDetailPage(authenticated_page)

    productNameLocators = [productComponent.name_locator for productComponent in productsPage.get_product_components()]

    for productNameLocator in productNameLocators:
        productNameLocator.click()

        expect(productDetailPage.back_to_products_button_locator).to_be_visible()

        productsPage.goto()

def test_sort_by_name_ascending(authenticated_page):
    productsPage = ProductsPage(authenticated_page)

    expectedProductNamesAscending = sorted([item.name for item in ALL_PRODUCTS])

    productsPage.sort_product_list("az")

    productNameLocators = [productComponent.name_locator for productComponent in productsPage.get_product_components()]

    for i in range(len(productNameLocators)):
        expect(productNameLocators[i]).to_have_text(expectedProductNamesAscending[i])

def test_sort_by_name_descending(authenticated_page):
    productsPage = ProductsPage(authenticated_page)

    expectedProductNamesDescending = sorted([item.name for item in ALL_PRODUCTS], reverse=True)

    productsPage.sort_product_list("za")

    productNameLocators = [productComponent.name_locator for productComponent in productsPage.get_product_components()]

    for i in range(len(productNameLocators)):
        expect(productNameLocators[i]).to_have_text(expectedProductNamesDescending[i])

def test_sort_by_price_ascending(authenticated_page):
    productsPage = ProductsPage(authenticated_page)

    expectedProductPricesAscending = sorted([item.price for item in ALL_PRODUCTS])

    productsPage.sort_product_list("lohi")

    productPriceLocators = [productComponent.price_locator for productComponent in productsPage.get_product_components()]

    for i in range(len(productPriceLocators)):
        expect(productPriceLocators[i]).to_have_text("$" + str(expectedProductPricesAscending[i]))

def test_sort_by_price_descending(authenticated_page):
    productsPage = ProductsPage(authenticated_page)

    expectedProductPricesDescending = sorted([item.price for item in ALL_PRODUCTS], reverse=True)

    productsPage.sort_product_list("hilo")

    productPriceLocators = [productComponent.price_locator for productComponent in productsPage.get_product_components()]

    for i in range(len(productPriceLocators)):
        expect(productPriceLocators[i]).to_have_text("$" + str(expectedProductPricesDescending[i]))