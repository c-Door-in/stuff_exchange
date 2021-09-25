import json

class Database:
    def __init__(self, db_type, db_path='db/'):
        self.db_path = f'{db_path}{db_type}.json'
        self.db_type = db_type

    def create_db(self, adding_dict={}):
        with open(self.db_path, 'w') as ouf:
            json.dump(adding_dict, ouf)
        return True

    def open_db(self):
        with open(self.db_path, 'r') as inf:
            db_dict = json.load(inf)
        return db_dict

    def write_to_db(self, db_dict):
        with open(self.db_path, 'w') as ouf:
            json.dump(db_dict, ouf)
        return True

    def add_new_item(self, adding_data_dict):
        db = self.open_db()
        for index, content_dict in adding_data_dict.items():
            db[index] = content_dict
        self.write_to_db(db)
        return True

    def show_db(self):
        db = self.open_db()
        return db