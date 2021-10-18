from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
import re
import fileinput

class Pars:
	def __init__(self,titulus):
		self.titulus = ""
		self.prooemium = None
		self.quaestiones = []
	def addeQuaestio(self,quaestio):
		self.quaestiones.append(quaestio)
	def __str__(self):
		pars = str(self.titulus)+"\n\n\n"
		for quaestio in self.quaestiones:
			pars += str(quaestio)+"\n"
		return(pars+"\n")

class Quaestio:
	def __init__(self,titulus):
		self.titulus = titulus
		self.prooemium = None
		self.articuli = []
	def addeArticulus(self,articulus):
		self.articuli.append(articulus)
	def addeProoemium(self,prooemium):
		self.prooemium = prooemium
	def __str__(self):
		quaestio = str(self.titulus)+"\n\n"
		quaestio += str(self.prooemium)+"\n"
		for articulus in self.articuli:
			quaestio += str(articulus)+"\n"
		return(quaestio+"\n")

class Articulus:
	def __init__(self,titulus):
		self.titulus = titulus
		self.argumenta = []
	def addeArgumentum(self,argumentum):
		self.argumenta.append(argumentum)
	def __str__(self):
		articulus = str(self.titulus)+"\n\n"
		for argumentum in self.argumenta:
			articulus += str(argumentum) +"\n"
		return(articulus+"\n")

class Argumentum:
	def __init__(self,titulus):
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

class Prooemium:
	def __init__(self,titulus):
		self.titulus = titulus
		self.corpus = ""
	def addeCorpus(self,addecorpus):
		italic = re.compile("<i>(.*?)</i>")
		if italic.match(addecorpus) == None:
			self.corpus += addecorpus
		else:
			self.corpus += "*"+italic.match(addecorpus).group(1)+"*"
	def __str__(self):
		return(str(self.titulus)+"\n\n"+str(self.corpus)+"\n")

def transferrePaginam(numero):
	# Téléchargement d'une page sur www.corpusthomisticum.org
	try:
	    url = "https://www.corpusthomisticum.org/sth"+str(numero)+".html"
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

	# Création du fichier texte associé au chapitre
	f = open('temp.txt', 'w')

	inQuaestio = False
	inArticulus = False
	inProoemium = False

	for data in soup.find_all():
		if data.name == "div":
			if data.attrs['class'] == ['D']:
				if inQuaestio:
					quaestio.addeArticulus(articulus)
					primaPars.addeQuaestio(quaestio)
				quaestio = Quaestio(data.getText())
				inQuaestio = True
				inArticulus = False
				inProoemium = False
			elif data.attrs['class'] == ['centro']:
				if inQuaestio:
					primaPars.addeQuaestio(quaestio)
				inArticulus = False
				inQuaestio = False
			elif data.attrs['class'] == ['G']:
				inArticulus = False
				inProoemium = True
				prooemium = Prooemium(data.getText())
			elif data.attrs['class'] == ['E']:
				if inArticulus:
					quaestio.addeArticulus(articulus)
					articulus=Articulus(data.getText())
				else:
					inArticulus = True
					articulus=Articulus(data.getText())
			else :
				if inArticulus:
					quaestio.addeArticulus(articulus)
				inArticulus = False
				inProoemium = False
		elif data.name == "p" and inArticulus:
			argumentum = Argumentum(data.attrs['title'])
			for i in range(1,len(data.contents)):
				argumentum.addeCorpus(str(data.contents[i]))
			articulus.addeArgumentum(argumentum)
		elif data.name == "p" and inProoemium:
			for i in range(1,len(data.contents)):
				prooemium.addeCorpus(str(data.contents[i]))
			quaestio.addeProoemium(prooemium)
			inProoemium = False
	f.close()


### MAIN ###

primaPars = Pars("Prima Pars")
#primaParsNumero = [1001,1002,1003,1015,1028,1044,1050,1065,1075,1077,1084,1090,1103]
primaParsNumero = [1003]
for numero in primaParsNumero:
	transferrePaginam(numero)

print(len(primaPars.quaestiones))
#print(primaPars)


