import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import logging
import os
from datetime import datetime

# Suppress logs
logging.getLogger("selenium").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("webdriver_manager").setLevel(logging.WARNING)
logging.getLogger("WDM").setLevel(logging.WARNING)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

@pytest.fixture(scope="function")
def driver():
    """Set up and tear down WebDriver"""
    
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--log-level=3")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    
    service = Service(ChromeDriverManager().install())
    service.creationflags = 0
    
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)
    
    # REMOVED: driver.maximize_window()
    # Using --window-size=1920,1080 instead
    
    yield driver
    driver.quit()

@pytest.fixture
def logger():
    return logging.getLogger(__name__)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        if "driver" in item.fixturenames:
            driver = item.funcargs["driver"]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_dir = "screenshots/failures"
            os.makedirs(screenshot_dir, exist_ok=True)
            filename = f"{screenshot_dir}/{item.name}_{timestamp}.png"
            driver.save_screenshot(filename)
            print(f"\n📸 Screenshot saved: {filename}")

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    print("\n" + "="*60)
    print("📊 TEST EXECUTION SUMMARY")
    print("="*60)
    
    passed = len(terminalreporter.stats.get('passed', []))
    failed = len(terminalreporter.stats.get('failed', []))
    skipped = len(terminalreporter.stats.get('skipped', []))
    errors = len(terminalreporter.stats.get('error', []))
    total = passed + failed + skipped + errors
    
    print(f"✅ Passed:  {passed}")
    print(f"❌ Failed:  {failed}")
    print(f"⏭️  Skipped: {skipped}")
    print(f"⚠️  Errors:  {errors}")
    print(f"📝 Total:   {total}")
    print("="*60)
    
    if failed > 0 or errors > 0:
        print("🔴 Some tests failed! Check the screenshots in 'screenshots/failures/'")
    else:
        print("🟢 All tests passed!")
    print("="*60)