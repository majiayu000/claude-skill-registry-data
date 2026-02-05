---
name: neon-db-skill
description: Reusable Neon PostgreSQL skill for serverless database operations, connection pooling, and async connections. Use with Neon MCP server.
---

# Neon DB Skill

Use this skill when working with Neon Serverless PostgreSQL databases.

## Connection Pattern

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Neon connection string format
DATABASE_URL = "postgresql+asyncpg://user:password@ep-xyz.region.neon.tech/dbname?sslmode=require"

# Create async engine for Neon
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Set to False in production
    pool_size=5,
    max_overflow=10,
)

# Session factory
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

## Environment Variables

```bash
# .env
DATABASE_URL="postgresql+asyncpg://user:pass@ep-xyz.region.neon.tech/db?sslmode=require"
```

## Testing Connection

```python
async def test_connection():
    """Test Neon database connection."""
    try:
        async with engine.begin() as conn:
            result = await conn.execute("SELECT 1")
            print("Connection successful!")
    except Exception as e:
        print(f"Connection failed: {e}")
```

## Schema Operations

```python
# Create table
async def create_tables():
    """Create all SQLModel tables."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

# Drop table
async def drop_tables():
    """Drop all SQLModel tables."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
```

## Index Creation

```python
async def create_indexes():
    """Create indexes for better query performance."""
    async with engine.begin() as conn:
        # Single column index
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id)"
        )
        # Composite index
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_user_completed ON tasks(user_id, completed)"
        )
```

## Neon MCP Server Usage

Use `@neon:run-sql` for queries:
```python
# Get tables
@neon:run_sql "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
```

Use `@neon:describe_table_schema` for schema:
```python
@neon:describe_table_schema tableName="tasks"
```

## Best Practices

1. Always use `sslmode=require` for Neon
2. Use async engine with `asyncpg` driver
3. Set reasonable pool sizes (5-10)
4. Use `expire_on_commit=False` to avoid refresh issues
5. Always close sessions in finally block
6. Create indexes on foreign keys and frequently filtered columns
7. Use connection pooling for serverless functions
