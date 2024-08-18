from langchain.chat_models.gigachat import GigaChat
from langgraph.prebuilt import create_react_agent
from langchain.schema import SystemMessage, HumanMessage

# Используем модель GigaChat-Pro с авторизацией
model = GigaChat(credentials="GIGACHAT_CREDENTIALS", model="GigaChat-Pro", verify_ssl_certs=False)

# Создаем агента с моделью GigaChat-Pro
graph = create_react_agent(model, tools=[])

# Тестовая генерация текста
messages = [
    SystemMessage(content="Ты копирайтер."),
    HumanMessage(content="Напиши рекламный текст для нового продукта.")
]

response = model(messages)
print("Сгенерированный текст:", response.content)
