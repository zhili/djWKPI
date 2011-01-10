import os, sys

apache_configuration= os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)
sys.path.append(workspace) 

sys.path.append('/usr/lib/pymodules/python2.6/django')
sys.path.append('/home/karpar/public-html/wkpi.com/djWKPI')
os.environ['DJANGO_SETTINGS_MODULE'] = 'djWKPI.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
