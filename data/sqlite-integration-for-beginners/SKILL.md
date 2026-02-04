---
name: sqlite-integration-for-beginners
description: Add SQLite database to Flask or Sinatra app with beginner-friendly code examples and teaching comments
license: Complete terms in LICENSE.txt
---

# SQLite Integration for Beginners
**Version:** 0.17.0

## When to Use
- User has app with in-memory storage (lists/arrays)
- User asks "How do I save data permanently?"
- User wants data to persist after restart

## Prerequisites
- Working Flask/Sinatra app
- Understanding routes and templates
- At least one feature using list storage

## What is SQLite?
**List/Array:** Like whiteboard notes - disappears when server stops
**SQLite:** Like notebook - saved to file (`notes.db`), persists forever

Perfect for beginners:
- No server setup
- Built into Python
- Easy SQL basics
- Upgrades to PostgreSQL later

## Key Concepts

### Database Structure
```
Table = Spreadsheet
Columns = Data types (id, name, email)
Rows = Data entries
```

### SQL Commands
| Command | Purpose |
|---------|---------|
| CREATE TABLE | Make new table |
| INSERT INTO | Add data |
| SELECT | Get data |
| UPDATE | Change data |
| DELETE | Remove data |

## Implementation

### Flask
```python
import sqlite3

def get_db():
    conn = sqlite3.connect('notes.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    conn = get_db()
    notes = conn.execute('SELECT * FROM notes').fetchall()
    conn.close()
    return render_template('index.html', notes=notes)
```

### Sinatra
```ruby
require 'sqlite3'
DB = SQLite3::Database.new 'notes.db'
DB.results_as_hash = true

DB.execute <<-SQL
  CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  )
SQL

get '/' do
  @notes = DB.execute('SELECT * FROM notes')
  erb :index
end
```

## SQL Explanation
- `CREATE TABLE IF NOT EXISTS`: Safe to run multiple times
- `PRIMARY KEY AUTOINCREMENT`: Unique auto-incrementing ID
- `NOT NULL`: Value required
- `DEFAULT CURRENT_TIMESTAMP`: Auto-filled time
- `?` placeholder: Prevents SQL injection

## Common Questions
- **Database location:** `notes.db` in project folder
- **View inside:** DB Browser for SQLite
- **Mistake?** Delete `notes.db`, it recreates
- **Ruby install:** `gem install sqlite3`

## Troubleshooting
| Error | Solution |
|-------|----------|
| no such table | Run `init_db()` function |
| Database locked | Close DB Browser, restart server |
| no such column | Check spelling in SQL |

---

**End of Skill**
