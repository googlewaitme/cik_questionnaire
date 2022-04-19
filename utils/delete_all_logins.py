from db_api.models import LoginToken, User


def delete_all_logins():
    confirmation = bool(input(
        "Подтвердите удаление всех авторизаций и ключей(1 - да, 0 - нет): "))
    if not confirmation:
        return
    for el in LoginToken.select():
        el.delete_instance()
    for el in User.select():
        el.delete_instance()
    print('Удаление завершено')


if __name__ == '__main__':
    delete_all_logins()
