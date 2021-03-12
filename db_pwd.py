import sqlite3                # TODO: make delay before showing messages
from hashlib import sha256
from getpass import getpass

DB_FILE_NAME = "access.db"


class Pwd_handler:
    def __init__(self, db_file_name, enter_attempts_allowed=3):
        self.enter_attempts_allowed = enter_attempts_allowed
        self.db = sqlite3.connect(db_file_name)
        self.cursor = self.db.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS pwdhash (
            pwd TEXT
            )""")
        self.db.commit()
        self.cursor.execute("SELECT pwd FROM pwdhash")
        if self.cursor.fetchone() is None:
            self._new()
        self.cursor.execute(f"SELECT pwd FROM pwdhash")
        self.hashed_pwd = self.cursor.fetchall()[0][0]

    def _new(self):
        print("I detected that you have no password here.")
        pwd = self._create()
        hashed_pwd = self._encrypt(pwd)
        self.cursor.execute(f"INSERT INTO pwdhash VALUES (?)", (hashed_pwd,))
        self.db.commit()
        print("Your password successfully recorded!\n")

    def _create(self):
        pwd = getpass("Enter new password: ")
        pwd_rpt = getpass("Confirm your new password: ")
        while not pwd == pwd_rpt:
            print("Your passwords do not match!")
            pwd = getpass("\nEnter password: ")
            pwd_rpt = getpass("Confirm your new password: ")
        return pwd

    def inputpwd(self):
        pwd = getpass("Enter your code-word: ")
        correct = self._check(pwd)
        attempts = 1
        while not correct:

            if attempts == self.enter_attempts_allowed:
                print("You have too much attempts :(\nExiting...")
                exit()
            attempts += 1

            if attempts != self.enter_attempts_allowed:
                pwd = getpass("Wrong! Enter again: ")
            else:
                pwd = getpass("Last try! Enter again: ")
            correct = self._check(pwd)

    def _check(self, word):
        hashed_word = sha256(word.encode("utf-8")).hexdigest()
        self.cursor.execute(f"SELECT pwd FROM pwdhash "
                            f"WHERE pwd = '{hashed_word}'")
        if self.cursor.fetchone() is None:
            return False
        else:
            return True

    def set_new(self):
        print("\nTo set new password, you firstly need to enter old one")
        self.inputpwd()
        new_pwd = self._create()
        new_hashed_pwd = self._encrypt(new_pwd)
        self.cursor.execute(f"UPDATE pwdhash SET pwd = '{new_hashed_pwd}'")
        self.db.commit()
        print("Password successfully updated!")

    def _encrypt(self, pwd):
        return sha256(pwd.encode("utf-8")).hexdigest()


def main():
    print("Nice to meet you here bro :)\n")
    pwd_handler = Pwd_handler(DB_FILE_NAME)
    pwd_handler.inputpwd()
    print("Access granted :)")
    pwd_handler.set_new()


if __name__ == '__main__':
    main()
