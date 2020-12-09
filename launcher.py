import sqlite3
import os

db = sqlite3.connect("debtors.db")
cursor = db.cursor()
WIDTH = 75


def setup():
    cursor.execute("""CREATE TABLE IF NOT EXISTS debtors(
        name TEXT,
        debt INT
    )""")
    db.commit()


def get_name():
    if len(cmd) == 1:
        return 0
    else:
        name = " ".join(cmd[1:])
        return name


def get_name_and_value():
    if len(cmd) == 1:
        return 0, 0
    else:
        name = " ".join(cmd[1:-1])
        value = cmd[-1]

    try:
        value = int(value)
        return name, value
    except:
        return 0, 0


def clearwin():
    os.system("cls")
    print(" LAUNCHER ".center(WIDTH, "-"))


def add_debtor(debtor_name, debtor_debt):
    cursor.execute(f"SELECT name FROM debtors WHERE name = '{debtor_name}'")
    if cursor.fetchone() is None:
        cursor.execute(f"INSERT INTO debtors VALUES (?, ?)",
                        (debtor_name, debtor_debt))
        db.commit()
        print("Зарегистрировано!")
    else:
        print("Такое имя уже существует!")


def delete_debtor(debtor_name):
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


def set_debt(debtor_name, value):
    cursor.execute(f"SELECT name FROM debtors WHERE name = '{debtor_name}'")
    if cursor.fetchone() is None:
        print("Такого имени не существует!")
    else:
        cursor.execute(f"UPDATE debtors SET debt = {value} "
                       f"WHERE name = '{debtor_name}'")
        db.commit()
        print("Долг успешно обновлен!")


def add_debt(debtor_name, value):
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


def reduce_debt(debtor_name, value):
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
    print("clear\t\t\tочищает экран")
    print("dec <name> <value>\tуменьшить долг")
    print("del <name>\t\tудаление имени")
    print("exit\t\t\tвыход из лаунчера")
    print("help\t\t\tвыводит на экран все команды лаунчера")
    print("inc <name> <value>\tувеличить долг")
    print("names\t\t\tвыводит на экран список имен")
    print("new <name> <value>\tдобавление нового имени <name> "
          "с долгом <value>")
    print("set <name> <value>\tустановить имени <name> значение долга <value>")
    print("showall\t\t\tвыводит на экран всю информацию")


if __name__ == '__main__':
    clearwin()
    setup()
    print("Инициализация успешна.")
    print("Добро пожаловать в базу данных! (v. 2.1)\n")
    print('Для вывода списка команд введите "help"\n')
    run = True
    while run:
        cmd = input(": ").strip().split()

        if cmd[0] == "dec":
            name, value = get_name_and_value()
            if (name, value) == (0, 0):
                print("Ошибка в синтаксисе команды!\n")
                continue

            reduce_debt(name, value)
            print()
        elif cmd[0] == "del":
            name = get_name()
            if name == 0:
                print("Ошибка в синтаксисе команды!\n")
                continue

            delete_debtor(name)
            print()
        elif cmd[0] == "exit":
            run = False
            os.system("cls")
        elif cmd[0] == "help":
            print()
            print_cmds()
            print()
        elif cmd[0] == "inc":
            name, value = get_name_and_value()
            if (name, value) == (0, 0):
                print("Ошибка в синтаксисе команды!\n")
                continue

            add_debt(name, value)
            print()
        elif cmd[0] == "names":
            print()
            debtors()
            print()
        elif cmd[0] == "new":
            name, value = get_name_and_value()
            if (name, value) == (0, 0):
                print("Ошибка в синтаксисе команды!\n")
                continue

            add_debtor(name, value)
            print()
        elif cmd[0] == "set":
            name, value = get_name_and_value()
            if (name, value) == (0, 0):
                print("Ошибка в синтаксисе команды!\n")
                continue

            set_debt(name, value)
            print()
        elif cmd[0] == "showall":
            print()
            db_print()
            print()
        elif cmd[0] == "clear":
            clearwin()
        else:
            print("Неизвестная команда!\n")
