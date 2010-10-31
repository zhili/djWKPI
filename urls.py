from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    # (r'^polls/$', 'polls.views.index'),
    #     (r'^polls/(?P<poll_id>\d+)/$', 'polls.views.detail'),
    #     (r'^polls/(?P<poll_id>\d+)/results/$', 'polls.views.results'),
    #     (r'^polls/(?P<poll_id>\d+)/vote/$', 'polls.views.vote'),

    (r'^polls/', include('polls.urls')),
    (r'^admin/upload/$', 'polls.views.upload'),
    (r'^admin/', include(admin.site.urls)),
)
# urlpatterns = patterns('polls.views',
#     (r'^polls/$', 'index'),
#     (r'^polls/(?P<poll_id>\d+)/$', 'detail'),
#     (r'^polls/(?P<poll_id>\d+)/results/$', 'results'),
#     (r'^polls/(?P<poll_id>\d+)/vote/$', 'vote'),
# )