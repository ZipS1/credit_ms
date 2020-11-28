import sqlite3
import os

db = sqlite3.connect("debtors.db")
cursor = db.cursor()
WIDTH = 50


def setup():
    cursor.execute("""CREATE TABLE IF NOT EXISTS debtors(
        name TEXT,
        debt INT
    )""")
    db.commit()


def clearwin():
    os.system("cls")
    print(" LAUNCHER ".center(WIDTH, "-"))


def add_debtor():
    debtor_name = input("Имя: ")
    debtor_debt = int(input("Долг: "))

    cursor.execute(f"SELECT name FROM debtors WHERE name = '{debtor_name}'")
    if cursor.fetchone() is None:
        cursor.execute(f"INSERT INTO debtors VALUES (?, ?)",
                        (debtor_name, debtor_debt))
        db.commit()
        print("Зарегистрировано!")
    else:
        print("Такое имя уже существует!")


def delete_debtor():
    debtor_name = input("Имя: ")

    cursor.execute(f"SELECT name FROM debtors WHERE name = '{debtor_name}'")
    if cursor.fetchone() is None:
        print("Такого имени не существует!")
    else:
        cursor.execute(f"DELETE FROM debtors WHERE name = '{debtor_name}'")
        db.commit()
        print("Имя удалено!")


def db_print():
    runned = False
    for value in cursor.execute("SELECT * FROM debtors"):
        runned = True
        print(f"{value[0]:<15} {value[1]}")
    if not runned:
        print("Данных нет!")


def debtors():
    runned = False
    for value in cursor.execute("SELECT name FROM debtors"):
        runned = True
        print(value[0])
    if not runned:
        print("Данных нет!")


def set_debt():
    debtor_name = input("Имя: ")
    value = int(input("Долг:  "))

    cursor.execute(f"SELECT name FROM debtors WHERE name = '{debtor_name}'")
    if cursor.fetchone() is None:
        print("Такого имени не существует!")
    else:
        cursor.execute(f"UPDATE debtors SET debt = {value} "
                       f"WHERE name = '{debtor_name}'")
        db.commit()
        print("Долг успешно обновлен!")


def add_debt():
    debtor_name = input("Имя: ")
    value = int(input("Добавить: "))

    cursor.execute(f"SELECT name FROM debtors WHERE name = '{debtor_name}'")
    if cursor.fetchone() is None:
        print("Такого имени не существует!")
    else:
        cursor.execute(f"SELECT debt FROM debtors "
                       f"WHERE name = '{debtor_name}'")
        debt = cursor.fetchone()[0]
        cursor.execute(f"UPDATE debtors SET debt = {debt + value} "
                       f"WHERE name = '{debtor_name}'")
        db.commit()
        print("Долг увеличен!")


def reduce_debt():
    debtor_name = input("Имя: ")
    value = int(input("Уменьшить на: "))

    cursor.execute(f"SELECT name FROM debtors WHERE name = '{debtor_name}'")
    if cursor.fetchone() is None:
        print("Такого имени не существует!")
    else:
        cursor.execute(f"SELECT debt FROM debtors "
                       f"WHERE name = '{debtor_name}'")
        debt = cursor.fetchone()[0]
        if debt - value > 0:
            cursor.execute(f"UPDATE debtors SET debt = {debt - value} "
                           f"WHERE name = '{debtor_name}'")
            db.commit()
            print("Долг уменьшен!")
        else:
            cursor.execute(f"DELETE FROM debtors WHERE name = '{debtor_name}'")
            db.commit()
            print("Имя удалено за неимением долга!")


def print_cmds():
    print("clear     очищает экран")
    print("dec       уменьшить долг")
    print("del       удаление имени")
    print("exit      выход из лаунчера")
    print("help      выводит на экран все команды лаунчера")
    print("inc       увеличить долг")
    print("names     выводит на экран только имена")
    print("new       добавление нового имени")
    print("set       установить значение долга")
    print("showall   выводит на экран всю информацию базы данных")


if __name__ == '__main__': #TODO: make a clearwin() usage more smarter
    clearwin()
    setup()
    print("Инициализация успешна.")
    print("Добро пожаловать в базу данных! (v. 1.0)\n")
    print('Для вывода списка команд введите "help"\n')
    run = True
    while run:
        cmd = input(": ").strip()
        if cmd == "clear":
            clearwin()
        elif cmd == "dec":
            clearwin()
            reduce_debt()
            print()
        elif cmd == "del":
            clearwin()
            delete_debtor()
            print()
        elif cmd == "exit":
            run = False
            os.system("cls")
        elif cmd == "help":
            print()
            print_cmds()
            print()
        elif cmd == "inc":
            clearwin()
            add_debt()
            print()
        elif cmd == "names":
            print()
            debtors()
            print()
        elif cmd == "new":
            clearwin()
            add_debtor()
            print()
        elif cmd == "set":
            clearwin()
            set_debt()
            print()
        elif cmd == "showall":
            print()
            db_print()
            print()
        else:
            print("Неизвестная команда!\n")
