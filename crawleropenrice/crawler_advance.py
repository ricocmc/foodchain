#!/usr/bin/python
#-*- coding: utf8 -*-

import urllib2
from lxml import etree
from lxml.html import parse
from db_crawlingList import db_crawlingList
from db_restaurantLinks import db_restaurantLinks

crawleringNumber = 0
restaurantNumber = 0
db_crawlingList = db_crawlingList()
db_restaurantLinks = db_restaurantLinks()

def crawlFromUrl(url):
   global crawleringNumber
   global restaurantNumber
   global db_crawlingList
   global db_restaurantLinks

   if (not db_crawlingList.crawled(url)):
      crawleringNumber += 1
      print str(crawleringNumber) + '. Crawlering... ' + url

      # getting the website content
      file = urllib2.urlopen(url)
      data = file.read()
      data = data.decode('utf-8')
      file.close()

      parser = etree.HTMLParser(encoding='utf-8')
      tree   = etree.fromstring(data.encode('utf-8'), parser)
      temp = tree.findall('.//a')

      for tempElement in temp:
         if (tempElement is not None) and (tempElement.get('href') is not None):
            hrefText = tempElement.get('href').encode('utf-8')
            if ("sr1.htm" in hrefText):
               if (not db_crawlingList.exist(hrefText)):
                  # fix openrice url
                  if (hrefText.startswith('/')):
                     hrefText = 'http://www.openrice.com' + hrefText
                  
                  db_crawlingList.insert(hrefText)

            if ("sr2.htm" in hrefText):
               if (not db_restaurantLinks.exist(hrefText)):
                  # fix openrice url
                  if (hrefText.startswith('/')):
                     hrefText = 'http://www.openrice.com' + hrefText

                  db_restaurantLinks.insert(hrefText)
                     
      db_crawlingList.update(url, True)

      for tempElement in temp:
         if (tempElement is not None) and (tempElement.get('href') is not None):
            hrefText = tempElement.get('href').encode('utf-8')
            if ("sr1.htm" in hrefText):
               # fix openrice url
               if (hrefText.startswith('/')):
                  hrefText = 'http://www.openrice.com' + hrefText
                   
               if (not db_crawlingList.crawled(hrefText)):
                  crawlFromUrl(hrefText)

crawlFromUrl('http://www.openrice.com/restaurant/sr1.htm?s=1&dishes_id=&amenity_id=&theme_id=&price=&inputcategory=cname&inputstrrest=&ST=1&district_id=2010')
