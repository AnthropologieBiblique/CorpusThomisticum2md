from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
import re
import fileinput
import os
import csv
import pathlib

try:
    url = "https://www.corpusthomisticum.org/scg"+"4001"+".html"
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
    req = urllib.request.Request(url, headers = headers)
    resp = urllib.request.urlopen(req)
    respData = resp.read().decode('utf-8')
    saveFile = open('temp.html','w')
    saveFile.write(str(respData))
    saveFile.close()
except Exception as e:
    print(str(e))

# Ouverture du html pour parsing
file = open('temp.html', 'r')
contents = file.read()
soup = BeautifulSoup(contents, 'html.parser')
#print(soup.prettify())
print(soup)

for data in soup.find_all():
				if data.name == "div":
					if data.attrs['class'] == ['cuatro']:
						#regex = re.compile("cap. ([0-9]*) tit. (.*)")
						regex = re.compile(".*cap. ([0-9]*) tit. (.*)")
						titre = data.getText()
						print(titre)
						print(regex.match(titre))
						print(regex.match(titre).group(1))
						print(regex.match(titre).group(2))
				if data.name == "p":
					print(data.attrs['title'])
					for i in range(1,len(data.contents)):
						print(str(data.contents[i]))