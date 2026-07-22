import pytest
import random
import string
import time
from pages.home_page import HomePage
from pages.login_page import LoginPage
from test_data.config import TestData

class TestRegistration:
    
    def test_new_user_registration(self, driver, logger):
        """Test registering a new user"""
        logger.info("Starting registration test")
        
        # Generate unique email
        random_str = ''.join(random.choices(string.ascii_lowercase, k=8))
        email = f"testuser_{random_str}@example.com"
        logger.info(f"Generated email: {email}")
        
        home_page = HomePage(driver)
        home_page.open()
        home_page.click_signup_login()
        
        login_page = LoginPage(driver)
        
        # Fill signup form
        login_page.enter_signup_name("John Doe")
        login_page.enter_signup_email(email)
        login_page.click_signup_button()
        
        # Wait for registration form to load
        time.sleep(2)
        
        registration_data = TestData.REGISTRATION
        
        # Fill registration form
        login_page.select_gender("Mr")
        login_page.enter_password(registration_data["password"])
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
        
        # Click create account with ad handling
        login_page.click_create_account()
        
        # Wait for account creation page
        time.sleep(3)
        
        # Verify account created using improved method
        assert login_page.is_account_created(), "Account creation failed - success message not found"
        logger.info("✅ Account created successfully!")
        
        # Continue and verify user is logged in
        login_page.click_continue()
        
        # Wait for home page
        time.sleep(2)
        assert home_page.is_home_page_loaded(), "Home page not loaded after registration"
        logger.info("✅ Registration test passed!")
    
    def test_existing_user_signup(self, driver, logger):
        """Test signing up with existing email"""
        logger.info("Starting existing user signup test")
        
        home_page = HomePage(driver)
        home_page.open()
        home_page.click_signup_login()
        
        login_page = LoginPage(driver)
        login_page.enter_signup_name("Test User")
        login_page.enter_signup_email(TestData.VALID_EMAIL)
        login_page.click_signup_button()
        
        time.sleep(1)
        
        # Verify error message
        error_msg = login_page.get_signup_error()
        assert error_msg is not None and "already exist" in error_msg.lower(), f"Expected 'already exist', got '{error_msg}'"
        logger.info("✅ Existing user signup test passed!")
    
    def test_registration_with_empty_fields(self, driver, logger):
        """Test registration with empty fields"""
        logger.info("Starting empty fields registration test")
        
        home_page = HomePage(driver)
        home_page.open()
        home_page.click_signup_login()
        
        login_page = LoginPage(driver)
        login_page.enter_signup_name("")
        login_page.enter_signup_email("")
        login_page.click_signup_button()
        
        time.sleep(1)
        
        # Check if we're still on the login page (should be)
        current_url = driver.current_url
        logger.info(f"Current URL: {current_url}")
        
        # The test passes if we're still on the login page or signup page
        assert "login" in current_url or "signup" in current_url, f"Expected login/signup page, got {current_url}"
        logger.info("✅ Empty fields test passed!")