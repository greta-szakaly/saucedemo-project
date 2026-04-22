from pageobjects.BasePage import BasePage
from components.ProductComponent import ProductComponent

class ProductsPage(BasePage):
    def __init__(self, page):
        self.page = page

    def goto(self):
        self.page.goto("https://www.saucedemo.com/inventory.html")

    @property
    def product_locators(self):
        return self.page.get_by_test_id("inventory-item")
    
    @property
    def sort_dropdown_locator(self):
        return self.page.get_by_test_id("product-sort-container")
    
    def get_product_components(self):
        return [ProductComponent(product_locator) for product_locator in self.product_locators.all()]
    
    def sort_product_list(self, option):
        self.sort_dropdown_locator.select_option(option)