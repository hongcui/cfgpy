'''
Created on Aug 31, 2012

@author: alex
'''
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cfgpy.settings")

# This application object is used by the development server
# as well as any WSGI server configured to use this file.
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

path = '/home/alex/workspace/cfgpy/src/cfgpy'
path2 = '/home/alex/workspace/cfgpy/src'
if path not in sys.path:
    sys.path.append(path)
if path2 not in sys.path:
    sys.path.append(path2)
