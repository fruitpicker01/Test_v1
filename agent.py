from langchain.chat_models import ChatOpenAI
from langgraph.prebuilt import create_react_agent

# Загрузка ключа API из переменной окружения
import os
openai_api_key = os.getenv('OPENAI_API_KEY')

# Настройка модели GPT-4o
model = ChatOpenAI(openai_api_key=openai_api_key, model="gpt-4o")

# Создание простого агента с использованием prebuilt функции
graph = create_react_agent(model)

if __name__ == "__main__":
    print("Граф агента успешно создан.")
