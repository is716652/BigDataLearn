import sqlite3
import json

# 连接数据库
conn = sqlite3.connect('DB/app.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

# 查询Shell脚本模块的所有知识点
topics = c.execute('''
    SELECT t.id, t.title, c.data 
    FROM topics t 
    JOIN contents c ON t.id = c.topic_id 
    JOIN modules m ON t.module_id = m.id 
    WHERE m.title LIKE '%Shell%' 
    ORDER BY t.ord
''').fetchall()

print(f"Shell脚本模块共有 {len(topics)} 个知识点：\n")

for i, topic in enumerate(topics, 1):
    data = json.loads(topic['data'])
    print(f"=== 知识点 {i}: {topic['title']} ===")
    print(f"理论内容前100字符: {data.get('theory', '')[:100]}...")
    print(f"代码内容前100字符: {data.get('code', '')[:100]}...")
    print(f"案例内容前100字符: {data.get('case', '')[:100]}...")
    print("\n")

# 检查内容是否重复
theory_contents = [json.loads(t['data']).get('theory', '') for t in topics]
code_contents = [json.loads(t['data']).get('code', '') for t in topics]
case_contents = [json.loads(t['data']).get('case', '') for t in topics]

print("=== 重复检查 ===")
print(f"理论内容是否都相同: {len(set(theory_contents)) == 1}")
print(f"代码内容是否都相同: {len(set(code_contents)) == 1}")
print(f"案例内容是否都相同: {len(set(case_contents)) == 1}")

conn.close()