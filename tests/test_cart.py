import pytest
import time
from pages.home_page import HomePage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage

class TestCart:
    
    @pytest.mark.smoke
    def test_add_product_to_cart(self, driver, logger):
        """Test adding a product to cart"""
        logger.info("Starting add to cart test")
        
        home_page = HomePage(driver)
        home_page.open()
        home_page.click_products()
        
        products_page = ProductsPage(driver)
        products_page.add_first_product_to_cart()
        products_page.click_continue_shopping()
        
        # Go to cart and verify
        home_page.click_cart()
        cart_page = CartPage(driver)
        
        assert cart_page.get_cart_item_count() > 0, "Cart is empty"
        logger.info("✅ Add to cart test passed!")
    
    @pytest.mark.regression
    def test_remove_item_from_cart(self, driver, logger):
        """Test removing an item from cart"""
        logger.info("Starting remove item test")
        
        # First add a product
        home_page = HomePage(driver)
        home_page.open()
        home_page.click_products()
        
        products_page = ProductsPage(driver)
        products_page.add_first_product_to_cart()
        products_page.click_continue_shopping()
        
        # Go to cart and remove
        home_page.click_cart()
        cart_page = CartPage(driver)
        
        initial_count = cart_page.get_cart_item_count()
        cart_page.remove_first_item()
        time.sleep(1)
        final_count = cart_page.get_cart_item_count()
        
        assert final_count == initial_count - 1, "Item not removed"
        logger.info("✅ Remove item test passed!")