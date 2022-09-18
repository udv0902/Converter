import telebot
import requests
from bs4 import BeautifulSoup
import config

resp = requests.get("https://finance.rambler.ru/currencies/")
soup = BeautifulSoup(resp.text, "lxml")
res_eur = soup.find_all("div", class_="currency-block__marketplace-value")[4].text

resp = requests.get("https://finance.rambler.ru/currencies/")
soup = BeautifulSoup(resp.text, "lxml")
res_usd = soup.find("div", class_="currency-block__marketplace-value").text

bot = telebot.TeleBot(config.token)


@bot.message_handler(content_types=['text'])
def start(message):
	markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
	markup.row("EURO", "USD")
	# markup.row("USD")
	if message.text == "/start":
		msg = bot.send_message(message.chat.id, "Выберите валюту", reply_markup=markup)
		bot.register_next_step_handler(msg, currensy)


def currensy(message):
	if message.text == "EURO":
		msg = bot.send_message(message.chat.id, "Введите сумму в рублях")
		bot.register_next_step_handler(msg, euro)
	elif message.text == "USD":
		msg = bot.send_message(message.chat.id, "Введите сумму в рублях")
		bot.register_next_step_handler(msg, usd)
	else:
		msg = bot.send_message(message.chat.id, "Введите корректные данные")
		bot.register_next_step_handler(msg, currensy)


def euro(message):
	try:
		bot.send_message(message.chat.id, float(message.text) / float(res_eur))
	except ValueError:
		bot.send_message(message.chat.id, "Введите корректные данные")


def usd(message):
	try:
		bot.send_message(message.chat.id, float(message.text) / float(res_usd))
	except ValueError:
		bot.send_message(message.chat.id, "Введите корректные данные")


bot.polling(none_stop=True)
