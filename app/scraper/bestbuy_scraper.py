import logging
import re
from .scraper import Scraper
from datetime import datetime
from typing import List, Dict

logger = logging.getLogger("bestbuy - scraper")

class BestBuyScraper(Scraper):

    BASE_URL: str = "https://www.bestbuy.ca/en-ca/category/gaming-laptops/36712"
    NEXT_BUTTON_SELECTOR: str = "button[aria-label='Show more products']"
    ITEM_SELECTOR: str = "//li[contains(@class, 'productLine') and contains(@class, 'x-productListItem')]"
    PRODUCT_NAME_SELECTOR: str = "[data-automation='productItemName']"
    PRODUCT_PRICE_SELECTOR: str = "[data-automation='product-price']"
    RATING_SELECTOR: str = "meta[itemprop='ratingValue']"
    SPONSORED_LABEL_SELECTOR: str = "[data-automation='sponsoredProductLabel']"
    IMAGE_SELECTOR: str = "img"
    SPONSORED_LINK_SELECTOR: str = "a[class^='styles-module_link']"
    PRODUCT_URL_SELECTOR: str = "[itemprop='url']"
    ONETRUST_BANNER_ID: str = "onetrust-banner-sdk"
    ONETRUST_CLOSE_BUTTON_SELECTOR: str = "button.onetrust-close-btn-handler"
    LANDMARK_PRODUCT_LISTING_ID: str = "landmark-product-listing"

    def __init__(self, headless: bool = True):
        super().__init__(self.BASE_URL, headless=headless)

    def parse_element(self, element) -> Dict[str, str]:
        title: str = self.selenium.extract_text(element, self.PRODUCT_NAME_SELECTOR)
        price: str = self.selenium.extract_text(element, self.PRODUCT_PRICE_SELECTOR)
        price = re.findall(r"\$?([\d,]+\.\d{2})", price)[0].replace(",", "")
        rating: str = self.selenium.extract_attribute(element, self.RATING_SELECTOR, "content")
        sponsor: str = self.selenium.extract_text(element, self.SPONSORED_LABEL_SELECTOR)
        img: str = self.selenium.extract_attribute_till_loaded(element, self.IMAGE_SELECTOR, "src")
        if sponsor:
            url: str = self.selenium.extract_attribute(element, self.SPONSORED_LINK_SELECTOR, "href")
            url = self.selenium.resolve_and_get_current_url(url)
            id = self.resolve_id_from_url(url)
        else:
            url: str = self.selenium.extract_attribute(element, self.PRODUCT_URL_SELECTOR, "href")
            id = self.resolve_id_from_url(url)
        if title.startswith("Open Box"):
            brand: str = title.split(" ")[3]
        else:
            brand: str = title.split(" ")[0]

        return {
            "id": id,
            "title": title,
            "price": price,
            "rating": rating,
            "url": url,
            "brand": brand,
            "img": img,
            "scrape_timestamp": datetime.now().isoformat()
        }
    
    def resolve_id_from_url(self, url: str) -> str:
        match = re.search(r'/(\d+)(?:\?|$)', url)
        return match.group(1) if match else None

    def scrape(self, url: str, max_pages: int = 3) -> List[Dict[str, str]]:
        all_items: List[Dict[str, str]] = []
        current_page: int = 0

        self.selenium.navigate_to(url)
        self.selenium.wait_for_element_by_id(self.LANDMARK_PRODUCT_LISTING_ID)

        one_trust_banner = self.selenium.get_element_by_id(self.ONETRUST_BANNER_ID)

        if one_trust_banner:
            close_button = self.selenium.get_element(self.ONETRUST_CLOSE_BUTTON_SELECTOR)
            if close_button:
                close_button.click()
            logger.info("One trust banner accepted")

        while current_page < max_pages:
            logger.info(f"Scraping page {current_page + 1}")

            current_items = self.selenium.get_elements_by_X_Path(self.ITEM_SELECTOR)

            for element in current_items[len(all_items):]:  # Only process new items
                item_data = self.parse_element(element)
                if item_data:
                    all_items.append(item_data)

            if not self.selenium.navigate_to_next_page(self.NEXT_BUTTON_SELECTOR, self.ITEM_SELECTOR):
                break

            current_page += 1

        logger.info(f"Scraped {len(all_items)} items from {current_page} pages")

        return all_items