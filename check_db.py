#!/usr/bin/env python3
import sqlite3

def check_database():
    conn = sqlite3.connect('bigdata_learning.db')
    cursor = conn.cursor()
    
    # 检查所有表
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("数据库中的表:")
    for table in tables:
        print(f"- {table[0]}")
    
    # 检查每个表的结构
    for table in tables:
        table_name = table[0]
        print(f"\n表 {table_name} 的结构:")
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
    
    conn.close()

if __name__ == "__main__":
    check_database()