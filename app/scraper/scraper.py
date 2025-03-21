import logging
from selenium_helper import SeleniumHelper
from abc import ABC, abstractmethod

logger = logging.getLogger("scraper")

class Scraper(ABC):
    """scraper parent class"""

    def __init__(self, base_url, headless=True):
        self.base_url = base_url
        self.selenium = SeleniumHelper(headless=headless)

    @abstractmethod
    def parse_element(self, element):
        """abstract method for child class implementation"""
        pass

    def scrape(self, url, item_selector, next_button_selector, max_pages=3):
        pass

    def close(self):
        """close webDriver"""
        self.selenium.close()
