import sqlite3
import os
from sys import platform
from db_pwd import Pwd_handler

DB_NAME = "debtors.db"
WIDTH = 75
VERSION = "2.3"
db = sqlite3.connect(DB_NAME)
cursor = db.cursor()


class Command():
    def __init__(self, string):
        self.string = string.split()
        self.action = self.string[0]
        self.len = len(self.string)

    def get_action(self):
        return self.action

    def get_name_and_value(self):
        if self.len < 3:
            return 0, 0

        name = " ".join(self.string[1:-1])
        value = self.string[-1]

        try:
            value = int(value)
            return name, value
        except:
            return 0, 0

    def _check_for_comma(self, cmd):
        contains_comma = False
        comma_index = 0
        for ind, i in enumerate(cmd):

            if i.endswith(",") and contains_comma:
                contains_comma = False
                break

            if i.endswith(","):
                contains_comma = True
                comma_index = ind
                continue
        return contains_comma, comma_index

    def get_names(self):
        if self.len < 3:
            return 0, 0

        if self.len > 3:
            contains_comma, comma_ind = self._check_for_comma(self.string)

            if not contains_comma:
                return 0, 0

            old_name = " ".join(self.string[1:comma_ind + 1])[:-1]
            new_name = " ".join(self.string[comma_ind + 1:])
            return old_name, new_name
        else:
            old_name = self.string[1]
            new_name = self.string[2]
            return old_name, new_name

    def get_name(self):
        if self.len == 1:
            return 0
        else:
            name = " ".join(self.string[1:])
            return name


def setup():
    cursor.execute("""CREATE TABLE IF NOT EXISTS debtors(
        name TEXT,
        debt INT
    )""")
    db.commit()


def clearwin():
    if platform == "win32":
        os.system("cls")
    elif platform == "linux":
        os.system("clear")
    else:
        print("Ошибка: неизвестная ОС")


def clear_app_win():
    clearwin()
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
        print(f"{value[0]:<20} {value[1]}")
    if not runned:
        print("Данных нет!")


def debtors():
    runned = False
    for value in cursor.execute("SELECT name FROM debtors"):
        runned = True
        print(value[0])
    if not runned:
        print("Данных нет!")


def rename(debtor_name, new_name):
    cursor.execute(f"SELECT name FROM debtors WHERE name = '{debtor_name}'")
    if cursor.fetchone() is None:
        print("Такого имени не существует!")
    else:
        cursor.execute(f"UPDATE debtors SET name = '{new_name}'"
                       f" WHERE name = '{debtor_name}'")
        db.commit()
        print("Имя изменено!")


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
    print("dec <name> <value>\tуменьшает долг")
    print("inc <name> <value>\tувеличивает долг")
    print("set <name> <value>\tустанавливает имени <name>"
          " значение долга <value>")
    print("new <name> <value>\tдобавляет имя <name> с долгом <value>")
    print("del <name>\t\tудаляет имя")
    print("rename <old>[,] <new>\tизменяет имя <old> на <new>")
    print("help\t\t\tвыводит на экран список команд")
    print("names\t\t\tвыводит на экран список имен")
    print("showall\t\t\tвыводит на экран список имен с долгом")
    print("exit\t\t\tвыходит из лаунчера")


if __name__ == '__main__':
    pwd_handler = Pwd_handler(DB_NAME)
    pwd_handler.inputpwd()
    clear_app_win()
    setup()
    print("Инициализация успешна.")
    print(f"Добро пожаловать в базу данных! (v. {VERSION})\n")
    print('Для вывода списка команд введите "help"\n')
    run = True
    while run:
        string = input(": ").strip()
        if not string:
            continue
        else:
            cmd = Command(string)

        if cmd.get_action() == "dec":
            name, value = cmd.get_name_and_value()
            if (name, value) == (0, 0):
                print("Ошибка в синтаксисе команды!\n")
                continue
            else:
                reduce_debt(name, value)
                print()

        elif cmd.get_action() == "del":
            name = cmd.get_name()
            if name == 0:
                print("Ошибка в синтаксисе команды!\n")
                continue
            else:
                delete_debtor(name)
                print()

        elif cmd.get_action() == "exit":
            run = False
            clearwin()

        elif cmd.get_action() == "help":
            print()
            print_cmds()
            print()

        elif cmd.get_action() == "inc":
            name, value = cmd.get_name_and_value()
            if (name, value) == (0, 0):
                print("Ошибка в синтаксисе команды!\n")
                continue
            else:
                add_debt(name, value)
                print()

        elif cmd.get_action() == "rename":
            old_name, new_name = cmd.get_names()
            if (old_name, new_name) == (0, 0):
                print("Ошибка в синтаксисе команды!\n")
                continue
            else:
                rename(old_name, new_name)
                print()

        elif cmd.get_action() == "names":
            print()
            debtors()
            print()

        elif cmd.get_action() == "new":
            name, value = cmd.get_name_and_value()
            if (name, value) == (0, 0):
                print("Ошибка в синтаксисе команды!\n")
                continue
            else:
                add_debtor(name, value)
                print()

        elif cmd.get_action() == "set":
            name, value = cmd.get_name_and_value()
            if (name, value) == (0, 0):
                print("Ошибка в синтаксисе команды!\n")
                continue
            else:
                set_debt(name, value)
                print()

        elif cmd.get_action() == "showall":
            print()
            db_print()
            print()

        elif cmd.get_action() == "clear":
            clear_app_win()

        else:
            print("Неизвестная команда!\n")
