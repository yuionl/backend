import os

old_url = 'https://backend-e7n3-lhd26la3q-yuionls-projects.vercel.app'
new_url = 'https://backend-e7n3-2azwnafkl-yuionls-projects.vercel.app'

base_path = r'd:\微信web开发者工具\毕业设计'

count = 0
files_modified = []

for root, dirs, files in os.walk(base_path):
    for file in files:
        if file.endswith('.js'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            if old_url in content:
                new_content = content.replace(old_url, new_url)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                count += 1
                files_modified.append(filepath)

print(f"修改了 {count} 个文件")
for f in files_modified:
    print(f"  - {f}")