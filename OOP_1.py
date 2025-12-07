class ATM:
    def __init__(self, balance=2500):
        self.balance = balance
        self.history = []

    def check_balance(self):
        print(f"Ваш баланс: {self.balance} BYN")
        self.history.append(f"Проверка баланса: {self.balance}")

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            print(f"Вы сняли {amount} BYN. Остаток: {self.balance} BYN")
            self.history.append(f"Снятие: {amount}")
        else:
            print("Недостаточно средств!")
            self.history.append(f"Неудачная попытка снятия: {amount}")

    def deposit(self, amount):
        self.balance += amount
        print(f"Баланс пополнен на {amount} BYN. Новый баланс: {self.balance} BYN")
        self.history.append(f"Пополнение: {amount}")

    def show_history(self):
        print("История операций:")
        if self.history:
            for h in self.history:
                print("-", h)
        else:
            print("История пуста.")

atm = ATM()

status = True
while status:
    print("\nВыберите операцию: \n 1. Проверить баланс \n 2. Снять наличные \n 3. Пополнить баланс \n "
          "4. История операций \n 5. Выйти")

    choice = input("Введите номер: ")

    if choice == "1":
        atm.check_balance()
    elif choice == "2":
        amount = int(input("Введите сумму: "))
        atm.withdraw(amount)
    elif choice == "3":
        amount = int(input("Введите сумму: "))
        atm.deposit(amount)
    elif choice == "4":
        atm.show_history()
    elif choice == "5":
        print("Спасибо за использование банкомата!")
        break
    else:
        print("Неверный ввод, попробуйте снова.")
