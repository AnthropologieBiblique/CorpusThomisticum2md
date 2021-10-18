from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
import re
import fileinput
import os

titulus = "I q. 3 a. 1 arg. 1"

indexArg = re.compile(".*(arg.*)")
indexSc = re.compile("(s. c.)")
indexCo = re.compile("(co.)")
indexAd = re.compile("(ad [0-9]*)")

print(indexArg.match(titulus).group(1))