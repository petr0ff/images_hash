from src.hash_tools import *
from src import config


def init_db():
    db = Database()
    db.calculate_hash_strings_in_dir(config.images_dir)

if __name__ == "__main__":
    init_db()


