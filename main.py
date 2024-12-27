import os
from pathlib import Path


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


class Dir:
    def __init__(self):
        pass

    def create_dir(self):
        pass

    def update_dir(self):
        pass

    def get_dir(self):
        pass

    def delete_dir(self):
        pass


class File:
    def __init__(self, name: str, location: list):
        self.name = name
        self.location = location
        self.project_path = Path.cwd()

    def create_file(self):
        file_dir = os.path.join(Path.cwd(), self.location)
        print(file_dir)
        # print(Path(self.project_path / self.location))
        # print(Path.is_dir(self.project_path / self.location))
        # print(self.location)
        # print(self.project_path)

    def rename_file(self, name):
        pass

    def get_file(self):
        pass

    def delete_file(self):
        pass

    def write_to_file(self, data):
        pass


# TODO: going to make this more like buckets, need to make into server
def main():
    # file_system = FileSystem()
    # file_system.config('data', '~/test')
    # file_system.create_file_system()
    file = File('test', '/data')
    new_file = File('test2', '/data/test')
    file.create_file()
    new_file.create_file()


if __name__ == "__main__":
    main()
