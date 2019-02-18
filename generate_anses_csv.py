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

MEDIA_FILE = './data/sources.csv'
MEDIAS_TRIE = LRUTrie.from_csv(MEDIA_FILE, detailed=True)

DIR_PATH = './data/contentfiles/'


def _manageDuplicate(duplicate, original):
    print(("Duplicate : " + duplicate['name'] +
           ", Original : " + original['name']))


def main():
    try:
        files = []
        entries = os.listdir(DIR_PATH)
        entries.sort()
        for entry in entries:
            entry_path = os.path.join(DIR_PATH, entry)
            if not os.path.isdir(entry_path):
                stats = os.stat(entry_path)
                files.append(
                    {'name': entry, 'path': entry_path, 'size': stats.st_size})

        files.sort(lambda x, y: int(x['size']-y['size']))

        last_checked = {'name': '', 'path': '', 'size': -1}

        # Identifying URL duplicates (same pages stored with different IDs)

        with open("./data/urls.csv", "r") as csvfile:
            urls = csv.DictReader(csvfile)
            id_url_dict = {}  # links each file to its url
            id_date_dict = {}  # links each file to its publication date
            url_dict = defaultdict(list)
            for line in urls:
                id_url_dict[line['id']] = line['url']
                date_str = line['date']
                try:
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                    id_date_dict[line['id']] = str(date_obj)
                except:
                    id_date_dict[line['id']] = ""
                url_dict[line['url']].append(line['id'])

            url_duplicates = set()  # contains all the ids of the file that are url duplicates
            for url, id_list in url_dict.iteritems():  # d.items() in py3k
                if len(id_list) > 1:
                    for fileid in id_list[1:]:
                        url_duplicates.add(fileid)

        print(str(len(url_duplicates)) + " URL duplicates found.")

        # Building the csv with id, url, text content and duplicate info

        nb_duplicates = 0
        media_recognition_errors_list = []

        with open('./data/anses_processed_urls.csv', 'w') as resultfile:
            fieldnames = ['id', 'url', 'media_name', 'webentity', 'publication_date',
                          'extracted_content', 'is_url_duplicate', 'is_content_duplicate', 'is_empty', 'contains_anses']
            writer = csv.DictWriter(resultfile, fieldnames=fieldnames)
            writer.writeheader()

            media_recognition_errors = 0

            for file in files:
                file_id = file['name'][:-4]
                file_url = id_url_dict[file_id]
                file_media = MEDIAS_TRIE.longest(file_url)

                if file_media is None:
                    if 'feedproxy.google.com' in file_url:
                        if 'agoravox' in file_url:
                            file_media_name = 'Agoravox'
                            file_media_entity = 'Agoravox.fr'
                        elif 'les-crises-fr' in file_url:
                            file_media_name = 'Les Crises'
                            file_media_entity = 'Les-Crises.fr'
                    else:
                        media_recognition_errors += 1
                        media_recognition_errors_list.append(file_url)
                        file_media_name = ''
                        file_media_entity = ''
                else:
                    file_media_name = file_media['name']
                    file_media_entity = file_media['webentity']

                print(" - " + file_media_name + " - " + file_media_entity +
                      " - " + str(file_id) + " - " + str(file_url)[:])
                file_date = id_date_dict[file_id]
                text_content = None
                is_url_duplicate = False
                is_content_duplicate = False
                is_empty = False
                contains_anses = False

                with open(DIR_PATH + file_id + ".txt") as f:
                    text_content = f.read()

                if 'anses' in text_content.lower():
                    contains_anses = True

                if file_id in url_duplicates:
                    is_url_duplicate = True

                if file['size'] == 0:
                    is_empty = True
                    continue

                # Detecting content duplicates (different URLs with the same content)
                if file['size'] == last_checked['size'] and not is_url_duplicate:
                    if filecmp.cmp(file['path'], last_checked['path'], shallow=False):
                        is_content_duplicate = True
                        nb_duplicates += 1
                last_checked = file

                writer.writerow({'id': file_id, 'url': file_url, 'media_name': file_media_name, 'webentity': file_media_entity, 'publication_date': file_date,
                                 'extracted_content': text_content, 'is_url_duplicate': is_url_duplicate, 'is_content_duplicate': is_content_duplicate, 'is_empty': is_empty, 'contains_anses': contains_anses})

            print(str(media_recognition_errors) + " media recognition errors.")
            print(sorted(media_recognition_errors_list))
        print(str(nb_duplicates) + " content duplicates found.")

    except KeyboardInterrupt:
        message("\nTerminated by user action")


main()
