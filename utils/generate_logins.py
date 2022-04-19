from db_api.models import LoginToken
import uuid
import csv


def generate_logins(names: list):
    logins = []
    for name in names:
        login = str(uuid.uuid4())[:8]
        LoginToken.create(name=name, login=login)
        logins.append((name, login))
    return logins


def input_names_from_keyboard(count_of_names: int):
    names = []
    for _ in range(count_of_names):
        name = input()
        names.append(name)
    return names


def write_logins_in_file(logins: list, filename: str):
    with open(filename, 'w', newline='') as file_output:
        fieldnames = ['name', 'login']
        writer = csv.writer(file_output)
        writer.writerow(fieldnames)
        for name, login in logins:
            writer.writerow([name, login])


if __name__ == '__main__':
    filename = 'logins.csv'
    count_of_names = int(input("Введите количество УИКов: "))
    print(f"Теперь нужно ввести {count_of_names} имен"
          " УИКов, каждое имя на новой строке")
    names = input_names_from_keyboard(count_of_names)
    logins = generate_logins(names)
    print('---')
    print('Генерация завершена')
    write_logins_in_file(logins)
    print(f'---\nЗапись в файл {filename} завершена')
