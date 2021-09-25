from database import Database

class Users:
    def __init__(self):
        self.db = Database('users')

    def create_user(self, user_index, user_name):
        new_user = {user_index: {'name': user_name}}
        if self.db.add_new_item(new_user):
            return user_index

    def show_users_db(self):
        return self.db.show_db()

    def check_for_user(self, user_index):
        db = self.db.open_db()
        if user_index in db:
            return True
        return False
