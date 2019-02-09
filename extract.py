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
    "ACM Comput. Surv.": "CSUR",
    "Electr. Notes Theor. Comput. Sci.": "ENTCS",
    "ACM Trans. Internet Techn.": "TOIT",
    # "": "",
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

key = re.sub("https?://dblp.uni-trier.de/rec/[a-z]+/", "", key)

xml_url = "https://dblp.uni-trier.de/rec/xml/" + key
html_url = "https://dblp.uni-trier.de/rec/html/" + key

response = urllib.request.urlopen(xml_url)
htmlparser = etree.HTMLParser()
tree = etree.parse(response, htmlparser)

# grab title, drop trailing dot
title = tree.xpath("//dblp//title")[0].text
title = re.sub(".$", "", title)

# extract authors, drop '0001'-style unique identifiers and extracts last names
author_elements = tree.xpath("//dblp//author")
author_names = [el.text for el in author_elements]
author_names_cleaned = [re.sub(" [0-9][0-9][0-9][0-9]", "", author) for author in author_names]
author_lastnames = [author.split(" ")[-1] for author in author_names_cleaned]

if len(author_lastnames) == 1:
    authors_abbrv = author_lastnames[0][0:3]
else:
    authors_abbrv = "".join([a[0] for a in author_lastnames[0:3]])
    if len(author_lastnames) > 3:
        authors_abbrv += "+"

authors_list = ", ".join(author_names_cleaned)
ee = tree.xpath("//dblp//ee")
if len(ee) > 0:
    pub_url = ee[0].text
else:
    pub_url = ""
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
    venue_abbrv = venues[venue]
else:
    venue_abbrv = venue

cells = [pub_url, html_url, authors_list, authors_abbrv, title, venue, venue_abbrv, year]
row = "\t".join(cells)
print(row)
pyperclip.copy(row)
