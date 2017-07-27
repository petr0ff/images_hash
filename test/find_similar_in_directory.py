from utils.db_tools import Database
from utils.hash_tools import *
from utils import config
from PIL import Image
import time


def test():
    db = Database()
    img = Image.open(config.test_files_dir + 'test1.jpg')
    start = time.time()
    db.find_in_directory(img)
    finish = time.time()
    duration = "%0.3f" % (finish - start)

    print "\nDuration for duplicates search in directory with " + str(
        db.images_count) + " images is: " + duration + " ms"


if __name__ == "__main__":
    test()
