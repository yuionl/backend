import sys
sys.stdout.reconfigure(encoding='utf-8')

import psycopg2

try:
    print("尝试连接 Neon 数据库...")
    conn = psycopg2.connect(
        dbname="neondb",
        user="neondb_owner",
        password="npg_HWIGQDhTs71Y",
        host="ep-rough-wind-aogm1es1-pooler.c-2.ap-southeast-1.aws.neon.tech",
        port="5432",
        sslmode="require"
    )
    print("数据库连接成功!")
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()
    print(f"PostgreSQL 版本: {version[0]}")
    conn.close()
except Exception as e:
    print(f"数据库连接失败: {e}")