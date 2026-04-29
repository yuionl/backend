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

    # 检查 user_app_user 表
    cur.execute("SELECT COUNT(*) FROM user_app_user;")
    count = cur.fetchone()[0]
    print(f"\nuser_app_user 表中有 {count} 条记录")

    if count > 0:
        cur.execute("SELECT id, username, name, role FROM user_app_user LIMIT 10;")
        rows = cur.fetchall()
        print("\n用户列表:")
        for row in rows:
            print(f"  ID: {row[0]}, 用户名: {row[1]}, 姓名: {row[2]}, 角色: {row[3]}")
    else:
        print("数据库是空的！需要迁移数据。")

    conn.close()
except Exception as e:
    print(f"错误: {e}")