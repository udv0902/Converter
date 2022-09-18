import telebot
import requests
from bs4 import BeautifulSoup
import config

resp = requests.get("https://finance.rambler.ru/currencies/")
soup = BeautifulSoup(resp.text, "lxml")
res_eur = soup.find_all("div", class_="currency-block__marketplace-value")[4].text
res_eur = float(res_eur)

resp = requests.get("https://finance.rambler.ru/currencies/")
soup = BeautifulSoup(resp.text, "lxml")
res_usd = soup.find_all("div", class_="currency-block__marketplace-value")[0].text
res_usd = float(res_usd)

bot = telebot.TeleBot(config.token)


@bot.message_handler(content_types=['text'])
def start(message):
	markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
	markup.row("EURO", "USD")
	# markup.row("USD")
	if message.text == "/start":
		msg = bot.send_message(message.chat.id, "Нажмите на кнопку нужной валюты", reply_markup=markup)
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
		markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
		markup.row("EURO", "USD")
		rub = float(message.text)
		evro = round((rub / res_eur), 4)
		bot.send_message(message.chat.id, evro)
		bot.send_message(message.chat.id, "Введите команду /start")
	except ValueError:
		bot.send_message(message.chat.id, "Введите корректные данные")


def usd(message):
	try:
		markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
		markup.row("EURO", "USD")
		rub = float(message.text)
		dollar = round((rub / res_usd), 4)
		bot.send_message(message.chat.id, dollar)
		bot.send_message(message.chat.id, "Введите команду /start")
	except ValueError:
		bot.send_message(message.chat.id, "Введите корректные данные")


bot.polling(none_stop=True)
