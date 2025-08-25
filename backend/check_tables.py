#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect('bigdata_learning.db')
cursor = conn.cursor()

# 检查所有表
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("数据库中的表:")
for table in tables:
    print(f"- {table[0]}")

# 如果有contents表，检查Shell脚本模块的内容
if any('contents' in str(t) for t in tables):
    print("\n检查Shell脚本模块内容:")
    cursor.execute("SELECT t.title, c.data FROM topics t JOIN contents c ON t.id = c.topic_id WHERE t.module_id = 2")
    rows = cursor.fetchall()
    for row in rows:
        print(f"知识点: {row[0]}")
        print(f"数据长度: {len(row[1])} 字符")
        print("---")

conn.close()