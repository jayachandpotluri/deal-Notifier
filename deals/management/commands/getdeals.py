from django.core.management.base import BaseCommand, CommandError
from dealNotifier.deals.models import Wish, Client , Category , DealArchive , PushedDeals
from dealNotifier.deals import feedparser
from dealNotifier.deals.BeautifulSoup import BeautifulSoup
import re

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



class Command(BaseCommand):
        

   


    
    def handle(self , *args, **options):
        
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
                               add_deal = DealArchive(categoryId=categoryId,dealId=dealID,dealUrl=dealUrl,brand=brand,titleString=titleString,imageUrl=imageUrl,originalPrice=originalPrice,offerPrice=offerPrice)     
                               add_deal.save()
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
                add_mobile = DealArchive(categoryId=categoryId,dealId=dealID,dealUrl=dealUrl,brand=brand,titleString=titleString,imageUrl=imageUrl,originalPrice=originalPrice,offerPrice=offerPrice)    
                add_mobile.save()
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
                               add_camera = DealArchive(categoryId=categoryId,dealId=dealID,dealUrl=dealUrl,brand=brand,titleString=titleString,imageUrl=imageUrl,originalPrice=originalPrice,offerPrice=offerPrice)    
                               add_camera.save()
        
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
                               add_tablet = DealArchive(categoryId=categoryId,dealId=dealID,dealUrl=dealUrl,brand=brand,titleString=titleString,imageUrl=imageUrl,originalPrice=originalPrice,offerPrice=offerPrice)    
                               add_tablet.save()
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
                               add_mp3 = DealArchive(categoryId=categoryId,dealId=dealID,dealUrl=dealUrl,brand=brand,titleString=titleString,imageUrl=imageUrl,originalPrice=originalPrice,offerPrice=offerPrice)    
                               add_mp3.save()
        
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
                               add_shoe = DealArchive(categoryId=categoryId,dealId=dealID,dealUrl=dealUrl,brand=brand,titleString=titleString,imageUrl=imageUrl,originalPrice=originalPrice,offerPrice=offerPrice)  
                               add_shoe.save()
        
        
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
                               add_watches = DealArchive(categoryId=categoryId,dealId=dealID,dealUrl=dealUrl,brand=brand,titleString=titleString,imageUrl=imageUrl,originalPrice=originalPrice,offerPrice=offerPrice)
                               add_watches.save()
        
        ######################################################################################################################################################################

        
        DealArchive.objects.all().delete()
        update_laptopdeals_archive()
        update_mobilephonedeals_archive()
        update_cameradeals_archive()
        update_mp3playerdeals_archive()
        update_shoedeals_archive()
        update_tabletdeals_archive()
        update_watchdeals_archive()   
        return 'deals updated'
                
    #########################################################################
    #Private methods
    #########################################################################

