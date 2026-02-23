from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

DATABASE_URL = "postgresql://admin:admin@localhost:5435/ainews"

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class NewsEntry(Base):
    __tablename__ = "news_analysis"

    id = Column(Integer, primary_key=True, index=True)
    original_text = Column(String)
    summary = Column(String)
    sentiment = Column(String)
    tags = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)