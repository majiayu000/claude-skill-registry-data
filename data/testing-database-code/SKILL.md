---
name: testing-database-code
description: Use when writing tests for pgdbm-based code - provides fixture selection decision tree and complete usage patterns without needing testing docs
---

# Testing Database Code: Fixtures and Patterns

## Overview

**Core Principle:** Import fixtures, choose based on speed vs isolation needs, write tests.

pgdbm provides 6 test fixtures covering different testing scenarios. This skill helps you choose the right one in <10 seconds.

## Quick Setup

```python
# tests/conftest.py
from pgdbm.fixtures.conftest import *

# All fixtures now available to all tests
```

That's it. No configuration needed.

## Fixture Selection Decision Tree

```
Which fixture should I use?
│
├─ Need SPEED (large test suite, CI/CD)?
│  └─ → test_db_isolated (transaction rollback)
│
├─ Need MULTIPLE databases in one test?
│  └─ → test_db_factory
│
├─ Need SAMPLE DATA already populated?
│  └─ → test_db_with_data (3 users, 2 projects, 5 agents)
│
├─ Need EMPTY TABLES (users, projects, agents)?
│  └─ → test_db_with_tables
│
├─ Need SCHEMA ISOLATION testing?
│  └─ → test_db_with_schema
│
└─ Need BLANK database (custom schema)?
   └─ → test_db (most flexible)
```

## Fixtures Quick Reference

| Fixture | Speed | What You Get | Best For |
|---------|-------|--------------|----------|
| `test_db_isolated` | **Fastest** | Transaction rollback | Large test suites, speed critical |
| `test_db` | Slow | Blank database | Custom schema, migrations |
| `test_db_with_tables` | Slow | Empty tables (users, projects, agents) | CRUD testing |
| `test_db_with_data` | Slow | Tables + sample data | Read operations, queries |
| `test_db_with_schema` | Slow | Blank + test_schema | Multi-tenant testing |
| `test_db_factory` | Slowest | Multiple databases | Microservices, distributed |

## Complete Usage Examples

### 1. test_db - Blank Database

**Use when:** Testing migrations, need custom schema

```python
async def test_custom_schema(test_db):
    # Create your own tables
    await test_db.execute("""
        CREATE TABLE products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        )
    """)

    product_id = await test_db.execute_and_return_id(
        "INSERT INTO products (name) VALUES ($1)",
        "Widget"
    )

    assert product_id == 1
```

### 2. test_db_with_tables - Most Common

**Use when:** Testing CRUD operations (most common use case)

**Tables provided:**
- `users(id, email, full_name, is_active, created_at)`
- `projects(id, name, owner_id, description, created_at)`
- `agents(id, project_id, title, status, assigned_to, created_at)`

```python
async def test_user_creation(test_db_with_tables):
    # Tables exist but are empty
    user_id = await test_db_with_tables.execute_and_return_id(
        "INSERT INTO users (email, full_name) VALUES ($1, $2)",
        "alice@example.com",
        "Alice"
    )

    user = await test_db_with_tables.fetch_one(
        "SELECT * FROM users WHERE id = $1",
        user_id
    )

    assert user["email"] == "alice@example.com"
```

### 3. test_db_with_data - Pre-Populated

**Use when:** Testing queries, don't want to set up data

**Sample data:**
- 3 users: alice@example.com, bob@example.com, charlie@example.com
- 2 projects (owned by alice)
- 5 agents across projects

```python
async def test_project_stats(test_db_with_data):
    # Data already exists!
    users = await test_db_with_data.fetch_all(
        "SELECT * FROM users ORDER BY email"
    )

    assert len(users) == 3
    assert users[0]["email"] == "alice@example.com"

    # Test aggregations
    stats = await test_db_with_data.fetch_one("""
        SELECT
            COUNT(DISTINCT p.id) as project_count,
            COUNT(a.id) as agent_count
        FROM projects p
        LEFT JOIN agents a ON p.id = a.project_id
    """)

    assert stats["project_count"] == 2
    assert stats["agent_count"] == 5
```

### 4. test_db_isolated - Fast Rollback

**Use when:** Speed critical, large test suite

**Key differences:**
- Returns `TransactionManager` (not `AsyncDatabaseManager`)
- All changes roll back automatically
- Much faster (no DB create/drop)

```python
async def test_fast_isolation(test_db_isolated):
    # Create table (will rollback)
    await test_db_isolated.execute("""
        CREATE TABLE temp_table (
            id SERIAL PRIMARY KEY,
            data TEXT
        )
    """)

    await test_db_isolated.execute(
        "INSERT INTO temp_table (data) VALUES ($1)",
        "test data"
    )

    result = await test_db_isolated.fetch_one(
        "SELECT * FROM temp_table"
    )

    assert result["data"] == "test data"
    # All changes automatically rolled back after test
```

### 5. test_db_with_schema - Schema Isolation

**Use when:** Testing multi-tenant, schema-specific ops

**Schema:** `test_schema` pre-created

```python
async def test_schema_qualified_tables(test_db_with_schema):
    # Create table with template syntax
    await test_db_with_schema.execute("""
        CREATE TABLE {{tables.tenants}} (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255)
        )
    """)

    # {{tables.tenants}} becomes "test_schema".tenants
    await test_db_with_schema.execute(
        "INSERT INTO {{tables.tenants}} (name) VALUES ($1)",
        "Tenant A"
    )

    tenant = await test_db_with_schema.fetch_one(
        "SELECT * FROM {{tables.tenants}}"
    )

    assert tenant["name"] == "Tenant A"
```

### 6. test_db_factory - Multiple Databases

**Use when:** Testing microservices, distributed systems

```python
async def test_multiple_services(test_db_factory):
    # Create separate databases
    users_db = await test_db_factory.create_db(
        suffix="users",
        schema="users"
    )

    orders_db = await test_db_factory.create_db(
        suffix="orders",
        schema="orders"
    )

    # Set up users database
    await users_db.execute("""
        CREATE TABLE {{tables.users}} (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255)
        )
    """)

    await users_db.execute(
        "INSERT INTO {{tables.users}} (email) VALUES ($1)",
        "user@example.com"
    )

    # Set up orders database
    await orders_db.execute("""
        CREATE TABLE {{tables.orders}} (
            id SERIAL PRIMARY KEY,
            user_email VARCHAR(255),
            total DECIMAL(10,2)
        )
    """)

    await orders_db.execute(
        "INSERT INTO {{tables.orders}} (user_email, total) VALUES ($1, $2)",
        "user@example.com",
        99.99
    )

    # Both databases are independent
    user_count = await users_db.fetch_value(
        "SELECT COUNT(*) FROM {{tables.users}}"
    )
    order_count = await orders_db.fetch_value(
        "SELECT COUNT(*) FROM {{tables.orders}}"
    )

    assert user_count == 1
    assert order_count == 1
    # All databases cleaned up automatically
```

## Testing Patterns

### Pattern: Custom Fixtures

Build on base fixtures for reusable test setup:

```python
# tests/conftest.py
import pytest_asyncio
from pgdbm.fixtures.conftest import *

@pytest_asyncio.fixture
async def user_with_project(test_db_with_tables):
    """Create user and project for testing."""
    user_id = await test_db_with_tables.execute_and_return_id(
        "INSERT INTO users (email, full_name) VALUES ($1, $2)",
        "test@example.com",
        "Test User"
    )

    project_id = await test_db_with_tables.execute_and_return_id(
        "INSERT INTO projects (name, owner_id) VALUES ($1, $2)",
        "Test Project",
        user_id
    )

    return {
        "user_id": user_id,
        "project_id": project_id,
        "db": test_db_with_tables
    }

# tests/test_projects.py
async def test_project_access(user_with_project):
    db = user_with_project["db"]
    project_id = user_with_project["project_id"]

    project = await db.fetch_one(
        "SELECT * FROM projects WHERE id = $1",
        project_id
    )

    assert project is not None
```

### Pattern: Transaction Testing

Test commit and rollback behavior:

```python
async def test_transaction_commit(test_db_with_tables):
    async with test_db_with_tables.transaction() as tx:
        await tx.execute(
            "INSERT INTO users (email, full_name) VALUES ($1, $2)",
            "commit@example.com",
            "Commit Test"
        )
        # Commits automatically on context exit

    # Verify committed
    user = await test_db_with_tables.fetch_one(
        "SELECT * FROM users WHERE email = $1",
        "commit@example.com"
    )

    assert user is not None


async def test_transaction_rollback(test_db_with_tables):
    import pytest

    with pytest.raises(ValueError):
        async with test_db_with_tables.transaction() as tx:
            await tx.execute(
                "INSERT INTO users (email, full_name) VALUES ($1, $2)",
                "rollback@example.com",
                "Rollback Test"
            )
            raise ValueError("Force rollback")

    # Verify rolled back
    user = await test_db_with_tables.fetch_one(
        "SELECT * FROM users WHERE email = $1",
        "rollback@example.com"
    )

    assert user is None
```

### Pattern: Testing Migrations

```python
from pgdbm import AsyncMigrationManager

async def test_apply_migrations(test_db):
    # Apply migrations to blank database
    migrations = AsyncMigrationManager(
        test_db,
        migrations_path="migrations",
        module_name="test"
    )

    result = await migrations.apply_pending_migrations()

    # Verify migrations applied
    assert len(result["applied"]) > 0

    # Verify tables created
    tables = await test_db.fetch_all("""
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'public'
    """)

    table_names = {t["tablename"] for t in tables}
    assert "users" in table_names
```

## Common Mistakes

### ❌ Not Importing Fixtures

```python
# WRONG: Fixtures not available
async def test_something(test_db):  # NameError!
    ...
```

**Fix:** Add to `conftest.py`:
```python
from pgdbm.fixtures.conftest import *
```

### ❌ Using Wrong Fixture

```python
# WRONG: Using isolated for schema testing
async def test_schema(test_db_isolated):
    # test_db_isolated doesn't have schema setup
    await test_db_isolated.execute("CREATE SCHEMA test_schema")
    # Fails - schema rolls back immediately
```

**Fix:** Use `test_db_with_schema` for schema testing.

### ❌ Expecting Data in test_db_with_tables

```python
# WRONG: Tables are empty
async def test_query(test_db_with_tables):
    users = await test_db_with_tables.fetch_all("SELECT * FROM users")
    assert len(users) == 3  # Fails - tables are empty!
```

**Fix:** Either insert data yourself or use `test_db_with_data`.

### ❌ Calling .connect() on Fixtures

```python
# WRONG: Fixture already connected
async def test_something(test_db):
    await test_db.connect()  # Don't do this!
```

**Fix:** Fixtures are already connected, just use them.

## Performance Comparison

On typical laptop (PostgreSQL 15):

| Fixture | ~Time per Test | Relative Speed |
|---------|---------------|----------------|
| `test_db_isolated` | ~5ms | 100x faster |
| `test_db` | ~500ms | Baseline |
| `test_db_with_tables` | ~600ms | Slower (creates tables) |
| `test_db_with_data` | ~700ms | Slowest (inserts data) |
| `test_db_factory` (2 DBs) | ~1000ms | 2x slower |

**For 100 tests:**
- With `test_db`: ~50 seconds
- With `test_db_isolated`: ~0.5 seconds

## When to Use Each (Summary)

**Daily development:** `test_db_with_tables` (most flexible for CRUD)

**CI/CD pipelines:** `test_db_isolated` (speed matters)

**Migration testing:** `test_db` (blank slate)

**Query/reporting tests:** `test_db_with_data` (pre-populated)

**Multi-tenant tests:** `test_db_with_schema` (schema isolation)

**Distributed systems:** `test_db_factory` (multiple DBs)

## Environment Variables

Override test database connection:

```bash
export TEST_DB_HOST=localhost
export TEST_DB_PORT=5432
export TEST_DB_USER=postgres
export TEST_DB_PASSWORD=postgres
export TEST_DB_VERBOSE=1  # Enable verbose logging
export TEST_DB_LOG_SQL=1  # Log all SQL queries
```

## Complete Test File Template

```python
# tests/test_example.py
import pytest

async def test_basic_operation(test_db_with_tables):
    """Test with empty tables (most common)."""
    user_id = await test_db_with_tables.execute_and_return_id(
        "INSERT INTO users (email, full_name) VALUES ($1, $2)",
        "test@example.com",
        "Test User"
    )

    assert user_id is not None


async def test_with_data(test_db_with_data):
    """Test with sample data."""
    users = await test_db_with_data.fetch_all("SELECT * FROM users")
    assert len(users) == 3


async def test_fast_isolated(test_db_isolated):
    """Fast test with rollback."""
    await test_db_isolated.execute(
        "CREATE TABLE temp (id SERIAL PRIMARY KEY)"
    )
    # Rolls back automatically
```

That's everything you need for testing pgdbm code.

## Related Skills

- For mental model: `pgdbm:using-pgdbm`
- For patterns: `pgdbm:choosing-pattern`
- For implementation: `pgdbm:shared-pool-pattern`, `pgdbm:dual-mode-library`
