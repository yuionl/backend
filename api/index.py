#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Import Django and setup
import django
django.setup()

# Import the ASGI application
from backend.asgi import application as asgi_application

# Vercel ASGI handler
async def app(scope, receive, send):
    await asgi_application(scope, receive, send)