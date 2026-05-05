import os
import re

def fix_js_files(directory):
    old_pattern = r'backend-e7n3-[a-z0-9]+-yuionls-projects\.vercel\.app'
    new_url = 'backend-e7n3.vercel.app'
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.js'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 替换旧URL
                    new_content = re.sub(old_pattern, new_url, content)
                    
                    if new_content != content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Updated: {filepath}")
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")

if __name__ == '__main__':
    fix_js_files('d:\\微信web开发者工具\\毕业设计')
    print("Done!")