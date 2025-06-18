class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username_field = page.get_by_role("textbox", name="Username", exact=True)
        self.password_field = page.get_by_role("textbox", name="Password", exact=True)
        self.login_button = page.get_by_role("button", name="Login", exact=True)
        self.login_error_message = page.locator("[data-test='error']")

    def login(self, username, password):
        self.username_field.click()
        self.username_field.fill(username)
        self.password_field.click()
        self.password_field.fill(password)
        self.login_button.click()