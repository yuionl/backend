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
cur.execute("SELECT COUNT(*) FROM user_app_user")
count = cur.fetchone()[0]
print("Count:", count)

if count > 0:
    cur.execute("SELECT id, username, name, role FROM user_app_user LIMIT 5")
    for row in cur.fetchall():
        print(row)
else:
    print("EMPTY - need to migrate data")

conn.close()