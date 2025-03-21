import logging
from scraper import Scraper
from datetime import datetime

logger = logging.getLogger("bestbuy - scraper")

class BestBuyScraper(Scraper):
    """bestbuy scraper class"""

    def __init__(self, headless=True):
        super().__init__("https://www.bestbuy.ca/en-ca/category/gaming-laptops/36712", headless=headless)
        self.next_button_selector = "button[aria-label='Show more products']"
        self.item_selector = "//li[contains(@class, 'productLine') and contains(@class, 'x-productListItem')]"

    def parse_element(self, element):
        """parse element"""
        title = self.selenium.extract_text(element, "[data-automation='productItemName']")
        price = self.selenium.extract_text(element, "[data-automation='product-price']")

        return {
            "title": title,
            "price": price,
            "scrape_timestamp": datetime.now().isoformat()
        }
    
    def scrape(self, url, item_selector, next_button_selector, max_pages=3):
        all_items = []
        current_page = 0

        self.selenium.navigate_to(url)
        self.selenium.wait_for_element_by_id("landmark-product-listing")

        one_trust_banner = self.selenium.get_element_by_id("onetrust-banner-sdk")

        if(one_trust_banner):
            close_button = self.selenium.get_element("button.onetrust-close-btn-handler")
            if close_button:
                close_button.click()
            logger.info("One trust banner accepted")

        while current_page < max_pages:
            logger.info(f"Scraping page {current_page + 1}")

            current_items = self.selenium.get_elements_by_X_Path(item_selector)

            for element in current_items[len(all_items):]:  # Only process new items
                item_data = self.parse_element(element)
                if item_data:
                    all_items.append(item_data)

            if not self.selenium.navigate_to_next_page(next_button_selector, item_selector):
                break

            # TODO Wait for new items to be loaded

            current_page += 1

        logger.info(f"Scraped {len(all_items)} items from {current_page} pages")

        return all_items
    
if __name__ == "__main__":
    scraper = BestBuyScraper(headless=False)
    jobs = scraper.scrape(
        "https://www.bestbuy.ca/en-ca/category/gaming-laptops/36712/",
        scraper.item_selector,
        scraper.next_button_selector,
    )
    scraper.close()
    print(jobs)