-- 表结构: users
-- 导出时间: 2025-08-25 20:20:11

DROP TABLE IF EXISTS users;

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE,
  student_id TEXT UNIQUE,
  name TEXT,
  role TEXT NOT NULL DEFAULT 'student',
  password_hash TEXT NOT NULL
, class_name TEXT, phone TEXT, email TEXT, status TEXT DEFAULT "active", created_at DATETIME);

