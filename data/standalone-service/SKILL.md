---
name: standalone-service
description: Use when building simple standalone service or microservice with its own database - provides complete setup without shared pool complexity
---

# Standalone Service Pattern

## Overview

**Core Principle:** Create own pool with DatabaseConfig, run migrations, use database.

Simplest pgdbm pattern for services that own their database.

## When to Use This

From `pgdbm:choosing-pattern` skill - use when:
- Single service with dedicated database
- Background worker (separate process)
- Simple microservice
- Development/testing
- Learning pgdbm

## Complete Implementation

```python
from pgdbm import AsyncDatabaseManager, AsyncMigrationManager, DatabaseConfig

# Create configuration
config = DatabaseConfig(
    connection_string="postgresql://localhost/myservice",
    min_connections=5,
    max_connections=20,
)

# Create database manager
db = AsyncDatabaseManager(config)
await db.connect()

# Run migrations
migrations = AsyncMigrationManager(
    db,
    migrations_path="./migrations",
    module_name="myservice"  # Required
)

result = await migrations.apply_pending_migrations()

# Use database
user_id = await db.execute_and_return_id(
    "INSERT INTO {{tables.users}} (email, name) VALUES ($1, $2)",
    "alice@example.com",
    "Alice"
)

# Cleanup (on shutdown)
await db.disconnect()
```

That's it. Complete standalone setup.

## FastAPI Integration

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from pgdbm import AsyncDatabaseManager, AsyncMigrationManager, DatabaseConfig

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create database connection
    config = DatabaseConfig(
        connection_string="postgresql://localhost/myapp",
        min_connections=5,
        max_connections=20,
    )

    db = AsyncDatabaseManager(config)
    await db.connect()

    # Run migrations
    migrations = AsyncMigrationManager(
        db,
        migrations_path="./migrations",
        module_name="myapp"
    )
    await migrations.apply_pending_migrations()

    # Store in app state
    app.state.db = db

    yield

    # Shutdown: Close connection
    await db.disconnect()

app = FastAPI(lifespan=lifespan)

@app.post("/users")
async def create_user(email: str, name: str, request: Request):
    db = request.app.state.db

    user_id = await db.execute_and_return_id(
        "INSERT INTO {{tables.users}} (email, name) VALUES ($1, $2)",
        email,
        name
    )

    return {"id": user_id, "email": email}

@app.get("/users/{user_id}")
async def get_user(user_id: int, request: Request):
    db = request.app.state.db

    user = await db.fetch_one(
        "SELECT * FROM {{tables.users}} WHERE id = $1",
        user_id
    )

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
```

## Project Structure

```
myservice/
├── main.py              # FastAPI app or entry point
├── migrations/
│   ├── 001_create_users.sql
│   ├── 002_create_posts.sql
│   └── 003_add_indexes.sql
├── tests/
│   ├── conftest.py
│   └── test_users.py
├── .env                 # DATABASE_URL
└── pyproject.toml
```

## Environment Configuration

```bash
# .env
DATABASE_URL=postgresql://user:password@localhost:5432/myservice
```

```python
import os
from pgdbm import DatabaseConfig

# Load from environment
config = DatabaseConfig(
    connection_string=os.getenv("DATABASE_URL"),
    min_connections=int(os.getenv("DB_MIN_CONN", "5")),
    max_connections=int(os.getenv("DB_MAX_CONN", "20")),
)
```

## Background Worker Example

```python
import asyncio
from pgdbm import AsyncDatabaseManager, AsyncMigrationManager, DatabaseConfig

async def process_job(db, job):
    """Process a single job."""
    result = await do_work(job)

    await db.execute(
        "INSERT INTO {{tables.job_results}} (job_id, result) VALUES ($1, $2)",
        job.id,
        result
    )

async def main():
    # Setup database
    config = DatabaseConfig(
        connection_string="postgresql://localhost/worker",
        min_connections=2,
        max_connections=10,
    )

    db = AsyncDatabaseManager(config)
    await db.connect()

    # Run migrations
    migrations = AsyncMigrationManager(
        db,
        migrations_path="./migrations",
        module_name="worker"
    )
    await migrations.apply_pending_migrations()

    # Worker loop
    while True:
        job = await get_next_job()
        if job:
            await process_job(db, job)
        else:
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
```

## With Schema Isolation

Even standalone services can use schemas:

```python
config = DatabaseConfig(
    connection_string="postgresql://localhost/mydb",
    schema="myservice",  # Service gets own schema
    min_connections=5,
    max_connections=20,
)

db = AsyncDatabaseManager(config)
await db.connect()

# Migrations automatically go to "myservice" schema
migrations = AsyncMigrationManager(
    db,
    migrations_path="./migrations",
    module_name="myservice"
)
await migrations.apply_pending_migrations()

# All queries automatically scoped to schema
# {{tables.users}} → "myservice".users
```

**When to use schema:**
- Sharing database with other services
- Want namespace isolation
- Multi-tenant within service

## Testing

```python
# tests/conftest.py
from pgdbm.fixtures.conftest import *

# tests/test_users.py
async def test_create_user(test_db):
    """Test user creation."""
    # Apply your migrations to test database
    migrations = AsyncMigrationManager(
        test_db,
        migrations_path="./migrations",
        module_name="test"
    )
    await migrations.apply_pending_migrations()

    # Test your code
    user_id = await test_db.execute_and_return_id(
        "INSERT INTO {{tables.users}} (email) VALUES ($1)",
        "test@example.com"
    )

    assert user_id == 1
```

## When NOT to Use Standalone

Don't use standalone if:
- You have multiple services in same Python process → Use shared pool
- Building reusable library → Use dual-mode
- Multiple routers in FastAPI app → Use shared pool

Standalone is for truly independent services.

## Quick Checklist

- [ ] Create DatabaseConfig with connection_string
- [ ] Create AsyncDatabaseManager(config)
- [ ] Call await db.connect()
- [ ] Create AsyncMigrationManager with unique module_name
- [ ] Apply migrations
- [ ] Use {{tables.}} syntax in all SQL
- [ ] Call await db.disconnect() on shutdown

That's the complete standalone pattern.

## Related Skills

- For pattern selection: `pgdbm:choosing-pattern`
- For mental model: `pgdbm:using-pgdbm`
- For complete API: `pgdbm:core-api-reference`, `pgdbm:migrations-api-reference`
- For testing: `pgdbm:testing-database-code`
