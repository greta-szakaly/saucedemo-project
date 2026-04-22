from models.Product import Product

class ProductComponent:
    def __init__(self, root):
        self.root = root

    @property
    def name_locator(self):
        return self.root.get_by_test_id("inventory-item-name")
    
    @property
    def descripion_locator(self):
        return self.root.get_by_test_id("inventory-item-desc")
    
    @property
    def price_locator(self):
        return self.root.get_by_test_id("inventory-item-price")
        
    @property
    def image_locator(self): 
        return self.root.get_by_role("img")
    
    @property
    def add_to_cart_button_locator(self):
        return self.root.get_by_role("button", name="Add to cart")
    
    @property
    def remove_from_cart_button_locator(self):
        return self.root.get_by_role("button", name="Remove")

    def get_name(self):
        return self.name_locator.inner_text()
    
    def get_descripion(self):
        return self.descripion_locator.inner_text()
    
    def get_price(self):
        return float((self.price_locator.inner_text()).strip("$"))
    
    def click_image(self):
        self.image_locator.click()

    def add_to_cart(self):
        self.add_to_cart_button_locator.click()

    def remove_from_cart(self):
        self.remove_from_cart_button_locator.click()

    def to_model(self):
        return Product(self.get_name(), self.get_descripion(), self.get_price())