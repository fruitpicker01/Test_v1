from langchain_community.chat_models.gigachat import GigaChat
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]

# Подключение модели GigaChat
model = GigaChat(
    credentials="ZDRkMGFhNmQtN2NjYS00NDMxLWIxNTAtZTc5NDJhZmM1NThiOjYyODE4MWJmLTM5ZjAtNGI4MC05NWU3LWFhYWY4NjRlYmU0YQ==",
    scope="GIGACHAT_API_PERS",
    model="GigaChat-Pro",
    verify_ssl_certs=False,
    streaming=True, # Важно: включите потоковую передачу
)

# Определение логики продолжения работы агента
def should_continue(state):
    messages = state['messages']
    last_message = messages[-1]
    if "function_call" not in last_message.additional_kwargs:
        return "end"
    else:
        return "continue"

# Определение функции вызова модели (ИСПРАВЛЕНО)
def call_model(state):
    messages = state['messages']
    response = model.stream(messages)
    # Преобразуем генератор в список сообщений
    message_list = [message for message in response] 
    return {"messages": message_list}

# Добавляем системное сообщение для первого агента
def handle_product(state):
    system_message = SystemMessage(content="Ты являешься маркетологом. Твоя задача - создать рекламное SMS-сообщение на основе введенной информации о продукте.")
    state['messages'].append(system_message)
    return call_model(state)

# Добавляем системное сообщение для второго агента
def handle_customer(state):
    system_message = SystemMessage(content="Ты являешься специалистом по персонализации. На основе информации о клиенте ты должен адаптировать SMS-сообщение.")
    state['messages'].append(system_message)
    return call_model(state)

# Создание графа работы агентов
workflow = StateGraph(AgentState)

# Добавляем узлы в граф
workflow.add_node("product_agent", handle_product)
workflow.add_node("customer_agent", handle_customer)

# Задаем последовательность работы агентов
workflow.set_entry_point("product_agent")
workflow.add_edge("product_agent", "customer_agent")

# Задаем условное ребро для продолжения работы
workflow.add_conditional_edges(
    "customer_agent",
    should_continue,
    {
        "continue": "customer_agent",
        "end": END
    }
)

# Компиляция графа
app = workflow.compile()
