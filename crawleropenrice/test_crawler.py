#!/usr/bin/python
#-*- coding: utf8 -*-
from lxml.html import parse
from lxml import etree

def fromYahooStock(stoNum):
    qurl = 'http://www.openrice.com/restaurant/sr1.htm?s=1&dishes_id=&amenity_id=&theme_id=&price=&inputcategory=cname&inputstrrest=&ST=1'
    root = parse(qurl).getroot()
    #print root
    temp = root.xpath('/html/body/center/table/tr/td/table/tr/td/a')[0]
    #temp = root.xpath('/html/body')[0]
    print temp.text
    for child in root.iterdescendants():
            print etree.tostring(child)

if __name__ == "__main__":
        fromYahooStock(1398) 
