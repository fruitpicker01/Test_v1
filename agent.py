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

# Агент для генерации рекламного сообщения о продукте
def handle_product(state):
    system_message = SystemMessage(content="Ты являешься маркетологом. Твоя задача - создать рекламное SMS-сообщение на основе введенной информации о продукте.")
    state['messages'].append(system_message)
    return call_model(state)

# Агент для генерации персонализированного сообщения на основе информации о клиенте
def handle_customer(state):
    system_message = SystemMessage(content="Ты маркетолог, создающий персонализированное рекламное SMS-сообщение на основе информации о клиенте.")
    state['messages'].append(system_message)
    return call_model(state)

# Создание графа для первого агента
product_workflow = StateGraph(AgentState)

# Добавляем узлы в граф первого агента
product_workflow.add_node("product_agent", handle_product)
product_workflow.set_entry_point("product_agent")

# Задаем условное ребро для продолжения работы первого агента
product_workflow.add_conditional_edges(
    "product_agent",
    should_continue,
    {
        "continue": "product_agent",
        "end": END
    }
)

# Компиляция графа первого агента
product_app = product_workflow.compile()

# Создание графа для второго агента
customer_workflow = StateGraph(AgentState)

# Добавляем узлы в граф второго агента
customer_workflow.add_node("customer_agent", handle_customer)
customer_workflow.set_entry_point("customer_agent")

# Задаем условное ребро для продолжения работы второго агента
customer_workflow.add_conditional_edges(
    "customer_agent",
    should_continue,
    {
        "continue": "customer_agent",
        "end": END
    }
)

# Компиляция графа второго агента
customer_app = customer_workflow.compile()
