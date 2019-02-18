import csv
import sys
import random
from os import listdir
from os.path import isfile, join, abspath
import webbrowser
# from goose import Goose
# import eatiht
import dragnet
import libextract.api
from newspaper import Article
import justext
# try:
#     from boilerpipe.extract import Extractor
# except:
#     from boilerpipe3.extract import Extractor

DATA_PATH = './data/htmlfiles/'
RESULT_FILE = './data/justextvsdragnet.csv'


def rank(input):
    if input == '&':
        score = 1
    elif input == 'é':
        score = 0.8
    elif input == '"':
        score = 0.5
    elif input == "'":
        score = 0
    return score


def random_html_file():
    """Returns a random filename in ./data/htmlfiles/"""
    nb_of_files = len([name for name in listdir(DATA_PATH)])
    list_of_files = [f for f in listdir(
        DATA_PATH) if isfile(join(DATA_PATH, f))]
    random_nb = random.randint(0, nb_of_files - 1)
    return random.choice(list_of_files)


def benchmark(extract_size=800):
    """Picks a random html file and prints an extract of the result of each method"""
    random_file = random_html_file()
    with open(join(DATA_PATH, random_file), 'r') as f:
        html_string = f.read()

        # GOOSE
        try:
            g = Goose({'browser_user_agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
                       'enable_image_fetching': False})
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
        except Exception as e:
            dragnet_result = '  Dragnet error: ' + str(e)

        # LIBEXTRACT

        try:
            textnodes = list(libextract.api.extract(html_string))
            libextract_result = textnodes[0].text_content()
        except:
            libextract_result = '   Libextract error.'

        # BOILERPIPE (CanolaExtractor)

        try:
            extractor = Extractor(
                extractor='CanolaExtractor', html=html_string)
            boilerpipe_result = extractor.getText()
        except:
            boilerpipe_result = '   Boilerpipe error.'

        # NEWSPAPER

        try:
            article = Article('url')
            article.download(input_html=html_string)
            article.parse()
            print('Auteurs:', article.authors)
            print('Date de publication:', article.publish_date)
            newspaper_result = article.text
        except:
            newspaper_result = '   Newspaper error.'

        # JUSTEXT

        try:
            paragraphs = justext.justext(
                html_string, justext.get_stoplist("French"))
            print('PARAGRAPHS')
            for p in paragraphs:
                if not p.is_boilerplate:
                    print(p.text)
            justext_result = '\n'.join(
                paragraph.text for paragraph in paragraphs if not paragraph.is_boilerplate)
            print('JUSTEXT_RESULT', justext_result)

        except Exception as e:
            justext_result = '   Justext error: ' + str(e)
            print(justext_result)

        # Results

        try:
            # finds the url associated with the file in a "filename-url" csv
            with open('./data/urls.csv', 'r') as csvfile:

                urls = dict((line['id'], line['url'])
                            for line in csv.DictReader(csvfile))
                url = urls[random_file[:-5]]

            print('\n\n >>> URL n.' + random_file[:-5] + ' : ' + url)
        except:
            print('\n\n (URL of the html file not found. To print the associated URL, please provide a urls.csv file featuring filename & url in /data)')
        # webbrowser.open(url, autoraise=False)
        path = abspath('temp.html')
        local_url = 'file://' + path
        with open(path, 'w') as f:
            f.write(html_string)
        webbrowser.open(local_url)

        # print('\n\n     /// GOOSE /// \n')
        # print(goose_result[:extract_size])
        # print('\n\n     /// EATIHT /// \n')
        # print(eatiht_result[:extract_size])
        print('\n ------ [[DRAGNET]] ------',
              len(dragnet_result), 'caractères\n')
        print(dragnet_result[:extract_size] +
              '\n...\n' + dragnet_result[-extract_size:])
        print('\n ------ [[NEWSPAPER]] ------',
              len(newspaper_result), 'caractères\n')
        print(newspaper_result[:extract_size] +
              '\n...\n' + newspaper_result[-extract_size:])
        print('\n ------ [[JUSTEXT]] ------',
              len(justext_result), 'caractères\n')
        print(justext_result[:extract_size] +
              '\n...\n' + justext_result[-extract_size:])
        # print('\n\n     /// LIBEXTRACT /// \n')
        # print(libextract_result[:extract_size])
        # print('\n\n     /// BOILERPIPE (CanolaExtractor) /// \n\n')
        # print(boilerpipe_result[:extract_size])
        # print('\n\n')
        return(url)


if __name__ == '__main__':
    benchmarking = True
    fieldnames = ['Dragnet_result',
                  'Newspaper_result', 'Justext_result', 'url']

    if not isfile(RESULT_FILE):
        with open(RESULT_FILE, 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

    with open(RESULT_FILE, 'a') as result_file:
        writer = csv.DictWriter(result_file, fieldnames=fieldnames)
        while benchmarking:
            url = benchmark()
            while True:
                dragnet_input = input(
                    '\n >> Dragnet result (from 1 for success to 4 for fail, p for pass, q for quit): ')
                if dragnet_input not in ('&', 'é', '"', "'", 'q', 'p'):
                    print("Choice must be either between 1 and 4 or 'q'")
                else:
                    break
            if dragnet_input == 'p':
                continue
            elif dragnet_input == 'q':
                benchmarking = False
                continue
            while True:
                newspaper_input = input(
                    '\n >> Newspaper result (from 1 for success to 4 for fail, p for pass, q for quit): ')
                if newspaper_input not in ('&', 'é', '"', "'", 'q', 'p'):
                    print("Choice must be either between 1 and 4 or 'q'")
                else:
                    break
            while True:
                justext_input = input(
                    '\n >> Justext result (from 1 for success to 4 for fail, p for pass, q for quit): ')
                if justext_input not in ('&', 'é', '"', "'", 'q', 'p'):
                    print("Choice must be either between 1 and 4 or 'q'")
                else:
                    break
            print(dragnet_input, newspaper_input)
            if dragnet_input == 'q' or newspaper_input == 'q':
                benchmarking = False
                continue
            elif dragnet_input == 'p' or newspaper_input == 'p':
                continue
            else:
                dragnet_score = rank(dragnet_input)
                newspaper_score = rank(newspaper_input)
                justext_score = rank(justext_input)
                writer.writerow({'Dragnet_result': dragnet_score,
                                 'Newspaper_result': newspaper_score, 'Justext_result': justext_score, 'url': url})
