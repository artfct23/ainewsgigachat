import logging
import asyncio
import json
from aiokafka import AIOKafkaConsumer
from core.llm_engine import analyze_news
from core.database import SessionLocal, NewsEntry, init_db

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def consume():
    consumer = AIOKafkaConsumer(
        'raw_news',
        bootstrap_servers='localhost:9092',
        group_id="news_group"
    )
    await consumer.start()
    init_db()
    logger.info("Воркер запущен и готов к работе с Kafka")

    try:
        async for msg in consumer:
            news_text = msg.value.decode('utf-8')
            logger.info(f"Получена новость: {news_text[:50]}...")

            try:
                analysis = analyze_news(news_text)

                with SessionLocal() as db:
                    new_entry = NewsEntry(
                        original_text=news_text,
                        summary=analysis.summary,
                        sentiment=analysis.sentiment,
                        tags=analysis.tags
                    )
                    db.add(new_entry)
                    db.commit()
                logger.info("Успешно проанализировано и сохранено в БД")
            except Exception as e:
                logger.error(f"Ошибка при обработке новости: {e}")

    finally:
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(consume())