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

    (r'^(?P<cellname>\w+)/data/$', 'polls.views.chart_data'),
    (r'^(?P<cellname>\w+)/(?P<chart_id>\d+)/data/$', 'polls.views.chart_by_id'),
    (r'^worst-cells/(?P<ratetype>\w+)$', 'polls.views.worst_cells'),
    (r'^search/$', 'polls.views.tag_autocomplete'),
    (r'^results/(?P<cellname>\w+)$', 'polls.views.results'),
    # (r'^celldetail/$', 'polls.views.cellDetail')
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
