"""Test data configuration for Automation Exercise"""

class TestData:
    """Test data for Automation Exercise website"""
    
    BASE_URL = "https://www.automationexercise.com/"
    
    # Test user credentials (for existing user)
    VALID_EMAIL = "testuser123@example.com"
    VALID_PASSWORD = "TestPass123"
    
    # New user registration data
    REGISTRATION = {
        "first_name": "John",
        "last_name": "Doe",
        "company": "Test Company",
        "address": "123 Main Street",
        "country": "United States",
        "state": "California",
        "city": "Los Angeles",
        "zipcode": "90210",
        "mobile": "1234567890",
        "password": "TestPass123"
    }
    
    # Product search terms
    SEARCH_TERMS = {
        "existing": "tshirt",
        "non_existing": "nonexistentproductxyz"
    }
    
    # Checkout data
    CHECKOUT = {
        "card_name": "John Doe",
        "card_number": "1234567890123456",
        "cvc": "123",
        "expiry_month": "12",
        "expiry_year": "2025"
    }