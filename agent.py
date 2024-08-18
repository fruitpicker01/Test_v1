from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

# Используем модель GPT-4o
model = ChatOpenAI(model="gpt-4o", temperature=0)

# Оставляем пустой список инструментов, так как Tavily убрали
tools = []

# Создаем агент с моделью GPT-4o и без инструментов
graph = create_react_agent(model, tools)
