from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
import re
import fileinput

class Questio:
	def __init__(self,title):
		self.title = title
		self.articles = []
	def addArticle(self,article):
		self.articles.append(article)
	def __str__(self):
		questio = str(self.title)+"\n\n"
		for article in self.articles:
			questio += str(article)+"\n"
		return(questio+"\n")

class Article:
	def __init__(self,title):
		self.title = title
		self.paragraphs = []
	def addParagraph(self,paragraph):
		self.paragraphs.append(paragraph)
	def __str__(self):
		article = str(self.title)+"\n\n"
		for paragraph in self.paragraphs:
			article += str(paragraph) +"\n"
		return(article+"\n")

class Paragraph:
	def __init__(self):
		self.title = ""
		self.ref = ""
		self.corpus = ""
	def setTitle(self,title):
		self.title = title
	def setRef(self,ref):
		self.ref = ref
	def setCorpus(self,corpus):
		self.corpus = corpus
	def __str__(self):
		return(str(self.title)+"\n"+str(self.ref)+"\n"+str(self.corpus)+"\n")

def telechargerPage():
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
	
	# Création du fichier texte associé au chapitre
	f = open('temp.txt', 'w')
	# Trouver tous les articles de la page
	#print(soup.prettify())
	inArticle = False
	inParagraph = False

	for data in soup.find_all():
		if data.name == "div":
			if data.attrs['class'] == ['D']:
				print("It's a questio")
				print(data.getText())
				inArticle = False
			elif data.attrs['class'] == ['G']:
				print("It's a prooemium")
				print(data.getText())
				inArticle = False
			elif data.attrs['class'] == ['E']:
				print("It's an article")
				print(data.getText())
				inArticle = True
			else :
				inArticle = False
		elif data.name == "p" and inArticle:
			print(data.attrs['title'])
			print(data.contents[1])
			inParagraph = True
		elif data.name == "a" and inParagraph:
			print(data.attrs['name'])
			inParagraph = False
	f.close()

telechargerPage()

paragraph = Paragraph()
print(paragraph)

paragraph.setTitle("test")
paragraph.setRef("testRef")
paragraph.setCorpus("testCorpus")

print(paragraph)

article = Article("titreArticle")
article.addParagraph(paragraph)
article.addParagraph(paragraph)
print(article)