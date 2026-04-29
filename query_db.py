import psycopg2

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
print("User a001:", user)
conn.close()