#!/usr/bin/env python
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
import django
django.setup()

from django.db import connection

def fix_all_sequences():
    tables = [
        'user_app_user',
        'user_app_course',
        'user_app_question',
        'user_app_task',
        'user_app_classroom',
        'user_app_answerrecord',
        'user_app_taskscore',
        'user_app_coursestudent'
    ]
    
    print("Checking and fixing database sequences...\n")
    
    for table_name in tables:
        try:
            with connection.cursor() as cursor:
                # 获取最大id
                cursor.execute(f"SELECT COALESCE(MAX(id), 0) FROM {table_name}")
                max_id = cursor.fetchone()[0]
                
                # 获取序列名
                cursor.execute(f"SELECT pg_get_serial_sequence('{table_name}', 'id')")
                seq_name = cursor.fetchone()[0]
                
                if seq_name:
                    # 获取当前序列值
                    cursor.execute(f"SELECT last_value FROM {seq_name}")
                    current_val = cursor.fetchone()[0]
                    
                    print(f"Table: {table_name}")
                    print(f"  Max ID in table: {max_id}")
                    print(f"  Current sequence value: {current_val}")
                    
                    if current_val < max_id:
                        # 修复序列
                        cursor.execute(f"SELECT setval('{seq_name}', {max_id}, true)")
                        new_val = cursor.fetchone()[0]
                        print(f"  Fixed! New sequence value: {new_val}")
                    else:
                        print(f"  Sequence is already synchronized")
                else:
                    print(f"Table: {table_name} - No sequence found")
                
                print()
                
        except Exception as e:
            print(f"Error with {table_name}: {str(e)}\n")

if __name__ == '__main__':
    fix_all_sequences()
    print("Sequence check completed!")