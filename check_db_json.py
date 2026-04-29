import psycopg2
import json

result = {"status": "unknown", "count": 0, "users": [], "error": ""}

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
    cur.execute("SELECT COUNT(*) FROM user_app_user")
    count = cur.fetchone()[0]
    result["count"] = count

    if count > 0:
        result["status"] = "has_data"
        cur.execute("SELECT id, username, name, role FROM user_app_user LIMIT 5")
        result["users"] = [list(row) for row in cur.fetchall()]
    else:
        result["status"] = "empty"

    conn.close()
except Exception as e:
    result["status"] = "error"
    result["error"] = str(e)

with open("db_result.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False)