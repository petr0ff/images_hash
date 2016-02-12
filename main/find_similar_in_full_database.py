from src.db_tools import Database
from src.hash_tools import *
from src import config
from PIL import Image
import time


def test():
    db = Database()
    img = Image.open(config.test_files_dir + 'Boea.jpg')
    db.find_in_full_database(img)

if __name__ == "__main__":
    test()
