from database import Database

class Users:
    def __init__(self):
        self.db = Database('users')

    def create_user(self, user_index):
        new_user = {user_index: {'name': ''}}
        if self.db.add_new_item(new_user):
            return user_index

    def show_users_db(self):
        return self.db.show_db()

    def check_for_user(self, user_index):
        db = self.db.open_db()
        if user_index in db:
            return True
        self.create_user(user_index)
        return False