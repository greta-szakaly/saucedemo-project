class BasePage:
    @property
    def cart_badge_locator(self):
        return self.get_by_test_id("shopping-cart-badge")
    
    def get_cart_badge_amount(self):
        return self.cart_badge_locator.inner_text()