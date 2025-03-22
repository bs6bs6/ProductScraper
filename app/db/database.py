from sqlmodel import SQLModel, create_engine
from sqlalchemy import text
from settings import config

engine = create_engine(
    config.DATABASE_URI,
    echo=config.DATABASE_ECHO
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)