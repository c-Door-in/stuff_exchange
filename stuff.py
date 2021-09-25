import collections
from database import Database


class Stuff:
    def __init__(self, user_index):
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
        db = self.db.open_db()
        db['stuff_cards'][self.count_stuff_index()] = stuff_dict
        return self.db.add_to_db(db)

    def delete_stuff(self, stuff_index):
        db = self.db.open_db()
        del db['stuff_cards'][stuff_index]
        return self.db.add_to_db(db)

    def show_stuff_one_by_one(self):
        db = self.db.open_db()
        for stuff_index, card in db['stuff_cards'].items():
            if not 'seen' in card:
                db['stuff_cards'][stuff_index]['seen'] = True
                self.db.add_to_db(db)
                return (stuff_index, card)
        for stuff_index, card in db['stuff_cards'].items():
            del db['stuff_cards'][stuff_index]['seen']
        self.db.add_to_db(db)
        return False

    def check_for_likes(self):
        db = self.db.open_db()
        liked_users = collections.defaultdict(list)
        for stuff_index, card in db['stuff_cards'].items():
            if 'likes' in card:
                for user in card['likes']:
                    liked_users[user].append(stuff_index)
                return liked_users
        return False

    # def add_like(self, owner_index, stuff_index):
    #     db = self.db.open_db()
    #     if not 'likes' in db[owner_index]['stuff_cards'][str(stuff_index)]:
    #         user_dict[owner_index]['stuff_cards'][str(stuff_index)]['likes'] = [str(user_index)]
    #     else:
    #         user_dict[owner_index]['stuff_cards'][str(stuff_index)]['likes'].append(user_index)
    #     self.db.add_to_db(user_dict)
    #     return

    # def add_changed_status(self, user_index, stuff_index):
    #     user_dict = self.db.open_db()
    #     user_dict[str(user_index)]['stuff_cards'][str(stuff_index)]['changed'] = True
    #     self.db.add_to_db(user_dict)
    #     return

    # def get_card_by_index(self, user_index, stuff_index):
    #     user_dict = self.db.open_db()
    #     return user_dict[str(user_index)]['stuff_cards'][str(stuff_index)]