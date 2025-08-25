-- 表结构: contents
-- 导出时间: 2025-08-25 20:20:11

DROP TABLE IF EXISTS contents;

CREATE TABLE contents (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  topic_id INTEGER NOT NULL,
  data TEXT NOT NULL,
  FOREIGN KEY(topic_id) REFERENCES topics(id)
);

