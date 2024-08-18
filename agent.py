from langchain.chat_models.gigachat import GigaChat

# Установите параметры для модели GigaChat-Pro
model = GigaChat(
    credentials="ZDRkMGFhNmQtN2NjYS00NDMxLWIxNTAtZTc5NDJhZmM1NThiOjYyODE4MWJmLTM5ZjAtNGI4MC05NWU3LWFhYWY4NjRlYmU0YQ==",
    scope="GIGACHAT_API_PERS",
    model="GigaChat-Pro",
    verify_ssl_certs=False,
    streaming=True,  # Включает потоковую передачу токенов
)

# Определяем сообщения, которые будут отправлены модели
messages = [
    {"role": "system", "content": "Ты ассистент AI, помогаешь пользователям."},
    {"role": "user", "content": "Расскажи мне про GigaChat."},
]

# Отправляем запрос к модели GigaChat
response = model(messages)

# Выводим ответ модели
print("Ответ от GigaChat:", response)
