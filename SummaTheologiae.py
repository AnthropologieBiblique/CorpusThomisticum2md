from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
import re
import fileinput

class Questio:
	def __init__(self,titulus):
		self.titulus = titulus
		self.articuli = []
	def addeArticulus(self,articulus):
		self.articuli.append(articulus)
	def __str__(self):
		questio = str(self.titulus)+"\n\n"
		for articulus in self.articuli:
			questio += str(articulus)+"\n"
		return(questio+"\n")

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
		self.index = ""
		self.corpus = ""
	def mutareTitulus(self,titulus):
		self.titulus = titulus
	def addeCorpus(self,addecorpus):
		italic = re.compile("<i>(.*?)</i>")
		if italic.match(addecorpus) == None:
			self.corpus += addecorpus
		else:
			self.corpus += "*"+italic.match(addecorpus).group(1)+"*"
	def __str__(self):
		return(str(self.titulus)+"\n"+str(self.corpus)+"\n")

def transferrePaginam():
	# Téléchargement d'une page sur www.corpusthomisticum.org
	try:
	    url = "https://www.corpusthomisticum.org/sth1001.html"
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

	inArticulus = False
	questioAlbum = []

	for data in soup.find_all():
		if data.name == "div":
			if data.attrs['class'] == ['D']:
				questio = Questio(data.getText())
				inArticulus = False
			elif data.attrs['class'] == ['G']:
				inArticulus = False
			elif data.attrs['class'] == ['E']:
				if inArticulus:
					questio.addeArticulus(articulus)
					articulus=Articulus(data.getText())
				else:
					inArticulus = True
					articulus=Articulus(data.getText())
			else :
				if inArticulus:
					questio.addeArticulus(articulus)
				inArticulus = False
		elif data.name == "p" and inArticulus:
			argumentum = Argumentum(data.attrs['title'])
			for i in range(1,len(data.contents)):
				argumentum.addeCorpus(str(data.contents[i]))
			articulus.addeArgumentum(argumentum)
	print(questio)
	print(questio.articuli)
	f.close()

transferrePaginam()