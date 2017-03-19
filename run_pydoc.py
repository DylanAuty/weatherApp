import django
import pydoc
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'weatherProj.settings'
django.setup()
pydoc.cli()

