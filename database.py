import json


def create_db(db_dict, dict_type, path='modules/'):
    with open(f'{path}{dict_type}.json', 'w') as ouf:
        json.dump(db_dict, ouf)
    return

users = {
    'index': 0
}

create_db(users, 'users')