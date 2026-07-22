import pytest
import time
from pages.home_page import HomePage
from pages.products_page import ProductsPage
from test_data.config import TestData

class TestProducts:
    
    @pytest.mark.smoke
    def test_search_existing_product(self, driver, logger):
        """Test searching for an existing product"""
        logger.info("Starting existing product search test")
        
        home_page = HomePage(driver)
        home_page.open()
        home_page.click_products()
        
        products_page = ProductsPage(driver)
        products_page.search_product(TestData.SEARCH_TERMS["existing"])
        
        # Verify products found
        product_names = products_page.get_product_names()
        assert len(product_names) > 0, "No products found"
        logger.info(f"Found {len(product_names)} products")
        logger.info("✅ Existing product search test passed!")
    
    @pytest.mark.regression
    def test_search_non_existing_product(self, driver, logger):
        """Test searching for a non-existing product"""
        logger.info("Starting non-existing product search test")
        
        home_page = HomePage(driver)
        home_page.open()
        home_page.click_products()
        
        products_page = ProductsPage(driver)
        products_page.search_product(TestData.SEARCH_TERMS["non_existing"])
        
        # Verify no products found
        product_names = products_page.get_product_names()
        assert len(product_names) == 0, "Products found for non-existing search"
        logger.info("✅ Non-existing product search test passed!")