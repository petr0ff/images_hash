from src.hash_tools import *
from src import config
from PIL import Image

img1 = Image.open(config.test_files_dir + 'test1.jpg')
scan_for_similarity(img1)


