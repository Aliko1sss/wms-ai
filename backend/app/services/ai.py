from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import initialize_agent, AgentType
from app.config import get_settings
from app.services.ledger import get_stock_balance
from app.models.product import Product
from app.database import SessionLocal
import json

settings = get_settings()

@tool
def query_stock(sku: str) -> str:
    """Возвращает текущие остатки и ячейки для артикула"""
    db = SessionLocal()
    try:
        product = db.query(Product).filter(Product.sku == sku).first()
        if not product:
            return json.dumps({"error": "Товар не найден"})
        balance = get_stock_balance(db, product.id)
        return json.dumps({"sku": sku, "name": product.name, **balance})
    finally:
        db.close()

llm = ChatOpenAI(model=settings.AI_MODEL, api_key=settings.AI_API_KEY, temperature=0.1)
agent = initialize_agent(
    tools=[query_stock],
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    handle_parsing_errors=True,
    max_iterations=5
)

def process_ai_query(prompt: str, user_id: str) -> dict:
    system_prompt = (
        "Ты ИИ-помощник склада. Отвечай строго на русском. "
        "Используй только доступные инструменты. "
        "Если запрос требует изменения данных (переместить, списать, изменить), "
        "верни ответ с фразой 'Действие требует подтверждения'. "
        "Никогда не выдумывай данные."
    )
    try:
        response = agent.run(f"{system_prompt}\n\nЗапрос пользователя: {prompt}")
        needs_confirm = any(k in response.lower() for k in ["переместить", "списать", "изменить", "требует подтверждения"])
        return {"response": response, "requires_confirm": needs_confirm}
    except Exception as e:
        return {"response": "ИИ-сервис временно недоступен. Повторите запрос позже.", "requires_confirm": False}