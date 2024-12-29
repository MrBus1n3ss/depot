import sqlite3
from datetime import datetime
from pathlib import Path
import hashlib


home_dir = Path.home()
data_dir = home_dir / 'data'


class DB:
    def __init__(self, path, db_name):
        self.db_path = path / db_name
        self.connection = sqlite3.connect(self.db_path)

    def total_changes(self):
        return self.connection.total_changes

    def get_cursor(self):
        return self.connection.cursor()


class DepotSystem:
    def __init__(self, name, db):
        self.name = name
        self.db = db
        self.created_at = datetime.now()
        self.cursor = self.db.get_cursor()

    def create_depot(self, depot_name):
        row = self.cursor.execute("select name, hash from depot_mapping").fetchone()
        if row is None:
            hash = self.create_hash()
            self.cursor.execute("insert into depot_mapping values (?, ?)", (depot_name, hash,))
            print(self.cursor.execute("select name, hash from depot_mapping").fetchall())
            self.db.connection.commit()

        else:
            raise Exception(f'{depot_name} already exists')

    def create_hash(self):
        hash = hashlib.sha256()
        hash.update(bytes(self.name.encode('utf-8')))
        hash.update(bytes(str(self.created_at).encode('utf-8')))
        return hash.hexdigest()



class Depot:
    def __init__(self, name, created_at, db):
        self.name = name
        self.created_at = created_at
        self.db = db

    def store_file(self):
        pass

    def remove_file(self):
        pass

    def update_file(self):
        pass

    def hash_file(self):
        pass

    def compress_file(self):
        pass

    def decompress_file(self):
        pass


# TODO: going to make this more like buckets, need to make into server
def main():
    depot_mapping = DB(data_dir, "depot_mapping.db")
    depot_mapping.get_cursor().execute("create table if not exists depot_mapping (name text, hash text)")
    depot_mapping.connection.commit()
    depot_system = DepotSystem('test', depot_mapping)
    depot_system.create_depot('test')


if __name__ == "__main__":
    main()
