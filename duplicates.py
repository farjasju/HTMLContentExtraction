import os
import os.path
import csv
import pprint
import filecmp
from collections import defaultdict

DIR_PATH = './data/contentfiles/'

def _manageDuplicate(duplicate, original):
    print(("Duplicate : " + duplicate['name'] + ", Original : " + original['name']))

def main():
    try:
        files = []
        entries = os.listdir(DIR_PATH)
        entries.sort()
        for entry in entries:
            entry_path = os.path.join(DIR_PATH, entry)
            if not os.path.isdir(entry_path):
                stats = os.stat(entry_path)
                files.append({'name': entry, 'path' : entry_path, 'size': stats.st_size})

        files.sort(lambda x, y: int(x['size']-y['size']))

        last_checked = {'name': '', 'path' : '', 'size': -1}

        # Identifying URL duplicates (same pages stored with different IDs)

        with open("./data/urls.csv", "r") as csvfile:
            urls = csv.DictReader(csvfile)
            id_url_dict = {} # links each file to its url
            url_dict = defaultdict(list)
            for line in urls:
                id_url_dict[line['id']] = line['url']
                url_dict[line['url']].append(line['id'])

            url_duplicates = set() # contains all the ids of the file that are url duplicates
            for url,id_list in url_dict.iteritems(): # d.items() in py3k
                if len(id_list) > 1:
                    for fileid in id_list[1:]:
                        url_duplicates.add(fileid)

        print(str(len(url_duplicates)) + " URL duplicates found.")

        # Building the csv with id, url, text content and duplicate info

        nb_duplicates = 0

        with open('./data/processed_urls.csv','w') as resultfile:
            fieldnames = ['id','url','extracted_content','is_url_duplicate', 'is_content_duplicate', 'is_empty']
            writer = csv.DictWriter(resultfile, fieldnames=fieldnames)
            writer.writeheader()

            for file in files:
                file_id = file['name'][:-4]
                file_url = id_url_dict[file_id]
                text_content = None
                is_url_duplicate = False
                is_content_duplicate = False
                is_empty = False

                with open(DIR_PATH + file_id + ".txt") as f:
                    text_content = f.read()

                if file_id in url_duplicates:
                    is_url_duplicate = True

                if file['size']==0:
                    is_empty = True
                    continue

                if file['size']==last_checked['size'] and not is_url_duplicate: # Detecting content duplicates (different URLs with the same content)
                    if filecmp.cmp(file['path'], last_checked['path'], shallow=False):
                        is_content_duplicate = True
                        nb_duplicates += 1
                last_checked = file

                writer.writerow({'id':file_id,'url':file_url,'extracted_content':text_content,'is_url_duplicate':is_url_duplicate,'is_content_duplicate':is_content_duplicate,'is_empty':is_empty})

        print(str(nb_duplicates) + " content duplicates found.")

    except KeyboardInterrupt:
        message("\nTerminated by user action")

main()