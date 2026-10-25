---
name: manage-database-session
description: >
  This skill covers patterns for managing database sessions and models.
  Trigger: Load when working with database interactions.
license: Apache-2.0
metadata:
  author: repoforge
  version: "1.0"
  complexity: low
  token_estimate: 350
  dependencies: []
  related_skills: []
  load_priority: high
---

<!-- L1:START -->
# manage-database-session

This skill covers patterns for managing database sessions and models.

**Trigger**: Load when working with database interactions.
<!-- L1:END -->

<!-- L2:START -->
## Quick Reference

| Task | Pattern |
|------|---------|
| Create a database session | `get_db()` |
| Define a database model | `Base` |

## Critical Patterns (Summary)
- **Create a database session**: Use `get_db()` to create a session for database operations.
- **Define a database model**: Utilize `Base` to define your database models.
<!-- L2:END -->

<!-- L3:START -->
## Critical Patterns (Detailed)

### Create a database session

Use `get_db()` to create a session for database operations, ensuring proper management of database connections.

```python
from apps.server.app.models.database import get_db

async def some_database_operation():
    async with get_db() as session:
        # Perform database operations
        pass
```

### Define a database model

Utilize `Base` to define your database models, which will serve as the foundation for your ORM mappings.

```python
from apps.server.app.models.database import Base
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
```

## When to Use

- When creating a new database session for CRUD operations.
- When defining new models for your database schema.

## Commands

```bash
python -m alembic upgrade head
```

## Anti-Patterns

### Don't: Use raw SQL queries directly

Using raw SQL queries bypasses the ORM and can lead to security vulnerabilities and maintenance issues.

```python
# BAD
async def raw_query():
    await db.execute("SELECT * FROM users")
```
<!-- L3:END -->