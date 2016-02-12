from src.hash_tools import *
from src import config
from src.db_tools import Database


def init_db():
    db = Database()
    db.calculate_hash_strings_in_dir(config.images_dir)

if __name__ == "__main__":
    init_db()


