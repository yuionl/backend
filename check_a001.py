import psycopg2

result = {}

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
    cur.execute("SELECT id, username, password, name, role FROM user_app_user WHERE username = 'a001'")
    user = cur.fetchone()
    if user:
        result = {
            "id": user[0],
            "username": user[1],
            "password": user[2],
            "name": user[3],
            "role": user[4]
        }
    conn.close()
except Exception as e:
    result = {"error": str(e)}

with open("a001_result.json", "w", encoding="utf-8") as f:
    import json
    json.dump(result, f, ensure_ascii=False)