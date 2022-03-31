from utils.db_api.models import User, LoginToken


class UserApi:
    def __init__(self, telegram_id):
        self.telegram_id = telegram_id
        self.name = "noname"

    def is_exist(self):
        query = User.select().where(User.telegram_id == self.telegram_id)
        return query.exists()

    def get(self):
        return User.get(telegram_id=self.telegram_id)

    def is_login(self, login):
        query = LoginToken.select().where(LoginToken.login == login)
        if query.exists():
            self.name = query[0].name
            return True
        return False

    def create(self):
        User.create(
            telegram_id=self.telegram_id,
            name=self.name
        )

    def get_name(self):
        user = self.get()
        return user.name

    @staticmethod
    def get_all_users():
        query = User.select()
        return query
