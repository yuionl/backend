import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

# Import Django and setup
import django
django.setup()

from backend.wsgi import application

# Vercel requires the app to be called "app"
app = application