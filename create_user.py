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
    cur.execute("INSERT INTO user_app_user (username, password, name, role) VALUES ('test001', 'test123', 'TestUser', 1)")
    conn.commit()
    print("Test user created!")

    # 验证
    cur.execute("SELECT id, username, password, name, role FROM user_app_user WHERE username = 'test001'")
    user = cur.fetchone()
    if user:
        with open("test_result.txt", "w") as f:
            f.write(f"Success! User: {user[1]}, Pass: {user[2]}")

    conn.close()
except Exception as e:
    with open("test_result.txt", "w") as f:
        f.write(f"Error: {str(e)}")