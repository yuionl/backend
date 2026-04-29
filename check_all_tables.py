import sys
sys.stdout.reconfigure(encoding='utf-8')

import psycopg2

try:
    print("连接 Neon 数据库...")
    conn = psycopg2.connect(
        dbname="neondb",
        user="neondb_owner",
        password="npg_HWIGQDhTs71Y",
        host="ep-rough-wind-aogm1es1-pooler.c-2.ap-southeast-1.aws.neon.tech",
        port="5432",
        sslmode="require"
    )
    print("连接成功!")
    cur = conn.cursor()

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

    result = {}
    for table in tables:
        try:
            cur.execute(f"SELECT COUNT(*) FROM {table};")
            count = cur.fetchone()[0]
            result[table] = count
            print(f"{table}: {count} 条")
        except Exception as e:
            print(f"{table}: 表不存在或错误: {e}")
            result[table] = 'ERROR'

    # 保存结果到文件
    with open('db_check.txt', 'w', encoding='utf-8') as f:
        for table, count in result.items():
            f.write(f"{table}: {count}\n")

    print("\n检查完成！结果已保存到 db_check.txt")
    conn.close()

except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()