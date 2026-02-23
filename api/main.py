import logging
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import List
from core.database import SessionLocal, NewsEntry, init_db
from core.llm_engine import analyze_news

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ainewsgigachat API",
    description="Система анализа новостей через GigaChat и Kafka",
    version="1.0.0"
)

class NewsRequest(BaseModel):
    text: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def on_startup():
    init_db()
    logger.info("API запущено, таблицы в БД проверены")


@app.post("/analyze", response_model=None)
def process_news(request: NewsRequest, db: Session = Depends(get_db)):
    try:
        analysis = analyze_news(request.text)

        new_entry = NewsEntry(
            original_text=request.text,
            summary=analysis.summary,
            sentiment=analysis.sentiment,
            tags=analysis.tags
        )
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
        return new_entry
    except Exception as e:
        logger.error(f"Ошибка при ручном анализе: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/history")
def get_history(db: Session = Depends(get_db)):
    return db.query(NewsEntry).order_by(NewsEntry.id.desc()).all()


@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    total = db.query(NewsEntry).count()

    sentiment_counts = (
        db.query(NewsEntry.sentiment, func.count(NewsEntry.id))
        .group_by(NewsEntry.sentiment)
        .all()
    )

    return {
        "total_processed": total,
        "sentiment_breakdown": {s: count for s, count in sentiment_counts},
        "system_status": "Online",
        "database": "Connected"
    }