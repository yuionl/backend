#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

import django
django.setup()

from django.core.wsgi import get_wsgi_application
from wsgiref.simple_server import make_server

application = get_wsgi_application()

print("Starting Django server at http://127.0.0.1:8000 ...")
httpd = make_server('0.0.0.0', 8000, application)
print("Server is running! Press CTRL+C to stop.")
httpd.serve_forever()
