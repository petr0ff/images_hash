from src.hash_tools import *
from src import config
from PIL import Image


img1 = Image.open(config.images_dir + 'derevo1.jpg')
img2 = Image.open(config.images_dir + 'derevo8.jpg')

hash1 = build_dhash(img1)
hash2 = build_dhash(img2)

dist = hamming_distance(hash1, hash2)

print hash1 + ", " + hash2 + " The same?: " + str(similarity(dist)) + ". Difference: " + str(dist)