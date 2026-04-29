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

    # 检查用户是否存在
    cur.execute("SELECT id, username, password, name, role FROM user_app_user WHERE username = 'a001'")
    user = cur.fetchone()

    if user:
        with open("db_status.txt", "w") as f:
            f.write(f"User a001 exists!\n")
            f.write(f"ID: {user[0]}\n")
            f.write(f"Username: {user[1]}\n")
            f.write(f"Password: {user[2]}\n")
            f.write(f"Name: {user[3]}\n")
            f.write(f"Role: {user[4]}\n")
    else:
        with open("db_status.txt", "w") as f:
            f.write("User a001 NOT found!")

    conn.close()
except Exception as e:
    with open("db_status.txt", "w") as f:
        f.write(f"Error: {str(e)}")