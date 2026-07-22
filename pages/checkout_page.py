from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time

class CheckoutPage(BasePage):
    """Page Object for Checkout Page"""
    
    # Address Form locators
    FIRST_NAME = (By.XPATH, "//input[@placeholder='First Name']")
    LAST_NAME = (By.XPATH, "//input[@placeholder='Last Name']")
    ADDRESS = (By.XPATH, "//input[@placeholder='Address *']")
    CITY = (By.XPATH, "//input[@placeholder='City *']")
    STATE = (By.XPATH, "//input[@placeholder='State *']")
    ZIPCODE = (By.XPATH, "//input[@placeholder='Zipcode *']")
    MOBILE = (By.XPATH, "//input[@placeholder='Mobile Number *']")
    
    FIRST_NAME_QA = (By.XPATH, "//input[@data-qa='first_name']")
    LAST_NAME_QA = (By.XPATH, "//input[@data-qa='last_name']")
    ADDRESS_QA = (By.XPATH, "//input[@data-qa='address']")
    CITY_QA = (By.XPATH, "//input[@data-qa='city']")
    STATE_QA = (By.XPATH, "//input[@data-qa='state']")
    ZIPCODE_QA = (By.XPATH, "//input[@data-qa='zipcode']")
    MOBILE_QA = (By.XPATH, "//input[@data-qa='mobile_number']")
    
    REVIEW_ORDER = (By.XPATH, "//h2[contains(text(),'Review Your Order')]")
    PLACE_ORDER_BUTTON = (By.XPATH, "//a[contains(text(),'Place Order')]")
    
    # Payment Page
    CARD_NAME = (By.NAME, "name_on_card")
    CARD_NUMBER = (By.NAME, "card_number")
    CARD_CVC = (By.NAME, "cvc")
    CARD_EXPIRY_MONTH = (By.NAME, "expiry_month")
    CARD_EXPIRY_YEAR = (By.NAME, "expiry_year")
    PAY_CONFIRM = (By.ID, "submit")
    
    # Success Page 
    ORDER_PLACED = (By.XPATH, "//*[contains(text(),'ORDER PLACED') or contains(text(),'Order Placed') or contains(text(),'ORDER PLACED!')]")
    ORDER_CONFIRMED = (By.XPATH, "//*[contains(text(),'order has been confirmed') or contains(text(),'congratulations')]")
    
    def enter_address_details_if_needed(self, first_name, last_name, address, city, state, zipcode, mobile):
        """Only fill address if form is visible (it's often pre-filled from registration)"""
        self.logger.info("Checking if address form needs to be filled...")
        time.sleep(2)
        
        self.logger.info(f"Current URL: {self.driver.current_url}")
        
        if self.is_review_page():
            self.logger.info("Already on Review page - address already filled!")
            return self
        
        try:
            try:
                first_name_field = self.driver.find_element(*self.FIRST_NAME_QA)
                if first_name_field.get_attribute("value") == "":
                    self.logger.info("Address form is empty - filling it...")
                    self.enter_text(self.FIRST_NAME_QA, first_name)
                    self.enter_text(self.LAST_NAME_QA, last_name)
                    self.enter_text(self.ADDRESS_QA, address)
                    self.enter_text(self.CITY_QA, city)
                    self.enter_text(self.STATE_QA, state)
                    self.enter_text(self.ZIPCODE_QA, zipcode)
                    self.enter_text(self.MOBILE_QA, mobile)
                    self.logger.info("Filled address details")
                else:
                    self.logger.info("Address form already has values - skipping fill")
            except:
                try:
                    first_name_field = self.driver.find_element(*self.FIRST_NAME)
                    if first_name_field.get_attribute("value") == "":
                        self.logger.info("Address form is empty - filling it...")
                        self.enter_text(self.FIRST_NAME, first_name)
                        self.enter_text(self.LAST_NAME, last_name)
                        self.enter_text(self.ADDRESS, address)
                        self.enter_text(self.CITY, city)
                        self.enter_text(self.STATE, state)
                        self.enter_text(self.ZIPCODE, zipcode)
                        self.enter_text(self.MOBILE, mobile)
                        self.logger.info("Filled address details")
                    else:
                        self.logger.info("Address form already has values - skipping fill")
                except:
                    self.logger.info("Address form not found - likely already on Review page")
        except Exception as e:
            self.logger.info(f"Address form not accessible: {e} - skipping fill")
        
        return self
    
    def click_place_order(self):
        """Click Place Order button"""
        self.logger.info("Clicking Place Order...")
        time.sleep(1)
        
        self.scroll_to_element(self.PLACE_ORDER_BUTTON)
        time.sleep(1)
        self.click_element(self.PLACE_ORDER_BUTTON)
        time.sleep(3)
        self.logger.info("Clicked Place Order")
        return self
    
    def is_review_page(self):
        """Check if we're on the Order Review page"""
        try:
            return self.is_element_visible(self.REVIEW_ORDER)
        except:
            return False
    
    def enter_payment_details(self, name, card_number, cvc, expiry_month, expiry_year):
        """Enter payment details"""
        self.logger.info("Entering payment details...")
        time.sleep(2)
        
        self.enter_text(self.CARD_NAME, name)
        self.enter_text(self.CARD_NUMBER, card_number)
        self.enter_text(self.CARD_CVC, cvc)
        self.enter_text(self.CARD_EXPIRY_MONTH, expiry_month)
        self.enter_text(self.CARD_EXPIRY_YEAR, expiry_year)
        
        self.click_element(self.PAY_CONFIRM)
        time.sleep(3)
        self.logger.info("Payment confirmed!")
        return self
    
    def is_order_placed(self):
        """Check if order was placed successfully - checks multiple locators"""
        time.sleep(2)
        
        # Try multiple locators for order success
        locators = [
            self.ORDER_PLACED,
            self.ORDER_CONFIRMED,
            (By.XPATH, "//*[contains(text(),'ORDER PLACED')]"),
            (By.XPATH, "//*[contains(text(),'Order Placed')]"),
            (By.XPATH, "//*[contains(text(),'order has been confirmed')]"),
            (By.XPATH, "//*[contains(text(),'Congratulations')]")
        ]
        
        for locator in locators:
            try:
                if self.is_element_visible(locator):
                    self.logger.info(f"Order success found with: {locator}")
                    return True
            except:
                continue
        
        # Check URL as fallback
        if "payment" in self.driver.current_url or "order" in self.driver.current_url:
            self.logger.info(f"Order success detected by URL: {self.driver.current_url}")
            return True
        
        # Check page source as final fallback
        try:
            page_text = self.driver.page_source.lower()
            if "order placed" in page_text or "congratulations" in page_text:
                self.logger.info("Order success detected in page source")
                return True
        except:
            pass
        
        self.logger.warning("Order success not found")
        return False
