#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
from os import walk
import hashlib
from multiprocessing import Pool
from contextlib import closing
import dragnet

HTML_FILES_PATH = os.path.join('data', 'htmlfiles')
CONTENT_FILES_PATH = os.path.join('data', 'contentfiles')


def HTML_to_content(filename):
    """creates a txt file in /data/contentfiles/ with the main content of the HTML file"""
    if not os.path.isfile(os.path.join(CONTENT_FILES_PATH, filename[:-5] + '.txt')):
        with open(os.path.join(HTML_FILES_PATH, filename)) as f:
            html_string = f.read()
            try:
                dragnet_result = dragnet.extract_content(html_string)
            except Exception as e:
                print('Dragnet extraction error:', e)
                dragnet_result = 'Dragnet extraction error'

        with open(CONTENT_FILES_PATH + filename[:-5] + '.txt', 'w') as result:
            result.write(dragnet_result.encode('utf-8'))


def extract_content():
    nb_of_processed_files = 0
    if not os.path.exists(os.path.join('data', 'contentfiles')):
        os.makedirs(os.path.join('data', 'contentfiles'))
    for html_file in os.listdir(HTML_FILES_PATH):
        HTML_to_content(html_file)
        nb_of_processed_files += 1
        print ("Content of " + html_file + " extracted to " + CONTENT_FILES_PATH +
               html_file[:-5] + ".txt (File n°" + str(nb_of_processed_files) + ")")
