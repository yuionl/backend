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

# 查询所有序列
cur.execute("""
    SELECT schemaname, sequencename
    FROM pg_sequences
    WHERE schemaname = 'public'
    ORDER BY sequencename;
""")

print('Sequences in database:')
for seq in cur.fetchall():
    print(f'  {seq[0]}.{seq[1]}')

print('\n---\n')

# 查询所有表
cur.execute("""
    SELECT tablename
    FROM pg_tables
    WHERE schemaname = 'public'
    ORDER BY tablename;
""")

print('Tables in database:')
for table in cur.fetchall():
    print(f'  {table[0]}')

conn.close()
