from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'paste.views.add', name='home'),
    url(r'^add', 'paste.views.add', name='add'),
    url(r'^(?P<pk>[a-zA-Z0-9]{6})(?:/(?P<output_type>download|raw)?)/?$', 'paste.views.view', name='view'),
    url(r'^sync$', 'paste.db_gen_laxers.view'),
)
