from langchain_community.chat_models.gigachat import GigaChat
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Sequence
import operator
import json
from langchain_core.messages import BaseMessage, FunctionMessage, SystemMessage, HumanMessage

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]

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
    if "function_call" not in last_message.additional_kwargs:
        return "end"
    else:
        return "continue"

# Определение функции вызова модели
def call_model(state):
    messages = state['messages']
    response = model.invoke(messages)
    return {"messages": [response]}

# Создание графа работы агента
workflow = StateGraph(AgentState)

# Добавляем системное сообщение для направления работы агента
def handle_product(state):
    system_message = SystemMessage(content="Ты являешься маркетологом. Твоя задача - создать рекламное SMS-сообщение на основе введенной информации о продукте.")
    state['messages'].append(system_message)
    return call_model(state)

# Добавляем узлы в граф
workflow.add_node("customer_agent", handle_product)
workflow.set_entry_point("customer_agent")

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
