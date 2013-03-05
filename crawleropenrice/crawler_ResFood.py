#!/usr/bin/python
#-*- coding: utf8 -*-

#import library to do http requests:
import urllib2

from lxml import etree
from lxml.html import parse

from db_restaurantLinks import db_restaurantLinks
from db_restaurant import db_restaurant
from db_food import db_food

def getResName(treeNode):
    resNameElementList = treeNode.xpath('/html/body/div/div/div/div/div/div/div/h1/a')
    if (len(resNameElementList) == 1):
        return resNameElementList[0].text
    elif (len(resNameElementList) == 2):
        return resNameElementList[0].text
        #for resNameEle in resNameElementList:
            #if resNameEle.text is not None:
                #print resNameEle.text

def getAddress(treeNode):
    resAddressElementList = treeNode.xpath('/html/body/div/div/div/div/div/div/table/tr/td/table/tr/td/div/table/tr')
    for resAddress in resAddressElementList:
        infoTd = resAddress.findall('.//td')
        resTitle = infoTd[0].findall('.//b')
        if (len(resTitle)>0) and (resTitle[0].text.encode('utf-8') == "地址"):
            addressEng = infoTd[2].getchildren()
            for node in addressEng:
                if (node.tag == "div"):
                    infoTd[2].remove(node)
            
            textlist = list(infoTd[2].itertext())
            outputAddress  = ""
            for text in textlist:
                outputAddress += text
            
            return outputAddress.strip()
        #elif (len(resTitle)>0) and (resTitle[0].text.encode('utf-8') == "電話"):
            #return resTitle[2].text

def getTel(treeNode):
    resTelElementList = treeNode.xpath('/html/body/div/div/div/div/div/div/table/tr/td/table/tr/td/div')
    
    def processDiv(resTelDiv):
        elechildren = resTelDiv.getchildren()
        for child in elechildren:
            if ((child.tag == 'div') or (child.tag == 'table') or (child.tag == 'span')):
                resTelDiv.remove(child)
            
        textList = resTelDiv.itertext()
        count=0
        resultreturn  = ""
        for text in textList:
            count +=1
            if (count==2):
                resultreturn = text
        return resultreturn.replace(":", "").replace(" ", "").strip()
    
    if (len(resTelElementList) > 1):
        result = processDiv(resTelElementList[1])
        if (result.encode('utf-8') == "儲存為心水餐廳"):
            result = processDiv(resTelElementList[0])
    elif (len(resTelElementList)>0):
        result = processDiv(resTelElementList[0])
    else:
        result = ""
        
    return result
    
def getFoodList(treeNode):
    resInfoTr = treeNode.xpath('/html/body/div/div/div/div/div/div/table/tr/td/table/tr')

    hasFood = False
    allFoodText = ""
    
    for tempElement in resInfoTr:
        temp2 = tempElement.findall('.//td')
        if (temp2[0].text is not None) and ((temp2[0].text.encode('utf-8') == "食家推介") or (temp2[0].text.encode('utf-8') == "招牌菜")):
            hasFood = True
            allFoodText = temp2[1].text

    foodList = allFoodText.encode('utf-8').split('、')

    return foodList


d = db_restaurantLinks()
resLinks = d.getAllUncrawled()

for resRecord in resLinks:
    #download the file:
    file = urllib2.urlopen(resRecord[1])
    data = file.read()
    data = data.decode('utf-8')
    file.close()

    parser = etree.HTMLParser(encoding='utf-8')
    tree   = etree.fromstring(data.encode('utf-8'), parser)

    url = resRecord[1]
    resname = getResName(tree)
    if (resname is None):
        continue
    resaddress = getAddress(tree)
    restel = getTel(tree)
    print ""
    print "------------------------"
    print "URL: "+url
    #print "------------------------"
    print "NAME: "+resname
    #print "------------------------"
    print "ADDRESS: "+resaddress
    #print "------------------------"
    print "TEL: "+restel
    #print "------------------------"
    
    d2 = db_restaurant()
    d2.insert(resname.encode('utf-8'),  restel.encode('utf-8'),  resaddress.encode('utf-8'))
    resUID = d2.getUID(resname)
    
    d3 = db_food()
    foodList = getFoodList(tree)
    for food in foodList:
        if (food != ""):
            d3.insert(food)
            foodUID = d3.getUID(food)
            print food + "(" + str(resUID) + "," + str(foodUID) + ")"
            d3.insertFoodRes(foodUID,  resUID)
    print "------------------------"
    print ""
