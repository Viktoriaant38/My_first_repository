import telebot
import datetime

utc_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
TOKEN = '8342699333:AAGlyGv93PTolkOX-4klNqomo-nzUbRO0m4'

bot = telebot.TeleBot(TOKEN)

balance = 2500
history = []
operation = ('Проверить баланс', 'Снять наличные', 'Пополнить баланс', 'История операций', 'Выйти')

kb = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(*operation)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Выберите нужную операцию', reply_markup=kb)

@bot.message_handler(func=lambda message: message.text == 'Проверить баланс')
def check_balance(message):
    global balance
    bot.send_message(message.chat.id, f"Ваш баланс составляет {balance} BYN")
    history.append(f'Просмотр баланса: {balance}, {utc_now}')


@bot.message_handler(func=lambda message: message.text == 'Снять наличные')
def withdraw(message):
    bot.send_message(message.chat.id, "Введите сумму для снятия:")
    bot.register_next_step_handler(message, process_withdraw)

def process_withdraw(message):
    global balance
    try:
        amount = int(message.text)
        if amount <= balance:
            balance -= amount
            bot.send_message(message.chat.id, f"Вы сняли {amount} BYN. Остаток: {balance} BYN")
            history.append(f'Снятие: {amount}, {utc_now}')
        else:
            bot.send_message(message.chat.id, "Недостаточно средств")
            history.append(f'Неудачная попытка снятия: {amount}, {utc_now}')
    except ValueError:
        bot.send_message(message.chat.id, "Введите корректное число!")

@bot.message_handler(func=lambda message: message.text == 'Пополнить баланс')
def insert(message):
    bot.send_message(message.chat.id, "Введите сумму для пополнения:")
    bot.register_next_step_handler(message, process_insert)

def process_insert(message):
    global balance
    try:
        amount = int(message.text)
        balance += amount
        bot.send_message(message.chat.id, f" Баланс пополнен на {amount} BYN. Новый баланс: {balance} BYN")
        history.append(f'Пополнение: {amount}, {utc_now}')
    except ValueError:
        bot.send_message(message.chat.id, "Введите корректное число!")

@bot.message_handler(func=lambda message: message.text == 'История операций')
def show_history(message):
    if history:
        bot.send_message(message.chat.id, " История операций:\n" + "\n".join(history))
    else:
        bot.send_message(message.chat.id, "История пуста.")

@bot.message_handler(func=lambda message: message.text == 'Выйти')
def exit_bot(message):
    bot.send_message(message.chat.id, " Спасибо за использование банкомата!")

bot.polling()
