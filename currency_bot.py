"""
https://www.nbrb.by/apihelp/exrates
"""
import requests
import telebot

TOKEN = "8553429622:AAFJGxgMx6g0Ku_5LVhC8BPY7Uo-zfJjv3E"

class TelegramBot:
    def __init__(self):
        self.bot = telebot.TeleBot(TOKEN)
        self.api = NBRBClient()
        self.current = ""

    def create_keyboard(self):
        self.keyboard = telebot.types.ReplyKeyboardMarkup(True)
        self.keyboard.add("USD", "EUR")

    def runbot(self):
        self.create_keyboard()
        self.commands()
        self.bot.polling()

    def commands(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            self.bot.send_message(message.chat.id, "Добро пожаловать\n"
                                                   "Текущие курсы валют\n"
                                                   f"USD: {self.api.get_value(1,"USD")}\n"
                                                   f"EUR: {self.api.get_value(1,"EUR")}\n"
                                                   f"Выберите валюту", reply_markup=self.keyboard)
            self.bot.register_next_step_handler(message, enter_currency)

        def enter_currency(message):
            self.bot.send_message(message.chat.id, f"Вы выбрали {message.text}\nВведите сумму")
            self.current = message.text
            self.bot.register_next_step_handler(message, enter_sum)

        def enter_sum(message):
            self.bot.send_message(message.chat.id, f"{message.text} {self.current} в BYN = "
                                                   f"{self.api.get_value(float(message.text),self.current)}\n")



class NBRBClient:
    def __init__(self):
        self.usd_url = "https://api.nbrb.by/exrates/rates/USD?parammode=2"
        self.eur_url = "https://api.nbrb.by/exrates/rates/EUR?parammode=2"

    def get_value(self, rub, currency):
        if currency == 'USD':
            currency_url = self.usd_url
        elif currency == 'EUR':
            currency_url = self.eur_url
        else:
            raise Exception('Currency must be USD or EUR')

        r = requests.get(currency_url)
        data = r.json()
        return data["Cur_OfficialRate"] * rub

if __name__ == '__main__':
    bot = TelegramBot()
    bot.runbot()