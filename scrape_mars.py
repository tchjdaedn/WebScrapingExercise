from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
from splinter import Browser
import pandas as pd


def scrape():
	#define browser path
	executable_path = {'executable_path': 'chromedriver.exe'}
	browser = Browser('chrome', **executable_path, headless=False)

	#Scrape Mars News
	newsurl = 'https://mars.nasa.gov/news/'
	response = requests.get(newsurl)
	soup = bs(response.text, 'html.parser')
	
	results = soup.find('div', class_="slide")

	newsdict = {}

	try:
		newsdict['title'] = results.find('div', class_="content_title").text.strip()
		newsdict['description'] = results.find('div', class_="rollover_description_inner").text.strip()

	except AttributeError as e:
		print(e)

	#Scrape Mars Images
		#split the url to use later
	jplurl = 'https://www.jpl.nasa.gov/spaceimages/'
	searchurl = '?search=Mars&category=Mars'

		#get the page
	browser.visit(jplurl+searchurl)
	html=browser.html

		# find the featured image 
	soup = bs(html, 'html.parser')
	section = soup.find('a', class_='button fancybox')['data-fancybox-href']

		#get the fullsize version
	imgparts = section.split("/")
	imgpart=imgparts[4]
	imgpart = imgpart.split("_",1)[0]
	featured_image_url = jplurl+imgparts[2]+"/wallpaper/"+imgpart+"-1920x1200.jpg"

	#Scrape Mars Weather
	weatherurl = 'https://twitter.com/marswxreport?lang=en'
	response = requests.get(weatherurl)
	soup = bs(response.text, 'html.parser')
	mars_weather = soup.find('p', class_="TweetTextSize").text.strip()

	#Scrape Mars Facts
	factsurl = 'http://space-facts.com/mars/'
	tables = pd.read_html(factsurl)
	table = tables[0]
	table = table.to_html(header=False,index=False, index_names=False)

	#Scrape Hemispheres
	hemiurl = 'http://web.archive.org'
	hemiweb = '/web/20181114171728/https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

	browser.visit(hemiurl+hemiweb)
	html=browser.html

	soup = bs(html, 'html.parser')

		#find all rerturns both & thumnails
	Product = soup.find_all('a', class_='itemLink')
	Strlen = len(Product)
	Product2 = []

		#identify and strip out thumbnails
	for i in range(0,Strlen):
		if Product[i].text.strip() != "":
			Product2.append(Product[i])

		#initialize storage variables
	hemisphere_image_urls = []
	holder = {"title":'holder', "img_url":'holder.jpg'}

	Strlen2 = len(Product2)

		#cycle through results list
	for i in range(0,Strlen2):
		
		#grab Title & link for each result
		#strip title & store in holder
		holder["title"] = Product2[i].text.strip()
		
		#navigate to full-size link
		browser.visit(hemiurl+Product2[i]['href'])
		html2=browser.html
		soup2 = bs(html2, 'html.parser')
		
		#find link within page
		link = soup2.find('img', class_='wide-image')['src']
		
		#store in holder
		holder["img_url"] = hemiurl+link
		
		#add holder to list
		hemisphere_image_urls.append(dict(holder))
		
	#return results News (dictionary), 
	#		featured image url (string)
	#		weather tweet (string)
	#		fact table (html table)
	#		hemisphere image url (dictionary)
	marsdict={}
	marsdict['News'] = newsdict
	marsdict['Featured']=featured_image_url
	marsdict['Weather']=mars_weather
	marsdict['FactTable'] = table
	marsdict['Hemispheres'] = hemisphere_image_urls
	
	return marsdict

	
