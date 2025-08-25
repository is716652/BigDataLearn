#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""数据库导入脚本"""

import sqlite3
import os

def import_database(db_path='DB/app.db', sql_dir='SQL'):
    """导入数据库结构和数据"""
    
    # 确保数据库目录存在
    db_dir = os.path.dirname(db_path)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    
    # 连接数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 导入数据库结构
        schema_file = os.path.join(sql_dir, 'database_schema.sql')
        if os.path.exists(schema_file):
            print(f"导入数据库结构: {schema_file}")
            with open(schema_file, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
            
            # 执行结构SQL（分割成单独的语句）
            statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip() and not stmt.strip().startswith('--')]
            for statement in statements:
                try:
                    cursor.execute(statement)
                except sqlite3.Error as e:
                    print(f"执行语句时出错: {statement[:50]}... 错误: {e}")
            
            conn.commit()
            print("数据库结构导入完成")
        
        # 导入数据
        data_file = os.path.join(sql_dir, 'database_data.sql')
        if os.path.exists(data_file):
            print(f"导入数据: {data_file}")
            with open(data_file, 'r', encoding='utf-8') as f:
                data_sql = f.read()
            
            # 执行数据SQL
            statements = [stmt.strip() for stmt in data_sql.split(';') if stmt.strip() and not stmt.strip().startswith('--')]
            for statement in statements:
                try:
                    cursor.execute(statement)
                except sqlite3.Error as e:
                    print(f"执行语句时出错: {statement[:50]}... 错误: {e}")
            
            conn.commit()
            print("数据导入完成")
        
        print("数据库导入成功！")
        
    except Exception as e:
        print(f"导入过程中出错: {e}")
        conn.rollback()
    
    finally:
        conn.close()

if __name__ == '__main__':
    import_database()
