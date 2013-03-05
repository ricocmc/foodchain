#!/usr/bin/python
#-*- coding: utf8 -*-

#import library to do http requests:
import urllib2

from lxml import etree
from lxml.html import parse
#import easy to use xml parser called minidom:
#from xml.dom.minidom import parseString
#all these imports are standard on most modern python implementations
 
#download the file:
file = urllib2.urlopen('http://www.openrice.com/restaurant/sr1.htm?s=1&dishes_id=&amenity_id=&theme_id=&price=&inputcategory=cname&inputstrrest=&ST=1&district_id=2010')
#convert to string:
data = file.read()
data = data.decode('utf-8')
#close file because we dont need it anymore:
file.close()

#data = '<div>'+data+'</div>'

#root = parse(data).getroot()
#print data
#ele = etree.fromstring(data)
#html = etree.HTML(data)
parser = etree.HTMLParser(encoding='utf-8')
tree   = etree.fromstring(data.encode('utf-8'), parser)

#print(etree.tostring(tree))

# This is the sponsor link
#temp = tree.xpath('/html/body/div/div/div/div/div/table/tbody/tr/td/div/a')

# This is the normal links
#temp = tree.xpath('/html/body/div/div/div/table/tr/td/div/span/a')

# This is all the a
#temp = tree.xpath('/a')
temp = tree.findall('.//a')

count = 0
for tempElement in temp:
   if (tempElement is not None) and (tempElement.get('href') is not None):
      if ("sr2.htm" in tempElement.get('href')):
         count += 1
         print tempElement.get('href')

print 'Total: ' + str(count)
#result = etree.tostring(tree.getroot(),pretty_print=True, method="html")
#print(result)

#print html

#data = '<div>'+data+'</div>'

#print data
#parse the xml you downloaded
#dom = parseString(data)
#retrieve the first xml tag (<tag>data</tag>) that the parser finds with name tagName:
#xmlTag = dom.getElementsByTagName('a')[0].toxml()
#strip off the tag (<tag>data</tag>  --->   data):
#xmlData=xmlTag.replace('<tagName>','').replace('</tagName>','')
#print out the xml tag and data in this format: <tag>data</tag>
#print xmlTag
#just print the data
#print xmlData
