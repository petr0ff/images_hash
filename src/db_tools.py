import csv, requests, collections, codecs, cStringIO
from hash_tools import *

class UTF8Recoder:
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)
    def __iter__(self):
        return self
    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    def __init__(self, f, dialect=csv.excel, encoding="utf-8-sig", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)
    def next(self):
        '''next() -> unicode
        This function reads and returns the next line as a Unicode string.
        '''
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]
    def __iter__(self):
        return self

class UnicodeWriter:
    def __init__(self, f, dialect=csv.excel, encoding="utf-8-sig", **kwds):
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()
    def writerow(self, row):
        '''writerow(unicode) -> None
        This function takes a Unicode string and encodes it to the output.
        '''
        self.writer.writerow([s.encode("utf-8") for s in row])
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        data = self.encoder.encode(data)
        self.stream.write(data)
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

class Database:
    images_count = 0
    hashing = Hashing()

    def build_full_db(self, db_data):
        # Write headers
        with open(config.full_db_path, 'w') as db:
            a = UnicodeWriter(db, delimiter=',', lineterminator='\n')
            a.writerow(["Image name", "Image Link", "Image path", "dash"])

        # Write rows
        with open(config.full_db_path, 'a') as db:
            a = UnicodeWriter(db, delimiter=',', lineterminator='\n')
            for f in db_data:
                data = [[f['Name'], f['WikiUrl'], f['ImagePath'], f['dHash']]]
                a.writerows(data)

        print "Completed! Database is initiated."

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
                h = self.hashing.build_phash(Image.open(directory + f))
                data = [[f, h]]
                a.writerows(data)

        print "Completed! Database is initiated."

    def find_in_small_db(self, img):
        self.find_in_database(img, config.db_path)

    def find_in_full_database(self, img):
        self.find_in_database(img, config.full_db_path)

    def find_in_database(self, img, db_path):
        # Scan through Database to find similar pics, than order by difference
        h = self.hashing.build_dhash(img)
        diffs = {}
        with open(db_path, "rb") as db:
            reader = csv.reader(db, delimiter="\n")
            rownum = 0
            for row in reader:
                # Exclude header row
                if rownum > 0:
                    f_and_h = row[0].split(',')
                    h2 = f_and_h[-1]
                    if "No dHash Available" != h2:
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