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

