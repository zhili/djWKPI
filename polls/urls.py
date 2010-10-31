from django.conf.urls.defaults import *
from django.conf import settings
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

    (r'^$', 'polls.views.index'),
    # (r'^(?P<poll_id>\d+)/$', 'polls.views.detail'),
    # (r'^(?P<poll_id>\d+)/results/$', 'polls.views.results'),
    # (r'^(?P<poll_id>\d+)/vote/$', 'polls.views.vote'),

    (r'^data/$', 'polls.views.chart_data')

)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
# urlpatterns = patterns('polls.views',
#     (r'^polls/$', 'index'),
#     (r'^polls/(?P<poll_id>\d+)/$', 'detail'),
#     (r'^polls/(?P<poll_id>\d+)/results/$', 'results'),
#     (r'^polls/(?P<poll_id>\d+)/vote/$', 'vote'),
# )