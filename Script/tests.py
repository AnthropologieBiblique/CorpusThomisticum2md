from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
import re
import fileinput
import os
import csv

# Attention aux ult. et ultimo
#" (CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})"

class vinculumMachina:
	def __init__(self,ref,multiple,indicatList):
		self.indicatList = indicatList
		self.ref = ref
		self.regObjects = []
		if multiple == "TRUE":
			self.prefix = "(?<!(I|V))"
		else:
			self.prefix = "(?<!(I|V) )"
		self.suffix = " ((CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3}))."
		self.roman = {'I':1,'V':5,'X':10,'L':50,'C':100,'IV':4,'IX':9,'XL':40,'XC':90}
		self.createRegObjects()
	def createRegObjects(self):
		for indicat in self.indicatList:
			regString = self.prefix+"("+indicat+")"+self.suffix
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
		for regObject in self.regObjects:
			if regObject.search(retour) != None:
				number = self.roman2int(regObject.search(retour).group(3))
				retour = regObject.sub("[["+self.ref+" "+str(number)+"]]",retour)
		return retour


class vinculumBiblia:
	def __init__(self,bibleReferences):
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
		


#indicatList = ["Ioan.","Ioann."]
#indicatList2 = ["II Ioan","II Ioann"]
#ref = "Jn"
#Jn = vinculumMachina(ref,False,indicatList)
#IJn = vinculumMachina("2 Jn",True,indicatList2)
#print(Jn.createLinks("Ceci est un test Ioan. IV. et Ioann. XCV. II Ioann XVIII. etc... "))


test = vinculumBiblia('bibleReferences')

print(test.listMachinae[49].createLinks("Ceci est un test Ioan. IV. et Ioann. XCV. I Ioann. XVIII. etc... "))





#jn = re.compile(".*"+"(Ioan.)"+" (CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})")
#print(jn.match("Ceci est un test Ioan. I etc...").group(4))


# Pour ceux avec un II devant, fonction speciale !

#(?<!(I|V) )Ioann. ((CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})).
#(?<!I)I Ioann. ((CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})).
