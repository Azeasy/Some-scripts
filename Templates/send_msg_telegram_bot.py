# Very simple script that just sends a message to the chosen chat

# requirements:
# pip install python-telegram-bot

from telegram import Bot


def send(token, chat_id, text='Я сломался((('):
    tg_bot = Bot(token)

    tg_bot.send_message(chat_id=chat_id,
                        text=text,
                        )
