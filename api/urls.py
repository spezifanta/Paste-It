from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'api.views.index'),
    #url(r'^v01/add/(?P<content>.+?)/?$', 'api.v01.views.add'),
    #url(r'^v01/add/(?P<content>.+?)(?P<language>/[a-z]{2,8})?/?', 'api.v01.views.add'),
    url(r'^v01/add/?', 'api.v01.views.add'),
)
