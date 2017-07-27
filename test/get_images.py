from utils.hash_tools import Hashing
from utils.db_tools import Database
import requests, collections
from bs4 import BeautifulSoup
from lxml import html
from utils import config
from PIL import Image
import os


def store_fl():
    hashing = Hashing()
    db = Database()
    links = []
    names = []
    imgs = []
    db_data = []
    base_url = "https://en.wikipedia.org"
    house_plants = base_url + "/wiki/Category:House_plants"
    r = requests.get(house_plants)
    data = r.text
    soup = BeautifulSoup(data)
    print "Getting plant names..."
    for link in soup.select("div.mw-category-group a"):
        lnk = link.get('href')
        name = link.get('title')
        links.append(lnk)
        names.append(name)

    print "Getting plant images..."
    for link, name in zip(links, names):
        r = requests.get(base_url + link)
        data = r.text
        soup = BeautifulSoup(data)
        img = soup.select("table.infobox a.image img")
        if img:
            imgs.append(img[0].get('utils'))
        else:
            imgs.append("No image for " + name)

    print "Downloading plant images, counting dHash, preparing csv file..."
    for img, name, link in zip(imgs, names, links):
        item_data = collections.OrderedDict()
        if "No image" not in img:
            img_path = config.images_dir + name + ".jpg"
            if not os.path.exists(img_path):
                r = requests.get("http:" + img, stream=True)
                if r.status_code == 200:
                    with open(img_path, 'wb') as f:
                        for chunk in r.iter_content():
                            f.write(chunk)

        item_data['Name'] = name
        item_data['WikiUrl'] = base_url + link
        if "No image" not in img:
            item_data['ImagePath'] = img_path
            imgh = Image.open(img_path)
            item_data['dHash'] = hashing.build_dhash(imgh)
        else:
            item_data['ImagePath'] = "No Image Available"
            item_data['dHash'] = "No dHash Available"

        db_data.append(item_data)

    db.build_full_db(db_data)


if __name__ == "__main__":
    store_fl()