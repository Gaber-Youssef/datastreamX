# src/infrastructure/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URI = "postgresql://user:password@localhost/mydb"
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
