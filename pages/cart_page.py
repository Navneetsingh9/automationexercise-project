from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):
    """Page Object for Cart Page"""
    
    # Locators
    CART_ITEMS = (By.XPATH, "//tbody/tr")
    PRODUCT_NAME_IN_CART = (By.XPATH, "//td[@class='cart_description']/h4/a")
    PRODUCT_PRICE_IN_CART = (By.XPATH, "//td[@class='cart_price']/p")
    PRODUCT_QUANTITY = (By.XPATH, "//td[@class='cart_quantity']/button")
    REMOVE_BUTTONS = (By.XPATH, "//a[@class='cart_quantity_delete']")
    CHECKOUT_BUTTON = (By.XPATH, "//a[contains(text(),'Proceed To Checkout')]")
    EMPTY_CART_MESSAGE = (By.XPATH, "//p[contains(text(),'Cart is empty!')]")
    REGISTER_LINK_CHECKOUT = (By.XPATH, "//a[contains(text(),'Register / Login')]")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def get_cart_item_count(self):
        """Get number of items in cart"""
        items = self.driver.find_elements(*self.CART_ITEMS)
        return len(items)
    
    def get_product_names_in_cart(self):
        """Get all product names in cart"""
        products = self.driver.find_elements(*self.PRODUCT_NAME_IN_CART)
        return [product.text for product in products]
    
    def remove_first_item(self):
        """Remove the first item from cart"""
        buttons = self.driver.find_elements(*self.REMOVE_BUTTONS)
        if buttons:
            buttons[0].click()
            self.logger.info("Removed first item from cart")
        return self
    
    def remove_all_items(self):
        """Remove all items from cart"""
        buttons = self.driver.find_elements(*self.REMOVE_BUTTONS)
        for button in buttons:
            button.click()
            self.logger.info("Removed an item from cart")
        return self
    
    def proceed_to_checkout(self):
        """Click Proceed To Checkout button"""
        self.click_element(self.CHECKOUT_BUTTON)
        self.logger.info("Proceeded to checkout")
        return self
    
    def is_cart_empty(self):
        """Check if cart is empty"""
        return self.is_element_visible(self.EMPTY_CART_MESSAGE)
    
    def get_cart_total(self):
        """Get cart total (simplified)"""
        # This is a simplified version - you can expand as needed
        prices = self.driver.find_elements(*self.PRODUCT_PRICE_IN_CART)
        total = 0
        for price in prices:
            value = price.text.replace("Rs.", "").replace(" ", "")
            if value.isdigit():
                total += int(value)
        return total