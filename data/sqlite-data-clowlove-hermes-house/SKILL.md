---
name: sqlite-data
description: SQLite 数据库操作 - 创建/查询/聚合 Hermes Agent 的结构化数据。存储新闻聚合、趋势数据、任务状态等。
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
prerequisites:
  commands: [python3, sqlite3]
  api_keys: []
metadata:
  hermes:
    tags: [database, sqlite, data-storage, query]
    homepage: https://github.com/hermes-agent
---

# SQLite 数据存储

用于 Hermes Agent 的轻量级结构化数据存储。适合存储聚合的新闻、趋势数据、任务状态、用户偏好等。

---

## 核心概念

| 模式 | 用途 |
|------|------|
| `db.execute()` | 单次执行 SQL |
| `db.executemany()` | 批量操作 |
| `db.query()` | 查询并返回结果 |
| 上下文管理器 | 自动提交/回滚 |

---

## 快速开始

### 1. 创建/连接数据库

```python
import sqlite3

# 连接或创建数据库
db = sqlite3.connect('/path/to/data.db')
cursor = db.cursor()

# 或使用上下文管理器（自动提交）
with sqlite3.connect('/path/to/data.db') as db:
    cursor = db.cursor()
    # 执行操作
```

### 2. 创建表

```python
# 新闻聚合表
db.execute('''
    CREATE TABLE IF NOT EXISTS news_aggregates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT NOT NULL,
        title TEXT NOT NULL,
        platform TEXT,
        url TEXT,
        weight REAL DEFAULT 1.0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# 趋势数据表
db.execute('''
    CREATE TABLE IF NOT EXISTS trends (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT NOT NULL,
        date DATE NOT NULL,
        mentions INTEGER DEFAULT 0,
        sentiment REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# 任务状态表
db.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_id TEXT UNIQUE,
        name TEXT,
        status TEXT DEFAULT 'pending',
        result TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP
    )
''')

db.commit()
```

### 3. 插入数据

```python
# 单条插入
db.execute(
    'INSERT INTO news_aggregates (topic, title, platform, url) VALUES (?, ?, ?, ?)',
    ('AI', 'OpenAI 发布 GPT-5', 'zhihu', 'https://zhihu.com/p/123')
)
db.commit()

# 批量插入
data = [
    ('AI', '新闻1', 'weibo', 'url1'),
    ('AI', '新闻2', 'twitter', 'url2'),
    ('AI', '新闻3', 'zhihu', 'url3'),
]
db.executemany(
    'INSERT INTO news_aggregates (topic, title, platform, url) VALUES (?, ?, ?, ?)',
    data
)
db.commit()
```

### 4. 查询数据

```python
# 基本查询
cursor = db.execute('SELECT * FROM news_aggregates WHERE topic = ?', ('AI',))
rows = cursor.fetchall()

# 带排序和限制
cursor = db.execute('''
    SELECT title, platform, weight, created_at 
    FROM news_aggregates 
    WHERE topic = ?
    ORDER BY weight DESC, created_at DESC
    LIMIT 10
''', ('AI',))

# 聚合查询（统计）
cursor = db.execute('''
    SELECT platform, COUNT(*) as count, AVG(weight) as avg_weight
    FROM news_aggregates
    WHERE topic = ?
    GROUP BY platform
    ORDER BY count DESC
''', ('AI',))

# 日期范围查询
cursor = db.execute('''
    SELECT topic, date, SUM(mentions) as total
    FROM trends
    WHERE date BETWEEN '2025-01-01' AND '2025-01-31'
    GROUP BY topic, date
''')
```

### 5. 更新和删除

```python
# 更新
db.execute('''
    UPDATE tasks 
    SET status = 'completed', result = ?, updated_at = CURRENT_TIMESTAMP
    WHERE job_id = ?
''', ('{"success": true}', 'job_123'))

# 删除
db.execute('DELETE FROM news_aggregates WHERE created_at < ?', ('2025-01-01',))
db.commit()
```

---

## 实用模式

### 检查表是否存在

```python
cursor = db.execute('''
    SELECT name FROM sqlite_master 
    WHERE type='table' AND name=?
''', ('news_aggregates',))
exists = cursor.fetchone() is not None
```

### 获取表结构

```python
cursor = db.execute('PRAGMA table_info(news_aggregates)')
for col in cursor:
    print(col[1], col[2])  # name, type
```

### 分页查询

```python
page = 1
page_size = 20
offset = (page - 1) * page_size

cursor = db.execute('''
    SELECT * FROM news_aggregates 
    WHERE topic = ?
    ORDER BY created_at DESC
    LIMIT ? OFFSET ?
''', (topic, page_size, offset))
```

### Upsert（存在则更新）

```python
db.execute('''
    INSERT INTO tasks (job_id, name, status)
    VALUES (?, ?, ?)
    ON CONFLICT(job_id) DO UPDATE SET
        status = excluded.status,
        updated_at = CURRENT_TIMESTAMP
''', ('job_123', 'my_task', 'running'))
```

### 全文搜索

```python
# 创建 FTS 表
db.execute('''
    CREATE VIRTUAL TABLE IF NOT EXISTS news_fts 
    USING fts5(title, content, content=news_aggregates)
''')

# 搜索
cursor = db.execute('''
    SELECT n.* FROM news_aggregates n
    JOIN news_fts f ON n.rowid = f.rowid
    WHERE news_fts MATCH ?
''', ('AI AND GPT',))
```

---

## 性能优化

```python
# 创建索引
db.execute('CREATE INDEX IF NOT EXISTS idx_news_topic ON news_aggregates(topic)')
db.execute('CREATE INDEX IF NOT EXISTS idx_news_date ON news_aggregates(created_at)')
db.execute('CREATE INDEX IF NOT EXISTS idx_trends_date ON trends(date)')

# 使用连接池（大量操作时）
from sqlite3 import dbapi2 as sqlite3_pool

# 批量提交（减少 I/O）
db.execute('BEGIN')
for i in range(1000):
    db.execute('INSERT INTO big_table (data) VALUES (?)', (i,))
db.execute('COMMIT')
```

---

## 数据导出

```python
import json

# 导出为 JSON
cursor = db.execute('SELECT * FROM news_aggregates WHERE topic = ?', (topic,))
columns = [desc[0] for desc in cursor.description]
rows = cursor.fetchall()

data = [dict(zip(columns, row)) for row in rows]
print(json.dumps(data, indent=2, default=str))

# 导出为 CSV
import csv
cursor = db.execute('SELECT * FROM news_aggregates WHERE topic = ?', (topic,))
with open('export.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([desc[0] for desc in cursor.description])
    writer.writerows(cursor)
```

---

## 错误处理

```python
try:
    with sqlite3.connect('/path/to/data.db') as db:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM news_aggregates')
        results = cursor.fetchall()
except sqlite3.OperationalError as e:
    print(f"数据库错误: {e}")
except sqlite3.IntegrityError as e:
    print(f"数据完整性错误: {e}")
```

---

## 与其他工具对比

| 场景 | 推荐工具 |
|------|----------|
| 简单配置存储 | SQLite ✅ |
| 复杂查询/分析 | PostgreSQL |
| 高并发写入 | PostgreSQL/MySQL |
| 临时数据 | 内存 dict/list |
| 持久化缓存 | Redis |
| 大规模数据 | parquet/数据库 |

SQLite 适合：
- 单 Agent 的数据存储
- 中小量数据（< 100GB）
- 无需多进程并发写入
- 快速原型

---

## 下一步

1. 确定数据存储路径（如 `~/.hermes/data/agent.db`）
2. 设计表结构
3. 与 cron 任务集成进行数据持久化