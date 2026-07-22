from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage
import time

class ProductsPage(BasePage):
    """Page Object for Products Page"""
    
    # Locators - Verified for AutomationExercise.com
    SEARCH_INPUT = (By.ID, "search_product")
    SEARCH_BUTTON = (By.ID, "submit_search")
    PRODUCT_LIST = (By.XPATH, "//div[@class='productinfo text-center']")
    PRODUCT_NAMES = (By.XPATH, "//div[@class='productinfo text-center']/p")
    ADD_TO_CART_BUTTONS = (By.XPATH, "//a[contains(text(),'Add to cart')]")
    VIEW_CART_LINK = (By.XPATH, "//u[contains(text(),'View Cart')]")
    CONTINUE_SHOPPING = (By.XPATH, "//button[contains(text(),'Continue Shopping')]")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def search_product(self, product_name):
        """Search for a product"""
        try:
            self.enter_text(self.SEARCH_INPUT, product_name)
            self.click_element(self.SEARCH_BUTTON)
            self.logger.info(f"Searched for: {product_name}")
        except Exception as e:
            self.logger.error(f"Search failed: {e}")
            raise
        return self
    
    def get_product_names(self):
        """Get all product names from the list"""
        try:
            # Wait for products to load
            time.sleep(2)
            products = self.driver.find_elements(*self.PRODUCT_NAMES)
            if not products:
                self.logger.warning("No products found")
                return []
            return [product.text for product in products]
        except Exception as e:
            self.logger.warning(f"Error getting product names: {e}")
            return []
    
    def add_first_product_to_cart(self):
        """Add the first product to cart"""
        self.scroll_to_element(self.ADD_TO_CART_BUTTONS)
        time.sleep(0.5)
        self.click_element(self.ADD_TO_CART_BUTTONS)
        self.logger.info("Added first product to cart")
        return self
    
    def add_product_to_cart_by_index(self, index=0):
        """Add product to cart by index"""
        buttons = self.driver.find_elements(*self.ADD_TO_CART_BUTTONS)
        if index < len(buttons):
            buttons[index].click()
            self.logger.info(f"Added product at index {index} to cart")
        else:
            self.logger.error(f"Index {index} out of range")
        return self
    
    def click_view_cart(self):
        """Click View Cart link from modal"""
        self.click_element(self.VIEW_CART_LINK)
        return self
    
    def click_continue_shopping(self):
        """Click Continue Shopping from modal"""
        try:
            self.click_element(self.CONTINUE_SHOPPING)
        except:
            self.logger.warning("Continue Shopping button not found, using direct navigation")
            self.driver.back()
        return self