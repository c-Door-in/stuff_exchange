import json
from pprint import pprint


class Database:
    def __init__(self, type, path='modules/'):
        self._path = path
        self._type = type

    def open_db(self):
        with open(f'{self._path}{self._type}.json', 'r') as inf:
            db_dict = json.load(inf)
        return db_dict

    def write_to_db(self, db_dict):
        with open(f'{self._path}{self._type}.json', 'w') as ouf:
            json.dump(db_dict, ouf)
        return

    def add_to_db(self, adding_data_dict):
        db_dict = self.open_db()
        for index, content_dict in adding_data_dict.items():
            db_dict[index] = content_dict
        self.write_to_db(db_dict)
        return

    def show_db(self):
        db = self.open_db()
        return db


class User:
    def __init__(self, users_db=Database('users')):
        self.users_db = users_db

    def user_index(self):
        type_dict = self.users_db.open_db()
        index = type_dict['index']
        type_dict['index'] += 1
        self.users_db.write_to_db(type_dict)
        return index

    def create(self, user_name):
        index = self.user_index()
        new_user = {
            index: {
                'name': user_name,
                'stuff_cards': {
                    'stuff_index': 0
                }
            }
        }
        self.users_db.add_to_db(new_user)
        return

    def show_users_db(self):
        return self.users_db.show_db()

user = User()
user.create('Kate')
user.create('Vasily')
user.create('Egor')
pprint(user.show_users_db())


