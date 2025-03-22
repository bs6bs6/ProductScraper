import logging
import time
from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from typing import List, Optional

logger = logging.getLogger("selenium_helper")

class SeleniumHelper:
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.driver = self.setup_driver()

    def setup_driver(self) -> Chrome:
        """Initialize and return a Selenium WebDriver."""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")

        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )

        driver = Chrome(options=chrome_options)
        logger.info("WebDriver initialized successfully")
        return driver
        
    def navigate_to(self, url: str) -> bool:
        """Navigate to a given URL."""
        try:
            self.driver.get(url)
            logger.info(f"Navigated to {url}")
        except Exception as e:
            logger.error(f"Failed to navigate to {url}: {str(e)}")
            return False
        return True
    
    def wait_for_element_by_id(self, selector: str, by: By = By.ID, timeout: int = 10) -> Optional[WebElement]:
        return self.wait_for_element(selector, by, timeout)
    
    def wait_for_element(self, selector: str, by: By = By.CSS_SELECTOR, timeout: int = 10) -> Optional[WebElement]:
        """Wait for an element to be present on the page."""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, selector))
            )
        except TimeoutException:
            logger.warning(f"Timeout waiting for element: {selector}")
            return None
    
    def wait_for_element_to_be_clickable(self, selector: str, by: By = By.CSS_SELECTOR, timeout: int = 10) -> Optional[WebElement]:
        """Wait until the element is visible, scroll it into view, and ensure it's clickable."""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, selector))
            )
            return element
        except TimeoutException:
            logger.error(f"Element not clickable: {selector}")
            return None
        
    def get_elements_by_X_Path(self, selector: str) -> List[WebElement]:
        return self.get_elements(selector, By.XPATH)
        
    def get_elements_by_id(self, selector: str) -> List[WebElement]:
        return self.get_elements(selector, By.ID)
    
    def get_elements(self, selector: str, by: By = By.CSS_SELECTOR) -> List[WebElement]:
        """Retrieve all elements matching a selector."""
        try:
            return self.driver.find_elements(by, selector)
        except NoSuchElementException:
            logger.warning(f"No elements found for selector: {selector}")
            return []
        
    def get_element_by_id(self, selector: str) -> Optional[WebElement]:
        return self.get_element(selector, By.ID)
        
    def get_element(self, selector: str, by: By = By.CSS_SELECTOR) -> Optional[WebElement]:
        """Retrieve the first element matching a selector."""
        try:
            return self.driver.find_element(by, selector)
        except NoSuchElementException:
            logger.warning(f"No element found for selector: {selector}")
            return None

    def extract_text(self, element: WebElement, selector: str, by: By = By.CSS_SELECTOR) -> str:
        """Extract text from a child element."""
        try:
            return element.find_element(by, selector).text.strip()
        except (NoSuchElementException, StaleElementReferenceException):
            logger.warning(f"Could not extract text from {selector}")
            return ""

    def extract_attribute(self, element: WebElement, selector: str, attribute: str, by: By = By.CSS_SELECTOR) -> str:
        """Extract an attribute from a child element"""
        try:
            child_element = element.find_element(by, selector)
            s = child_element.get_attribute(attribute)
            return s
        except (NoSuchElementException, StaleElementReferenceException):
            logger.warning(f"Could not extract attribute {attribute} from {selector}")
            return ""

    def extract_attribute_till_loaded(self, element: WebElement, selector: str, attribute: str, by: By = By.CSS_SELECTOR) -> str:
        """Extract an attribute from a child element"""
        try:
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            WebDriverWait(element, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            child_element = element.find_element(by, selector)
            return child_element.get_attribute(attribute)
        except (NoSuchElementException, StaleElementReferenceException):
            logger.warning(f"Could not extract attribute {attribute} from {selector}")
            return
        
    def resolve_and_get_current_url(self, url: str, timeout: int = 5) -> str:
        """Open the URL in a new tab, wait for redirect to resolve, and return the final URL."""
        original_window = self.driver.current_window_handle

        self.driver.execute_script("window.open('');")
        WebDriverWait(self.driver, timeout).until(EC.number_of_windows_to_be(2))

        new_window = [w for w in self.driver.window_handles if w != original_window][0]
        self.driver.switch_to.window(new_window)

        self.driver.get(url)
        
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.current_url != url
            )
        except Exception as e:
            print("Timeout resolving link:", url)

        resolved_url = self.driver.current_url

        self.driver.close()
        self.driver.switch_to.window(original_window)

        return resolved_url
        
    def has_next_page(self, next_button_selector: str) -> bool:
        """Check if a next page button is available"""
        try:
            next_button = self.driver.find_element(By.CSS_SELECTOR, next_button_selector)
            return next_button.is_enabled() and next_button.is_displayed()
        except NoSuchElementException:
            return False

    def navigate_to_next_page(self, next_button_selector: str, content_selector: str, timeout: int = 10) -> bool:
        """Click the next page button and wait for new content to load."""
        try:
            current_elements = len(self.driver.find_elements(By.XPATH, content_selector))
            
            next_button = self.driver.find_element(By.CSS_SELECTOR, next_button_selector)
            self.wait_for_element_to_be_clickable(next_button_selector)
            
            self.driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            while True:
                is_in_viewport = self.driver.execute_script(
                    "var rect = arguments[0].getBoundingClientRect();"
                    "return (rect.top >= 0 && rect.bottom <= window.innerHeight);",
                    next_button
                )
                if is_in_viewport:
                    break
                time.sleep(0.5)

            next_button.click()

            WebDriverWait(self.driver, timeout).until(
                lambda driver: len(driver.find_elements(By.XPATH, content_selector)) > current_elements
            )

            logger.info(f"Successfully navigated to next page: {self.driver.current_url}")
            return True
        except (NoSuchElementException, TimeoutException) as e:
            logger.error(f"Failed to navigate to the next page: {str(e)}")
            return False
        
    def close(self) -> None:
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()
            logger.info("WebDriver closed")
