from django.http import HttpResponse
from django.shortcuts import render_to_response
from models import Client,Category,DealArchive,PushedDeals,Wish

import urllib2
import time
import feedparser
import BeautifulSoup
#from imaplib import USER
import re




class JSONCreatedResponse(HttpResponse):
    def __init__(self, *args, **kwargs):
        super(JSONCreatedResponse, self).__init__(args, kwargs)
        self.status_code = 201
        self['Content-Type'] = 'application/json'


class JSONResponse(HttpResponse):
    def __init__(self, *args, **kwargs):
        super(JSONResponse, self).__init__(args, kwargs)
        self.status_code = 200
        self['Content-Type'] = 'application/json'

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    """
    return dict(message=('Hello World'))



#########################################################################
# Table Structure
#db.define_table('Client',Field('UDID'),Field('TokenID'),Field('BundleID')) 
#db.define_table('Category',Field('Name'),Field('ServiceID'),Field('ServiceName')) 
#db.define_table('Wish',Field('UserID'),Field('CategoryId'),Field('MinPrice'),Field('MaxPrice'),Field('Keyword')) 
#########################################################################
    
    
def createUser(request):
    _udid = request.GET['udid']
    _tokenId = request.GET['tokenId']
    _bundleId = request.GET['bundleId']
    userId = ""
    try : 
        user = Client.objects.get(udid =_udid)
        user.tokenId = _tokenId
        user.bundleId = _bundleId
        userId = user.id
        user.save()
    except :
        add_to_db = Client(udid=_udid,tokenId=_tokenId,bundleId=_bundleId)
        add_to_db.save()
        userId= add_to_db.id
    return JSONResponse({'userId':userId})
    
 
def addWish(request):
    _userId= request.GET['userId']
    _categoryId = request.GET['categoryId']
    _minPrice = request.GET['minPrice']
    _maxPrice= request.GET['maxPrice']
    _brand= request.GET['brand']
    record=Wish(userId=_userId,categoryId=_categoryId,minPrice=_minPrice,maxPrice=_maxPrice,brand=_brand)
    record.save()
    wishId = record.id
    return JSONResponse({'wishId':wishId})
 
     
def deleteWish(request):
    _userId = request.GET['userId']
    _wishId = request.GET['wishId']
    Dwish = Wish.objects.filter(userId = _userId)
    Dwish.delete()
    Dpush_deals = PushedDeals.objects.filter(wishId = _wishId)
    Dpush_deals.delete()
    return JSONResponse({'wishId':_wishId})
    
    
     
def getDealWithId(request):
    req_dealId = request.GET['dealId']
    deal = DealArchive.objects.get(dealId = req_dealId)
    return JSONResponse({"deal":deal})   
      
     
                                    

     
def getDeals(request):
    _categoryID = request.GET['categoryID']
    _pageNumber = int(request.GET['page'])
    deals = DealArchive.objects.filter(categoryId = _categoryID)
    totalDeals=len(deals)
    totalPages=totalDeals/10
    subsetDeals=deals[(_pageNumber-1)*10:_pageNumber*10]
    return JSONResponse(dict(currentPage=_pageNumber,totalPages=totalPages,products=subsetDeals))          
 

     
"""def getBuyProductInfo():
    serviceUrl = "http://couponfeed.linksynergy.com/coupon?token=8a6d716093aeed7b79a38146d4e059ff668eca73620dd6f498877bd96953fd10&category=13&network=1&resultsperpage=100&pagenumber=1"
    response = urllib2.urlopen(serviceUrl) 
    return response"""
 
        
#########################################################################
#Private methods
#########################################################################
priceregex =  '\$[0-9]+\,?\.?[0-9]*'
categoryId_mobilePhones = 1
categoryId_camera = 2
categoryId_laptop = 3
categoryId_mp3player = 4
categoryId_books = 5
categoryId_tablet = 6
categoryId_shoe = 7
categoryId_watch = 8
categoryId_glasses = 9


def getPriceFromString(string1):
    matches = re.findall(priceregex,string1)
    if matches.__len__() > 0:
        match = matches[0]
        match = match.replace("$", "")
        match = match.replace(",", "")
        return float(match)
    else:
        return 0






        
         
#########################################################################
#########################################################################

   
#########################################################################
#Laptopdeals    
#########################################################################

def isLaptopExistsInString(string1):
    if ("laptop" in string1.lower()) or ("notebook" in string1.lower()) or ("netbook" in string1.lower() or ("macbook" in string1.lower())):
        return True
    else:
        return False  
    
def macmall_laptopdeals():
    d = feedparser.parse('feed://www.macmall.com/mall/rss/bestSellersElectronics.xml')
    entries = d['entries']
    output = []
    for item in entries:
        titleString = item['title']
        if isLaptopExistsInString(titleString):
            newDict = {}
            newDict['catid'] = categoryId_laptop
            newDict['id']=item['link']
            newDict['title'] = item['title']
            newDict['url'] = item['link']
            newDict['price'] = getPriceFromString(titleString)
            newDict['imageurl'] = ''
            output.append(newDict)

    return output

def tigerdirect_laptopdeals():
    d = feedparser.parse('feed://www.tigerdirect.com/xml/rsstigercat17.xml')
    entries = d['entries']
    output = []
    for item in entries:
        newDict = {}
        newDict['title'] = item['title']
        newDict['url'] = item['link']
        newDict['id'] = item['id']
        newDict['catid'] = categoryId_laptop
        newDict['price'] = getPriceFromString(item['title'])
        newDict['imageurl'] =   BeautifulSoup(item['summary']).find("img")['src']
        output.append(newDict)

    return output

    

def newegg_laptopdeals():
    d = feedparser.parse('feed://www.newegg.com/Product/RSS.aspx?Submit=DailyDeals&N=40000032&IsNodeId=1&ShowDeactivatedMark=False')
    entries = d['entries']
    output = []
    for item in entries:
        newDict = {}
        newDict['title'] =  item['title_detail']['value']
        newDict['price'] = getPriceFromString(item['title'])
        newDict['url'] = item['link']
        newDict['catid'] = categoryId_laptop
        newDict['id'] = item['id']
        newDict['imageurl'] =   BeautifulSoup(item['summary']).find("img")['src']
        output.append(newDict)
    return output  


def woot_laptopdeals():
    d = feedparser.parse('feed://www.woot.com/Blog/Feed.ashx')
    entries = d['entries']
    output = []
    if entries.__len__() <= 0:
        return
    
    item = entries[0] # only todays deal has to be checked
    titleString = item['title_detail']['value']
    if isLaptopExistsInString(titleString):
        newDict = {}
        newDict['title'] =  titleString
        newDict['url'] = item['link']
        newDict['id'] = item['id']
        newDict['catid'] = categoryId_laptop
        newDict['price'] = getPriceFromString(titleString)

        media = item['media_content']
        if media.__len__() > 0:
            for mediaitem in media:
                if mediaitem['type'] == "image/jpeg":
                    newDict['imageurl'] = mediaitem['url']
                        
        output.append(newDict)
    return output         


def amazon_laptopdeals():
    d = feedparser.parse('feed://rssfeeds.s3.amazonaws.com/goldbox')
    entries = d['entries']
    output = []
    for item in entries:
        titleString = item['title_detail']['value']
        if isLaptopExistsInString(titleString):
            newDict = {}
            newDict['title'] =  titleString
            newDict['url'] = item['link']
            newDict['id'] = item['id']
            newDict['catid'] = categoryId_laptop
            newDict['price'] = getPriceFromString(titleString)
            newDict['imageurl'] =   BeautifulSoup(item['summary']).find("img")['src']   
            output.append(newDict)
    return output   

 
def update_laptopdeals_archive():
    DealArchive.objects.get(categoryId = categoryId_laptop).delete() 
    deals = []
    deals.extend(amazon_laptopdeals())
    deals.extend(woot_laptopdeals())
    deals.extend(newegg_laptopdeals())
    deals.extend(tigerdirect_laptopdeals())
    deals.extend(macmall_laptopdeals())
    for deal in deals:
                       dealID=deal['id']
                       dealUrl=deal['url']
                       brand=''
                       titleString=deal['title']
                       imageUrl=deal['imageurl']
                       offerPrice = 0
                       originalPrice = 0
                       categoryId = deal['catid']
                       if  deal.has_key('price'):
                            offerPrice=  int(float(deal['price']))
                       DealArchive.objects.filter(dealId = dealID).update(categoryId=categoryId,dealId=dealID,dealUrl=dealUrl,brand=brand,titleString=titleString,imageUrl=imageUrl,originalPrice=originalPrice,offerPrice=offerPrice)     
    
#########################################################################
#mobile phone deals    
#########################################################################    
    
def isMobileExistsInString(string1):
    if ("cellphone" in string1.lower()) or ("mobilephone" in string1.lower()) or ("iphone" in string1.lower() or (" phone " in string1.lower())):
        return True
    else:
        return False  
 
def macmall_phonedeals():
    d = feedparser.parse('feed://www.macmall.com/mall/rss/bestSellersElectronics.xml')
    entries = d['entries']
    output = []
    for item in entries:
        titleString = item['title']
        if isMobileExistsInString(titleString):
            newDict = {}
            newDict['catid'] = categoryId_mobilePhones
            newDict['id']= item['link']
            newDict['title'] = item['title']
            newDict['url'] = item['link']
            newDict['price'] = getPriceFromString(titleString)
            newDict['imageurl'] =  ''
            output.append(newDict)

    return output
def tigerdirect_mobiledeals():
    d = feedparser.parse('feed://www.tigerdirect.com/xml/rsstigercat5116.xml')
    entries = d['entries']
    output = []
    for item in entries:
        newDict = {}
        newDict['title'] = item['title']
        newDict['url'] = item['link']
        newDict['id'] = item['id']
        newDict['catid'] = categoryId_mobilePhones
        newDict['price'] = getPriceFromString(item['title'])
        newDict['imageurl'] =   BeautifulSoup(item['summary']).find("img")['src']
        output.append(newDict)

    return output

def newegg_mobiledeals():
    d = feedparser.parse('feed://www.newegg.com/Product/RSS.aspx?Submit=RSSDailyDeals&Depa=0')
    entries = d['entries']
    output = []
    for item in entries:
        titleString = item['title_detail']['value']
        if isMobileExistsInString(titleString):
            newDict = {}
            newDict['title'] =  titleString
            newDict['url'] = item['link']
            newDict['id'] = item['id']
            newDict['catid'] = categoryId_mobilePhones
            newDict['imageurl'] =   BeautifulSoup(item['summary']).find("img")['src']
            newDict['price'] = getPriceFromString(titleString)
            output.append(newDict)
    return output 

def woot_mobiledeals():
    d = feedparser.parse('feed://www.woot.com/Blog/Feed.ashx')
    entries = d['entries']
    output = []
    item = entries[0]
    titleString = item['title_detail']['value']
    if isMobileExistsInString(titleString):
        newDict = {}
        newDict['title'] = titleString
        newDict['url'] = item['link']
        newDict['id'] = item['id']
        newDict['catid'] = categoryId_mobilePhones
        newDict['price'] = getPriceFromString(titleString)

        media = item['media_content']
        if media.__len__() > 0:
            for mediaitem in media:
                if mediaitem['type'] == "image/jpeg":
                    newDict['imageurl'] = mediaitem['url']
        output.append(newDict)
    return output  

def amazon_mobiledeals():
    d = feedparser.parse('feed://rssfeeds.s3.amazonaws.com/goldbox')
    entries = d['entries']
    output = []
    for item in entries:
        titleString = item['title_detail']['value']
        if isMobileExistsInString(titleString):
            newDict = {}
            newDict['title'] =  titleString
            newDict['url'] = item['link']
            newDict['id'] = item['id']
            newDict['catid'] = categoryId_mobilePhones
            newDict['price'] = getPriceFromString(titleString)
            newDict['imageurl'] =   BeautifulSoup(item['summary']).find("img")['src']   
            output.append(newDict)
    return output 



 
def update_mobilephonedeals_archive():
    DealArchive.objects.filter(categoryId = categoryId_mobilePhones).delete() 
    deals = []
    deals.extend(amazon_mobiledeals())
    deals.extend(woot_mobiledeals())
    deals.extend(newegg_mobiledeals())
    deals.extend(tigerdirect_mobiledeals())
    deals.extend(macmall_phonedeals())
    for deal in deals:
        dealID=deal['id']
        dealUrl=deal['url']
        brand=''
        titleString=deal['title']
        imageUrl=deal['imageurl']
        offerPrice = 0
        originalPrice = 0
        categoryId = deal['catid']
        if  deal.has_key('price'):
            offerPrice=  int(float(deal['price']))
            DealArchive(DealArchive.dealId == dealID,categoryId=categoryId,dealId=dealID,dealUrl=dealUrl,brand=brand,titleString=titleString,imageUrl=imageUrl,originalPrice=originalPrice,offerPrice=offerPrice)    

#########################################################################
#camera deals    
#########################################################################  

def tigerdirect_cameradeals():
    d = feedparser.parse('feed://feeds.feedburner.com/FeaturedDigitalCamera-Tigerdirectcom')
    entries = d['entries']
    output = []
    for item in entries:
        newDict = {}
        newDict['title'] = item['title']
        newDict['url'] = item['link']
        newDict['id'] = item['id']
        newDict['catid'] = categoryId_camera
        newDict['price'] = getPriceFromString(item['title'])
        newDict['imageurl'] =   BeautifulSoup(item['summary']).find("img")['src']
        output.append(newDict)

    return output

def newegg_cameradeals():
    d = feedparser.parse('feed://www.newegg.com/Product/RSS.aspx?Submit=RSSDailyDeals&Depa=0')
    entries = d['entries']
    output = []
    for item in entries:
        titleString = item['title_detail']['value']
        if "camera" in titleString.lower():
            newDict = {}
            newDict['title'] =  titleString
            newDict['url'] = item['link']
            newDict['id'] = item['id']
            newDict['catid'] =categoryId_camera
            newDict['imageurl'] =   BeautifulSoup(item['summary']).find("img")['src']
            newDict['price'] = getPriceFromString(titleString)
            output.append(newDict)
    return output 

def woot_cameradeals():
    d = feedparser.parse('feed://www.woot.com/Blog/Feed.ashx')
    entries = d['entries']
    output = []
    item = entries[0]
    titleString = item['title_detail']['value']
    if "camera" in titleString.lower():
        newDict = {}
        newDict['title'] =  titleString
        newDict['url'] = item['link']
        newDict['id'] = item['id']
        newDict['catid'] = categoryId_camera
        newDict['price'] = getPriceFromString(titleString)
        media = item['media_content']
        if media.__len__() > 0:
            for mediaitem in media:
                if mediaitem['type'] == "image/jpeg":
                    newDict['imageurl'] = mediaitem['url']
        output.append(newDict)
    return output  

def amazon_cameradeals():
    d = feedparser.parse('feed://rssfeeds.s3.amazonaws.com/goldbox')
    entries = d['entries']
    output = []
    for item in entries:
        titleString = item['title_detail']['value']

        if "camera" in titleString.lower():
            newDict = {}
            newDict['title'] =  titleString
            newDict['url'] = item['link']
            newDict['id'] = item['id']
            newDict['catid'] =categoryId_camera
            newDict['price'] = getPriceFromString(titleString)
            newDict['imageurl'] =   BeautifulSoup(item['summary']).find("img")['src']   
            output.append(newDict)
    return output 

 
def update_cameradeals_archive():
    DealArchive.objects.filter(categoryId = categoryId_camera).delete() 
    deals = []
    deals.extend(amazon_cameradeals())
    deals.extend(woot_cameradeals())
    deals.extend(newegg_cameradeals())
    deals.extend(tigerdirect_cameradeals())
    for deal in deals:
                       dealID=deal['id']
                       dealUrl=deal['url']
                       brand=''
                       titleString=deal['title']
                       imageUrl=deal['imageurl']
                       offerPrice = 0
                       originalPrice = 0
                       categoryId = deal['catid']
                       if  deal.has_key('price'):
                            offerPrice=  int(float(deal['price']))
                       DealArchive.objects.filter(dealId = dealID).update(categoryId=categoryId,dealId=dealID,dealUrl=dealUrl,brand=brand,titleString=titleString,imageUrl=imageUrl,originalPrice=originalPrice,offerPrice=offerPrice)    


#########################################################################
#tablet deals    
#########################################################################  

def isTabletExistsInString(string1):
    if ("tablet" in string1.lower()) or ("ipad" in string1.lower()):
        return True
    else:
        return False 



def macmall_tabletdeals():
    d = feedparser.parse('feed://www.macmall.com/mall/rss/bestSellersElectronics.xml')
    entries = d['entries']
    output = []
    for item in entries:
        titleString = item['title']
        if isTabletExistsInString(titleString):
            newDict = {}
            newDict['catid'] = categoryId_tablet
            newDict['id']=item['link']
            newDict['title'] = titleString
            newDict['url'] = item['link']
            newDict['price'] = getPriceFromString(titleString)
            newDict['imageurl'] = ''
            output.append(newDict)

    return output


def tigerdirect_tabletdeals():
    d = feedparser.parse('feed://www.tigerdirect.com/xml/rsstigercat6838.xml')
    entries = d['entries']
    output = []
    for item in entries:
        newDict = {}
        newDict['title'] = item['title']
        newDict['url'] = item['link']
        newDict['id'] = item['id']
        newDict['catid'] = categoryId_tablet
        newDict['price'] = getPriceFromString(item['title'])
        newDict['imageurl'] =   BeautifulSoup(item['summary']).find("img")['src']
        output.append(newDict)

    return output

def newegg_tabletdeals():
    d = feedparser.parse('feed://www.newegg.com/Product/RSS.aspx?Submit=RSSDailyDeals&Depa=0')
    entries = d['entries']
    output = []
    for item in entries:
        titleString = item['title_detail']['value']
        if isTabletExistsInString(titleString):
            newDict = {}
            newDict['title'] =  titleString
            newDict['url'] = item['link']
            newDict['id'] = item['id']
            newDict['catid'] = categoryId_tablet
            newDict['imageurl'] =   BeautifulSoup(item['summary']).find("img")['src']
            newDict['price'] = getPriceFromString(titleString)
            output.append(newDict)
    return output 

def woot_tabletdeals():
    d = feedparser.parse('feed://www.woot.com/Blog/Feed.ashx')
    entries = d['entries']
    output = []
    item = entries[0]
    titleString = item['title_detail']['value']
    if isTabletExistsInString(titleString):
        newDict = {}
        newDict['title'] =  titleString
        newDict['url'] = item['link']
        newDict['id'] = item['id']
        newDict['catid'] = categoryId_tablet
        newDict['price'] = getPriceFromString(titleString)
        media = item['media_content']
        if media.__len__() > 0:
            for mediaitem in media:
                if mediaitem['type'] == "image/jpeg":
                    newDict['imageurl'] = mediaitem['url']
        output.append(newDict)
    return output  

def amazon_tabletdeals():
    d = feedparser.parse('feed://rssfeeds.s3.amazonaws.com/goldbox')
    entries = d['entries']
    output = []
    for item in entries:
        titleString = item['title_detail']['value']
        if isTabletExistsInString(titleString):
            newDict = {}
            newDict['title'] =  titleString
            newDict['url'] = item['link']
            newDict['id'] = item['id']
            newDict['catid'] = categoryId_tablet
            newDict['price'] = getPriceFromString(titleString)
            newDict['imageurl'] =   BeautifulSoup(item['summary']).find("img")['src']   
            output.append(newDict)
    return output 

 
def update_tabletdeals_archive():
    DealArchive.objects.filter(categoryId = categoryId_tablet).delete() 
    deals = []
    deals.extend(amazon_tabletdeals())
    deals.extend(woot_tabletdeals())
    deals.extend(newegg_tabletdeals())
    deals.extend(tigerdirect_tabletdeals())
    deals.extend(macmall_tabletdeals())
    for deal in deals:
                       dealID=deal['id']
                       dealUrl=deal['url']
                       brand=''
                       titleString=deal['title']
                       imageUrl=deal['imageurl']
                       offerPrice = 0
                       originalPrice = 0
                       categoryId = deal['catid']
                       if  deal.has_key('price'):
                            offerPrice=  int(float(deal['price']))
                       DealArchive.objects.filter(dealId = dealID).update(categoryId=categoryId,dealId=dealID,dealUrl=dealUrl,brand=brand,titleString=titleString,imageUrl=imageUrl,originalPrice=originalPrice,offerPrice=offerPrice)    

#########################################################################
#mp3player deals    
#########################################################################  

def isMp3PlayerExistsInString(string1):
    if ("mediaplayer" in string1.lower()) or ("mp3player" in string1.lower()) or ("ipod" in string1.lower()):
        return True
    else:
        return False

def macmall_mp3playerdeals():
    d = feedparser.parse('feed://www.macmall.com/mall/rss/bestSellersElectronics.xml')
    entries = d['entries']
    output = []
    for item in entries:
        titleString = item['title']
        if isMp3PlayerExistsInString(titleString):
            newDict = {}
            newDict['catid'] = categoryId_mp3player
            newDict['id']= item['link']
            newDict['title'] = titleString
            newDict['url'] = item['link']
            newDict['price'] = getPriceFromString(titleString)
            newDict['imageurl'] = ''
            output.append(newDict)

    return output

def tigerdirect_mp3playerdeals():
    d = feedparser.parse('feed://www.tigerdirect.com/xml/rsstigercat15.xml')
    entries = d['entries']
    output = []
    for item in entries:
        newDict = {}
        newDict['title'] = item['title']
        newDict['url'] = item['link']
        newDict['id'] = item['id']
        newDict['catid'] = categoryId_mp3player
        newDict['price'] = getPriceFromString(item['title'])
        newDict['imageurl'] =   BeautifulSoup(item['summary']).find("img")['src']
        output.append(newDict)

    return output

def newegg_mp3playerdeals():
    d = feedparser.parse('feed://www.newegg.com/Product/RSS.aspx?Submit=RSSDailyDeals&Depa=0')
    entries = d['entries']
    output = []
    for item in entries:
        titleString = item['title_detail']['value']
        if isMp3PlayerExistsInString(titleString):
            newDict = {}
            newDict['title'] = titleString
            newDict['url'] = item['link']
            newDict['id'] = item['id']
            newDict['catid'] = categoryId_mp3player
            newDict['imageurl'] =   BeautifulSoup(item['summary']).find("img")['src']
            newDict['price'] = getPriceFromString(titleString)
            output.append(newDict)
    return output 

def woot_mp3playerdeals():
    d = feedparser.parse('feed://www.woot.com/Blog/Feed.ashx')
    entries = d['entries']
    output = []
    if entries.__len__() <= 0:
        return
    item = entries[0]
    titleString = item['title_detail']['value']
    if isMp3PlayerExistsInString(titleString):
        newDict = {}
        newDict['title'] =  titleString
        newDict['url'] = item['link']
        newDict['id'] = item['id']
        newDict['catid'] = categoryId_mp3player
        newDict['price'] = getPriceFromString(titleString)
        media = item['media_content']
        if media.__len__() > 0:
            for mediaitem in media:
                if mediaitem['type'] == "image/jpeg":
                    newDict['imageurl'] = mediaitem['url']
        output.append(newDict)
    return output  

def amazon_mp3playerdeals():
    d = feedparser.parse('feed://rssfeeds.s3.amazonaws.com/goldbox')
    entries = d['entries']
    output = []
    for item in entries:
        titleString = item['title_detail']['value']
        if isMp3PlayerExistsInString(titleString):
            newDict = {}
            newDict['title'] =  titleString
            newDict['url'] = item['link']
            newDict['id'] = item['id']
            newDict['catid'] = categoryId_mp3player
            newDict['price'] = getPriceFromString(titleString)
            newDict['imageurl'] =   BeautifulSoup(item['summary']).find("img")['src']   
            output.append(newDict)
    return output 


 
def update_mp3playerdeals_archive():
    DealArchive.objects.filter(categoryId = categoryId_mp3player).delete() 
    deals = []
    deals.extend(amazon_mp3playerdeals())
    deals.extend(woot_mp3playerdeals())
    deals.extend(newegg_mp3playerdeals())
    deals.extend(tigerdirect_mp3playerdeals())
    deals.extend(macmall_mp3playerdeals())
    for deal in deals:
                       dealID=deal['id']
                       dealUrl=deal['url']
                       brand=''
                       titleString=deal['title']
                       imageUrl=deal['imageurl']
                       offerPrice = 0
                       originalPrice = 0
                       categoryId = deal['catid']
                       if  deal.has_key('price'):
                            offerPrice=  int(float(deal['price']))
                       DealArchive.objects.filter(dealId = dealID).update(categoryId=categoryId,dealId=dealID,dealUrl=dealUrl,brand=brand,titleString=titleString,imageUrl=imageUrl,originalPrice=originalPrice,offerPrice=offerPrice)    


#########################################################################
#shoe deals    
######################################################################### 

def shoebuy_shoedeals():
    d = feedparser.parse('feed://www.shoebuy.com/rss-sale-shoes')
    entries = d['entries']
    output = []
    for item in entries:
        newDict = {}
        newDict['title'] = item['title']
        newDict['url'] = item['link']
        newDict['id'] = item['link']
        newDict['catid'] = 7
        newDict['price'] = getPriceFromString(item['summary'])
        newDict['imageurl'] =   BeautifulSoup(item['summary']).find("img")['src']
        output.append(newDict)

    return output

 
def update_shoedeals_archive():
    DealArchive.objects.filter(categoryId = 7).delete() 
    deals = []
    deals.extend(shoebuy_shoedeals())
    for deal in deals:
                       dealID=deal['id']
                       dealUrl=deal['url']
                       brand=''
                       titleString=deal['title']
                       imageUrl=deal['imageurl']
                       offerPrice = 0
                       originalPrice = 0
                       categoryId = deal['catid']
                       if  deal.has_key('price'):
                            offerPrice=  int(float(deal['price']))
                       DealArchive.objects.filter(dealId = dealID).update(categoryId=categoryId,dealId=dealID,dealUrl=dealUrl,brand=brand,titleString=titleString,imageUrl=imageUrl,originalPrice=originalPrice,offerPrice=offerPrice)  



#########################################################################
#watch deals    
#########################################################################  

def onedayawatch_watchdeals():
    d = feedparser.parse('feed://www.onedaywatch.com/rss.xml')
    entries = d['entries']
    output = []
    for item in entries:
        newDict = {}
        newDict['title'] = item['title']
        newDict['url'] = item['link']
        newDict['id'] = item['id']
        newDict['catid'] = 8
        newDict['price'] = getPriceFromString(item['title'])
        newDict['imageurl'] =   BeautifulSoup(item['summary']).find("img")['src']
        output.append(newDict)

    return output

 
def update_watchdeals_archive():
    DealArchive.objects.filter(categoryId = 3).delete() 
    deals = []
    deals.extend(onedayawatch_watchdeals())
    for deal in deals:
                       dealID=deal['id']
                       dealUrl=deal['url']
                       brand=''
                       titleString=deal['title']
                       imageUrl=deal['imageurl']
                       offerPrice = 0
                       originalPrice = 0
                       categoryId = deal['catid']
                       if  deal.has_key('price'):
                            offerPrice=  int(float(deal['price']))
                       DealArchive.objects.filter(dealId = dealID).update(categoryId=categoryId,dealId=dealID,dealUrl=dealUrl,brand=brand,titleString=titleString,imageUrl=imageUrl,originalPrice=originalPrice,offerPrice=offerPrice)


######################################################################################################################################################################

def keywordsExistsInString(keywords,fullString):
    for keyword1 in keywords:
        if keyword1 in fullString:
            return True
    return False

 
"""def runmatch():
    categories = Category.select()
    Matches = []
    for category in categories:
        categoryId=int(category['categoryId'])
        wishes =  db(db.Wish.categoryId ==categoryId).select()
        deals = db().select(db.DealArchive.categoryId ==categoryId)
        return response.json(dict(wishes=wishes))
        for wish in  wishes:
            wishPrice = wish.maxPrice
            wishBrand= wish.brand
            keywords = []
            if wishBrand.__len__ > 0:
                keywords.extend(wishBrand.split())
            for deal in  deals:
                if (deal['offerPrice'] < wishPrice) & (keywordsExistsInString(keywords,deal['titleString'])):
                    userRecords= db(db.Client.id ==wish['userId']).select()
                    if userRecords.__len__ > 0:
                         userRecord = userRecords[0]
                         match=dict (userRecord['tokenId'],wish['id'],deal['dealId'])
                         Matches.append(match)
                         pushDeals(userRecord['tokenId'],wish['id'],deal['dealId'])
    return  response.json(dict(matches = Matches))
"""


     
def pushDeals(tokenID,wishID,dealId):
    logging.info('push deals method started')
    application_key ='6hjfR2XsT6-isgb8ren5aA'
    master_secret = 'XIYG_6PAQyWPKWfTARCNBg'
    finalDict=dict (wishId=wishID,dealId=dealId)
    
    import urbanairship
    airship = urbanairship.Airship(application_key, master_secret)
    airship.register(tokenID, alias='shirish')
    airship.push({'aps': {'alert': 'Hey! we have found some deals of your choice.',"sound": "default","deal":[finalDict]}},device_tokens=[tokenID])
    return 'push sucess'


######################################################################################################################################################################
#Testing methods
######################################################################################################################################################################
 
def getAllDeals():
    categories = Category.objects.all()
    Matches = []
    for category in categories:
        categoryId=category['categoryId']
        wishes = Wish.objects.filter(categoryId = categoryId)
        deals = DealArchive.objects.filter(categoryId =categoryId) 
        Matches.extend(deals)
    return JSONResponse(dict(matches = Matches))

 
def getAllWishes():
    categories = Category.objects.all()
    Matches = []
    for category in categories:
        categoryId=int(category['categoryId'])
        wishes = Wish.objects.filter(categoryId =categoryId)
        #wishes =  db(db.Wish.ALL).select()
        deals = DealArchive.objects.filter(categoryId =categoryId)
        Matches.extend(wishes)
    return JSONResponse(dict(matches = Matches))



 
def wipePushedDeals():
     PushedDeals.objects.all().delete()
     return 'deleted all records sucessfully'

 
def testUrbanAirship():
    application_key ='6hjfR2XsT6-isgb8ren5aA'
    master_secret = 'XIYG_6PAQyWPKWfTARCNBg'
    tokenID = 'E11F4E9B43F3D9E31DBCBCC4EC1FDAD947ED4EE3E1904AE2FFF9FDF6791D344B'
    
    import urbanairship
    airship = urbanairship.Airship(application_key, master_secret)
    airship.register(tokenID, alias='shirish')
    airship.push({'aps': {'alert': 'Hey! we have found some deals of your choice.',"sound": "default"}},device_tokens=[tokenID])
    return 'sucess'

