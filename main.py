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

    def close_connection(self):
        self.connection.close()


# Row name:str depot:str dirs:list date_created:timestamp
# TODO: create dir for depots
class Depots:
    def __init__(self, db):
        self.db = db
        self.cursor = self.db.get_cursor()
        self.cursor.execute("""
            create table if not exists depots
            (
                name text not null unique,
                created_at text,
                created_by text,
                modify_at text,
                modify_by text
            );
            """)
        self.cursor.execute("""
            create table if not exists dirs
            (
                dir_name text not null,
                parent_dir text,
                depot_name text not null,
                created_at text,
                created_by text,
                modify_at text,
                modify_by text,
                foreign key(depot_name) references depots(name)
                unique(dir_name, depot_name, parent_dir)
            );
            """)
        self.db.connection.commit()

    def get_depot(self, name):
        row = self.cursor.execute("select * from depots where name = ?", (name,)).fetchone()
        if not row:
            raise Exception(f'{name} does not exist')
        if row[0] == name:
            return Depot(row[0], row[1], row[2], row[3])

    def create_depot(self, depot):
        self.cursor.execute("insert into depots values (?, ?, ?, ?, ?)",
                                (depot.name,
                                 depot.created_at,
                                 depot.created_by,
                                 depot.modify_by,
                                 depot.modify_at))
        self.db.connection.commit()

    def delete_depot(self, depot):  # TODO cascade delete with deleting all files 
        pass


class Depot:
    def __init__(self,
                 name: str,
                 dirs: list,
                 created_by: str,
                 modify_by: str):
        now = datetime.now()  # TODO: will need to change how this works
        self.name = name
        self.dirs = dirs
        self.created_at = now
        self.created_by = created_by
        self.modify_at = now
        self.modify_by = modify_by

    def create_dir(self, db, dir_name, parent_dir='root'):  # TODO: figure out how I want to do the db part
        cursor = db.get_cursor()
        # TODO: validate dir name
        cursor.execute("insert into dirs values(?, ?, ?, ?, ?, ?, ?)",
                       (dir_name,
                        parent_dir,
                        self.name,
                        self.created_at,
                        self.created_by,
                        self.modify_at,
                        self.modify_by))
        db.connection.commit()

    def get_dir_tree(self):
        pass

    def get_dirs(self, db):
        cursor = db.get_cursor()
        rows = cursor.execute("select * from dirs where depot_name = ?",
                              (self.name,)).fetchall()
        return rows


    def get_dir(self):
        pass

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


def filename_parser(filename):
    return filename.split(':')

# These are for testing ========================================================
def create_test_dir(depot_mapping, depot):
    depot.create_dir(depot_mapping, 'test_dir')


def create_parent_dir(depot_mapping, depot):
    depot.create_dir(depot_mapping, 'parent_dir')
    depot.create_dir(depot_mapping, 'child_dir', 'parent_dir')


def create_test_depot(depots):
    name = 'test'
    depot = Depot(name, [], 'jrichardson12', 'jrichardson12')
    depots.create_depot(depot)


def get_depots():
    depot_mapping = DB(data_dir, "depots.db")
    depot_mapping.connection.commit()
    return Depots(depot_mapping), depot_mapping


def get_test_depot(depots):
    return depots.get_depot('test')
# ==============================================================================


# TODO: going to make this more like buckets, need to make into server
def main():
    depots, depot_mapping = get_depots()
    create_test_depot(depots)
    depot = get_test_depot(depots)
    create_test_dir(depot_mapping, depot)
    create_parent_dir(depot_mapping, depot)
    print(depot.get_dirs(depot_mapping))


if __name__ == "__main__":
    main()
