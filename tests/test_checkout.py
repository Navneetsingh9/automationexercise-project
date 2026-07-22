import pytest
import random
import string
import time
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from test_data.config import TestData

class TestCheckout:
    
    @pytest.mark.regression
    def test_checkout_as_registered_user(self, driver, logger):
        """Test checkout with registered user"""
        logger.info("Starting checkout test")
        
        # Register a new user
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
        
        # Add product to cart
        home_page.click_products()
        products_page = ProductsPage(driver)
        products_page.add_first_product_to_cart()
        products_page.click_continue_shopping()
        
        # Go to cart
        home_page.click_cart()
        cart_page = CartPage(driver)
        
        # Verify cart has items
        cart_count = cart_page.get_cart_item_count()
        assert cart_count > 0, "Cart is empty"
        logger.info(f"Cart has {cart_count} items")
        
        # STEP 1: Proceed to checkout from cart
        cart_page.proceed_to_checkout()
        time.sleep(3)
        
        # STEP 2: Check if address form needs filling (it's often pre-filled)
        checkout_page = CheckoutPage(driver)
        checkout_page.enter_address_details_if_needed(
            first_name=registration_data["first_name"],
            last_name=registration_data["last_name"],
            address=registration_data["address"],
            city=registration_data["city"],
            state=registration_data["state"],
            zipcode=registration_data["zipcode"],
            mobile=registration_data["mobile"]
        )
        
        # STEP 3: If on review page, click Place Order; else click it from address form
        if checkout_page.is_review_page():
            logger.info("On Review page - clicking Place Order...")
            checkout_page.click_place_order()
        else:
            logger.info("On address form page - clicking Place Order...")
            checkout_page.click_place_order()
            # After first click, we should be on Review page, click Place Order again
            time.sleep(2)
            if checkout_page.is_review_page():
                logger.info("Now on Review page - clicking Place Order again...")
                checkout_page.click_place_order()
        
        # STEP 4: Enter payment details
        checkout_page.enter_payment_details(
            name="Test User",
            card_number="1234567890123456",
            cvc="123",
            expiry_month="12",
            expiry_year="2025"
        )
        
        # STEP 5: Verify order success
        assert checkout_page.is_order_placed(), "Order not placed successfully"
        logger.info("✅ Checkout test passed!")