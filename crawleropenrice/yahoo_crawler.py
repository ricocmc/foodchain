#!/usr/bin/python
#-*- coding: utf8 -*-
from lxml.html import parse

def fromYahooStock(stoNum):
        qurl = 'http://tw.stock.yahoo.com/q/q?s=' + str(stoNum)
        root = parse(qurl).getroot()
        temp = root.xpath('/html/body/center/table/tr/td/table/tr/td/a')[0]
        print temp.text

if __name__ == "__main__":
        fromYahooStock(1201) 
