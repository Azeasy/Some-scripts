"""
Simple template for the python-telegram-bot
"""

from telegram.ext import (
    Updater,
    CommandHandler,
)
from telegram.ext.dispatcher import run_async

import logging

# Dubugging logic
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot token from Botfather
BOT_TOKEN = ""


# Start function with markdown and built-in async logic
@run_async
def start(bot, update):
    text = "`Hello, World!`"
    bot.send_message(chat_id=update.message.chat_id,
                     text=text,
                     parse_mode="Markdown")


def main():
    updater = Updater(BOT_TOKEN)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
