from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'api.views.index'),
    url(r'^v01/add/?', 'api.v01.views.add'),
    url(r'^v02/add/?', 'api.v02.views.add'),
    url(r'^v02/list/?', 'api.v02.views.list'),
)
