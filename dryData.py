import requests,json
from bs4 import BeautifulSoup
from urlparse import urlparse
from mozscape import Mozscape, MozscapeError
from time import sleep
from itertools import cycle


headers = {
	'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',

}


def UseProxy():
	proxies = {
		'https':'http://89.47.31.145:3128'
	}
	response = requests.get('http://httpbin.org/ip',proxies=proxies)
	print response.text
UseProxy()
def GoogleQuery():

	arr = []
	index = 0
	response = requests.get('https://www.google.com/search?num=1&q=Philippines Loans&oq=Philippines Loans&&start=10',headers=headers).text
	soup = BeautifulSoup(response)
	print soup
	title = soup.findAll('div',attrs={'class':'g'})
	for titles in title:
		try:
			dictionary = {}
			index +=1
			dictionary['index#'] = str(index) 
			dictionary['meta_title'] = titles.find('h3').text
			dictionary['full_url'] = titles.find('a')['href']
			rootDomain = dictionary['full_url'].replace('/url?q=','')
			parsed_uri = urlparse(rootDomain)
			dictionary['rootDomain'] = rootDomain
			domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
			dictionary['root_domain'] = domain
			print dictionary['root_domain']
			dictionary['description'] = titles.find('span',attrs={'class':'st'}).text
			arr.append(dictionary)
		except AttributeError:
			continue
	return arr

def SocialMediaCount():
	arr = GoogleQuery()
	for items in arr:
		URLS = items['root_domain']
		facebookCount = requests.get('http://graph.facebook.com/?id='+URLS).text
		jsonObj = json.loads(facebookCount)
		facebookC = jsonObj['og_object'], jsonObj['share'], jsonObj['id']
		TwitterCount = requests.get('https://plusone.google.com/_/+1/fastbutton?url='+URLS).text
		soup = BeautifulSoup(TwitterCount)
		googleCount = soup.find('div',attrs={'id':'aggregateCount'}).text
		linkedin = requests.get('https://www.linkedin.com/countserv/count/share?url='+URLS).text
		soup = BeautifulSoup(linkedin)
		parsedObj = soup.find('p').text.replace('IN.Tags.Share.handleCount(','').replace(');','')
		loadAsJsonObj = json.loads(parsedObj)
		linkedinCount = loadAsJsonObj['count']

def FacebookData():
	arr = GoogleQuery()
	for items in arr[:1]:
		URLS = items['root_domain']
		facebookCount = requests.get('http://graph.facebook.com/?id='+URLS).text
		jsonObj = json.loads(facebookCount)
		facebookC = jsonObj['og_object'], jsonObj['share'], jsonObj['id']
		response = requests.get('https://www.google.com/search?num=3&q=site:facebook.com '+URLS+'&&start=10').text
		soup = BeautifulSoup(response)
		title = soup.findAll('div',attrs={'class':'g'})
		for titles in title:
			dictionary = {}
			dictionary['meta_title'] = titles.find('h3').text
			dictionary['full_url'] = titles.find('a')['href']
			rootDomain = dictionary['full_url'].replace('/url?q=','')
			parsed_uri = urlparse(rootDomain)
			dictionary['rootDomain'] = rootDomain
			parseGroupURL = dictionary['rootDomain'].split('&sa')[0]
			groupURL = parseGroupURL.replace('%3F','?').replace('%3D','=')
			print groupURL
#FacebookData()		


def addClients():
	MozarrClientArr = ['member-79ea116cb0','member-89df24f83c','member-aad6e04a94','member-1e51eae111','member-c1d37816b1','member-700eebf334','member-774cfbde7e','member-34c9052fba','member-587eb1767c','member-5fa34d7383']
	MozarrPass = ['43053334ef958fa5668a8afd8018195b','0d08685d31a8f724047decff5e445861','8a08a4f2477b3eda0a7b3afa8eb6faaf','4f1deaa49d0f4ec8f36778b80a58dba5','47501159d505413721caac9687818f68','0e7136b3468cd832f6dda555aa917661','481981b24f4a4f08d7c7dc9d5038428f','999d2d727bfc11256421c42c529331de','8c36e3b36b7d6d352fd943429d97837e','3986edd244ae54e1aa96c71404914578']
	huge_arr = []
	for key, value in zip(MozarrClientArr, MozarrPass):
		dictionary = {}
		dictionary['key'] = key
		dictionary['value'] = value
		huge_arr.append(dictionary)
	with open('credentials.json','wb') as outfile:
		json.dump(huge_arr,outfile,indent=4)



def TryCred():


	listO = open('credentials.json')
	B = json.load(listO)
	emptylist = []
	A = ['ass','hole','3','5','6','7','8','9','10','11','12','13']
	zip_list = zip(A, cycle(B)) if len(A) > len(B) else zip(cycle(A), B)
	for zipList in zip_list:
		print zipList[-1]['key']


def Clients():
	arr = GoogleQuery()
	Mozarr = []
	listO = open('credentials.json')
	B = json.load(listO)
	A = arr[:50]
	zip_list = zip(A, cycle(B)) if len(A) > len(B) else zip(cycle(A), B)
	for zipList in zip_list:
		try:
			print zipList[-1]['key'], zipList[-1]['value']
		 	values = zipList[-1]['key'] + zipList[-1]['value']
		 	print zipList[0]['rootDomain']
			client = Mozscape(zipList[-1]['key'],zipList[-1]['value'])
			authorities = client.urlMetrics(zipList[0]['root_domain'], Mozscape.UMCols.domainAuthority)
			Links = client.urlMetrics(zipList[0]['rootDomain'],Mozscape.UMCols.pageAuthority | Mozscape.UMCols.mozRank | Mozscape.UMCols.links)
			internal_dictionary = {}
			internal_dictionary['backURL'] = zipList[0]['rootDomain']
			internal_dictionary['PA'] = Links['upa']
			internal_dictionary['DA'] = authorities['pda']
			internal_dictionary['MozRank'] = Links['umrp']
			internal_dictionary['links'] = Links['uid']
			print internal_dictionary['backURL']
			Mozarr.append(internal_dictionary)
		except MozscapeError:
			sleep(11)
			continue
	with open('mozscapedata.json','wb') as outfile:
		json.dump(Mozarr,outfile,indent=4)