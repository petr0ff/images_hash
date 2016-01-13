from src.hash_tools import *
from src import config
from PIL import Image


def test():
    hashing = Hashing()
    img1 = Image.open(config.images_dir + 'risunok_1.jpg')
    # image = convert(img1)
    # #image = convert_and_resize_image(img1, 9, 8)
    # image.save(config.images_dir + 'converted1.jpg')
    hash1 = hashing.build_dhash(img1)

if __name__ == "__main__":
    test()
