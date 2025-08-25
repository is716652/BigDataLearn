#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os

def update_shell_topics():
    """更新Shell脚本模块的主题标题"""
    # 确保在backend目录下运行
    if not os.path.exists('bigdata_learning.db'):
        os.chdir('backend')
    
    conn = sqlite3.connect('bigdata_learning.db')
    cursor = conn.cursor()
    
    try:
        # Shell脚本模块的新主题标题
        new_titles = [
            "Shell脚本入门与环境配置",
            "变量定义与使用技巧", 
            "条件判断与分支控制",
            "循环结构与流程控制",
            "函数定义与模块化编程"
        ]
        
        # 获取Shell脚本模块的topic IDs
        print("获取Shell脚本模块的主题...")
        cursor.execute("SELECT id, ord FROM topics WHERE module_id = 2 ORDER BY ord")
        topics = cursor.fetchall()
        
        if not topics:
            print("未找到Shell脚本模块的主题")
            return
        
        print(f"找到 {len(topics)} 个主题")
        
        # 更新每个主题的标题
        for i, (topic_id, ord_num) in enumerate(topics):
            if i < len(new_titles):
                new_title = new_titles[i]
                cursor.execute(
                    "UPDATE topics SET title = ? WHERE id = ?",
                    (new_title, topic_id)
                )
                print(f"更新主题 {ord_num}: {new_title}")
        
        conn.commit()
        print("\nShell脚本模块主题标题更新完成！")
        
        # 验证结果
        cursor.execute("""
            SELECT ord, title 
            FROM topics 
            WHERE module_id = 2 
            ORDER BY ord
        """)
        results = cursor.fetchall()
        print("\n=== 验证结果 ===")
        for ord_num, title in results:
            print(f"主题 {ord_num}: {title}")
            
    except Exception as e:
        print(f"错误: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    update_shell_topics()