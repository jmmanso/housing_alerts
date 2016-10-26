
import os
import json
import urllib2
from bs4 import BeautifulSoup
import bs4
####
import configs
import emailer



rawcontents = urllib2.urlopen(configs.cl_search_url).read()
rawcontents = rawcontents.replace('class','clase')
soup = BeautifulSoup(rawcontents, "lxml")


listings = soup.findAll('span', clase='txt')
#listings[0].findAll('span', clase='pl')

todays_listings = {}
for i,l in enumerate(listings):
	dic_ = {}
	dic_['description'] = l.find('a', clase='hdrlnk').text
	post_id = l.find('a', clase='hdrlnk')['href']
	dic_['href'] = "http://sfbay.craigslist.org" + post_id
	dic_['datetime'] = l.find('time')['datetime']
	price_ = l.find('span',clase='price').text
	dic_['price'] = int(price_.split('$')[1])
	try:
		size_ = l.find('span',clase='housing').text
		dic_['size'] = int(size_.split('ft')[0][-3:])
	except:
		dic_['size'] = 'n/a'
	dic_['location'] = l.find('small').text.replace('(','').replace(')','').strip()
	todays_listings[post_id] = dic_

##
for url in [configs.dolores_search_url230, configs.dolores_search_url240]:
	rawcontents = urllib2.urlopen(url).read()
	soup = BeautifulSoup(rawcontents, "lxml")
	text_ = soup.text.lower()
	if "apply now" in text_ and "available" in text_:
		dic_ = {}
		dic_['description'] = "DOLORES Apartments"
		dic_['href'] = url
		dic_['price'] = 'n/a'
		dic_['size'] = 'n/a'
		dic_['location'] = 'n/a'
		todays_listings[url[11:14]] = dic_
##


new_listings = {}

if not os.path.exists(configs.cl_dump_json_path):
	print "creating new json"
	with open(configs.cl_dump_json_path, "w") as f:
		f.write(json.dumps(todays_listings))
	#
	new_listings = dict(todays_listings)
else:
	print "loading existing json"
	with open(configs.cl_dump_json_path, "r") as f:
		historic_listings = json.loads(f.read())
		for key in todays_listings.keys():
			if key not in historic_listings.keys():
				historic_listings[key] = todays_listings[key]
				new_listings[key] = todays_listings[key]
	with open(configs.cl_dump_json_path, "w") as f:
		f.write(json.dumps(historic_listings))

with open(configs.cl_new_json_path, "w") as f:
	f.write(json.dumps(new_listings))



if len(new_listings)>0:
	print "there are new listings..."
	emailer.mail(new_listings)
else:
	print "NO new listings."
