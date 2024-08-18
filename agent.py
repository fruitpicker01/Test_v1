from langchain_community.chat_models.gigachat import GigaChat
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Sequence
import operator
import json
from langchain_core.messages import BaseMessage, FunctionMessage, SystemMessage, HumanMessage

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]

model = GigaChat(
    credentials="ZDRkMGFhNmQtN2NjYS00NDMxLWIxNTAtZTc5NDJhZmM1NThiOjYyODE4MWJmLTM5ZjAtNGI4MC05NWU3LWFhYWY4NjRlYmU0YQ==",
    scope="GIGACHAT_API_PERS",
    model="GigaChat-Pro",
    verify_ssl_certs=False,
    streaming=False,
)

def should_continue(state):
    messages = state['messages']
    last_message = messages[-1]
    if "function_call" not in last_message.additional_kwargs:
        return "end"
    else:
        return "continue"

def call_model(state):
    messages = state['messages']
    response = model.invoke(messages)
    return {"messages": [response]}

def call_tool(state):
    messages = state['messages']
    last_message = messages[-1]
    action = ToolInvocation(
        tool=last_message.additional_kwargs["function_call"]["name"],
        tool_input=json.loads(last_message.additional_kwargs["function_call"]["arguments"]),
    )
    response = tool_executor.invoke(action)
    function_message = FunctionMessage(content=str(response), name=action.tool)
    return {"messages": [function_message]}

# Создаем первый граф для product_agent
product_workflow = StateGraph(AgentState)
product_workflow.add_node("product_agent", call_model)
product_workflow.set_entry_point("product_agent")
product_workflow.add_conditional_edges(
    "product_agent",
    should_continue,
    {
        "continue": "action",
        "end": END  # Используем зарезервированную вершину END
    }
)

# Создаем второй граф для customer_agent
customer_workflow = StateGraph(AgentState)
customer_workflow.add_node("customer_agent", handle_customer)
customer_workflow.set_entry_point("customer_agent")
customer_workflow.add_conditional_edges(
    "customer_agent",
    should_continue,
    {
        "continue": "action",
        "end": END  # Используем зарезервированную вершину END
    }
)

# Компилируем оба графа
product_app = product_workflow.compile()
customer_app = customer_workflow.compile()
