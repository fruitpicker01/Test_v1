from langchain_community.chat_models.gigachat import GigaChat
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

# Отправляем запрос к модели GigaChat и получаем ответ
response = model.invoke(messages)

# Выводим ответ модели
print("Ответ от GigaChat:", response.content)
