from django.core.management.base import BaseCommand, CommandError
from dealNotifier.deals.models import Wish, Client , Category


class Command(BaseCommand):
    
    def handle(self , *args, **options): 
        Client.objects.all().delete()
        f = open('temp/db_User.csv','r')
        usersId = {}
        i=1
        for line in f.xreadlines():
            line_s = line.split(',')
            _userid = line_s[0]
            _udid = line_s[1] 
            _tokenId = line_s[2] 
            _bundleId = line_s[3] 
            add_to_db = Client(udid=_udid,tokenId=_tokenId,bundleId=_bundleId)
            add_to_db.save()
            usersId[_userid ] = i
            i=i+1
        f.close()
        
        Wish.objects.all().delete()
        f = open('temp/db_Wish.csv','r')
        for line in f.xreadlines():
            line_s = line.split(',')
            uid = line_s[1]
            _userId = usersId[uid ]
            _categoryId = line_s[2] 
            _minPrice = line_s[3]
            _maxPrice = line_s[4]
            _brand = line_s[5]
            add_to_db = Wish(userId=_userId,categoryId=_categoryId,minPrice=_minPrice,maxPrice=_maxPrice,brand=_brand)
            add_to_db.save()
        f.close()
        
        Category.objects.all().delete()
        f = open('temp/db_Category.csv','r')
        for line in f.xreadlines():
            line_s = line.split(',')
            _categoryId = line_s[1]
            _name = line_s[2]
            _serviceId = line_s[3]
            _serviceName = line_s[4]
            _serviceUrl = line_s[5]
            add_to_db = Category(categoryId = _categoryId, name =_name, serviceId =_serviceId , serviceName = _serviceName, serviceUrl = _serviceUrl)
            add_to_db.save()
        f.close()
        return 'database updated'
