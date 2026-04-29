import pymysql

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='wgf04119',
    database='classroom_interactive'
)

cursor = conn.cursor()

print("=== 数据库中的表 ===")
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()
for table in tables:
    print(table[0])

print(f"\n总共 {len(tables)} 张表")

cursor.close()
conn.close()
