from pageobjects.BasePage import BasePage
from components.ProductComponent import ProductComponent

class ProductDetailPage(BasePage):
    def __init__(self, page):
        self.page = page

    @property
    def back_to_products_button_locator(self):
        return self.page.get_by_role("button", name="Back to products")

    @property
    def product_detail_locator(self):
        return self.page.get_by_test_id("inventory-item")

    def get_product_detail_component(self):
        return ProductComponent(self.product_detail_locator)
    
    def navigate_back_to_products(self):
        self.back_to_products_button_locator.click()