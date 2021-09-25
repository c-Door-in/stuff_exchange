from pprint import pprint
from database import Database
from users import Users
from stuff import Stuff


class Main:
    def __init__(self, user_index, user_name=''):
        self.user_index = str(user_index)
        self.user_name = user_name
        self.users_db = Users()
        self.stuff_db = Stuff(user_index)
        self.current_index = None
    
    def authorization(self):
        return self.users_db.check_for_user(self.user_index)

    def add_stuff(self, image_id, name='Без имени', description=''):
        if not self.authorization():
            self.users_db.create_user(self.user_index, self.user_name)
            self.stuff_db.create_stuff_db()
        new_stuff = {
            'name': name,
            'description': description,
            'image_id': image_id,
        }
        self.stuff_db.create_new_card(new_stuff)
        return 'Добавлено {name}, {description}'.format(**new_stuff)

    def remove_stuff(self, stuff_index):
        self.stuff_db.delete_stuff(stuff_index)
        user_index = self.user_index
        return f'Stuff {stuff_index} from {user_index} has been deleted'

    def find_stuff(self):
        for user_index in self.users_db.show_users_db().keys():
            if user_index != self.user_index:
                other_user_stuff_db = Stuff(user_index)
                next_card = other_user_stuff_db.show_stuff_one_by_one()
                if next_card:
                    stuff_index, stuff_card = next_card
                    print('show', stuff_card['name'])
                    # print(stuff_card['description'])
                    # print(stuff_card['image_id'])
                    self.current_index = (user_index, stuff_index)
                    return stuff_card
        return False

    # def change_stuff(self):
    #     owner_index, stuff_index = self.current_index
    #     liked_users = self.stuff_db.check_for_likes(user_id)
    #     if owner_index in liked_users:
    #         return self.execute_match(user_id, self.current_index, liked_users[owner_index])
    #     self.stuff_db.add_like(user_id, owner_index, stuff_index)
    #     return

    # def execute_match(self, user_id, current_stuff_tuple, liked_stuff_list):
    #     owner_index, stuff_index = current_stuff_tuple
    #     user_stuff = self.stuff_db.get_card_by_index(user_id, liked_stuff_list[0])
    #     other_stuff = self.stuff_db.get_card_by_index(owner_index, stuff_index)
    #     self.stuff_db.add_changed_status(user_id, liked_stuff_list[0])
    #     self.stuff_db.add_changed_status(owner_index, stuff_index)
    #     print('BINGO!!!')
    #     print('{name}\n{description}\n{image_path}'.format(**user_stuff))
    #     print('<-->')
    #     print('{name}\n{description}\n{image_path}'.format(**other_stuff))
    #     return
