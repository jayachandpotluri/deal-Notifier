from django.db import models

class Client(models.Model):
    udid = models.CharField(max_length = 50)
    tokenId = models.CharField(max_length = 50)
    bundleId = models.CharField(max_length = 50)
    
    def __unicode__(self):
        return self.udid
    
class Category(models.Model):
    categoryId = models.CharField(max_length = 50)
    name = models.CharField(max_length = 50)
    serviceId = models.CharField(max_length = 50)
    serviceName = models.CharField(max_length = 50)
    serviceUrl = models.CharField(max_length = 50)
    
    def __unicode__(self):
        return self.categoryId

class Wish(models.Model):
    userId = models.CharField(max_length = 50)
    categoryId = models.CharField(max_length = 50)
    minPrice = models.CharField(max_length = 50)
    maxPrice = models.CharField(max_length = 50)
    brand = models.CharField(max_length = 50)
    
    def __unicode__(self):
        return self.userId

class PushedDeals(models.Model):
    dealId = models.CharField(max_length = 50)
    wishId = models.CharField(max_length = 50)
    
    def __unicode__(self):
        return self.dealId

class DealArchive(models.Model):
    categoryId = models.CharField(max_length = 50)
    dealId = models.CharField(max_length = 50)
    dealUrl = models.CharField(max_length = 50)
    brand = models.CharField(max_length = 50)
    titleString = models.CharField(max_length = 50)
    imageUrl = models.CharField(max_length = 50)
    originalPrice = models.CharField(max_length = 50)
    offerPrice =models.CharField(max_length = 50)
    
    def __unicode__(self):
        return self.categoryId