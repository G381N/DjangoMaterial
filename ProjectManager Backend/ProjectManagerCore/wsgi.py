import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProjectManagerCore.settings')
import os
from django.core.wsgi import get_wsgi_application

# Set the Django settings module if not already defined
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProjectManagerCore.settings')

# Initialize MongoEngine DB connections (defined in ProjectManagerCore.db)
try:
	from .db import init_db
	init_db()
except Exception:
	pass  # defer connection errors to runtime

# WSGI application callable exposed to the WSGI server
application = get_wsgi_application()
