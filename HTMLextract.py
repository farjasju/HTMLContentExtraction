#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import urllib
from multiprocessing import Pool
from contextlib import closing
import os
import os.path

from lazypool import LazyThreadPoolExecutor

import ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def urltoHTMLfile(line):
    """generates a HTML file from a csv row containing an ID and a URL"""
    urlid = line["stories_id"]
    url = line["url"]
    if not os.path.isfile("./data/htmlfiles/" + str(urlid) + ".html"):
        try:
            sock = urllib.urlopen(url, context=ctx)
            html = sock.readlines()
            sock.close()
            with open("./data/htmlfiles/" + str(urlid) + ".html", "w") as file:
                for line in html:
                    file.write(line+"\n")
                #print("File " + str(urlid) + " generated.")
        except IOError as e:
            print(url)
            print("Erreur d acces a la page web : ", e)


def extract_html(csvfile="./data/gj.csv"):

    pool = LazyThreadPoolExecutor(4)
    with open(csvfile, "r") as csvfile:
        urls = csv.DictReader(csvfile)
        nb = 0
        if not os.path.exists(os.path.join('data', 'htmlfiles')):
            os.makedirs(os.path.join('data', 'htmlfiles'))
        for _ in pool.map(urltoHTMLfile, urls):
            nb += 1
            print("File " + str(nb) + " generated.")
    pool.shutdown()

    # with open(csvfile, "r") as csvfile, closing(Pool(processes=4)) as pool:
    #     urls = csv.DictReader(csvfile)
    #     nb = 0
    #     if not os.path.exists(os.path.join('data', 'htmlfiles')):
    #         os.makedirs(os.path.join('data', 'htmlfiles'))
    #     # multiprocessing calls to urltoHTMLfile
    #     for _ in pool.imap_unordered(urltoHTMLfile, urls):
    #         nb += 1
    #         print("File " + str(nb) + " generated.")
