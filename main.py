import sys
import os
import csv
import re
from getpass import getpass


def login(name, password):
    with open(db_path, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if row == [name.lower(), password]:
                print("Poprawnie zalogowano")
                grant()
                choice()
                return
    print("Logowanie nie powiodło się, spróbuj ponownie")
    access('L')
    return False


def register(name, password):
    if check_user_exists(name) == 0:
        print("Taki login już istnieje, wybierz inny")
        name = input("Login: ")
        password = getpass("Hasło: ")
        register(name.lower(), password)

    if re.fullmatch(r'[A-Za-z0-9@#$%^&+=?!]{8,}', password):
        print('Prawidłowe hasło')

        with open(db_path, 'a', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([name.lower(), password])

        name = input("Login: ")
        password = getpass("Hasło: ")
        login(name, password)

    else:
        print(
            'Hasło jest za słabe. Poprawne hasło powinno składać się z conajmniej 8 znaków, zawierać przynajmniej jedną cyfrę i znak specjalny')
        name = input("Login: ")
        password = getpass("Hasło: ")
        register(name, password)


def delete_user(name):
    lines = list()
    with open(db_path, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            lines.append(row)
            for field in row:
                if field == name:
                    lines.remove(row)
    with open(db_path, 'w', newline='') as writeFile:
        csv_writer = csv.writer(writeFile)
        for row in lines:
            csv_writer.writerow(row)
    print("Poprawnie usunięto")


def user_list():
    with open(db_path, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            print(row[0])


def check_db_exists(path):
    try:
        os.stat(path)
    except FileNotFoundError:
        f = open(path, "w")
        f.close()


def check_user_exists(username):
    with open(db_path, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if username == row[0]:
                return 0


def access(select):
    if (select == 'L'):
        name = input("Login: ")
        password = getpass("Hasło: ")
        login(name, password)
    else:
        name = input("Login: ")
        password = getpass("Hasło: ")
        register(name, password)


def program():
    global select
    print("Witaj w apcce logowania i rejestracji!")
    select = input("Wprowadź L aby przejść do logowania, lub R, aby przejść do rejestracji: ")
    if select != "L" and select != 'R':
        program()


def user_filter(select_f):
    select_f = input("Aby wyszukać konkretnego użytkownika, wpisz jakąś część loginu:   ")
    if select_f != '':
        with open(db_path, 'r', newline='') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if select_f in row[0]:
                    print(row[0])
    else:
        print("brak danych wejściowych")
        user_filter(select_f)


def grant():
    global granted
    granted = True


def choice():
    global select
    print("Witaj! Co chcesz zrobić?")
    select = input("Wybierz D, aby usunąć użytkownika, wybierz W aby wyświetlić listę wszystkich użytkowników:  ")
    if select == 'D':
        delete_user(input("podaj nazwę użytkownika do usunięcia:   "))
        choice()
    if select == 'W':
        user_list()
        user_filter(select_f=input("aby usunąć użytkownika, wybierz D, aby wyszukać użytkownika, wpisz S:   "))
#    if select == 'D':
 #       delete_user(input("podaj nazwę użytkownika do usunięcia:   "))
 #       choice()
    else:
        print("Wybierz co chcesz zrobić!")
        choice()


if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    db_path = os.path.join(current_dir, "db.csv")
    check_db_exists(db_path)
    granted = False
    global select
    program()
    access(select)
    if not granted:
        name = input("Login: ")
        password = getpass("Hasło: ")
        register(name, password)
        granted = True
        program()
