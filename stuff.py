import collections
from random import choice, shuffle
from database import Database
from pprint import pprint


class Stuff:
    def __init__(self, user_index):
        self.user_index = user_index
        self.db = Database(f'user_{user_index}')

    def create_stuff_db(self):
        adding_dict = {
            'stuff_index': 0,
            'stuff_cards': {},
        }
        return self.db.create_db(adding_dict)

    def count_stuff_index(self):
        db = self.db.open_db()
        stuff_index = db['stuff_index']
        db['stuff_index'] += 1
        self.db.write_to_db(db)
        return str(stuff_index)

    def create_new_card(self, stuff_dict):
        stuff_index = self.count_stuff_index()
        db = self.db.open_db()
        db['stuff_cards'][stuff_index] = stuff_dict
        return self.db.write_to_db(db)

    def delete_stuff(self, stuff_index):
        db = self.db.open_db()
        del db['stuff_cards'][stuff_index]
        return self.db.write_to_db(db)

    def show_stuff_one_by_one(self):
        db = self.db.open_db()
        user_cards = list(db['stuff_cards'].items())
        current_stuff_index, card = choice(user_cards)
        Database('current').write_to_db((self.user_index, current_stuff_index))
        return card

    def check_for_likes(self):
        db = self.db.open_db()
        liked_users = {}
        for stuff_index, card in db['stuff_cards'].items():
            if 'likes' in card:
                for user in card['likes']:
                    if not user in liked_users:
                        liked_users[user] = [stuff_index]
                    liked_users[user].append(stuff_index)
                return liked_users
        return False

    def add_like(self, stuff_index, user_id):
        db = self.db.open_db()
        if not 'likes' in db['stuff_cards'][stuff_index]:
            db['stuff_cards'][stuff_index]['likes'] = [user_id]
        else:
            db['stuff_cards'][stuff_index]['likes'].append(user_id)
        self.db.write_to_db(db)
        return

    def add_changed_status(self, stuff_index):
        db = self.db.open_db()
        db['stuff_cards'][stuff_index]['changed'] = True
        self.db.write_to_db(db)
        return

    def get_card_by_index(self, stuff_index):
        db = self.db.open_db()
        return db['stuff_cards'][stuff_index]
