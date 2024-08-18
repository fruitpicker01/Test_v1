from langchain_community.chat_models import GigaChat

model = GigaChat(verify_ssl_certs=False, scope="GIGACHAT_API_PERS")

tools = []  # Список инструментов, если нужно

graph = create_react_agent(model, tools)
