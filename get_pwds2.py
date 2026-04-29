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
    cur.execute("SELECT username, password FROM user_app_user")
    with open("output.txt", "w", encoding="utf-8") as f:
        for row in cur.fetchall():
            f.write(row[0] + "|" + (row[1] or "NULL") + "\n")
    conn.close()
except Exception as e:
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write("ERROR: " + str(e))