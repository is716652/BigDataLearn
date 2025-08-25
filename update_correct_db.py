#!/usr/bin/env python3
import sqlite3
import os

# 使用正确的数据库路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, 'DB')
DB_PATH = os.path.join(DB_DIR, 'app.db')

print(f"更新数据库: {DB_PATH}")

# 新的主题标题
new_titles = [
    "Shell脚本入门与环境配置",
    "变量定义与使用技巧", 
    "条件判断与分支控制",
    "循环结构与流程控制",
    "函数定义与模块化编程"
]

try:
    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 查询Shell脚本模块的主题
    cursor.execute('''
        SELECT t.id, t.title, t.ord 
        FROM topics t 
        JOIN modules m ON t.module_id = m.id 
        WHERE m.ord = 2 
        ORDER BY t.ord
    ''')
    
    topics = cursor.fetchall()
    print(f"找到 {len(topics)} 个Shell脚本主题:")
    
    for topic in topics:
        topic_id, old_title, ord_num = topic
        print(f"  ID: {topic_id}, 顺序: {ord_num}, 标题: {old_title}")
    
    # 更新主题标题
    for i, (topic_id, old_title, ord_num) in enumerate(topics):
        if i < len(new_titles):
            new_title = new_titles[i]
            cursor.execute('UPDATE topics SET title = ? WHERE id = ?', (new_title, topic_id))
            print(f"更新主题 {topic_id}: {old_title} -> {new_title}")
    
    conn.commit()
    
    # 验证更新结果
    print("\n验证更新结果:")
    cursor.execute('''
        SELECT t.id, t.title, t.ord 
        FROM topics t 
        JOIN modules m ON t.module_id = m.id 
        WHERE m.ord = 2 
        ORDER BY t.ord
    ''')
    
    updated_topics = cursor.fetchall()
    for topic in updated_topics:
        topic_id, title, ord_num = topic
        print(f"  ID: {topic_id}, 顺序: {ord_num}, 标题: {title}")
    
    conn.close()
    print("\n主题标题更新成功！")
    
except Exception as e:
    print(f"错误: {e}")