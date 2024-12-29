import sqlite3
from datatime import datetime
from pathlib import Path


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
    def __init__(self, db):
        self.db = db

    def create_dir(self):
        pass

    def create_hash(self):
        pass

class FileSystem(object):

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(FileSystem, cls).__new__(cls)
        return cls.instance

    def config(self, project, location):
        self.project = project
        self.location = location

    def create_file_system(self):
        try:
            print(self.project)
            print(self.location)
        except AttributeError:
            print('Please run config First')
        except Exception:
            print('Unknown Error')

    def update_file_system(self, location):
        pass

    def get_file_system(self, location):
        pass

    def delete_file_system(self, location):
        pass


# TODO: going to make this more like buckets, need to make into server
def main():
    depot_mapping = DB(data_dir, "depot_mapping.db")
    depot = DepotSystem(depot_mapping)


if __name__ == "__main__":
    main()
