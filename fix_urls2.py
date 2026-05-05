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
                    # 尝试用多种编码读取
                    content = None
                    encodings = ['utf-8', 'gbk', 'gb2312', 'cp1252']
                    
                    for enc in encodings:
                        try:
                            with open(filepath, 'r', encoding=enc) as f:
                                content = f.read()
                            break
                        except:
                            continue
                    
                    if content is None:
                        # 如果都失败，用二进制读取然后修复
                        with open(filepath, 'rb') as f:
                            binary_content = f.read()
                        # 尝试修复编码问题
                        content = binary_content.decode('utf-8', errors='replace')
                    
                    # 替换旧URL
                    new_content = re.sub(old_pattern, new_url, content)
                    
                    if new_content != content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Fixed: {filepath}")
                    else:
                        print(f"No change: {filepath}")
                        
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")

if __name__ == '__main__':
    fix_js_files('d:\\微信web开发者工具\\毕业设计')
    print("Done!")