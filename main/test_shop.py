import csv, requests, collections, codecs, cStringIO
from bs4 import BeautifulSoup
from lxml import html


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

def store_goods():
    categs_storage = {
        "Столы".decode('utf-8'): "Мебель".decode('utf-8'),
        "Мини-кухни".decode('utf-8'): "Мебель".decode('utf-8'),
        "Офисные перегородки".decode('utf-8'): "Мебель".decode('utf-8'),
        "Рецепции".decode('utf-8'): "Мебель".decode('utf-8'),
        "Металлическая мебель".decode('utf-8'): "Мебель".decode('utf-8'),
        "Медицинская мебель".decode('utf-8'): "Мебель".decode('utf-8'),
        "Зоны коммуникаций".decode('utf-8'): "Оборудование".decode('utf-8'),
        "Офисный свет".decode('utf-8'): "Оборудование".decode('utf-8'),
        "Кабинеты руководителей".decode('utf-8'): "Мебель".decode('utf-8'),
        "Мебель для персонала".decode('utf-8'): "Мебель".decode('utf-8'),
        "Кресла и стулья".decode('utf-8'): "Мебель".decode('utf-8'),
        "Мягкая мебель".decode('utf-8'): "Мебель".decode('utf-8')
    }

    item_data = collections.OrderedDict()
    #item_data['ID товара'.decode('utf-8')] = ""
    item_data['Название товара'.decode('utf-8')] = ""
    item_data['Псевдоним'.decode('utf-8')] = ""
    item_data['Артикул'.decode('utf-8')] = ""
    #item_data['Краткое описание'.decode('utf-8')] = ""
    #item_data['Описание'.decode('utf-8')] = ""
    item_data['Категория'.decode('utf-8')] = ""
    item_data['Дополнительные изображения'.decode('utf-8')] = ""
    item_data['Основное изображение'.decode('utf-8')] = ""
    #item_data['Цена'.decode('utf-8')] = ""
    #item_data['Шаблон товара'.decode('utf-8')] = "default"
    #item_data['Мета-загаловок'.decode('utf-8')] = ""
    #item_data['Мета-кейвордс'.decode('utf-8')] = ""
    #item_data['Характеристики'.decode('utf-8')] = ""
    #item_data['Количество'.decode('utf-8')] = "1"

    with open('C://shop//goods.csv','a') as fout:
        writer = UnicodeWriter(fout, lineterminator='\n', delimiter=";") #
        writer.writerow(item_data.keys())

    ind = 1

    categories = []
    base_url = "https://ru.wikipedia.org/w/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%A0%D0%B0%D1%81%D1%82%D0%B5%D0%BD%D0%B8%D1%8F_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83&from=%D0%90"
    r = requests.get(base_url)
    data = r.text
    soup = BeautifulSoup(data)
    for link in soup.find_all('a'):
        lnk = link.get('href')
        if "/category/" in lnk:
            categories.append(lnk)

    #print "There are totally " + str(len(categories)) + " categories"
    #categories = ['http://ergodesign.biz/category/ekonom-klass-personal']

    for categ in categories:
        tovari = []
        r = requests.get(categ)
        data = r.text
        soup = BeautifulSoup(data)
        for link in soup.find_all('a'):
            lnk = link.get('href')
            if "/page/" in lnk:
                if "http" not in lnk:
                    lnk = "http://ergodesign.biz" + lnk
                tovari.append(lnk)

        #print "There are " + str(len(tovari)) + " items in category " + categ + " let's store information for them"
        #tovari = ['http://ergodesign.biz/page/mebel-dlja-personala-mono-ljuks']

        if len(tovari) > 0:
            for idx,item in enumerate(tovari, ind):
                item_data = collections.OrderedDict()
                #Set default values
                #item_data['ID товара'.decode('utf-8')] = ""
                item_data['Название товара'.decode('utf-8')] = ""
                item_data['Псевдоним'.decode('utf-8')] = ""
                item_data['Артикул'.decode('utf-8')] = ""
                #item_data['Краткое описание'.decode('utf-8')] = ""
                #item_data['Описание'.decode('utf-8')] = ""
                item_data['Категория'.decode('utf-8')] = ""
                item_data['Дополнительные изображения'.decode('utf-8')] = ""
                item_data['Основное изображение'.decode('utf-8')] = ""
                #item_data['Цена'.decode('utf-8')] = ""
                #item_data['Шаблон товара'.decode('utf-8')] = "default"
                #item_data['Мета-загаловок'.decode('utf-8')] = ""
                #item_data['Мета-кейвордс'.decode('utf-8')] = ""
                #item_data['Характеристики'.decode('utf-8')] = ""
                #item_data['Количество'.decode('utf-8')] = "-1"

                descr = "Описание".decode('utf-8')
                details = "арактеристики".decode('utf-8')

                ri = requests.get(item)
                parsed_body = html.fromstring(ri.text)

                #Collect item data: name, price, description, details, etc.
                item_category = parsed_body.xpath("//*[@class='breadcrumbs']/a[contains(@href, '/category/')]/text()")
                item_sub_category = parsed_body.xpath("//*[@class='breadcrumbs']/a[contains(@href, '/category/')][2]/text()")
                item_name = parsed_body.xpath("//*[@class='good_header']/text()")
                item_price = parsed_body.xpath("//div[contains(@class, 'good-prise-order__price')]/text()")
                item_desc = parsed_body.xpath("//*[contains(., '" + descr + "')]/following-sibling::*")
                item_chars = parsed_body.xpath("//*[contains(., '" + details + "')]/following-sibling::*")
                item_images = parsed_body.xpath("//div[contains(@class, 'content')]//div[contains(@id, 'gallery')]//img")
                item_images_plus = parsed_body.xpath("//table[@class='pricelist']//img")

                #Set ID
                #item_data['ID товара'.decode('utf-8')] = str(idx)
                #Set pseudonim
                item_data['Псевдоним'.decode('utf-8')] = item.split('/')[-1]
                item_data['Артикул'.decode('utf-8')] = "atr000" + str(idx)
                #If parser found info, let's store it
                if len(item_category) > 0:
                    parent_categ = categs_storage.get(item_category[0])
                    if parent_categ is not None:
                        item_data['Категория'.decode('utf-8')] = parent_categ + "/" + item_category[0]
                        #item_data['Мета-кейвордс'.decode('utf-8')] = parent_categ + "," + item_category[0]
                    else:
                        item_data['Категория'.decode('utf-8')] = item_category[0]
                        #item_data['Мета-кейвордс'.decode('utf-8')] = item_category[0]
                if len(item_sub_category) > 0:
                    parent_categ = categs_storage.get(item_category[0])
                    if parent_categ is not None:
                        item_data['Категория'.decode('utf-8')] = parent_categ + "/" + item_category[0] + "/" + item_sub_category[0]
                        #item_data['Мета-кейвордс'.decode('utf-8')] = parent_categ + "," + item_category[0] + "," + item_sub_category[0]
                    else:
                        item_data['Категория'.decode('utf-8')] = item_category[0] + "/" + item_sub_category[0]
                        #item_data['Мета-кейвордс'.decode('utf-8')] = item_category[0] + "," + item_sub_category[0]
                if len(item_name) > 0:
                    item_data['Название товара'.decode('utf-8')] = item_name[0]
                    #item_data['Мета-загаловок'.decode('utf-8')] = item_name[0]
                    #item_data['Мета-кейвордс'.decode('utf-8')] += "," + item_name[0]
##                if len(item_price) > 0:
##                    item_data['Цена'.decode('utf-8')] = re.sub("\D", "", item_price[0])
##                if len(item_desc) > 0:
##                    item_data['Описание'.decode('utf-8')] = item_desc[0].text_content().replace('\n', '')
##                if len(item_chars) > 0:
##                    details = os.linesep.join([s.lstrip() for s in item_chars[0].text_content().splitlines() if s])
##                    item_data['Краткое описание'.decode('utf-8')] = details.strip()
                #Save images
                if len(item_images) > 0:
                    if len(item_images_plus) > 0:
                        item_images = item_images + item_images_plus
                    for img in item_images:
                        try:
                            if "/mini/" in img.attrib['src']:
                                r = requests.get(img.attrib['src'].replace('mini/',''), stream=True)
                            else:
                                r = requests.get(img.attrib['src'], stream=True)
                            if r.status_code == 200:
                                with open('C://shop//images//%s' % img.attrib['src'].split('/')[-1], 'wb') as f:
                                    for chunk in r.iter_content():
                                        f.write(chunk)
                            if len(item_images) == 1:
                                item_data['Основное изображение'.decode('utf-8')] = item_images[0].attrib['src'].split('/')[-1]+"#"
                            elif len(item_images) > 1:
                                item_data['Основное изображение'.decode('utf-8')] = item_images[0].attrib['src'].split('/')[-1]+"#"
                                imgs_names = ""
                                i=1
                                for i in range(i, len(item_images)):
                                    imgs_names += item_images[i].attrib['src'].split('/')[-1]+"#"
                                item_data['Дополнительные изображения'.decode('utf-8')] = imgs_names
                        except:
                            print "Couldn't download " + str(img.attrib['src'])

                #Write all info to the csv
                with open('C://shop//goods.csv','a') as fout:
                    writer = UnicodeWriter(fout, lineterminator='\n', delimiter=";") #
                    writer.writerow(item_data.values())

                ind = idx + 1

if __name__ == "__main__":
    store_goods()