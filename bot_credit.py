import telebot

TOKEN = '8203130823:AAEiYN67oAegx2KrLzroGdMn1CahpZ0l6uM'
bot = telebot.TeleBot(TOKEN)

operation = ('платеж текущего периода', 'остаток по кредиту', 'срок окончания кредита', 'связь с оператором', 'кредитный калькулятор')

kb = telebot.types.ReplyKeyboardMarkup(True)
kb.add(*operation)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Приветсвуем вас в нашем банке. Выберите, пожалуйста, нужную вам операцию',
                     reply_markup=kb)

@bot.message_handler(func = lambda message: message.text == 'платеж текущего периода')
def oper_1(message):
    bot.send_message(message.chat.id, 'Платеж в текущем месяце составляет 350 белорусских рублей')

@bot.message_handler(func = lambda message: message.text == 'остаток по кредиту')
def oper_2(message):
    bot.send_message(message.chat.id, 'Ваш остаток по кредиту составляет 25250 белорусских рублей')

@bot.message_handler(func = lambda message: message.text == 'срок окончания кредита')
def oper_3(message):
    bot.send_message(message.chat.id, 'срок окончания кредита: 15.10.2035 год')

@bot.message_handler(func = lambda message: message.text == 'связь с оператором')
def oper_4(message):
    bot.send_message(message.chat.id, 'подождите минутку, с вами свяжется наш специалист')

@bot.message_handler(func = lambda message: message.text == 'кредитный калькулятор')
def oper_5(message):
    bot.send_message(message.chat.id, 'введите сумму кредита, срок кредита в месяцах, процентную ставку через пробел. Пример ввода: 1200 36 20')

@bot.message_handler(func=lambda message: True)
def calculator(message):
    sum, period, proc = map(int, message.text.split())

    a = (int(sum) * int(proc) )/100/12 #процент месячный
    b = sum/period #сумма по основному долгу в месяц
    c = a + b #сумма ежемесячного платежа
    d = a * period # переплата по процентам

    bot.send_message(message.chat.id,
                     f'Ваш ежемесячный платеж составит {c}бел.руб. \nв том числе: \nпо основному долгу {b} бел. руб.'
                     f'\n по процентам {a} бел.руб.\nПереплата за все время пользования кредитом {d} бел.руб.')
bot.polling()

