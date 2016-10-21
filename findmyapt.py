

import urllib2 
import xmltodict
from bs4 import BeautifulSoup
from bs4 import BeautifulStoneSoup
import bs4

url = 'https://sfbay.craigslist.org/search/sfc/apa?is_paid=all&hasPic=1&search_distance_type=mi&nh=4&nh=5&nh=8&nh=11&nh=12&nh=10&nh=20&nh=18&nh=19&nh=23&nh=27&nh=2&max_price=2500&bedrooms=1&bathrooms=1&minSqft=450&no_smoking=1'


rawcontents = urllib2.urlopen(url).read()

rawcontents = rawcontents.replace('class','clase')

soup = BeautifulSoup(rawcontents)


soup.findAll('span', clase='price')

with open('pretty.html','w') as f:
	f.write(soup.prettify().encode('utf-8'))



listings = soup.findAll('span', clase='txt')
listings[0].findAll('span', clase='pl')

topdic = {}
for i,l in enumerate(listings):
	dic = {}
	dic['description'] = l.find('a', clase='hdrlnk').text
	dic['href'] = 'http://sfbay.craigslist.org'+l.find('a', clase='hdrlnk')['href']
	dic['datetime'] = l.find('time')['datetime']
	price_ = l.find('span',clase='price').text
	dic['price'] = int(price_.split('$')[1])
	size_ = l.find('span',clase='housing').text
	dic['size'] = int(size_.split('ft')[0][-3:])
	dic['location'] = l.find('small').text.replace('(','').replace(')','').strip()
	topdic[i] = dic


xml_ = listings[0]

u = BeautifulSoup(xml_, "xml")

xmltodict.parse(unicode(xml_))










