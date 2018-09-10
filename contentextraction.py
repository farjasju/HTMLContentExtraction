import sys
import os, os.path
from os import walk
import hashlib
from multiprocessing import Pool
from contextlib import closing
import dragnet

HTML_FILES_PATH = './data/htmlfiles/'
CONTENT_FILES_PATH = './data/contentfiles/'

def HTML_to_content(filename):
    """creates a txt file in /data/contentfiles/ with the main content of the HTML file"""
    if not os.path.isfile(CONTENT_FILES_PATH + filename[:-5] + '.txt'):
        with open(HTML_FILES_PATH + filename) as f:
            html_string = f.read().replace('\n', '')
            try:
                dragnet_result = dragnet.extract_content(html_string)
            except:
                print('Dragnet extraction error')

        with open(CONTENT_FILES_PATH + filename[:-5] + '.txt', 'w') as result:
            result.write(dragnet_result.encode('utf-8'))

nb_of_processed_files = 0
for html_file in os.listdir(HTML_FILES_PATH):
    HTML_to_content(html_file)
    nb_of_processed_files += 1
    print ("Content of " + html_file + " extracted to " + CONTENT_FILES_PATH + html_file[:-5] + ".txt (File " + str(nb_of_processed_files) + "/10714)")

