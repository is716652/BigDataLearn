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

