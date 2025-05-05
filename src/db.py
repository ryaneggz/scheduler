from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Database setup
DATABASE_URL = "postgresql+psycopg2://admin:test1234@localhost:5432/apscheduler"
engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
