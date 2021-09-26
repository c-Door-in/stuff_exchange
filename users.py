from database import Database

class Users:
    def __init__(self):
        self.db = Database('users')

    def create_user(self, user_index, username, first_name):
        new_user = {user_index: {'name': first_name, 'username': username}}
        if self.db.add_new_item(new_user):
            return user_index

    def show_users_db(self):
        return self.db.show_db()

    def get_username(self, user_index):
        return self.db.open_db()[user_index]['username']

    def check_for_user(self, user_index, username):
        db = self.db.open_db()
        if user_index in db:
            if not 'username' in db[user_index]:
                db[user_index]['username'] = username
                self.db.write_to_db(db)
            elif not db[user_index]['username']:
                db[user_index]['username'] = username
                self.db.write_to_db(db)
            return True
        return False