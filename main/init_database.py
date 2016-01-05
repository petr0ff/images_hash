from src.hash_tools import Hashing
from src import config


def init_db():
    hashing = Hashing()
    hashing.calculate_hash_strings_in_dir(config.images_dir)

if __name__ == "__main__":
    init_db()


