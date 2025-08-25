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

