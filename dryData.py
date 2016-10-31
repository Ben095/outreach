import requests,json
from bs4 import BeautifulSoup
from urlparse import urlparse
from mozscape import Mozscape, MozscapeError
from time import sleep
from itertools import cycle
import dryscrape

headers = {
	'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:27.0) Gecko/20100101 Firefox/27.0',
	'Cookie':'NID=89=Xx6qVlFq5MyhJC5y4-duwh50KFDhMFDVNUHpAX63aQs1J77jswVAUv1nrxu8ekuZjs9SGvA31VnN5O3wS1b4HQrBDDRKyMgERDrGbr2oWaBps46rBvepRIX5rKTqJJq1BN4ARj2ErQ2jAA; DV=wkE1gHCYxTAcLEWZLaMIXfRxgbYxsAI',
	'X-Firefox-Spdy':'3.1',
	'Host':'www.google.com',
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

proxies = {
	'https':'https://1069jeanbisson:t1nmcsca0z8m@185.152.128.57:10056'
}

def UseProxy():
	# sess = dryscrape.Session(base_url='https://www.google.com')
	# sess.visit('/')
	# sleep(2)


	#response = requests.get('http://httpbin.org/ip',proxies=proxies)
	tryGoogle = requests.get('https://www.google.com/search?num=1&site=&source=hp&q=ben',headers=headers, proxies=proxies)
	print tryGoogle.text
	#print response.text
#UseProxy()


def GoogleQuery():
    #################-------QUERIES GOOGLE FIRST STEP-------------######### Gets 10 results.
    ### ON QUERY NO TIMER NEEDED##########
    ### GoogleQuery() function returns an array of dictionary with crucial information
    ### Save google data in database (FIRST STEP!!!!!) #######

	arr = []
	index = 0
	response = requests.get('https://www.google.com/search?num=1&q=Philippines Loans&oq=Philippines Loans&&start=10',headers=headers,proxies=proxies).text
	soup = BeautifulSoup(response)
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
			#print dictionary['root_domain']
			dictionary['description'] = titles.find('span',attrs={'class':'st'}).text
			arr.append(dictionary)
		except AttributeError:
			continue
	return arr

#GoogleQuery()
def TwitterData():
	outputTwitterArr = []
	arr = GoogleQuery()
	for items in arr:
		sleep(5)
		URLS = items['root_domain']
		response = requests.get('https://www.google.com/search?num=1&q=site:twitter.com%20'+URLS, headers=headers,proxies=proxies).text
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
			print parseGroupURL
			outputTwitterArr.append(parseGroupURL)
	return outputTwitterArr

def TwitterScraper():
	arr = []
	DataList = TwitterData()
	removeDuplicates = list(set(DataList))
	for items in removeDuplicates:
		dictionary = {}
		response = requests.get(items).text
		soup = BeautifulSoup(response)
		Followers = soup.find('span',attrs={'class':'ProfileNav-value'}).text
		dictionary['twitter_profile_followers'] = Followers
		dictionary['twitter_url'] = items
		dictionary['twitter_shares'] = "None"
		arr.append(dictionary)
	return arr


def GooglePlusData():
	arr = GoogleQuery()
	googleAdditionalData = []
	for items in arr:
		URLS = items['root_domain']
		#print URLS
		response = requests.get('https://www.google.com/search?num=1&q=site:plus.google.com+'+str(URLS),headers=headers,proxies=proxies).text
		soup = BeautifulSoup(response)
		title = soup.findAll('div',attrs={'class':'g'})
		for titles in title:
			dictionary = {}
			dictionary['meta_title'] = titles.find('h3').text
			dictionary['full_url'] = titles.find('a')['href']
			rootDomain = dictionary['full_url'].replace('/url?q=','')
			parsed_uri = urlparse(rootDomain)
			dictionary['rootDomain'] = rootDomain
			googleAdditionalData.append(dictionary['rootDomain'].split('&')[0])
	return googleAdditionalData

def scrapeGooglePlus():
	googlePlusArr = []
	arr = GooglePlusData()
	removeDuplicates = list(set(arr))
	for visitFacebookPage in removeDuplicates[:1]:
		dictionary = {}
		TwitterCount = requests.get('https://plusone.google.com/_/+1/fastbutton?url='+visitFacebookPage,headers=headers,proxies=proxies).text
		soup = BeautifulSoup(TwitterCount)
		googleCount = soup.find('div',attrs={'id':'aggregateCount'}).text
		dictionary['googleplus_shares'] = googleCount
		response = requests.get(visitFacebookPage).text
		soup = BeautifulSoup(response)
		dictionary['googleplus_followers'] = soup.find('span',attrs={'class':'BOfSxb'}).text
		dictionary['googleplus_uRL'] = visitFacebookPage
		googlePlusArr.append(dictionary)
	return googlePlusArr


def LinkedInData():
	arr = GoogleQuery()
	linkedInAdditionalData = []
	for items in arr[:1]:
		sleep(5)
		URLS = items['root_domain']
		print URLS
		response = requests.get('https://www.google.com/search?num=1&site=&source=hp&q=site:www.linkedin.com+'+URLS,headers=headers,proxies=proxies).text
		soup = BeautifulSoup(response)
		title = soup.findAll('div',attrs={'class':'g'})
		for titles in title:
			dictionary = {}
			dictionary['meta_title'] = titles.find('h3').text
			dictionary['full_url'] = titles.find('a')['href']
			rootDomain = dictionary['full_url'].replace('/url?q=','')
			parsed_uri = urlparse(rootDomain)
			dictionary['rootDomain'] = rootDomain
			groupURL = dictionary['rootDomain'].split('&')[0]
			linkedInAdditionalData.append(groupURL)
	return linkedInAdditionalData


		



def FacebookData():
	##### Facebook Data Function()##### -> Loops through ALL the rootDomain URLS retrieved from first function
	####----> Only returns ONE result per URL -> Relying on google scraper!
	####-----> Has a timer per each URL query 5 seconds!
	###-->> Could possibly use Proxy in this case in near future!
	###--->> This returns me the facebook group URL!
	arr = GoogleQuery()
	facebookURLAdditionalData = []
	for items in arr:
		sleep(5)
		URLS = items['root_domain']
		print 'https://www.google.com/search?num=1&q=site:facebook.com '+URLS+'&&start=10'
		response = requests.get('https://www.google.com/search?num=1&q=site:facebook.com '+URLS+'&&start=10',headers=headers,proxies=proxies).text
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
			facebookURLAdditionalData.append(groupURL)
	return facebookURLAdditionalData


def FacebookScraper():
	#### This function scrapes and puts everything together for facebook field
	#### ---> Initates a new dictionary with {facebookshares:data,'facebookprofile':'data','profilelikes':'data'}
	#### ---> three fields!
	#### ----> This function is the last step for facebook to be shown in flask front-end
	#### -----> removes duplicates and possible conflict on any data and returns the Cleanest version for each group
	#### ----> This function returns an array with required field for social platform 'facebook'
	arr = []
	DataList = FacebookData()
	removeDuplicates = list(set(DataList))
	for visitFacebookPage in removeDuplicates:
		try:
			dictionary = {}
			facebookCount = requests.get('http://graph.facebook.com/?id='+URLS).text
			jsonObj = json.loads(facebookCount)
			facebookC = jsonObj['og_object'], jsonObj['share'], jsonObj['id']
			response = requests.get(visitFacebookPage).text
			soup = BeautifulSoup(response)
			likes = soup.find('div',attrs={'class':'_4-u2 _5tsm _4-u8'}).text
			dictionary['facebook_shares'] = jsonObj['share']
			dictionary['facebook_profile_url'] = visitFacebookPage
			dictionary['facebook_profile_likes'] = likes.encode('ascii','ignore').strip()
			arr.append(dictionary)
		except AttributeError:
			pass
	return arr
#FacebookScraper()






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
	A = GoogleQuery()
	Mozarr = []
	listO = open('credentials.json')
	B = json.load(listO)
	zip_list = zip(A, cycle(B)) if len(A) > len(B) else zip(cycle(A), B)
	for zipList in zip_list:
		try:
			#print zipList[-1]['key'], zipList[-1]['value']
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
			#print internal_dictionary['backURL']
			Mozarr.append(internal_dictionary)
		except MozscapeError:
			sleep(11)
			continue
	with open('mozscapedata.json','wb') as outfile:
		json.dump(Mozarr,outfile,indent=4)
Clients()