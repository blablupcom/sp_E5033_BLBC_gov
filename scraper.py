# -*- coding: utf-8 -*-

import scraperwiki
import urllib2
from datetime import datetime
from bs4 import BeautifulSoup

# Set up variables
entity_id = "E5033_BLBC_gov"
url = "http://brent.gov.uk/your-council/transparency-in-brent/open-data/spending/"

# Set up functions
def convert_mth_strings ( mth_string ):
	month_numbers = {'JAN': '01', 'FEB': '02', 'MAR':'03', 'APR':'04', 'MAY':'05', 'JUN':'06', 'JUL':'07', 'AUG':'08', 'SEP':'09','OCT':'10','NOV':'11','DEC':'12' }
	#loop through the months in our dictionary
	for k, v in month_numbers.items():
		#then replace the word with the number
		mth_string = mth_string.replace(k, v)
	return mth_string

# pull down the content from the webpage
html = urllib2.urlopen(url)
soup = BeautifulSoup(html)

# find all entries with the required class
blocks = soup.findAll('h2', {'class':'removeLowerMargin'})

for block in blocks:

	link = block.a['href']

	# add the right prefix onto the url
	pageUrl = link.replace("/your-council","http://www.brent.gov.uk/your-council")
	
	html2 = urllib2.urlopen(pageUrl)
	soup2 = BeautifulSoup(html2)
	
	csvYr = soup2.find('span',{'class':'h1Text'}).contents[0].strip()
	sublinks = soup2.findAll('a', href=True)
	
	for sublink in sublinks:
		subhref = sublink['href']
		if '/media' in subhref:
			fileUrl = subhref
			fileUrl = fileUrl.replace("/your-council","http://www.brent.gov.uk/your-council")
			
			title = sublink.contents[0]
			
			if title == None:
				print sublink
				exit
				
			# create the right strings for the new filename
			title = title.upper().strip()
			
			if len(title.split()) > 1:
				print 'not a single month'
			else:
				csvMth = title.split(' ')[0][:3]
				csvMth = convert_mth_strings(csvMth);
			
				filename = entity_id + "_" + csvYr + "_" + csvMth
			
				todays_date = str(datetime.now())
		
				scraperwiki.sqlite.save(unique_keys=['l'], data={"l": fileUrl, "f": filename, "d": todays_date })
				
				print filename
