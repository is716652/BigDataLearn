import sqlite3
import os
from datetime import datetime

class SQLExporter:
    """SQL导出工具类"""
    
    def __init__(self, db_path='DB/app.db'):
        self.db_path = db_path
        self.sql_dir = 'SQL'
        self.ensure_sql_directory()
    
    def ensure_sql_directory(self):
        """确保SQL目录存在"""
        if not os.path.exists(self.sql_dir):
            os.makedirs(self.sql_dir)
            print(f"创建SQL目录: {self.sql_dir}")
    
    def get_database_connection(self):
        """获取数据库连接"""
        return sqlite3.connect(self.db_path)
    
    def get_all_tables(self):
        """获取所有表名"""
        conn = self.get_database_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        return tables
    
    def export_table_schema(self, table_name):
        """导出表结构SQL"""
        conn = self.get_database_connection()
        cursor = conn.cursor()
        
        # 获取建表语句
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        result = cursor.fetchone()
        
        if result:
            create_sql = result[0]
            # 添加DROP TABLE语句
            schema_sql = f"-- 表结构: {table_name}\n"
            schema_sql += f"-- 导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            schema_sql += f"DROP TABLE IF EXISTS {table_name};\n\n"
            schema_sql += create_sql + ";\n\n"
            
            # 获取索引
            cursor.execute("SELECT sql FROM sqlite_master WHERE type='index' AND tbl_name=? AND sql IS NOT NULL", (table_name,))
            indexes = cursor.fetchall()
            
            if indexes:
                schema_sql += f"-- 索引\n"
                for index in indexes:
                    schema_sql += index[0] + ";\n"
                schema_sql += "\n"
            
            conn.close()
            return schema_sql
        
        conn.close()
        return None
    
    def export_table_data(self, table_name):
        """导出表数据SQL"""
        conn = self.get_database_connection()
        cursor = conn.cursor()
        
        # 获取表结构信息
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns_info = cursor.fetchall()
        column_names = [col[1] for col in columns_info]
        
        # 获取所有数据
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        data_sql = f"-- 表数据: {table_name}\n"
        data_sql += f"-- 导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        data_sql += f"-- 记录数: {len(rows)}\n\n"
        
        if rows:
            # 清空表数据
            data_sql += f"DELETE FROM {table_name};\n\n"
            
            # 生成INSERT语句
            columns_str = ', '.join(column_names)
            
            for row in rows:
                values = []
                for value in row:
                    if value is None:
                        values.append('NULL')
                    elif isinstance(value, str):
                        # 转义单引号
                        escaped_value = value.replace("'", "''")
                        values.append(f"'{escaped_value}'")
                    elif isinstance(value, (int, float)):
                        values.append(str(value))
                    else:
                        values.append(f"'{str(value)}'")
                
                values_str = ', '.join(values)
                data_sql += f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str});\n"
            
            data_sql += "\n"
        else:
            data_sql += f"-- 表 {table_name} 无数据\n\n"
        
        conn.close()
        return data_sql
    
    def export_all_schemas(self):
        """导出所有表结构"""
        tables = self.get_all_tables()
        
        # 创建完整的数据库结构文件
        all_schemas_sql = f"-- 数据库结构导出\n"
        all_schemas_sql += f"-- 导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        all_schemas_sql += f"-- 数据库文件: {self.db_path}\n\n"
        
        for table in tables:
            schema_sql = self.export_table_schema(table)
            if schema_sql:
                all_schemas_sql += schema_sql
                
                # 单独保存每个表的结构
                schema_file = os.path.join(self.sql_dir, f"{table}_schema.sql")
                with open(schema_file, 'w', encoding='utf-8') as f:
                    f.write(schema_sql)
                print(f"导出表结构: {schema_file}")
        
        # 保存完整结构文件
        all_schemas_file = os.path.join(self.sql_dir, "database_schema.sql")
        with open(all_schemas_file, 'w', encoding='utf-8') as f:
            f.write(all_schemas_sql)
        print(f"导出完整数据库结构: {all_schemas_file}")
        
        return all_schemas_file
    
    def export_all_data(self):
        """导出所有表数据"""
        tables = self.get_all_tables()
        
        # 创建完整的数据导出文件
        all_data_sql = f"-- 数据库数据导出\n"
        all_data_sql += f"-- 导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        all_data_sql += f"-- 数据库文件: {self.db_path}\n\n"
        
        for table in tables:
            data_sql = self.export_table_data(table)
            if data_sql:
                all_data_sql += data_sql
                
                # 单独保存每个表的数据
                data_file = os.path.join(self.sql_dir, f"{table}_data.sql")
                with open(data_file, 'w', encoding='utf-8') as f:
                    f.write(data_sql)
                print(f"导出表数据: {data_file}")
        
        # 保存完整数据文件
        all_data_file = os.path.join(self.sql_dir, "database_data.sql")
        with open(all_data_file, 'w', encoding='utf-8') as f:
            f.write(all_data_sql)
        print(f"导出完整数据库数据: {all_data_file}")
        
        return all_data_file
    
    def create_import_script(self):
        """创建数据导入脚本"""
        import_script = '''#!/usr/bin/env python3
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
'''
        
        import_file = os.path.join(self.sql_dir, "import_database.py")
        with open(import_file, 'w', encoding='utf-8') as f:
            f.write(import_script)
        print(f"创建导入脚本: {import_file}")
        
        return import_file
    
    def create_readme(self):
        """创建README说明文件"""
        readme_content = f'''# SQL导出文件说明

## 文件结构

### 数据库结构文件
- `database_schema.sql` - 完整数据库结构（所有表）
- `*_schema.sql` - 单个表结构文件

### 数据文件
- `database_data.sql` - 完整数据库数据（所有表）
- `*_data.sql` - 单个表数据文件

### 工具文件
- `import_database.py` - 数据库导入脚本
- `README.md` - 本说明文件

## 使用方法

### 1. 导入完整数据库
```bash
python import_database.py
```

### 2. 手动导入
```bash
# 导入结构
sqlite3 your_database.db < database_schema.sql

# 导入数据
sqlite3 your_database.db < database_data.sql
```

### 3. 导入单个表
```bash
# 导入单个表结构
sqlite3 your_database.db < table_name_schema.sql

# 导入单个表数据
sqlite3 your_database.db < table_name_data.sql
```

## 注意事项

1. 导入前请备份现有数据库
2. 结构文件包含 `DROP TABLE` 语句，会删除现有表
3. 数据文件包含 `DELETE` 语句，会清空现有数据
4. 建议先导入结构，再导入数据
5. 如果遇到编码问题，请确保文件以UTF-8编码保存

## 导出时间
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 数据库文件
{self.db_path}
'''
        
        readme_file = os.path.join(self.sql_dir, "README.md")
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print(f"创建说明文件: {readme_file}")
        
        return readme_file
    
    def export_all(self):
        """导出所有内容"""
        print("开始导出数据库...")
        print(f"数据库文件: {self.db_path}")
        print(f"导出目录: {self.sql_dir}")
        print("-" * 50)
        
        # 导出结构
        schema_file = self.export_all_schemas()
        
        # 导出数据
        data_file = self.export_all_data()
        
        # 创建导入脚本
        import_file = self.create_import_script()
        
        # 创建说明文件
        readme_file = self.create_readme()
        
        print("-" * 50)
        print("导出完成！")
        print(f"导出的文件位于: {os.path.abspath(self.sql_dir)}")
        
        return {
            'schema_file': schema_file,
            'data_file': data_file,
            'import_file': import_file,
            'readme_file': readme_file,
            'sql_dir': self.sql_dir
        }

def main():
    """主函数"""
    exporter = SQLExporter()
    
    # 检查数据库文件是否存在
    if not os.path.exists(exporter.db_path):
        print(f"错误: 数据库文件不存在: {exporter.db_path}")
        return
    
    # 导出所有内容
    result = exporter.export_all()
    
    # 显示结果
    print("\n导出文件列表:")
    for key, file_path in result.items():
        if key != 'sql_dir':
            print(f"  {key}: {file_path}")

if __name__ == '__main__':
    main()