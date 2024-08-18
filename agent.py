from langchain_community.chat_models.gigachat import GigaChat
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Sequence, List
import operator
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]

# Подключение модели GigaChat
model = GigaChat(
    credentials="ZDRkMGFhNmQtN2NjYS00NDMxLWIxNTAtZTc5NDJhZmM1NThiOjYyODE4MWJmLTM5ZjAtNGI4MC05NWU3LWFhYWY4NjRlYmU0YQ==",
    scope="GIGACHAT_API_PERS",
    model="GigaChat-Pro",
    verify_ssl_certs=False,
    streaming=False,
)

# Определение логики продолжения работы агента
def should_continue(state):
    messages = state['messages']
    last_message = messages[-1]
    # Изменено условие завершения
    if isinstance(last_message, AIMessage) and last_message.content.strip():
        return "end"
    return "continue"

# Определение функции вызова модели
def call_model(state):
    messages = state['messages']
    response = model.invoke(messages)
    return {"messages": [AIMessage(content=response.content)]}

# Добавляем системное сообщение для первого агента
def handle_product(state):
    system_message = SystemMessage(content="Ты являешься маркетологом. Твоя задача - создать рекламное SMS-сообщение на основе введенной информации о продукте.")
    return {"messages": [system_message] + state['messages']}

# Добавляем системное сообщение для второго агента
def handle_customer(state):
    system_message = SystemMessage(content="Ты являешься специалистом по персонализации. На основе информации о клиенте ты должен адаптировать SMS-сообщение.")
    return {"messages": [system_message] + state['messages']}

# Создание графа работы агентов
workflow = StateGraph(AgentState)

# Добавляем узлы в граф
workflow.add_node("product_agent", handle_product)
workflow.add_node("customer_agent", handle_customer)
workflow.add_node("model", call_model)

# Задаем последовательность работы агентов
workflow.set_entry_point("product_agent")
workflow.add_edge("product_agent", "model")
workflow.add_edge("model", "customer_agent")
workflow.add_edge("customer_agent", "model")

# Задаем условное ребро для продолжения работы
workflow.add_conditional_edges(
    "model",
    should_continue,
    {
        "continue": "customer_agent",
        "end": END
    }
)

# Компиляция графа
app = workflow.compile()
