#!/usr/bin/env python3
import sqlite3
import json

print("手动初始化数据库...")

# 连接数据库
conn = sqlite3.connect('bigdata_learning.db')
cursor = conn.cursor()

# 创建表
tables_sql = [
    '''CREATE TABLE IF NOT EXISTS modules (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      title TEXT NOT NULL,
      description TEXT,
      ord INTEGER
    );''',
    '''CREATE TABLE IF NOT EXISTS topics (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      module_id INTEGER NOT NULL,
      title TEXT NOT NULL,
      ord INTEGER,
      FOREIGN KEY(module_id) REFERENCES modules(id)
    );''',
    '''CREATE TABLE IF NOT EXISTS contents (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      topic_id INTEGER NOT NULL,
      data TEXT NOT NULL,
      FOREIGN KEY(topic_id) REFERENCES topics(id)
    );''',
    '''CREATE TABLE IF NOT EXISTS exam_sets (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL
    );''',
    '''CREATE TABLE IF NOT EXISTS questions (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      exam_id INTEGER NOT NULL,
      qtype TEXT NOT NULL,
      prompt TEXT NOT NULL,
      options TEXT,
      answer TEXT NOT NULL,
      score INTEGER NOT NULL,
      ord INTEGER,
      knowledge_ref TEXT,
      FOREIGN KEY(exam_id) REFERENCES exam_sets(id)
    );''',
    '''CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username TEXT UNIQUE,
      student_id TEXT UNIQUE,
      name TEXT,
      role TEXT NOT NULL DEFAULT 'student',
      password_hash TEXT NOT NULL
    );''',
    '''CREATE TABLE IF NOT EXISTS tokens (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      token TEXT NOT NULL,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY(user_id) REFERENCES users(id)
    );''',
    '''CREATE TABLE IF NOT EXISTS submissions (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      exam_id INTEGER NOT NULL,
      score INTEGER NOT NULL,
      total INTEGER NOT NULL,
      rate REAL NOT NULL,
      detail TEXT NOT NULL,
      wrong_qids TEXT,
      suggestions TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY(user_id) REFERENCES users(id),
      FOREIGN KEY(exam_id) REFERENCES exam_sets(id)
    );'''
]

for sql in tables_sql:
    try:
        cursor.execute(sql)
        print(f"表创建成功")
    except Exception as e:
        print(f"创建表失败: {e}")

conn.commit()

# 检查表
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("\n数据库中的表:")
for table in tables:
    print(f"- {table[0]}")

conn.close()
print("数据库表创建完成！")