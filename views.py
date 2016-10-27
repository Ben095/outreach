from flask import*
import requests, json
from bs4 import BeautifulSoup
import dryscrape, json
from time import sleep
from forms import QueryGoogle
app = Flask(__name__)
app.secret_key = '1234'

@app.route('/', methods=['GET','POST'])
def Google():
	form = QueryGoogle(request.form)
	arr = []
	if form.validate_on_submit():
		query = form.QueryGoogle.data
		response = requests.get('https://www.google.com/search?q='+query+'&oq='+query+'&&start=20').text
		soup = BeautifulSoup(response)
		title = soup.findAll('div',attrs={'class':'g'})
		for titles in title:
			try:
				dictionary = {}
				dictionary['postTitle'] = titles.find('h3').text
				dictionary['URL'] = titles.find('a')['href']
				dictionary['description'] = titles.find('span',attrs={'class':'st'}).text
				arr.append(dictionary)
			except AttributeError:
				continue
		return render_template('google.html', form=form, arr=arr)
	return render_template('google.html',form=form,arr=arr)










# search_term = 'Ben'
# sess = dryscrape.Session(base_url = 'http://google.com')
# sess.set_attribute('auto_load_images', False)
# sess.visit('/')
# q = sess.at_xpath('//*[@name="q"]')
# q.set(search_term)
# q.form().submit()

# for link in sess.xpath('//a[@href]'):
#   print link['href']