from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
import re
import fileinput
import os

# Attention aux ult. et ultimo
#" (CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})"

class vinculumMachina:
	def __init__(self,indicatList,ref):
		self.indicatList = indicatList
		self.ref = ref
		self.regObjects = []
		self.createRegObjects()
	def createRegObjects(self):
		for indicat in self.indicatList:
			regString = "("+indicat+")"+" ((CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3}))."
			regObject = re.compile(regString)
			self.regObjects.append(regObject)
	def roman2int(self,number):
		roman = {'I':1,'V':5,'X':10,'L':50,'C':100,'IV':4,'IX':9,'XL':40,'XC':90}
		i = 0
		num = 0
		print(number)
		print(len(number))
		while i < len(number):
			if i+1<len(number) and number[i:i+2] in roman:
				num+=roman[number[i:i+2]]
				i+=2
				print(num)
				print(i)
			else:
				num+=roman[number[i]]
				i+=1
				print(num)
		return num
	def createLinks(self,string):
		retour = string
		for regObject in self.regObjects:
			if regObject.search(retour) != None:
				number = self.roman2int(regObject.search(retour).group(2))
			retour = regObject.sub("[[Jn"+" "+str(number)+"]]",retour)
		return retour


indicatList = ["Ioan.","Ioann.","I Ioann."]
ref = "Jn"
Jn = vinculumMachina(indicatList,ref)
print(Jn.createLinks("Ceci est un test Ioan. IV. et Ioann. XCV. I Ioann. XC etc... "))

#jn = re.compile(".*"+"(Ioan.)"+" (CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})")
#print(jn.match("Ceci est un test Ioan. I etc...").group(4))


# Pour ceux avec un II devant, fonction speciale !