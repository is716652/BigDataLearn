-- 表结构: modules
-- 导出时间: 2025-08-25 20:20:11

DROP TABLE IF EXISTS modules;

CREATE TABLE modules (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  description TEXT,
  ord INTEGER
);

