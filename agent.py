from langchain_community.chat_models.gigachat import GigaChat
from langgraph.prebuilt import create_react_agent
from langchain.schema import SystemMessage, HumanMessage

# Устанавливаем модель GigaChat-Pro с правильными параметрами
model = GigaChat(
    credentials="ZDRkMGFhNmQtN2NjYS00NDMxLWIxNTAtZTc5NDJhZmM1NThiOjYyODE4MWJmLTM5ZjAtNGI4MC05NWU3LWFhYWY4NjRlYmU0YQ==",
    scope="GIGACHAT_API_PERS",
    model="GigaChat-Pro",
    verify_ssl_certs=False,
    streaming=True,  # Включение потоковой передачи данных
)

# Формируем правильный формат сообщений
messages = [
    SystemMessage(content="Ты помощник AI, который помогает пользователям."),
    HumanMessage(content="Какая сегодня погода?")
]

def handle_messages(state):
    # Отправляем запрос к модели GigaChat и получаем ответ
    response = model.invoke(messages)
    return {"messages": [response]}

# Создаем агента с моделью GigaChat-Pro
graph = create_react_agent(model, tools=[])

# Подключаем управление к графу до его компиляции
graph.add_node("handle_messages", handle_messages)
graph.add_edge("start", "handle_messages")

# Компилируем граф
compiled_graph = graph.compile()
