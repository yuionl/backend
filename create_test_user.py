import psycopg2

try:
    conn = psycopg2.connect(
        dbname="neondb",
        user="neondb_owner",
        password="npg_HWIGQDhTs71Y",
        host="ep-rough-wind-aogm1es1-pooler.c-2.ap-southeast-1.aws.neon.tech",
        port="5432",
        sslmode="require"
    )
    cur = conn.cursor()

    # 插入测试用户
    cur.execute("""
        INSERT INTO user_app_user (username, password, name, role)
        VALUES ('test001', 'test123', '测试用户', 1)
        ON CONFLICT (username) DO NOTHING
    """)
    conn.commit()

    # 验证插入成功
    cur.execute("SELECT id, username, password, name, role FROM user_app_user WHERE username = 'test001'")
    user = cur.fetchone()

    if user:
        print("测试用户创建成功!")
        print(f"ID: {user[0]}, 用户名: {user[1]}, 密码: {user[2]}, 姓名: {user[3]}, 角色: {user[4]}")
    else:
        print("用户已存在")

    conn.close()
except Exception as e:
    print(f"错误: {e}")