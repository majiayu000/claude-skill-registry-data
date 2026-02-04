---
name: sqlalchemy-conversion
description: This skill should be used when the user asks to "convert asyncpg to SQLAlchemy", "convert database queries", "migrate asyncpg code", "transform asyncpg patterns to SQLAlchemy", or "update FastAPI database layer". It provides systematic conversion of asyncpg code to SQLAlchemy async patterns with proper error handling and transaction management.
version: 1.0.0
---

# SQLAlchemy Conversion for AsyncPG Migration

This skill provides systematic conversion of asyncpg database code to SQLAlchemy 2.0+ with async support, maintaining async performance while providing ORM benefits.

## Conversion Strategy

Convert asyncpg procedural code to SQLAlchemy declarative patterns while preserving async functionality and improving maintainability.

## Core Conversion Patterns

### Import Replacement
Replace asyncpg imports with SQLAlchemy:
- `import asyncpg` → `from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine`
- `from asyncpg import Connection` → `from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker`

### Engine Configuration
Convert connection setup:
```python
# Before (asyncpg)
engine = await asyncpg.create_pool(dsn)

# After (SQLAlchemy)
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    poolclass=NullPool  # For asyncpg compatibility
)
```

### Session Management
Replace connection objects with async sessions:
```python
# Before (asyncpg)
async def get_user(db, user_id):
    async with db.acquire() as conn:
        result = await conn.fetchrow("SELECT * FROM users WHERE id = $1", user_id)
        return dict(result)

# After (SQLAlchemy)
async def get_user(session: AsyncSession, user_id: int):
    result = await session.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalar_one()
```

## Query Conversion Guidelines

### SELECT Queries
Transform fetch operations to SQLAlchemy Core/ORM:
- `fetchall()` → `execute().scalars().all()`
- `fetchrow()` → `execute().scalar_one()` or `execute().first()`
- `fetchval()` → `execute().scalar()`
- `iter()` → `execute().yield_per()`

### INSERT Operations
Convert execute patterns:
```python
# Before (asyncpg)
await conn.execute(
    "INSERT INTO users (name, email) VALUES ($1, $2)",
    name, email
)

# After (SQLAlchemy ORM)
session.add(User(name=name, email=email))
await session.commit()
```

### Transaction Handling
Update transaction patterns:
```python
# Before (asyncpg)
async with conn.transaction():
    await conn.execute("UPDATE users SET status = $1", status)

# After (SQLAlchemy)
async with session.begin():
    await session.execute(
        update(User).where(User.id == user_id).values(status=status)
    )
```

## Usage Instructions

To convert asyncpg code:

1. **Analyze detected patterns**: Use detection results to understand current codebase structure
2. **Apply systematic conversion**: Follow the pattern mapping for each identified asyncpg usage
3. **Handle edge cases**: Refer to complex cases documentation for advanced scenarios
4. **Validate conversions**: Test converted code to ensure functionality is preserved

## Error Handling Conversion

### Exception Types
Update exception handling:
- `asyncpg.PostgresError` → `sqlalchemy.exc.DBAPIError`
- `asyncpg.InterfaceError` → `sqlalchemy.exc.InterfaceError`
- `asyncpg.exceptions` → Use SQLAlchemy's built-in exceptions

### Connection Errors
Implement robust error handling:
```python
# Before
try:
    conn = await asyncpg.connect(dsn)
except asyncpg.PostgresError as e:
    logger.error(f"Database connection failed: {e}")

# After
try:
    engine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        pass
except SQLAlchemyError as e:
    logger.error(f"Database setup failed: {e}")
```

## Additional Resources

### Reference Files
- **`references/pattern-mapping.md`** - Comprehensive asyncpg to SQLAlchemy conversion mapping
- **`references/async-patterns.md`** - Async SQLAlchemy best practices
- **`references/error-handling.md`** - SQLAlchemy exception handling patterns

### Examples
- **`examples/conversion-comparison.md`** - Side-by-side asyncpg vs SQLAlchemy examples
- **`examples/migration-scripts.py`** - Automated conversion utilities
- **`examples/test-validation.py`** - Testing converted code patterns