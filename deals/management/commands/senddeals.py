from django.core.management.base import BaseCommand, CommandError
from dealNotifier.deals.models  import DealArchive , Category , PushedDeals , Client, Wish
from dealNotifier.deals import feedparser
from dealNotifier.deals  import urbanairship

class Command(BaseCommand):
    
    
    
    def handle(self , *args, **options):
        def matchDeals():   
            categories = Category.objects.all()
            #matchedDeals = []
            for  category in categories:
                categoryID = category.categoryId
                wishes= Wish.objects.filter(categoryId = categoryID)
                for wish in wishes:
                    #print wish.id
                    wishID = wish.id
                    wishBrand = wish.brand.rstrip()
                    wishBrandNames = wishBrand.split(',')
                    wishCategoryID = wish.categoryId
                    wishPrice = wish.maxPrice
                    wishUserID = wish.userId
                    deals_category = DealArchive.objects.filter(categoryId = wishCategoryID)
                    for deal in deals_category:
                        #print deal.dealId
                        dealID = deal.dealId
                        #dealUrl = deal.dealUrl
                        title_String = deal.titleString
                        #imageUrl = deal.imageUrl
                        #originalPrice = deal.originalPrice                        
                        offerPrice = deal.offerPrice
                        
                        if  offerPrice <  wishPrice:
                            if wishBrandNames[0] == "":
                                try:
                                    PushedDeals.objects.get(dealId = dealID)
                                    PushedDeals.objects.get(wishId = wishID)
                                except:
                                    PushedDeals(dealId=dealID,wishId=wishID).save()
                                    try:
                                        userRecord = Client.objects.get(id = wishUserID)
                                        #pushDeals(userRecord.tokenId,wishID,dealID)                                                    
                                        print 'token id :'+userRecord.tokenId
                                    except:
                                        print "no users"

                                                
                            else:
                                for temp in wishBrandNames:
                                    if (temp.lower().rstrip() in title_String.lower()):
                                        try:
                                            PushedDeals.objects.get(dealId = dealID)
                                            PushedDeals.objects.get(wishId = wishID)
                                        except:
                                            PushedDeals(dealId=dealID,wishId=wishID).save()
                                            try:
                                                userRecord = Client.objects.get(id = wishUserID)
                                                #pushDeals(userRecord.tokenId,wishID,dealID)                                                    
                                                print 'token id :'+userRecord.tokenId
                                            except:
                                                print "no users"
                                
                                            
                                            
                                            
                                            
        
        def pushDeals(tokenID,wishID,dealId):
            logging.info('push deals method started')
            application_key ='6hjfR2XsT6-isgb8ren5aA'
            master_secret = 'XIYG_6PAQyWPKWfTARCNBg'
            finalDict=dict (wishId=wishID,dealId=dealId)
            
            airship = urbanairship.Airship(application_key, master_secret)
            airship.register(tokenID, alias='shirish')
            airship.push({'aps': {'alert': 'Hey! we have found some deals of your choice.',"sound": "default","deal":[finalDict]}},device_tokens=[tokenID])
            return 'push sucess'
        
        matchDeals()        
        
        return "completed"
    
        
        
    