from langchain.chat_models.gigachat import GigaChat
from langgraph.prebuilt import create_react_agent

# Используем модель GigaChat-Pro с соответствующими ключами
model = GigaChat(credentials="GIGACHAT_CREDENTIALS", model="GigaChat-Pro", verify_ssl_certs=False)

# Пока оставляем инструменты пустыми
tools = []

# Создаем агента с моделью GigaChat-Pro и без инструментов
graph = create_react_agent(model, tools)
