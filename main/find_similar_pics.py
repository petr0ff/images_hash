from PIL import Image
from src.hash_tools import *
from src import config

#calculate_hash_strings_in_dir(config.images_dir)

img1 = Image.open(config.test_files_dir + 'test1.jpg')
scan_for_similarity(img1)


