import telebot
import datetime
utc_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
TOKEN = '8342699333:AAGlyGv93PTolkOX-4klNqomo-nzUbRO0m4'

bot = telebot.TeleBot(TOKEN)

balance = 2500
history = []
operation = ('проверить баланс', 'Снять наличные', 'Пополнить баланс', 'История операций', 'Выйти')
PIN = '1234'
POK = False

kb = telebot.types.ReplyKeyboardMarkup(True)
kb.add(*operation)

@bot.message_handler(commands=['start']) # /start
def start(message):
    bot.send_message(message.chat.id, "Введите PIN")

@bot.message_handler(func = lambda message: message.text == 'проверить баланс')
def balance(message):
    if POK:
        bot.send_message(message.chat.id, f"Ваш баланс составляет {balance}")
        history.append(f'просмотр баланса, {balance}, {utc_now}')
    else:
        start(message)

@bot.message_handler(func=lambda message: True)
def enter(message):
    if PIN == message.text:
        global POK
        bot.send_message(message.chat.id, 'PIN принят')
        POK = True
    else:
        bot.send_message(message.chat.id, 'неверный PIN')

    bot.send_message(message.chat.id, 'Выберите нужную операцию', reply_markup=kb)

@bot.message_handler(func = lambda message: message.text == 'Снять наличные')
def withdrow(message):
    if POK:
        bot.send_message(message.chat.id, f"Введите сумму, которую хотите снять")
        history.append(f'просмотр баланса, {balance}, {utc_now}')
    else:
        start(message)

@bot.message_handler(func=lambda message: True)
def sum_withdrow(message):
    global balance
    sum = message.text
    if sum > balance:
        bot.send_message(message.chat.id,
                                 f'у вас недостаточно средств')
    else:
        bot.send_message(message.chat.id,
                                 f'Операция выполнена успешно')
    balance -= sum
    history.append(f'снятие наличных, {sum}, {utc_now}')

@bot.message_handler(func = lambda message: message.text == 'Пополнить баланс')
def insert(message):
    global balance
    bot.send_message(message.chat.id, f"Введите сумму, которую хотите пополнить")
    sum_1 = message.text
    balance += sum_1
    history.append(f'пополнение, {sum_1}, {utc_now}')

@bot.message_handler(func = lambda message: message.text == 'История операций')
def histor(message):
    bot.send_message(message.chat.id, f"история ваших платежей {history}")

@bot.message_handler(func = lambda message: message.text == 'Выйти')
def endend(message):
    bot.send_message(message.chat.id, "пока!")


bot.polling()
