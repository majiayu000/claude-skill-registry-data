---
name: database-skill
description: Configure and operate TinyDB for JSON-based document storage. Use when setting up databases, creating queries, or managing data persistence.
allowed-tools: Write, Read, Bash
---

# Database Skill

## Purpose
Set up and manage TinyDB document database with proper configuration and query patterns.

## Instructions

### Database Setup
```python
from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
from pathlib import Path
from typing import Optional, List

class TodoDatabase:
    """TinyDB wrapper for todo task storage."""
    
    def __init__(self, db_path: str = "todo_data.json"):
        """Initialize database with caching."""
        self.db_path = Path(db_path)
        self.db = TinyDB(
            self.db_path,
            storage=CachingMiddleware(JSONStorage),
            indent=2,
            ensure_ascii=False
        )
        self.tasks = self.db.table('tasks')
        self.query = Query()
    
    def close(self):
        """Close database connection."""
        self.db.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
```

### ID Generation
```python
def get_next_id(self) -> int:
    """Generate next unique ID."""
    all_tasks = self.tasks.all()
    if not all_tasks:
        return 1
    return max(task['id'] for task in all_tasks) + 1
```

### CRUD Operations
```python
def insert(self, task: dict) -> int:
    """Insert a new task."""
    task['id'] = self.get_next_id()
    doc_id = self.tasks.insert(task)
    return task['id']

def get(self, task_id: int) -> Optional[dict]:
    """Get task by ID."""
    return self.tasks.get(self.query.id == task_id)

def get_all(self) -> List[dict]:
    """Get all tasks."""
    return self.tasks.all()

def update(self, task_id: int, updates: dict) -> bool:
    """Update task by ID."""
    result = self.tasks.update(updates, self.query.id == task_id)
    return len(result) > 0

def delete(self, task_id: int) -> bool:
    """Delete task by ID."""
    result = self.tasks.remove(self.query.id == task_id)
    return len(result) > 0
```

### Query Patterns
```python
# Simple equality
tasks = db.tasks.search(db.query.priority == 'high')

# Logical AND
tasks = db.tasks.search(
    (db.query.priority == 'high') & 
    (db.query.status == 'pending')
)

# Logical OR
tasks = db.tasks.search(
    (db.query.priority == 'high') | 
    (db.query.priority == 'urgent')
)

# NOT
tasks = db.tasks.search(~(db.query.status == 'completed'))

# Test function (for complex conditions)
tasks = db.tasks.search(
    db.query.title.test(lambda t: 'keyword' in t.lower())
)

# Check if value in list
tasks = db.tasks.search(
    db.query.tags.test(lambda tags: 'work' in tags)
)

# Exists check
tasks = db.tasks.search(db.query.due_date.exists())

# Comparison operators
tasks = db.tasks.search(db.query.priority != 'low')
```

## Full Database Class
```python
class TodoDatabase:
    def __init__(self, db_path: str = "todo_data.json"):
        self.db = TinyDB(
            db_path,
            storage=CachingMiddleware(JSONStorage),
            indent=2
        )
        self.tasks = self.db.table('tasks')
        self.query = Query()
    
    def get_next_id(self) -> int:
        all_tasks = self.tasks.all()
        return max((t['id'] for t in all_tasks), default=0) + 1
    
    def insert(self, task: dict) -> int:
        task['id'] = self.get_next_id()
        self.tasks.insert(task)
        return task['id']
    
    def get(self, task_id: int) -> Optional[dict]:
        return self.tasks.get(self.query.id == task_id)
    
    def get_all(self) -> List[dict]:
        return self.tasks.all()
    
    def search(self, condition) -> List[dict]:
        return self.tasks.search(condition)
    
    def update(self, task_id: int, updates: dict) -> bool:
        return bool(self.tasks.update(updates, self.query.id == task_id))
    
    def delete(self, task_id: int) -> bool:
        return bool(self.tasks.remove(self.query.id == task_id))
    
    def clear(self):
        self.tasks.truncate()
    
    def close(self):
        self.db.close()
```

## Best Practices

- Use CachingMiddleware for better performance
- Always handle database closing properly
- Use context managers for automatic cleanup
- Generate IDs automatically
- Use Query objects for type-safe queries
- Index frequently queried fields conceptually
