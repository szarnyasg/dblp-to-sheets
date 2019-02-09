#!/usr/bin/env python3

import re
import sys
import urllib.request

import pyperclip as pyperclip
from lxml import etree

venues = {
    "ACM Trans. Database Syst.": "TODS",
    "Inf. Syst.": "IS",
    "VLDB J.": "VLDBJ",
    "Software and System Modeling": "SOSYM",
    "IEEE Trans. Knowl. Data Eng.": "TKDE",
    "Data Knowl. Eng.": "DKE",
    "J. ACM": "JACM",
    "GRADES@SIGMOD/PODS": "GRADES",
    "PVLDB": "VLDB",
    "SIGMOD Conference": "SIGMOD",
    # "": "",
    # "": "",
    # "": "",
    # "": "",
    # "": "",
    # "": "",
}

if len(sys.argv) <= 1:
    print("No DBLP key provided")
    sys.exit(1)

key = sys.argv[1]
#key = "journals/tods/Chen76"
#key = "journals/corr/OngPV14"
#key = "journals/dagstuhl-manifestos/AbiteboulABBCD018"

key = re.sub("https?://dblp.uni-trier.de/rec/html/", "", key)

url = "https://dblp.uni-trier.de/rec/xml/" + key

response = urllib.request.urlopen(url)
htmlparser = etree.HTMLParser()
tree = etree.parse(response, htmlparser)

# grab title, drop trailing dot
title = tree.xpath("//dblp//title")[0].text
title = re.sub(".$", "", title)

author_elements = tree.xpath("//dblp//author")
author_names = [el.text for el in author_elements]
author_lastnames = [author.split(" ")[-1] for author in author_names]

if len(author_lastnames) == 1:
    refkey_author = author_lastnames[0] #[0:3]
else:
    refkey_author = "".join([a[0] for a in author_lastnames[0:3]])
    if len(author_lastnames) > 3:
        refkey_author += "+"

authors_list = ", ".join(author_names)
ee = tree.xpath("//dblp//ee")[0].text
year = tree.xpath("//dblp//year")[0].text

if key.startswith("conf"):
    venue = tree.xpath("//dblp//booktitle")[0].text
elif key.startswith("journal"):
    venue = tree.xpath("//dblp//journal")[0].text
else:
    print("Unsupported venue type")
    sys.exit(2)

# abbreviate venue name if possible
if venue in venues:
    refkey_venue = venues[venue]
else:
    refkey_venue = venue

refkey = refkey_author + ", " + refkey_venue + "'" + year[2:4]

row = ("[" + refkey + "]\t" +
    ee + "\t" +
    url + "\t" + "\t" +
    authors_list + "\t" +
    title + "\t" +
    venue + "\t" +
    year)
print(row)
pyperclip.copy(row)