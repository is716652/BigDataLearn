#!/usr/bin/env python3
import sqlite3
import json
from werkzeug.security import generate_password_hash

print("插入种子数据...")

# 连接数据库
conn = sqlite3.connect('bigdata_learning.db')
cursor = conn.cursor()

# 模块元数据
MODULES_META = [
    (1, 'Linux基础操作与环境熟悉', '掌握Linux常用命令、文件系统、权限管理与环境配置'),
    (2, 'Shell脚本基础语法与简单应用', '变量、条件判断、循环控制与函数定义'),
    (3, 'Shell脚本进阶（文件操作与进程监控）', '文件处理、进程管理、任务调度与系统监控'),
    (4, '基于Docker知识点', '容器技术、镜像管理、网络配置与Docker Compose'),
    (5, '基于Docker的Hadoop伪分布式集群搭建', 'Docker环境下Hadoop集群部署与配置实战')
]

# 插入模块
for ord_num, title, desc in MODULES_META:
    cursor.execute('INSERT OR REPLACE INTO modules(id, title, description, ord) VALUES(?, ?, ?, ?)',
                   (ord_num, title, desc, ord_num))
    print(f"插入模块: {title}")

# 为每个模块创建5个主题
for module_ord, module_title, _ in MODULES_META:
    for topic_ord in range(1, 6):
        topic_title = f"{module_title} - 知识点{topic_ord}"
        cursor.execute('INSERT OR REPLACE INTO topics(module_id, title, ord) VALUES(?, ?, ?)',
                       (module_ord, topic_title, topic_ord))
        
        # 获取topic_id
        topic_id = cursor.lastrowid
        
        # 创建内容数据
        content_data = {
            'title': topic_title,
            'theory': f'这是{module_title}第{topic_ord}个知识点的理论内容。',
            'code': f'# {module_title} 示例代码\necho "知识点{topic_ord}"',
            'case': f'这是{module_title}第{topic_ord}个知识点的案例内容。',
            'exercises': [
                f'{module_title}第{topic_ord}个知识点的练习题1',
                f'{module_title}第{topic_ord}个知识点的练习题2'
            ]
        }
        
        # 插入内容
        cursor.execute('INSERT OR REPLACE INTO contents(topic_id, data) VALUES(?, ?)',
                       (topic_id, json.dumps(content_data, ensure_ascii=False)))
        
        print(f"  插入主题: {topic_title}")

# 插入管理员用户
cursor.execute('INSERT OR REPLACE INTO users(username, name, role, password_hash) VALUES(?, ?, ?, ?)',
               ('admin', '管理员', 'admin', generate_password_hash('xv2010wr')))
print("插入管理员用户")

conn.commit()

# 检查数据
cursor.execute('SELECT COUNT(*) FROM modules')
module_count = cursor.fetchone()[0]
print(f"\n模块数量: {module_count}")

cursor.execute('SELECT COUNT(*) FROM topics')
topic_count = cursor.fetchone()[0]
print(f"主题数量: {topic_count}")

cursor.execute('SELECT COUNT(*) FROM contents')
content_count = cursor.fetchone()[0]
print(f"内容数量: {content_count}")

conn.close()
print("种子数据插入完成！")