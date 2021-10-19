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


REGEX ROMAN :
"^M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$"


# Attention aux ult. et ultimo


M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})