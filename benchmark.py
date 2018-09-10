import csv
import random
from os import listdir
from os.path import isfile, join
from goose import Goose
import eatiht
import dragnet
import libextract.api
from boilerpipe.extract import Extractor

DATA_PATH = './data/htmlfiles/'

def random_html_file():
    """Returns a random filename in ./data/htmlfiles/"""
    nb_of_files = len([name for name in listdir(DATA_PATH)])
    list_of_files = [f for f in listdir(DATA_PATH) if isfile(join(DATA_PATH, f))]
    random_nb = random.randint(0,nb_of_files - 1)
    return random.choice(list_of_files)

def benchmark(extract_size=1200):
    """Picks a random html file and prints an extract of the result of each method"""
    random_file = random_html_file()
    with open(join(DATA_PATH,random_file), 'r') as f:
        html_string = f.read().replace('\n', '')

        # GOOSE
        try:
            g = Goose({'browser_user_agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0','enable_image_fetching':False })
            goose_article = g.extract(raw_html=html_string)
            goose_result = goose_article.cleaned_text
        except:
            goose_result = '    Goose error.'

        # EATIHT
        try:
            eatiht_result = eatiht.extract(html_string)
        except:
            eatiht_result = '   Eatiht error.'

        # DRAGNET

        try:
            dragnet_result = dragnet.extract_content(html_string)
        except:
            dragnet_result = '  Dragnet error.'

        # LIBEXTRACT

        try:
            textnodes = list(libextract.api.extract(html_string))
            libextract_result = textnodes[0].text_content()
        except:
            libextract_result = '   Libextract error.'

        # BOILERPIPE (CanolaExtractor)

        try:
            extractor = Extractor(extractor='CanolaExtractor', html=html_string)
            boilerpipe_result = extractor.getText()
        except:
            boilerpipe_result = '   Boilerpipe error.'

        # Results

        try:
            with open('./data/urls.csv', 'r') as csvfile: #finds the url associated with the file in a "filename-url" csv

                urls = dict((line['id'],line['url']) for line in csv.DictReader(csvfile))
                url = urls[random_file[:-5]]

            print('\n\n >>> URL n.'+ random_file[:-5] + ' : ' + url)
        except:
            print('\n\n (URL of the html file not found. To print the associated URL, please provide a urls.csv file featuring filename & url in /data)')
        print('\n\n     /// GOOSE /// \n')
        print(goose_result[:extract_size])
        print('\n\n     /// EATIHT /// \n')
        print(eatiht_result[:extract_size])
        print('\n\n     /// DRAGNET /// \n')
        print(dragnet_result[:extract_size])
        print('\n\n     /// LIBEXTRACT /// \n')
        print(libextract_result[:extract_size])
        print('\n\n     /// BOILERPIPE (CanolaExtractor) /// \n\n')
        print(boilerpipe_result[:extract_size])
        print('\n\n')

benchmark()

