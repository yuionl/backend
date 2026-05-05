import os

def fix_encoding(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.js'):
                filepath = os.path.join(root, file)
                try:
                    # 先尝试用 gbk 读取（Windows 默认编码）
                    with open(filepath, 'r', encoding='gbk') as f:
                        content = f.read()
                    
                    # 用 utf-8 写回去
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Fixed encoding: {filepath}")
                    
                except Exception as e:
                    try:
                        # 如果 gbk 失败，尝试其他编码
                        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                            content = f.read()
                        
                        # 修复乱码字符
                        content = content.replace('\ufffd', '')
                        
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(content)
                        print(f"Fixed with utf-8: {filepath}")
                    except Exception as e2:
                        print(f"Failed to fix {filepath}: {e2}")

if __name__ == '__main__':
    fix_encoding('d:\\微信web开发者工具\\毕业设计')
    print("Done!")