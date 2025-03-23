from sqlmodel import SQLModel, create_engine, Session, select
from sqlalchemy import func
from settings import config
from typing import Any

engine = create_engine(
    config.DATABASE_URI,
    echo=config.DATABASE_ECHO
)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_db():
    with Session(engine) as session:
        yield session

def paginate(query: Any, page: int = 1, page_size: int = 10, session: Session = None) -> dict:
    total_query = select(func.count()).select_from(query.subquery())
    total = session.exec(total_query).one()
    items = session.exec(query.offset((page - 1) * page_size).limit(page_size)).all()
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": items
    }