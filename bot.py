from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import json
import logging

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s"
    level=logging.INFO,
    filename="bot.log"
)

def greet_user(bot, update):
    text = "Вызван /start"
    logging.info(text)
    update.message.reply_text(text)

def talk_to_me(bot, update):
    user_text = f"Привет! {update.message.chat.first_name}! Ты написал: {update.message.text}"
    logging.info("User: %s, Chat_id: %s, Message: %s", 
                  update.message.chat.username, 
                  update.message.chat.id, 
                  update.message.text)
    update.message.reply_text(user_text)

def main():
    settings = json.loads(open("settings.json").read())
    key = settings["KEY"]
    proxy_settings = settings["PROXY"]
    logging.info("Бот запускается")
    bot = Updater(key, request_kwargs=proxy_settings)

    dp = bot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    bot.start_polling()
    bot.idle()

if __name__ == "__main__":
    main()
