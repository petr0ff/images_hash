from utils.db_tools import Database
from utils.hash_tools import *
from utils import config
from PIL import Image


def test(run_times=1):
    avg_duration = 0.0
    for i in range(run_times):
        hashing = Hashing()

        img1 = Image.open(config.images_dir + 'derevo1.jpg')
        img2 = Image.open(config.images_dir + 'derevo3.jpg')

        res = hashing.compare_pixel_by_pixel(img1, img2)

        print "Images the same?: " + str(res)

        avg_duration += float(hashing.current_duration)

    print "Average duration for " + str(run_times) + " runs is: " + str(avg_duration / run_times) + " ms"


if __name__ == "__main__":
    test()
