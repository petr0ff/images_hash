from PIL import Image
import csv, os, time
import config


def convert_and_resize_image(image):
    # 'L' is for grayscale
    return image.convert('L').resize(
        (config.hash_size + 1, config.hash_size),  # (width, height)
        Image.BILINEAR,  # bilinear interpolation
    )


def collect_pixel_diff(image):
    # difference is a binary matrix
    difference = []
    for row in xrange(config.hash_size):
        for col in xrange(config.hash_size):
            pixel_left = image.getpixel((col, row))
            pixel_right = image.getpixel((col + 1, row))
            difference.append(pixel_left > pixel_right)
    return difference


def convert_to_hex(difference):
    # linear
    decimal_value = 0
    hex_string = []
    # Run through binary matrix and convert each value to hex value
    for index, value in enumerate(difference):
        if value:
            decimal_value += 2 ** (index % 8)
        if (index % 8) == 7:
            # append 0 if hex is of one char
            hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
            decimal_value = 0
    # Convert array of hex values to the single string and return it
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


class Hashing:
    current_duration = ""

    def build_dhash(self, image):
        # 1. Convert image to grayscale
        # 2. Resize image to 9+8 size (width and height)
        start = time.time()
        image = convert_and_resize_image(image)
        # 3. Comparing pixel by pixel (with neighbor pixel)
        difference = collect_pixel_diff(image)
        # 4. Convert to hexadecimal array
        finish = time.time()
        self.current_duration = "%0.3f" % (finish - start)
        return convert_to_hex(difference)


class Database:
    images_count = 0

    def calculate_hash_strings_in_dir(self, directory):
        # Get the dict of hash strings: linear
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
                h = self.build_dhash(Image.open(directory + f))
                data = [[f, h]]
                a.writerows(data)

        print "Completed! Database is initiated."

    def find_in_database(self, img):
        # Scan through Database to find similar pics, than order by dirrerence
        hashing = Hashing()
        h = hashing.build_dhash(img)
        diffs = {}
        with open(config.db_path, "rb") as db:
            reader = csv.reader(db, delimiter="\n")
            rownum = 0
            for row in reader:
                # Exclude header row
                if rownum > 0:
                    f_and_h = row[0].split(',')
                    h2 = f_and_h[1]
                    diffs[f_and_h[0]] = hamming_distance(h, h2)
                rownum += 1
            self.images_count = rownum - 1

        # Print results by the similarity value
        diffs = sorted([(value, key) for (key, value) in diffs.items()])
        for val in diffs:
            print similarity(val[0]) + ": " + val[1] + ", distance is: " + str(val[0])

    def find_in_directory(self, img, directory=config.images_dir):
        # Scan through directory to find similar pics, than order by dirrerence
        hashing = Hashing()
        h = hashing.build_dhash(img)
        diffs = {}
        files = os.listdir(directory)
        self.images_count = len(files)

        for f in files:
            h2 = hashing.build_dhash(Image.open(directory + f))
            diffs[f] = hamming_distance(h, h2)

        # Print results by the similarity value
        diffs = sorted([(value, key) for (key, value) in diffs.items()])
        for val in diffs:
            print similarity(val[0]) + ": " + val[1] + ", distance is: " + str(val[0])
