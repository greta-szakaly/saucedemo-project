import pytest
from playwright.sync_api import Page, expect
from models.Product import Product
from pageobjects.ProductsPage import ProductsPage
from pageobjects.ProductDetailPage import ProductDetailPage
from components.ProductComponent import ProductComponent

@pytest.fixture
def authenticated_page(authenticated_context):
    page = authenticated_context.new_page()
    page.goto("https://www.saucedemo.com/inventory.html")
    yield(page)
    page.close()

def test_product_information_is_consistent(authenticated_page):
    productsPage = ProductsPage(authenticated_page)
    productDetailPage = ProductDetailPage(authenticated_page)

    productComponents = productsPage.get_product_components()

    for productComponent in productComponents:
        currentProduct = productComponent.to_model()
        
        productComponent.click_image()

        productDetailComponent = productDetailPage.get_product_detail_component()

        expect(productDetailComponent.name_locator).to_have_text(currentProduct.name)
        expect(productDetailComponent.descripion_locator).to_have_text(currentProduct.description)
        expect(productDetailComponent.price_locator).to_have_text("$" + str(currentProduct.price))

        productsPage.goto()

def test_back_to_products_navigation(authenticated_page):
    productsPage = ProductsPage(authenticated_page)
    productDetailPage = ProductDetailPage(authenticated_page)

    productComponents = productsPage.get_product_components()
    productComponents[0].click_image()

    expect(productDetailPage.back_to_products_button_locator).to_be_enabled()

    productDetailPage.navigate_back_to_products()
    expect(authenticated_page).to_have_url("https://www.saucedemo.com/inventory.html")
