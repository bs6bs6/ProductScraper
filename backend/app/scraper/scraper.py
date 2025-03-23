import logging
from .selenium_helper import SeleniumHelper
from abc import ABC, abstractmethod
from typing import Any

logger = logging.getLogger("scraper")

class Scraper(ABC):
    """Scraper parent class"""

    def __init__(self, base_url: str, headless: bool = True):
        self.base_url = base_url
        self.selenium = SeleniumHelper(headless=headless)

    @abstractmethod
    def parse_element(self, element: Any) -> Any:
        """Abstract method for child class implementation"""
        pass
    
    @abstractmethod
    def scrape(self, max_pages: int = 3) -> None:
        """Scrape method to be implemented by child classes"""
        pass

    def close(self) -> None:
        """Close WebDriver"""
        self.selenium.close()
