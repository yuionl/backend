import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Setup Django
import django
django.setup()

# Create WSGI app
from django.core.wsgi import get_wsgi_application
app = get_wsgi_application()