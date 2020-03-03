from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import json
import logging
from collections import defaultdict
from commands import CalcCommand, CityGameCommand, PlanetCommand


logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename="bot.log"
)

with open("cities_list.txt", "r", encoding="utf-8") as f:
    CITIES_OF_RUSSIA = set([line.rstrip("\n") for line in f])

user_sessions = defaultdict(lambda : CityGameCommand(cities=CITIES_OF_RUSSIA))
commands = {}


def greet_user(bot, update):
    text = "Вызван /start"
    logging.info(text)
    update.message.reply_text(text)


def talk_to_me(bot, update):
    user_text = f"Привет! {update.message.chat.first_name}! Ты написал: {update.message.text}"
    logging.info(
        "User: %s, Chat_id: %s, Message: %s",
        update.message.chat.username,
        update.message.chat.id,
        update.message.text
    )
    update.message.reply_text(user_text)


def calc_command(bot, update):
    expression = update.message.text[update.message.text.find(" ") + 1:]
    logging.info("Вызвана команда /calc, выражение - %s", expression)
    cmd = commands["calc"]
    answer = cmd.run(expression)
    update.message.reply_text(answer)


def city_command(bot, update):
    city = update.message.text[update.message.text.find(" ") + 1:]
    logging.info("Вызвана команда /city, город - %s", city)
    user_id = update.message.from_user["id"]
    cmd = user_sessions[user_id]
    # если уже была игра и она закончилась, то обновляем список городов
    if cmd.game_over:
        cmd = CityGameCommand(cities=CITIES_OF_RUSSIA)
        user_sessions[user_id] = cmd
    answer = cmd.run(city)
    update.message.reply_text(answer)


def planet_command(bot, update):
    planet_name = update.message.text.split()[1]
    logging.info("Вызвана команда /planet, планета - %s", planet_name)
    cmd = commands["planet"]
    answer = cmd.run(planet_name)
    update.message.reply_text(answer)


def main():
    with open("settings.json") as settings_file:
        settings = json.load(settings_file)
    key = settings["KEY"]
    proxy_settings = settings["PROXY"]
    logging.info("Бот запускается")
    bot = Updater(key, request_kwargs=proxy_settings)

    commands["planet"] = PlanetCommand()
    commands["calc"] = CalcCommand()

    dp = bot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", planet_command))
    dp.add_handler(CommandHandler("calc", calc_command))
    dp.add_handler(CommandHandler("city", city_command))

    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    bot.start_polling()
    bot.idle()


if __name__ == "__main__":
    main()
