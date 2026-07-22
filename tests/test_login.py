import pytest
import random
import string
import time
from pages.home_page import HomePage
from pages.login_page import LoginPage
from test_data.config import TestData

class TestLogin:
    
    @pytest.mark.smoke
    def test_valid_login(self, driver, logger):
        """Test successful login with valid credentials"""
        logger.info("Starting valid login test")
        
        # First register a user
        random_str = ''.join(random.choices(string.ascii_lowercase, k=8))
        email = f"testuser_{random_str}@example.com"
        password = "TestPass123"
        
        home_page = HomePage(driver)
        home_page.open()
        home_page.click_signup_login()
        
        login_page = LoginPage(driver)
        login_page.enter_signup_name("Test User")
        login_page.enter_signup_email(email)
        login_page.click_signup_button()
        
        time.sleep(2)
        registration_data = TestData.REGISTRATION
        login_page.select_gender("Mr")
        login_page.enter_password(password)
        login_page.select_dob("1", "January", "1990")
        login_page.enter_first_name(registration_data["first_name"])
        login_page.enter_last_name(registration_data["last_name"])
        login_page.enter_company(registration_data["company"])
        login_page.enter_address(registration_data["address"])
        login_page.select_country(registration_data["country"])
        login_page.enter_state(registration_data["state"])
        login_page.enter_city(registration_data["city"])
        login_page.enter_zipcode(registration_data["zipcode"])
        login_page.enter_mobile(registration_data["mobile"])
        login_page.click_create_account()
        login_page.click_continue()
        
        # Logout
        time.sleep(2)
        home_page.click_logout()
        
        # Login with credentials
        home_page.click_signup_login()
        login_page.login(email, password)
        
        # Verify login success
        time.sleep(2)
        assert "Logout" in driver.page_source, "Logout link not found - user not logged in"
        logger.info("✅ Valid login test passed!")
    
    @pytest.mark.regression
    def test_invalid_password(self, driver, logger):
        """Test login with invalid password"""
        logger.info("Starting invalid password test")
        
        home_page = HomePage(driver)
        home_page.open()
        home_page.click_signup_login()
        
        login_page = LoginPage(driver)
        login_page.login("test@example.com", "WrongPass")
        
        time.sleep(1)
        assert login_page.is_login_error_displayed(), "Login error not displayed"
        logger.info("✅ Invalid password test passed!")
    
    @pytest.mark.regression
    def test_empty_fields(self, driver, logger):
        """Test login with empty fields"""
        logger.info("Starting empty fields test")
        
        home_page = HomePage(driver)
        home_page.open()
        home_page.click_signup_login()
        
        login_page = LoginPage(driver)
        login_page.login("", "")
        
        # Wait for error to appear
        time.sleep(2)
        
        # Check if error is displayed (using multiple methods)
        error_displayed = login_page.is_login_error_displayed()
        
        # If error not found, check URL to verify we're still on login page
        current_url = driver.current_url
        logger.info(f"Current URL: {current_url}")
        
        # Test passes if either error is displayed OR we're still on login page
        if error_displayed:
            logger.info("✅ Login error displayed")
        else:
            assert "login" in current_url, f"Expected login page, got {current_url}"
            logger.info("✅ Empty fields test passed (stayed on login page)")