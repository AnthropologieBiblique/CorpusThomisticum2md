from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
import re
import fileinput
import os
import csv
import pathlib

class Liber:
	def __init__(self,titulus, indicat,numero,tagNumero):
		self.vinculumBiblia = vinculumBiblia('bibleReferences')
		self.titulus = titulus
		self.indicat = indicat
		self.numero = numero
		self.tagNumero = tagNumero
		self.prooemium = None
		self.capita = []
		self.transferre()
		self.construereMd()
		print(self.vinculumBiblia.bibleCounter)
	def addeCaput(self,caput):
		self.capita.append(caput)
	def __str__(self):
		liber = str(self.titulus)+"\n\n\n"
		for caput in self.capita:
			liber += str(caput)+"\n"
		return(liber+"\n")
	def construereMd(self):
		os.mkdir("../SummaContraGentiles/"+self.titulus)
		f = open("../SummaContraGentiles/"+self.titulus+'.md', 'w')
		f.write('---'+'\n')
		f.write('tags : '+'\n')
		f.write('- '+'SCG/'+self.tagNumero+'\n')
		f.write('---'+'\n\n')
		f.write('# '+self.titulus+'\n\n')
		via = "../SummaContraGentiles/"+self.titulus
		for caput in self.capita:
			f.write('[['+self.indicat+', cap. '+caput.indicat+']]'+'\n\n')
			caput.adMd(via,self.indicat,self.vinculumBiblia)
		f.close()
		return()
	def transferre(self):
		for numero in self.numero:
			# Téléchargement d'une page sur www.corpusthomisticum.org
			try:
			    url = "https://www.corpusthomisticum.org/scg"+str(numero)+".html"
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

			inCaput = False
			start = False

			for data in soup.find_all():
				print(data)
				if data.name == "div":
					if data.attrs['class'] == ['cuatro']:
						if inCaput:
							self.addeCaput(caput)
						caput = Caput(data.getText(),self.tagNumero)
						inCaput = True
						start = True
					elif data.attrs['class'] == ['centro'] and start:
						self.addeCaput(caput)
						inCaput = False						
				elif data.name == "p" and inCaput:
					numerus = Numerus(data.attrs['title'])
					for i in range(1,len(data.contents)):
						numerus.addeCorpus(str(data.contents[i]))
					caput.addeNumerus(numerus)

class Caput:
	def __init__(self,titulus,tagNumero):
		regex = re.compile(".*cap. ([0-9]*[-[0-9]*]?) \s?tit. (.*)")
		self.indicat = regex.match(titulus).group(1)
		self.titulus = regex.match(titulus).group(2)
		self.prooemium = None
		self.numeri = []
		self.tagNumero = tagNumero
	def addeNumerus(self,numerus):
		self.numeri.append(numerus)
	def __str__(self):
		caput = str(self.titulus)+"\n\n"
		caput += str(self.prooemium)+"\n"
		for numerus in self.numeri:
			caput += str(numerus) +"\n"
		return(caput+"\n")
	def adMd(self,via,liberIndicat,vinculumBiblia):
		f = open(via+'/'+liberIndicat+', '+'cap. '+self.indicat+'.md', 'w')
		f.write('---'+'\n')
		f.write('tags : '+'\n')
		f.write('- '+'SCG/'+self.tagNumero+'/cap.'+self.indicat+'\n')
		f.write('---'+'\n\n')
		f.write('### '+self.titulus+'\n\n')
		for numerus in self.numeri:
			f.write('###### '+numerus.index+'\n')
			f.write(vinculumBiblia.createLinks(numerus.corpus)+'\n\n')
		f.close()
		return()

class Numerus:
	def __init__(self,titulus):
		index = re.compile(".*(n. [0-9]*)")
		self.index = index.match(titulus).group(1)
		self.titulus = titulus
		self.corpus = ""
	def addeCorpus(self,addecorpus):
		italic = re.compile("<i>(.*?)</i>")
		if italic.match(addecorpus) == None:
			self.corpus += addecorpus
		else:
			self.corpus += "*"+italic.match(addecorpus).group(1)+"*"
	def __str__(self):
		return(str(self.titulus)+"\n"+str(self.corpus)+"\n")

class vinculumMachina:
	def __init__(self,ref,multiple,indicatList):
		self.indicatList = indicatList
		self.ref = ref
		self.regObjects = []
		if multiple == "TRUE":
			self.prefix = "(?<!(I|V))"
		else:
			self.prefix = "(?<!(I|V) )"
		self.middle = "((C{0,3})(XC|XL|L?X{0,3})(X|IX|IV|V?I{0,3}))(?<!"
		self.suffix = " )"
		self.roman = {'I':1,'V':5,'X':10,'L':50,'C':100,'IV':4,'IX':9,'XL':40,'XC':90}
		self.createRegObjects()
	def createRegObjects(self):
		for indicat in self.indicatList:
			regString = self.prefix+"("+indicat+" )"+self.middle+indicat+self.suffix
			regObject = re.compile(regString)
			self.regObjects.append(regObject)
	def roman2int(self,number):
		i = 0
		num = 0
		while i < len(number):
			if i+1<len(number) and number[i:i+2] in self.roman:
				num+=self.roman[number[i:i+2]]
				i+=2
			else:
				num+=self.roman[number[i]]
				i+=1
		return num
	def createLinks(self,string):
		retour = string
		counter = 0
		for regObject in self.regObjects:
			if regObject.search(retour) != None:
				counter += 1
				number = self.roman2int(regObject.search(retour).group(3))
				retour = regObject.sub("[["+self.ref+" "+str(number)+"]]",retour)
		return retour,counter


class vinculumBiblia:
	def __init__(self,bibleReferences):
		self.bibleCounter = 0
		self.listMachinae = []
		with open(bibleReferences+'.csv', mode='r') as csv_file:
			csv_reader = csv.DictReader(csv_file, delimiter=';')
			line_count = 0
			for row in csv_reader:
				indicatList = []
				for i in range(3):
					if row["Indicat"+str(i+1)] != "":
						indicatList.append(row["Indicat"+str(i+1)])
				self.listMachinae.append(vinculumMachina(row["Ref"],row["Multiple"],indicatList))
	def createLinks(self,string):
		for vinculumMachina in self.listMachinae:
			#print(vinculumMachina.createLinks(string))
			(string,addCounter) = vinculumMachina.createLinks(string)
			self.bibleCounter += addCounter
		return string


### MAIN ###

liber1Numero = [1001,1010,1014,1029,1037,1044,1072,1097]
liber2Numero = [2001,2006,2039,2046,2056,2091]
liber3Numero = [3001,3064,3111]
liber4Numero = [4001,4027,4079]

liber1 = Liber("Liber 1","Contra Gentiles, lib. 1",liber1Numero,"lib.1")
liber2 = Liber("Liber 2","Contra Gentiles, lib. 2",liber2Numero,"lib.2")
liber3 = Liber("Liber 3","Contra Gentiles, lib. 3",liber3Numero,"lib.3")
liber4 = Liber("Liber 4","Contra Gentiles, lib. 4",liber4Numero,"lib.4")

