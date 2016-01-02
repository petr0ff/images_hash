from PIL import Image
import csv, os
import config


def build_dhash(image, hash_size=config.hash_size):
    # Resize image
    # Convert it to grayscale
    image = image.convert('L').resize(
        (hash_size + 1, hash_size),
        Image.BILINEAR,
    )

    # Comparing pixel by pixel (with neighbor pixel)
    difference = []
    for row in xrange(hash_size):
        for col in xrange(hash_size):
            pixel_left = image.getpixel((col, row))
            pixel_right = image.getpixel((col + 1, row))
            difference.append(pixel_left > pixel_right)

    # Convert to hexadecimal array
    decimal_value = 0
    hex_string = []
    for index, value in enumerate(difference):
        if value:
            decimal_value += 2 ** (index % 8)
        if (index % 8) == 7:
            hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
            decimal_value = 0

    # Return the hash string
    return ''.join(hex_string)


def hamming_distance(hash1, hash2):
    if len(hash1) != len(hash2):
        raise ValueError("Unequal length")
    return sum(bool(ord(ch1) - ord(ch2)) for ch1, ch2 in zip(hash1, hash2))


def similarity(distance):
    if distance == 0:
        return "Images are the same"
    if 0 < distance < 5:
        return "Most likely images are the same"
    if 5 < distance < 12:
        return "Images are similar but not the same"
    return "Images are different"


def calculate_hash_strings_in_dir(directory):
    # Get the dict of hash strings
    # Get the file names
    files = os.listdir(directory)
    # Write headers
    with open(config.db_path, 'w') as db:
        a = csv.writer(db, delimiter=',', lineterminator='\n')
        a.writerow(["Image path", "Hash"])

    # Write rows
    with open(config.db_path, 'a') as db:
        a = csv.writer(db, delimiter=',', lineterminator='\n')
        for f in files:
            h = build_dhash(Image.open(directory + f))
            data = [[f, h]]
            a.writerows(data)


def scan_for_similarity(img):
    # Scan through Database to find similar pics
    h = build_dhash(img)
    with open(config.db_path, "rb") as db:
        reader = csv.reader(db, delimiter="\n")
        rownum = 0
        for row in reader:
            # Exclude header row and the image itself.
            if rownum > 0:
                fandh = row[0].split(',')
                h2 = fandh[1]
                print similarity(hamming_distance(h, h2)) + ": " + fandh[0]
            rownum += 1

