-- 数据库结构导出
-- 导出时间: 2025-08-25 20:20:11
-- 数据库文件: DB/app.db

-- 表结构: modules
-- 导出时间: 2025-08-25 20:20:11

DROP TABLE IF EXISTS modules;

CREATE TABLE modules (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  description TEXT,
  ord INTEGER
);

-- 表结构: topics
-- 导出时间: 2025-08-25 20:20:11

DROP TABLE IF EXISTS topics;

CREATE TABLE topics (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  module_id INTEGER NOT NULL,
  title TEXT NOT NULL,
  ord INTEGER,
  FOREIGN KEY(module_id) REFERENCES modules(id)
);

-- 表结构: contents
-- 导出时间: 2025-08-25 20:20:11

DROP TABLE IF EXISTS contents;

CREATE TABLE contents (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  topic_id INTEGER NOT NULL,
  data TEXT NOT NULL,
  FOREIGN KEY(topic_id) REFERENCES topics(id)
);

-- 表结构: exam_sets
-- 导出时间: 2025-08-25 20:20:11

DROP TABLE IF EXISTS exam_sets;

CREATE TABLE exam_sets (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL
);

-- 表结构: questions
-- 导出时间: 2025-08-25 20:20:11

DROP TABLE IF EXISTS questions;

CREATE TABLE questions (
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
);

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

-- 表结构: tokens
-- 导出时间: 2025-08-25 20:20:11

DROP TABLE IF EXISTS tokens;

CREATE TABLE tokens (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  token TEXT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(user_id) REFERENCES users(id)
);

-- 表结构: submissions
-- 导出时间: 2025-08-25 20:20:11

DROP TABLE IF EXISTS submissions;

CREATE TABLE submissions (
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
);

