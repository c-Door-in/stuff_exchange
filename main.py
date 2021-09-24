import json
import collections
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
    def __init__(self, db=Database('users')):
        self.db = db

    def user_index(self):
        type_dict = self.db.open_db()
        index = type_dict['index']
        type_dict['index'] += 1
        self.db.write_to_db(type_dict)
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
        self.db.add_to_db(new_user)
        return

    def show_users_db(self):
        return self.db.show_db()

    def check_active_user(self, user_index):
        for index, content in self.show_users_db().items():
            if index == str(user_index):
                print('зашел')
                if not 'active' in content:
                    content['active'] = True
                return True
            elif type(content) is not int:
                if 'active' in content:
                    del content['active']
        return False


class Stuff:
    def __init__(self, db=Database('users')):
        self.db = db

    def stuff_index(self, user_index):
        user_dict = self.db.open_db()
        stuff_index = user_dict[str(user_index)]['stuff_cards']['stuff_index']
        user_dict[str(user_index)]['stuff_cards']['stuff_index'] += 1
        self.db.write_to_db(user_dict)
        return stuff_index

    def create_new_card(self, user_index, stuff_dict):
        stuff_index = self.stuff_index(user_index)
        user_dict_for_new_stuff = self.db.open_db()
        user_dict_for_new_stuff[str(user_index)]['stuff_cards'][str(stuff_index)] = stuff_dict
        self.db.add_to_db(user_dict_for_new_stuff)
        return

    def delete_stuff(self, user_index, stuff_index):
        user_dict = self.db.open_db()
        stuff_name = user_dict[str(user_index)]['stuff_cards'][str(stuff_index)]['name']
        del user_dict[str(user_index)]['stuff_cards'][str(stuff_index)]
        self.db.add_to_db(user_dict)
        return stuff_name

    def show_user_stuff_one_by_one(self, user_index):
        user_dict = self.db.open_db()
        pprint(user_dict[str(user_index)])
        for index, card in user_dict[str(user_index)]['stuff_cards'].items():
            if not 'seen' in card:
                user_dict[str(user_index)]['stuff_cards'][index]['seen'] = True
                return (index, card)
        for index, card in user_dict[str(user_index)]['stuff_cards'].items():
            del user_dict[str(user_index)]['stuff_cards'][index]['seen']
        self.db.add_to_db(user_dict)
        print('All cards was seen. Check them again')
        return

    def check_for_likes(self, user_index):
        user_dict = self.db.open_db()
        liked_users = collections.defaultdict(list)
        for stuff_index, card in user_dict[str(user_index)]['stuff_cards'].items():
            if 'likes' in card:
                for user in card['likes']:
                    liked_users[user].append(stuff_index)
        return liked_users

    def add_like(self, user_index, owner_index, stuff_index):
        user_dict = self.db.open_db()
        if not 'likes' in user_dict[owner_index]['stuff_cards'][str(stuff_index)]:
            user_dict[owner_index]['stuff_cards'][str(stuff_index)]['likes'] = [str(user_index)]
        else:
            user_dict[owner_index]['stuff_cards'][str(stuff_index)]['likes'].append(user_index)
        self.db.add_to_db(user_dict)
        return

    def add_changed_status(self, user_index, stuff_index):
        user_dict = self.db.open_db()
        user_dict[str(user_index)]['stuff_cards'][str(stuff_index)]['changed'] = True
        self.db.add_to_db(user_dict)
        return

    def get_card_by_index(self, user_index, stuff_index):
        user_dict = self.db.open_db()
        return user_dict[str(user_index)]['stuff_cards'][str(stuff_index)]


class Main:
    def __init__(self, user_index, users_db=User(), stuff_db=Stuff()):
        self.user_index = user_index
        self.users_db = users_db
        self.stuff_db = stuff_db
        self.current_index = None
    
    def authorization(self, user_index):
        if not self.users_db.check_active_user(user_index):
            print('User not found')
            return False
        return user_index

    def add_stuff(self, name, description, image_path):
        user_id = self.authorization(self.user_index)
        if not user_id:
            print('Добавить невозможно')
            return
        new_stuff = {
            'name': name,
            'description': description,
            'image_path': image_path,
        }
        self.stuff_db.create_new_card(user_id, new_stuff)
        return

    def remove_stuff(self, stuff_index):
        user_id = self.authorization(self.user_index)
        if not user_id:
            print('Удалить невозможно')
            return
        deleted_stuff_name = self.stuff_db.delete_stuff(user_id, stuff_index)
        print(f'Stuff {deleted_stuff_name} has been deleted')
        return

    def find_stuff(self):
        user_id = self.authorization(self.user_index)
        if not user_id:
            print('Найти невозможно')
            return
        for user_index in self.users_db.show_users_db().keys():
            if user_index != user_id:
                stuff_index, stuff_card = self.stuff_db.show_user_stuff_one_by_one(user_index)
                print(stuff_card['name'])
                print(stuff_card['description'])
                print(stuff_card['image_path'])
                self.current_index = (user_index, stuff_index)
        return 

    def change_stuff(self):
        user_id = self.authorization(self.user_index)
        if not user_id:
            print('Обменять невозможно')
            return
        owner_index, stuff_index = self.current_index
        liked_users = self.stuff_db.check_for_likes(user_id)
        if owner_index in liked_users:
            return self.execute_match(user_id, self.current_index, liked_users[owner_index])
        self.stuff_db.add_like(user_id, owner_index, stuff_index)
        return

    def execute_match(self, user_id, current_stuff_tuple, liked_stuff_list):
        owner_index, stuff_index = current_stuff_tuple
        user_stuff = self.stuff_db.get_card_by_index(user_id, liked_stuff_list[0])
        other_stuff = self.stuff_db.get_card_by_index(owner_index, stuff_index)
        self.stuff_db.add_changed_status(user_id, liked_stuff_list[0])
        self.stuff_db.add_changed_status(owner_index, stuff_index)
        print('BINGO!!!')
        print('{name}\n{description}\n{image_path}'.format(**user_stuff))
        print('<-->')
        print('{name}\n{description}\n{image_path}'.format(**other_stuff))
        return


main = Main(1)

main.add_stuff('good_stuff', 'very very good', 'image1')

main2 = Main(2)

main2.add_stuff('excellent_stuff', 'the best', 'image2')
main2.find_stuff()
main2.change_stuff()
