# SQL导出文件说明

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
2025-08-25 20:20:11

## 数据库文件
DB/app.db
