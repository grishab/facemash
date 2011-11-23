from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^index/$','mash.views.index'),
    (r'^chose/$','mash.views.chose'),
    (r'^chose/(?P<id>\d+)/$','mash.views.getchose'),
    (r'^res/(?P<sid>\d+)/(?P<eid>\d+)/$','mash.views.getres'),
    (r'^start/$','mash.views.start'),
    (r'^fetch/$','mash.views.mysql'),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':'./media/'}),    
)
