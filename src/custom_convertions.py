from PIL import Image
import config
import numpy as np


def weighted_average(pixel):
    return 0.299*pixel[0] + 0.587*pixel[1] + 0.114*pixel[2]


def convert_to_grayscale(image):
    if image.mode == 'RGB':
        # Getting image as a pixels array
        pixels = np.asarray(image)
        # Convert each pixel via formula Y' =  0.299 R' + 0.587 G' + 0.114 B'
        gray = np.dot(pixels[...,:3], [0.299, 0.587, 0.144])
        # Overwrite existing image with new pixels array
        image = Image.fromarray(np.uint8(gray))
    return image


def resize_image(image):
    return image.resize(
        (config.hash_size + 1, config.hash_size), # (width, height)
        Image.BILINEAR, # linear interpolation
    )