import urllib.request
import urllib.parse

# Test login API
print("测试登录 API...")
url = 'http://127.0.0.1:8000/login/'
data = urllib.parse.urlencode({'username': 'a001', 'password': 'wgf04119'}).encode()
req = urllib.request.Request(url, data=data)
req.add_header('Content-Type', 'application/x-www-form-urlencoded')

try:
    with urllib.request.urlopen(req, timeout=10) as response:
        result = response.read()
        print(f"✅ 成功! 响应: {result.decode('utf-8')}")
except Exception as e:
    print(f"❌ 错误: {e}")