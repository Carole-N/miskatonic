from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dto.config import SQLITE_DB

engine = create_engine(SQLITE_DB, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db_sqlite():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()