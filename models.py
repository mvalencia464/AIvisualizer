from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class Generation(Base):
    __tablename__ = 'generations'

    id = Column(Integer, primary_key=True)
    prompt = Column(String)
    image_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

# Connect to your PostgreSQL database
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
