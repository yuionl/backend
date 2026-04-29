import urllib.request
import urllib.parse
import json

# Test login API
print("Testing login API...")
url = 'http://127.0.0.1:8003/login/'
data = urllib.parse.urlencode({'username': 'a001', 'password': 'wgf04119'}).encode()
req = urllib.request.Request(url, data=data)
req.add_header('Content-Type', 'application/x-www-form-urlencoded')

try:
    with urllib.request.urlopen(req, timeout=5) as response:
        result = response.read()
        print(f"Response: {result.decode('utf-8')}")
except Exception as e:
    print(f"Error: {e}")