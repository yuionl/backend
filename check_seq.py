import psycopg2
import json

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

    # 查询所有序列
    cur.execute("""
        SELECT schemaname, sequencename
        FROM pg_sequences
        WHERE schemaname = 'public'
        ORDER BY sequencename;
    """)
    result['sequences'] = [{'schema': s[0], 'name': s[1]} for s in cur.fetchall()]

    # 查询所有表
    cur.execute("""
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'public'
        ORDER BY tablename;
    """)
    result['tables'] = [t[0] for t in cur.fetchall()]

    conn.close()
except Exception as e:
    result['error'] = str(e)

with open('seq_result.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print('Check complete, result saved to seq_result.json')
