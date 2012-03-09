from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('deals.views',
    # Examples:
    url(r'^createuser', 'createUser', name='createUser'),
    url(r'^addWish', 'addWish', name='addWish'),
    url(r'^deleteWish', 'deleteWish', name='deleteWish'),
    url(r'^getDealWithId', 'getDealWithId', name='getDealWithId'),
    url(r'^getDeals', 'getDeals', name='getDeals'),    
    
    
    
    

)
