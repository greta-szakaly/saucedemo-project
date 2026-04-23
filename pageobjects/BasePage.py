class BasePage:
    def __init__(self, page):
        self.page = page
        
    @property
    def cart_badge_locator(self):
        return self.page.get_by_test_id("shopping-cart-badge")
    
    def get_cart_badge_amount(self):
        return self.page.cart_badge_locator.inner_text()