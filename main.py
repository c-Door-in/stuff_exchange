from random import shuffle
from pprint import pprint
from database import Database
from users import Users
from stuff import Stuff


class Main:
    def __init__(self, user_index, username='', first_name=''):
        self.user_index = str(user_index)
        self.username = username
        self.first_name = first_name
        self.users_db = Users()
        self.stuff_db = Stuff(user_index)
    
    def authorization(self):
        return self.users_db.check_for_user(self.user_index, self.username)

    def add_stuff(self, image_id, name='Без имени', description=''):
        if not self.authorization():
            self.users_db.create_user(self.user_index, self.username, self.first_name)
            self.stuff_db.create_stuff_db()
        new_stuff = {
            'name': name,
            'description': description,
            'image_id': image_id,
        }
        self.stuff_db.create_new_card(new_stuff)
        return 'Добавлено {name}, {description}'.format(**new_stuff)

    def remove_stuff(self, stuff_index):
        deleted_card = self.stuff_db.get_card_by_index(stuff_index)
        self.stuff_db.delete_stuff(stuff_index)
        return deleted_card

    def find_stuff(self):
        liked_users = self.stuff_db.check_for_likes()
        if liked_users:
            for _ in liked_users:
                next_card = self.get_next_card()
                if next_card:
                    return next_card
        return self.get_next_card()

    def get_next_card(self):
        user_list = list(self.users_db.show_users_db().keys())
        shuffle(user_list)
        for user_index in user_list:
            if user_index != self.user_index:
                other_user_stuff_db = Stuff(user_index)
                next_card = other_user_stuff_db.show_stuff_one_by_one()
                if next_card:     
                    return next_card
        return False

    def change_stuff(self):
        owner_index, current_stuff_index = Database('current').open_db()
        liked_users = self.stuff_db.check_for_likes()
        print('this stuff', owner_index, current_stuff_index)
        print('user', self.user_index)
        print('liked_users', liked_users)
        if not liked_users:
            owner_stuff_db = Stuff(owner_index)
            owner_stuff_db.add_like(current_stuff_index, self.user_index)
            return False
        if owner_index in liked_users:
            match_set = (owner_index, current_stuff_index, liked_users[owner_index][0])
            return self.match_execute(match_set)

    def match_execute(self, match_set):
        owner_index, current_stuff_index, liked_stuff_index = match_set
        owner_username = self.users_db.get_username(owner_index)
        owner_stuff_db = Stuff(owner_index)
        user_stuff_card = self.stuff_db.get_card_by_index(liked_stuff_index)
        owner_stuff_card = owner_stuff_db.get_card_by_index(current_stuff_index)
        self.change_stuff_status((owner_index, current_stuff_index, liked_stuff_index))
        print('BINGO!!!')
        print('{0} от {1}'.format(user_stuff_card['name'], self.username))
        print('<-->')
        print('{0} от {1}'.format(owner_stuff_card['name'], self.users_db.show_users_db()[owner_index]['name']))
        return (user_stuff_card, owner_index, owner_username, owner_stuff_card)

    def change_stuff_status(self, match_set):
        owner_index, current_stuff_index, liked_stuff_index = match_set
        owner_stuff_db = Stuff(owner_index)
        self.stuff_db.add_changed_status(liked_stuff_index)
        owner_stuff_db.add_changed_status(current_stuff_index)
        return
