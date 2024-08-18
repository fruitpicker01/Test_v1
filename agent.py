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

def generate_response(messages):
    # Отправляем запрос к модели GigaChat и получаем ответ
    response = model.invoke(messages)
    return response.content

# Создаем агента с моделью GigaChat-Pro
graph = create_react_agent(model, tools=[])

# Определяем, как агент будет обрабатывать сообщения
def handle_messages(state):
    messages = [
        SystemMessage(content="Ты помощник AI, который помогает пользователям."),
        HumanMessage(content="Какая сегодня погода?")
    ]
    response_content = generate_response(messages)
    return {"messages": [response_content]}

# Добавляем узел и ребро к графу
graph.add_node("handle_messages", handle_messages)
graph.add_edge("start", "handle_messages")

# Компилируем граф
compiled_graph = graph.compile()
