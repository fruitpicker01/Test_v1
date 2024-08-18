from langchain_community.chat_models.gigachat import GigaChat
from langgraph.prebuilt import create_react_agent

# Setup the GigaChat model
model = GigaChat(
    credentials="ZDRkMGFhNmQtN2NjYS00NDMxLWIxNTAtZTc5NDJhZmM1NThiOjYyODE4MWJmLTM5ZjAtNGI4MC05NWU3LWFhYWY4NjRlYmU0YQ==",
    scope="GIGACHAT_API_PERS",
    model="GigaChat-Pro",
    verify_ssl_certs=False,
    streaming=True,
)

# Define an empty agent graph for now
graph = create_react_agent(model, tools=[])
