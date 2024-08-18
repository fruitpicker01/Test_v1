from langchain.chat_models.gigachat import GigaChat
from langgraph.prebuilt import create_react_agent

# Используем модель GigaChat-Pro с соответствующими ключами
model = GigaChat(credentials="ZDRkMGFhNmQtN2NjYS00NDMxLWIxNTAtZTc5NDJhZmM1NThiOjYyODE4MWJmLTM5ZjAtNGI4MC05NWU3LWFhYWY4NjRlYmU0YQ==", 
                 model="GigaChat-Pro", 
                 verify_ssl_certs=False)

# Пока оставляем инструменты пустыми
tools = []

# Создаем агента с моделью GigaChat-Pro и без инструментов
graph = create_react_agent(model, tools)
