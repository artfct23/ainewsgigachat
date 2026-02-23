import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_gigachat.chat_models import GigaChat

load_dotenv()


class NewsAnalysis(BaseModel):

    summary: str = Field(description="Краткое содержание новости в одном предложении")
    sentiment: str = Field(description="Тональность новости: Позитивная, Негативная или Нейтральная")
    tags: list[str] = Field(description="Список из 3-4 ключевых слов (тегов)")


def analyze_news(text: str):
    credentials = os.getenv("GIGACHAT_CREDENTIALS")

    if not credentials:
        raise ValueError("GIGACHAT_CREDENTIALS не найден!")

    llm = GigaChat(
        credentials=credentials,
        verify_ssl_certs=False,
        model="GigaChat"
    )

    structured_llm = llm.with_structured_output(NewsAnalysis)

    prompt = f"Проанализируй текст и заполни схему: {text}"
    result = structured_llm.invoke(prompt)
    return result


if __name__ == "__main__":
    test_text = "Сбер представил новую версию GigaChat, которая стала еще умнее в написании кода."
    analysis = analyze_news(test_text)
    print(analysis)