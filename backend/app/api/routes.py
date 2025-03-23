from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from db.database import get_db, paginate
from services.scraper_service import ScraperService
from models import Product
from typing import Optional, List

router = APIRouter(prefix="/data")

@router.get("/")
def get_all_data(
    page: int = Query(1, gt=0),
    page_size: int = Query(10, gt=0, le=100),
    brands: Optional[List[str]] = Query(None),
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_rating: Optional[float] = None,
    max_rating: Optional[float] = None,
    db: Session = Depends(get_db)
):
    query = select(Product)

    if brands:
        query = query.where(Product.brand.in_(brands))
    if min_price is not None:
        query = query.where(Product.price >= min_price)
    if max_price is not None:
        query = query.where(Product.price <= max_price)
    if min_rating is not None:
        query = query.where(Product.rating >= min_rating)
    if max_rating is not None:
        query = query.where(Product.rating <= max_rating)

    query = query.order_by(Product.scrape_timestamp.desc())
    return paginate(query, page, page_size, db)

@router.get("/brands", response_model=List[str])
def get_available_brands(db: Session = Depends(get_db)):
    brands = db.exec(select(Product.brand).distinct()).all()
    return sorted(set(brands))


@router.delete("/{id}")
def delete_entry(id: int, db: Session = Depends(get_db)):
    product = db.get(Product, id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}

@router.post("/scrape")
def run_scraper(max_pages: int = Query(3, gt=0)):
    scraper = ScraperService()
    scraper.run_scraper(max_pages=max_pages)
    return {"message": f"Scraped {max_pages} pages successfully"}