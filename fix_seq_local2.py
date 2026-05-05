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

print("=== 当前数据库中的序列 ===")
cur.execute("""
    SELECT schemaname, sequencename 
    FROM pg_sequences 
    WHERE schemaname = 'public' 
    ORDER BY sequencename;
""")
for seq in cur.fetchall():
    print("  " + seq[0] + "." + seq[1])

print("\n=== 正在修复序列 ===")

tables = [
    'user_app_user',
    'user_app_course',
    'user_app_question',
    'user_app_task', 
    'user_app_classroom',
    'user_app_answerrecord',
    'user_app_taskscore',
    'user_app_coursestudent'
]

for table_name in tables:
    try:
        cur.execute(f"SELECT COALESCE(MAX(id), 0) FROM {table_name}")
        max_id = cur.fetchone()[0]
        
        cur.execute(f"SELECT pg_get_serial_sequence('{table_name}', 'id')")
        seq_name = cur.fetchone()[0]
        
        if seq_name:
            cur.execute(f"SELECT setval('{seq_name}', {max_id}, true)")
            new_val = cur.fetchone()[0]
            print("OK " + table_name + ": max_id=" + str(max_id) + ", sequence " + seq_name + " set to " + str(new_val))
        else:
            print("NO SEQ " + table_name)
            
        conn.commit()
    except Exception as e:
        print("ERR " + table_name + ": " + str(e))
        conn.rollback()

conn.close()
print("\n=== 修复完成 ===")