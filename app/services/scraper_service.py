import logging
from sqlmodel import Session, select
from typing import List, Dict
from app.models.product import Product
from scraper import BestBuyScraper
from db import engine

logger = logging.getLogger("scraper_service")

class ScraperService:
    def __init__(self):
        self.scraper = BestBuyScraper(headless=True)

    def run_scraper(self, max_pages: int = 3) -> None:
        try:
            logger.info("Starting scraping process...")
            
            # Run the scraper
            scraped_data = self.scraper.scrape(
                BestBuyScraper.BASE_URL,
                max_pages=max_pages
            )
            
            # Save to database
            self.save_to_database(scraped_data)
            
            logger.info(f"Scraping completed. Saved {len(scraped_data)} items")
        except Exception as e:
            logger.error(f"Error during scraping: {str(e)}")
            raise
        finally:
            self.scraper.close()

    def save_to_database(self, items: List[Dict[str, str]]) -> None:
        with Session(engine) as session:
            try:
                for item in items:
                    if not item.get('rating'):
                        item['rating'] = None

                    existing_product = session.exec(
                        select(Product).where(Product.id == item['id'])
                    ).first()

                    if existing_product:
                        for key, value in item.items():
                            setattr(existing_product, key, value)
                    else:
                        laptop = Product(**item)
                        session.add(laptop)

                session.commit()
                logger.info(f"Successfully saved {len(items)} items to database")
            except Exception as e:
                session.rollback()
                logger.error(f"Error saving to database: {str(e)}")
                raise
