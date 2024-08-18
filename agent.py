from typing import Literal, TypedDict
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage
from langchain_community.chat_models.gigachat import GigaChat
from langgraph.graph import StateGraph, END

# Устанавливаем модель GigaChat-Pro с правильными параметрами
model = GigaChat(
    credentials="ZDRkMGFhNmQtN2NjYS00NDMxLWIxNTAtZTc5NDJhZmM1NThiOjYyODE4MWJmLTM5ZjAtNGI4MC05NWU3LWFhYWY4NjRlYmU0YQ==",
    scope="GIGACHAT_API_PERS",
    model="GigaChat-Pro",
    verify_ssl_certs=False,
    streaming=True,  # Включение потоковой передачи данных
)

# Определение состояния агента
class AgentState(TypedDict):
    messages: list[BaseMessage]

# Функция для вызова модели
def call_model(state: AgentState) -> dict:
    messages = state["messages"]
    response = model.invoke(messages)
    return {"messages": [response]}

# Функция, определяющая продолжение работы
def should_continue(state: AgentState) -> Literal["agent", END]:
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:  # Если модель сделала вызов инструмента
        return "agent"  # Продолжаем выполнение
    return END  # Завершаем выполнение

# Создание графа состояния
workflow = StateGraph(AgentState)

# Добавляем узлы
workflow.add_node("agent", call_model)

# Устанавливаем начальную точку
workflow.set_entry_point("agent")

# Добавляем условный переход
workflow.add_conditional_edges("agent", should_continue)

# Компиляция графа
compiled_graph = workflow.compile()
