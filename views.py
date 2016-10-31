import requests,json
from bs4 import BeautifulSoup
from urlparse import urlparse
from mozscape import Mozscape, MozscapeError
from time import sleep
from itertools import cycle
import dryscrape
from flask import*
from time import sleep
from forms import QueryGoogle
from models import*

app = Flask(__name__)
app.secret_key = '1234'
db.create_all()
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
@app.route('/google', methods=['GET','POST'])
def querygoogle():
	form = QueryGoogle(request.form)
	arr = []
	index = 0
	if form.validate_on_submit():
		arr = []
		query = form.QueryGoogle.data
		response = requests.get('https://www.google.com/search?num=3&q='+query+'&oq='+query+'&&start=10',headers=headers,proxies=proxies).text
		soup = BeautifulSoup(response)
		title = soup.findAll('div',attrs={'class':'g'})
		for titles in title:
			try:
				dictionary = {}
				index +=1
				#dictionary['index#'] = str(index) 
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
				addUser = Google(googleQuery=query,googleMetaTitle=dictionary['meta_title'],googleFullURL=dictionary['rootDomain'],googleRootDomain=dictionary['root_domain'])
				db.session.add(addUser)
				arr.append(dictionary)
			except AttributeError:
				continue
		db.session.commit()

		Mozarr = []
		secondaryURL = []
		listO = open('credentials.json')
		B = json.load(listO)
		A = arr
		zip_list = zip(A, cycle(B)) if len(A) > len(B) else zip(cycle(A), B)
		for zipList in zip_list:
			try:
				#print zipList[0]['rootDomain']
				#print zipList[-1]['key'], zipList[-1]['value']
			 	values = zipList[-1]['key'] + zipList[-1]['value']
			 	#print zipList[0]['rootDomain']
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
				secondaryURL.append(zipList[0]['rootDomain'])
			except MozscapeError:
				sleep(11)
				continue

		removeDuplicates = list(set(secondaryURL))
		for addtoDb in removeDuplicates:
			updateDatabase = Google.query.filter_by(googleRootDomain=addtoDb).all()
			print updateDatabase


		return render_template('google.html', form=form, arr=arr)
	return render_template('google.html',form=form,arr=arr)

if __name__ == "__main__":
	app.run(debug=True)


