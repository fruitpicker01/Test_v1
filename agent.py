import openai
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

# Загрузка ключа API из переменной окружения
openai.api_key = os.getenv('GPT_KEY')

# Настройка модели GPT-4o
def run_agent():
    model = ChatOpenAI(model="gpt-4o")
    prompt = "Привет! Как я могу помочь?"
    response = model([HumanMessage(content=prompt)])
    print(response[0].content)

if __name__ == "__main__":
    run_agent()