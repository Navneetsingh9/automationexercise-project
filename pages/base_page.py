from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import logging
import time

class BasePage:
    """Base class with common methods for all page objects"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.logger = logging.getLogger(__name__)
    
    def click_element(self, locator, retries=2):
        """Click on an element with retry and ad handling"""
        for attempt in range(retries):
            try:
                # Scroll to element first
                element = self.wait.until(EC.presence_of_element_located(locator))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                time.sleep(0.5)
                
                # Try JavaScript click (bypasses ads)
                try:
                    self.driver.execute_script("arguments[0].click();", element)
                    self.logger.info(f"Clicked element using JavaScript: {locator}")
                    return True
                except Exception as e:
                    self.logger.warning(f"JavaScript click failed: {e}")
                
                # If JavaScript click fails, try regular click
                self.wait.until(EC.element_to_be_clickable(locator)).click()
                self.logger.info(f"Clicked element: {locator}")
                return True
                
            except ElementClickInterceptedException as e:
                self.logger.warning(f"Click intercepted (attempt {attempt+1}): {e}")
                # Try to close any ad overlays
                self.close_ads()
                time.sleep(1)
                
            except Exception as e:
                if attempt == retries - 1:
                    self.logger.error(f"Failed to click element: {locator}, Error: {e}")
                    raise
                self.logger.warning(f"Retry {attempt+1} for element: {locator}")
                time.sleep(1)
        
        return False
    
    def close_ads(self):
        """Try to close any ad overlays"""
        try:
            # Try to close iframe ads
            iframes = self.driver.find_elements("tag name", "iframe")
            for iframe in iframes:
                try:
                    self.driver.execute_script("arguments[0].style.display='none';", iframe)
                    self.logger.info("Closed iframe ad")
                except:
                    pass
            
            # Try to close any close buttons
            close_selectors = [
                "//div[@class='ad-close']",
                "//span[contains(@class,'close')]",
                "//a[contains(@class,'close')]",
                "//div[@id='dismiss-button']"
            ]
            for selector in close_selectors:
                try:
                    close_btn = self.driver.find_element("xpath", selector)
                    self.driver.execute_script("arguments[0].click();", close_btn)
                    self.logger.info("Closed ad overlay")
                except:
                    pass
        except Exception as e:
            self.logger.warning(f"Failed to close ads: {e}")
    
    def enter_text(self, locator, text):
        """Enter text into an input field"""
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            element.clear()
            element.send_keys(text)
            self.logger.info(f"Entered text: {text}")
        except TimeoutException:
            self.logger.error(f"Element not found: {locator}")
            raise
    
    def get_text(self, locator):
        """Get text from an element"""
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            return element.text
        except TimeoutException:
            self.logger.error(f"Element not found: {locator}")
            return None
    
    def is_element_visible(self, locator):
        """Check if element is visible"""
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def scroll_to_element(self, locator):
        """Scroll to an element"""
        element = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        self.logger.info("Scrolled to element")
    
    def take_screenshot(self, name="screenshot"):
        """Take a screenshot"""
        self.driver.save_screenshot(f"screenshots/{name}.png")
        self.logger.info(f"Screenshot saved: {name}.png")