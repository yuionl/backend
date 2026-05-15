#!/usr/bin/env python
# -*- coding: utf-8 -*-
import psycopg2
import sys
import io

# 修复Windows控制台编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("Trying to connect Neon PostgreSQL database...")

try:
    conn = psycopg2.connect(
        dbname="neondb",
        user="neondb_owner",
        password="npg_HWIGQDhTs71Y",
        host="ep-rough-wind-aogm1es1-pooler.c-2.ap-southeast-1.aws.neon.tech",
        port="5432",
        sslmode="require",
        connect_timeout=15
    )
    
    print("SUCCESS: Database connected!")
    
    cur = conn.cursor()
    
    # 查询用户表
    cur.execute("SELECT id, username, name, role FROM user_app_user;")
    users = cur.fetchall()
    print(f"\nFound {len(users)} users:")
    for u in users:
        print(f"  - ID: {u[0]}, username: {u[1]}, name: {u[2]}, role: {u[3]}")
    
    cur.close()
    conn.close()
    
except Exception as e:
    print(f"FAILED: Database connection error: {e}")
