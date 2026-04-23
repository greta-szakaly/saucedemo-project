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
    
    def sort_product_list(self, option):
        self.sort_dropdown_locator.select_option(option)
    
    def to_product_components(self, locators):
        return [ProductComponent(product_locator) for product_locator in locators.all()]
    
    def get_all_product_components(self):
        return self.to_product_components(self.product_locators)

    def get_added_product_components(self):
        addedProductLocators = self.product_locators.filter(has=self.page.get_by_role("button", name="Remove"))
        return self.to_product_components(addedProductLocators)
    