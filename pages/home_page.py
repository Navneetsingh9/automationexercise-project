from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class HomePage(BasePage):
    """Page Object for Automation Exercise Home Page"""
    
    # Navigation Locators - Verified
    SIGNUP_LOGIN_LINK = (By.XPATH, "//a[normalize-space()='Signup / Login']")
    LOGOUT_LINK = (By.XPATH, "//a[normalize-space()='Logout']")
    PRODUCTS_LINK = (By.XPATH, "//a[contains(text(),' Products')]")
    CART_LINK = (By.XPATH, "//a[normalize-space()='Cart']")
    TEST_CASES_LINK = (By.XPATH, "//a[normalize-space()='Test Cases']")
    CONTACT_LINK = (By.XPATH, "//a[normalize-space()='Contact us']")
    
    # Home Page Elements
    CAROUSEL = (By.ID, "slider-carousel")
    FEATURES_ITEMS = (By.XPATH, "//div[@class='features_items']")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://www.automationexercise.com/"
    
    def open(self):
        """Open the home page"""
        self.driver.get(self.url)
        self.logger.info(f"Opened URL: {self.url}")
        # Wait for page to load
        self.wait.until(EC.visibility_of_element_located(self.CAROUSEL))
        return self
    
    def click_signup_login(self):
        """Click Signup / Login link"""
        self.click_element(self.SIGNUP_LOGIN_LINK)
        return self
    
    def click_logout(self):
        """Click Logout link"""
        self.click_element(self.LOGOUT_LINK)
        return self
    
    def click_products(self):
        """Click Products link - Updated with better locator"""
        # Try multiple locators for Products link
        locators = [
            (By.XPATH, "//a[contains(text(),' Products')]"),
            (By.XPATH, "//a[contains(@href, '/products')]"),
            (By.XPATH, "//a[normalize-space()='Products']"),
            (By.LINK_TEXT, "Products")
        ]
        
        for locator in locators:
            try:
                self.click_element(locator)
                self.logger.info(f"Clicked Products link using: {locator}")
                return self
            except Exception as e:
                self.logger.warning(f"Failed with {locator}: {e}")
                continue
        
        # If all fail, try direct navigation
        self.logger.warning("All Products link locators failed. Navigating directly.")
        self.driver.get("https://www.automationexercise.com/products")
        return self
    
    def click_cart(self):
        """Click Cart link"""
        self.click_element(self.CART_LINK)
        return self
    
    def click_contact(self):
        """Click Contact us link"""
        self.click_element(self.CONTACT_LINK)
        return self
    
    def is_home_page_loaded(self):
        """Verify home page loaded successfully"""
        return self.is_element_visible(self.CAROUSEL)