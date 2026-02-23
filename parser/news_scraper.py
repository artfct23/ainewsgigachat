from aiokafka import AIOKafkaProducer
import asyncio


async def send_to_kafka():
    producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')
    await producer.start()

    news_list = [
        "Сбер выпустил обновление GigaChat для разработчиков.",
        "Инвестиции в ИИ в России выросли в 2 раза за 2025 год."
    ]

    try:
        for news in news_list:
            print(f"Отправка в Kafka: {news[:40]}")
            await producer.send_and_wait("raw_news", news.encode('utf-8'))
    finally:
        await producer.stop()


if __name__ == "__main__":
    asyncio.run(send_to_kafka())