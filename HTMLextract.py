import csv
import urllib
from multiprocessing import Pool
from contextlib import closing
import os, os.path

def urltoHTMLfile(line):
    """generates a HTML file from a csv row containing an ID and a URL"""
    urlid = line["id"]
    url = line["url"]
    if not os.path.isfile("./data/htmlfiles/" + str(urlid) + ".html"):
        try:
            sock = urllib.urlopen(url)
            html = sock.readlines()
            sock.close()
            with open("./data/htmlfiles/" + str(urlid) + ".html", "w") as file:
                    for line in html:
                        file.write(line+"\n")
                    #print("File " + str(urlid) + " generated.")
        except IOError as e:
            print(url)
            print("Erreur d acces a la page web : ", e)

with open("./data/urls.csv", "r") as csvfile, closing(Pool(processes=4)) as pool:
    urls = csv.DictReader(csvfile)
    nb_rows = sum(1 for _ in urls)
    
    nb = 0
    for _ in pool.imap_unordered(urltoHTMLfile, urls): #multiprocessing calls to urltoHTMLfile 
        nb += 1
        print("File " + str(nb) + "/" + nb_rows + " generated.")
