from src.hash_tools import Hashing
from src import config
from PIL import Image
import time


def test():
    hashing = Hashing()
    img = Image.open(config.test_files_dir + 'test1.jpg')
    start = time.time()
    hashing.find_in_database(img)
    finish = time.time()
    duration = "%0.3f" % (finish - start)

    print "\nAverage duration for duplicates search in database with " + str(
        hashing.images_count) + " entries is: " + duration + " ms"


if __name__ == "__main__":
    test()
