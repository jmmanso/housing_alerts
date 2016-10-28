
import os
import json
import urllib2
from bs4 import BeautifulSoup
import bs4
####
import configs
import emailer


def fetch_cl_content():
	rawcontents = urllib2.urlopen(configs.cl_search_url).read()
	# rename tag to non-python keyword
	rawcontents = rawcontents.replace('class','clase')
	soup = BeautifulSoup(rawcontents, "lxml")
	return soup

def find_listings(soup):
	# get the "span" elements
	listings = soup.findAll('span', clase='txt')
	# assemble relevant listings as a small dictionary
	todays_listings = {}
	for i, l in enumerate(listings):
		dic_ = {}
		dic_['description'] = l.find('a', clase='hdrlnk').text
		post_id = l.find('a', clase='hdrlnk')['href']
		dic_['href'] = "http://sfbay.craigslist.org" + post_id
		dic_['datetime'] = l.find('time')['datetime']
		price_ = l.find('span',clase='price').text
		dic_['price'] = int(price_.split('$')[1])
		# if apt size was not given, assign n/a
		try:
			size_ = l.find('span',clase='housing').text
			dic_['size'] = int(size_.split('ft')[0][-3:])
		except:
			dic_['size'] = 'n/a'
		dic_['location'] = l.find('small').text.replace('(','').replace(')','').strip()
		todays_listings[post_id] = dic_
	return todays_listings


def add_extra_source(todays_listings):
	for url in [configs.dolores_search_url230, configs.dolores_search_url240]:
		rawcontents = urllib2.urlopen(url).read()
		soup = BeautifulSoup(rawcontents, "lxml")
		text_ = soup.text.lower()
		# Split text when unit # is mentioned
		chunks = text_.split("unit #")
		# if that tag is not mentioned, no splitting is done. Ignore and continue.
		# Otherwise, get the unit name and add listing to dictionary:
		if len(chunks)>1:
			for i in xrange(1,len(chunks)):
				unit_name = chunks[i][:3]
				dic_ = {}
				dic_['description'] = "DOLORES Apartments: %s" % unit_name
				dic_['href'] = url
				dic_['price'] = 'n/a'
				dic_['size'] = 'n/a'
				dic_['location'] = 'n/a'
				todays_listings["dolores_%s" % unit_name] = dic_
	return todays_listings



def find_new_listings(todays_listings):
	""" Find those listings that were not present
	last time. Save all of today's and the news ones
	in separate files. Return the new listings. """

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

	return new_listings


def email_listings(new_listings):
	if len(new_listings)>0:
		print "there are new listings..."
		emailer.mail(new_listings)
	else:
		print "NO new listings."


def full_wrapper():
	soup = fetch_cl_content()
	todays_listings = find_listings(soup)
	todays_listings = add_extra_source(todays_listings)
	new_listings = find_new_listings(todays_listings)
	email_listings(new_listings)


if __name__ == "__main__":
	full_wrapper()








#
