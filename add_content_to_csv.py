#!/usr/bin/python
# -*- coding: utf-8 -*-
from pprint import pprint
from lib.lru_trie import LRUTrie
import os
import os.path
import csv
import sys
import pprint
import filecmp
from collections import defaultdict
from datetime import datetime
sys.path.append(os.path.join(os.getcwd()))

CONTENT_FILES = './data/contentfiles/'
HTML_FILES = './data/htmlfiles/'
SOURCE_CSV = './data/source.csv'
RESULT_CSV = './data/result.csv'

MEDIA_FILE = './data/sources.csv'
MEDIAS_TRIE = LRUTrie.from_csv(MEDIA_FILE, detailed=True)

ID_COLUMN_NAME = 'stories_id'
MEDIACLOUD_ID_COLUMN_NAME = 'media_id'


def add_content_to_csv():

    with open(MEDIA_FILE, "r") as sources_csv:
        sources = csv.DictReader(sources_csv)
        mediacloud_id_dict = {}
        for line in sources:
            mediacloud_id_dict[line['mediacloud_id']] = line['webentity']

    with open(SOURCE_CSV, "r") as source_csv, open(RESULT_CSV, "w") as result_csv:
        fails = 0
        reader = csv.DictReader(source_csv)
        fieldnames = reader.fieldnames + ['extracted_content'] + ['webentity']
        writer = csv.DictWriter(
            result_csv, fieldnames=fieldnames)
        writer.writeheader()
        for line in reader:
            print(line['url'][:30], line[ID_COLUMN_NAME])
            file_id = line[ID_COLUMN_NAME]
            try:
                with open('data/contentfiles' + file_id + ".txt") as f:
                    text_content = f.read()
                line['extracted_content'] = text_content
            except:
                fails += 1
                line['extracted_content'] = ''
            line['webentity'] = mediacloud_id_dict.get(
                line[MEDIACLOUD_ID_COLUMN_NAME])
            writer.writerow(line)
        print(fails, 'fails')
