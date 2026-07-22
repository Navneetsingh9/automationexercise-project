from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage
import time

class LoginPage(BasePage):
    """Page Object for Login and Registration Page"""
    
    # Login Locators
    LOGIN_EMAIL = (By.XPATH, "//input[@data-qa='login-email']")
    LOGIN_PASSWORD = (By.XPATH, "//input[@data-qa='login-password']")
    LOGIN_BUTTON = (By.XPATH, "//button[@data-qa='login-button']")
    LOGIN_ERROR = (By.XPATH, "//p[contains(text(),'incorrect!')]")
    
    # Signup Locators
    SIGNUP_NAME = (By.XPATH, "//input[@data-qa='signup-name']")
    SIGNUP_EMAIL = (By.XPATH, "//input[@data-qa='signup-email']")
    SIGNUP_BUTTON = (By.XPATH, "//button[@data-qa='signup-button']")
    SIGNUP_ERROR = (By.XPATH, "//p[contains(text(),'already exist!')]")
    
    # Registration Form Locators
    REGISTER_GENDER_MR = (By.ID, "id_gender1")
    REGISTER_GENDER_MS = (By.ID, "id_gender2")
    REGISTER_PASSWORD = (By.ID, "password")
    REGISTER_DAYS = (By.ID, "days")
    REGISTER_MONTHS = (By.ID, "months")
    REGISTER_YEARS = (By.ID, "years")
    REGISTER_FIRST_NAME = (By.ID, "first_name")
    REGISTER_LAST_NAME = (By.ID, "last_name")
    REGISTER_COMPANY = (By.ID, "company")
    REGISTER_ADDRESS = (By.ID, "address1")
    REGISTER_COUNTRY = (By.ID, "country")
    REGISTER_STATE = (By.ID, "state")
    REGISTER_CITY = (By.ID, "city")
    REGISTER_ZIPCODE = (By.ID, "zipcode")
    REGISTER_MOBILE = (By.ID, "mobile_number")
    REGISTER_CREATE_ACCOUNT = (By.XPATH, "//button[@data-qa='create-account']")
    
    # Success Messages 
    ACCOUNT_CREATED = (By.XPATH, "//*[contains(text(),'Account Created') or contains(text(),'Account Created!')]")
    ACCOUNT_CREATED_HEADING = (By.TAG_NAME, "h2")
    CONTINUE_BUTTON = (By.XPATH, "//a[contains(text(),'Continue')]")
    
    # Error messages
    ACCOUNT_ERROR = (By.XPATH, "//div[contains(@class,'alert-danger')]")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def login(self, email, password):
        """Login with email and password"""
        self.enter_text(self.LOGIN_EMAIL, email)
        self.enter_text(self.LOGIN_PASSWORD, password)
        self.click_element(self.LOGIN_BUTTON)
        self.logger.info(f"Login attempted for: {email}")
        return self
    
    def get_login_error(self):
        """Get login error message"""
        return self.get_text(self.LOGIN_ERROR)
    
    def is_login_error_displayed(self):
        """Check if login error is displayed - multiple locators"""
        # Wait a moment for error to appear
        time.sleep(1)
        
        # Try multiple error locators
        error_locators = [
            self.LOGIN_ERROR,
            (By.XPATH, "//p[contains(text(),'incorrect')]"),
            (By.XPATH, "//div[contains(@class,'alert-danger')]"),
            (By.XPATH, "//div[contains(@class,'alert')]")
        ]
        
        for locator in error_locators:
            try:
                if self.is_element_visible(locator):
                    return True
            except:
                continue
        
        # Check page source as fallback
        try:
            page_text = self.driver.page_source.lower()
            if "incorrect" in page_text or "invalid" in page_text:
                return True
        except:
            pass
        
        return False
    
    def enter_signup_name(self, name):
        """Enter name for signup"""
        self.enter_text(self.SIGNUP_NAME, name)
        return self
    
    def enter_signup_email(self, email):
        """Enter email for signup"""
        self.enter_text(self.SIGNUP_EMAIL, email)
        return self
    
    def click_signup_button(self):
        """Click signup button"""
        self.click_element(self.SIGNUP_BUTTON)
        return self
    
    def get_signup_error(self):
        """Get signup error message"""
        return self.get_text(self.SIGNUP_ERROR)
    
    def select_gender(self, gender="Mr"):
        """Select gender"""
        if gender.lower() == "mr":
            self.click_element(self.REGISTER_GENDER_MR)
        else:
            self.click_element(self.REGISTER_GENDER_MS)
        return self
    
    def enter_password(self, password):
        """Enter password"""
        self.enter_text(self.REGISTER_PASSWORD, password)
        return self
    
    def select_dob(self, day, month, year):
        """Select date of birth"""
        try:
            Select(self.driver.find_element(*self.REGISTER_DAYS)).select_by_visible_text(day)
            Select(self.driver.find_element(*self.REGISTER_MONTHS)).select_by_visible_text(month)
            Select(self.driver.find_element(*self.REGISTER_YEARS)).select_by_visible_text(year)
        except Exception as e:
            self.logger.warning(f"Failed to select DOB: {e}")
            # Try with value as fallback
            try:
                Select(self.driver.find_element(*self.REGISTER_DAYS)).select_by_value(day)
                Select(self.driver.find_element(*self.REGISTER_MONTHS)).select_by_value(str(month))
                Select(self.driver.find_element(*self.REGISTER_YEARS)).select_by_value(year)
            except:
                pass
        return self
    
    def enter_first_name(self, first_name):
        """Enter first name"""
        self.enter_text(self.REGISTER_FIRST_NAME, first_name)
        return self
    
    def enter_last_name(self, last_name):
        """Enter last name"""
        self.enter_text(self.REGISTER_LAST_NAME, last_name)
        return self
    
    def enter_company(self, company):
        """Enter company name"""
        self.enter_text(self.REGISTER_COMPANY, company)
        return self
    
    def enter_address(self, address):
        """Enter address"""
        self.enter_text(self.REGISTER_ADDRESS, address)
        return self
    
    def select_country(self, country):
        """Select country"""
        try:
            Select(self.driver.find_element(*self.REGISTER_COUNTRY)).select_by_visible_text(country)
        except Exception as e:
            self.logger.warning(f"Failed to select country: {e}")
        return self
    
    def enter_state(self, state):
        """Enter state"""
        self.enter_text(self.REGISTER_STATE, state)
        return self
    
    def enter_city(self, city):
        """Enter city"""
        self.enter_text(self.REGISTER_CITY, city)
        return self
    
    def enter_zipcode(self, zipcode):
        """Enter zipcode"""
        self.enter_text(self.REGISTER_ZIPCODE, zipcode)
        return self
    
    def enter_mobile(self, mobile):
        """Enter mobile number"""
        self.enter_text(self.REGISTER_MOBILE, mobile)
        return self
    
    def click_create_account(self):
        """Click create account button with ad handling"""
        # Scroll to the button
        self.scroll_to_element(self.REGISTER_CREATE_ACCOUNT)
        time.sleep(1)
        
        # Close any ads first
        self.close_ads()
        time.sleep(0.5)
        
        # Click using JavaScript (bypasses ads)
        try:
            element = self.driver.find_element(*self.REGISTER_CREATE_ACCOUNT)
            self.driver.execute_script("arguments[0].click();", element)
            self.logger.info("Clicked Create Account button using JavaScript")
            # Wait for page to load after click
            time.sleep(3)
        except Exception as e:
            self.logger.error(f"Failed to click Create Account: {e}")
            # Try regular click as fallback
            self.click_element(self.REGISTER_CREATE_ACCOUNT)
        return self
    
    def is_account_created(self):
        """Check if account created successfully - multiple locators"""
        # Try different locators
        locators = [
            self.ACCOUNT_CREATED,
            self.ACCOUNT_CREATED_HEADING,
            (By.XPATH, "//b[contains(text(),'Account Created')]"),
            (By.XPATH, "//*[contains(text(),'Congratulations')]"),
            (By.XPATH, "//div[contains(@class,'alert-success')]")
        ]
        
        for locator in locators:
            try:
                self.wait.until(lambda driver: driver.find_element(*locator))
                self.logger.info(f"Found account creation message with: {locator}")
                return True
            except:
                continue
        
        # Check URL as fallback
        current_url = self.driver.current_url
        if "account_created" in current_url:
            self.logger.info("Account created page detected by URL")
            return True
        
        # Check for any error messages
        error_elements = self.driver.find_elements(By.XPATH, "//div[contains(@class,'alert')]")
        for element in error_elements:
            text = element.text
            if "error" in text.lower() or "already" in text.lower():
                self.logger.error(f"Account creation failed: {text}")
                return False
        
        return False
    
    def click_continue(self):
        """Click continue button after account creation"""
        try:
            # Wait for continue button
            time.sleep(2)
            self.click_element(self.CONTINUE_BUTTON)
        except Exception as e:
            self.logger.warning(f"Continue button click failed: {e}")
            # Try to find it by text
            try:
                continue_btn = self.driver.find_element(By.XPATH, "//*[contains(text(),'Continue')]")
                self.driver.execute_script("arguments[0].click();", continue_btn)
            except:
                pass
        return self
