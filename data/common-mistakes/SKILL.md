---
name: common-mistakes
description: Use before implementing pgdbm patterns to avoid common mistakes - provides rationalization table and red flags that prevent pool multiplication, schema errors, and template syntax violations
---

# pgdbm Common Mistakes: Prevention Guide

## Overview

**Core Principle:** Most pgdbm mistakes come from fighting the library's design instead of using it.

This skill provides explicit counters for common rationalizations that lead to bugs.

## The Iron Rules

**Violating these = your code is wrong:**

1. **ONE pool per database** - Never create multiple pools to same database in same process
2. **ALWAYS use {{tables.}}** - Never hardcode schema/table names
3. **ALWAYS specify module_name** - Never omit it in AsyncMigrationManager
4. **Schema is permanent** - Never change db.schema at runtime
5. **Conditional cleanup** - Only close connections you created
6. **Test cleanup in finally** - ALWAYS put `drop_test_database()` in a `finally` block

## Common Rationalizations Table

| Excuse | Reality | Fix |
|--------|---------|-----|
| "Each service needs different pool sizes" | Shared pool allocates dynamically. Pre-sizing is guessing. | ONE pool with total max |
| "Separate pools give better isolation" | Schema isolation is enough. Separate pools waste connections. | Schema-isolated managers |
| "It's simpler to just write the schema name" | Breaks portability. Code only works in one deployment mode. | Use `{{tables.}}` always |
| "I'll use search_path instead of templates" | Doesn't work with shared pools. Leads to race conditions. | Use `{{tables.}}` syntax |
| "module_name seems optional" | Causes migration conflicts when multiple modules share DB. | Always specify unique name |
| "I can switch schema at runtime for tenants" | Race conditions. Same manager used by concurrent requests. | Create manager per schema |
| "I'll close the db_manager in my library" | Closes parent app's pool. Crashes everything. | Check `_external_db` flag |
| "{{tables.}} is too verbose, I'll skip it" | Works until you use shared pools or change schemas. Then breaks. | Use always, no exceptions |
| "Cleanup doesn't need try/finally" | If test fails, cleanup never runs. Databases leak forever. | ALWAYS use try/finally |
| "I'll silence cleanup errors with except pass" | Hides failures. Databases accumulate silently for months. | Let cleanup errors propagate |

## Red Flags - STOP Immediately

If you're about to do ANY of these, you're making a mistake:

### 🚫 Creating Multiple Pools

```python
# WRONG
service1_db = AsyncDatabaseManager(DatabaseConfig(connection_string="postgresql://localhost/app"))
service2_db = AsyncDatabaseManager(DatabaseConfig(connection_string="postgresql://localhost/app"))
```

**What happens:**
- pgdbm logs warning: `"⚠️ Creating another connection pool to..."`
- You waste database connections
- Hit connection limits faster
- Reduce overall efficiency

**Fix:**
```python
# CORRECT
pool = await AsyncDatabaseManager.create_shared_pool(config)
service1_db = AsyncDatabaseManager(pool=pool, schema="service1")
service2_db = AsyncDatabaseManager(pool=pool, schema="service2")
```

### 🚫 Hardcoding Schema/Table Names

```python
# WRONG
await db.execute('INSERT INTO "myschema".users (email) VALUES ($1)', email)
await db.execute('INSERT INTO users (email) VALUES ($1)', email)
```

**What happens:**
- Code only works in one schema
- Breaks when used as library
- Can't test with different schemas
- Defeats dual-mode pattern

**Fix:**
```python
# CORRECT
await db.execute('INSERT INTO {{tables.users}} (email) VALUES ($1)', email)
```

### 🚫 Omitting module_name

```python
# WRONG
migrations = AsyncMigrationManager(db, "migrations")
# Uses "default" module name - conflicts with other modules!
```

**What happens:**
- Migration conflicts when multiple modules share database
- Can't track which migrations belong to which module
- Breaks schema isolation

**Fix:**
```python
# CORRECT
migrations = AsyncMigrationManager(db, "migrations", module_name="myservice")
```

### 🚫 Passing schema to AsyncMigrationManager

```python
# WRONG
migrations = AsyncMigrationManager(
    db,
    "migrations",
    schema="myschema"  # This parameter doesn't exist!
)
```

**What happens:**
- TypeError: unexpected keyword argument 'schema'

**Fix:**
```python
# CORRECT - schema comes from db
db = AsyncDatabaseManager(pool=pool, schema="myschema")
migrations = AsyncMigrationManager(db, "migrations", module_name="myservice")
```

### 🚫 Switching Schema at Runtime

```python
# WRONG
db = AsyncDatabaseManager(pool=pool, schema="tenant1")
# Later...
db.schema = "tenant2"  # Don't do this!
await db.execute("INSERT INTO {{tables.data}} ...")
```

**What happens:**
- Race conditions in concurrent requests
- Manager might be used by multiple requests simultaneously
- Unpredictable query routing

**Fix:**
```python
# CORRECT - create manager per schema
tenant1_db = AsyncDatabaseManager(pool=pool, schema="tenant1")
tenant2_db = AsyncDatabaseManager(pool=pool, schema="tenant2")
```

### 🚫 Calling connect() on Pool-Based Managers

```python
# WRONG
db = AsyncDatabaseManager(pool=shared_pool, schema="myservice")
await db.connect()  # ERROR!
```

**What happens:**
- Error: "Cannot call connect() when using an external pool"

**Fix:**
```python
# CORRECT - don't call connect() when using external pool
db = AsyncDatabaseManager(pool=shared_pool, schema="myservice")
# Just use it - no connect() needed
```

### 🚫 Not Closing Own Connections

```python
# WRONG in library
class MyLibrary:
    async def close(self):
        # Always disconnects, even if didn't create connection
        await self.db.disconnect()
```

**What happens:**
- Closes parent app's shared pool
- Crashes everything using that pool
- Other services fail

**Fix:**
```python
# CORRECT - conditional cleanup
class MyLibrary:
    async def close(self):
        if self.db and not self._external_db:
            await self.db.disconnect()
```

### 🚫 Mixing Template and Hardcoded References

```python
# WRONG - inconsistent
await db.execute('CREATE TABLE {{tables.users}} (...)')
await db.execute('INSERT INTO users (email) VALUES ($1)', email)
```

**What happens:**
- CREATE goes to schema, INSERT goes to public
- Table not found errors
- Confusing bugs

**Fix:**
```python
# CORRECT - use templates everywhere
await db.execute('CREATE TABLE {{tables.users}} (...)')
await db.execute('INSERT INTO {{tables.users}} (email) VALUES ($1)', email)
```

### 🚫 Test Database Cleanup Outside try/finally

```python
# WRONG - cleanup never runs if test fails
@pytest_asyncio.fixture
async def test_db():
    test_database = AsyncTestDatabase(TEST_CONFIG)
    await test_database.create_test_database()

    async with test_database.get_test_db_manager(schema="myapp") as db:
        yield db

    await test_database.drop_test_database()  # ← NEVER RUNS IF TEST FAILS
```

**What happens:**
- If ANY test fails, the database is never dropped
- Orphaned `test_*` databases accumulate (thousands over time)
- PostgreSQL runs out of connections/disk space

**Fix:**
```python
# CORRECT - cleanup in finally block
@pytest_asyncio.fixture
async def test_db():
    test_database = AsyncTestDatabase(TEST_CONFIG)
    await test_database.create_test_database()

    try:
        async with test_database.get_test_db_manager(schema="myapp") as db:
            yield db
    finally:
        await test_database.drop_test_database()  # ← ALWAYS RUNS
```

**Even better - use provided fixtures:**
```python
# BEST - just import and use pgdbm fixtures
# tests/conftest.py
from pgdbm.fixtures.conftest import *

# No manual cleanup needed - fixtures handle it
```

### 🚫 Swallowing Exceptions in Test Cleanup

```python
# WRONG - silently ignores cleanup failure
finally:
    try:
        await test_db.drop_test_database()
    except Exception:
        pass  # Database leaks silently!
```

**What happens:**
- Cleanup fails for some reason (connection issue, etc.)
- Exception is swallowed, no one notices
- Databases accumulate silently

**Fix:**
```python
# CORRECT - let cleanup failures be visible
finally:
    await test_db.drop_test_database()  # Failure will be reported
```

### 🚫 Manual Database Management in Test Functions

```python
# WRONG - duplicating fixture logic in every test
@pytest.mark.asyncio
async def test_something():
    test_db = AsyncTestDatabase(config)
    await test_db.create_test_database()
    try:
        # ... test code ...
    finally:
        await test_db.drop_test_database()
```

**What happens:**
- Code duplication across tests
- Easy to forget cleanup in some tests
- Interrupts (Ctrl+C) may skip finally blocks

**Fix:**
```python
# CORRECT - use fixtures
@pytest.mark.asyncio
async def test_something(test_db):  # Fixture handles everything
    # ... test code ...
```

### 🚫 Not Using Unique module_name Per Schema

```python
# WRONG
migrations = AsyncMigrationManager(db1, "migrations", module_name="mylib")
migrations = AsyncMigrationManager(db2, "migrations", module_name="mylib")
# Both use same module_name but different schemas!
```

**What happens:**
- Migration tracking conflicts
- Migrations might not run when they should
- Can't use same library twice with different schemas

**Fix:**
```python
# CORRECT - include schema in module_name
migrations = AsyncMigrationManager(db1, "migrations", module_name=f"mylib_{schema1}")
migrations = AsyncMigrationManager(db2, "migrations", module_name=f"mylib_{schema2}")
```

## Symptom-Based Debugging

### Symptom: Orphaned test_* Databases

**Possible causes:**
1. Custom fixtures without try/finally cleanup
2. Manual database creation in test functions
3. Exceptions swallowed in cleanup code
4. Tests interrupted with Ctrl+C

**Debug checklist:**
```bash
# Count orphaned databases
psql -U postgres -t -c "SELECT COUNT(*) FROM pg_database WHERE datname ~ '^test_[0-9a-f]{8}'"

# If count > 0, you have a cleanup problem
```

**Fix:**
1. Check all custom fixtures for try/finally pattern
2. Stop using manual AsyncTestDatabase in tests - use fixtures
3. Remove `except Exception: pass` from cleanup code
4. Prefer `test_db_isolated` fixture (uses rollback, no database created)

**Clean up orphaned databases:**
```bash
psql -U postgres -t -c \
  "SELECT 'DROP DATABASE IF EXISTS \"' || datname || '\";' FROM pg_database WHERE datname ~ '^test_[0-9a-f]{8}'" \
  | psql -U postgres
```

### Symptom: "Relation does not exist"

**Possible causes:**
1. Not using `{{tables.}}` syntax
2. Schema not created
3. Migrations not run
4. Wrong schema in manager

**Debug checklist:**
```python
# Check schema configuration
print(f"Configured schema: {db.schema}")  # Should match where tables are

# Debug template expansion
print(db.prepare_query("SELECT * FROM {{tables.users}}"))
# Shows: 'SELECT * FROM "myschema".users' or 'SELECT * FROM users'

# Check query uses templates
query = "SELECT * FROM {{tables.users}}"  # ✅
query = "SELECT * FROM users"  # ❌

# Verify schema exists
schemas = await db.fetch_all(
    "SELECT schema_name FROM information_schema.schemata"
)
print([s["schema_name"] for s in schemas])

# Check migrations ran
applied = await migrations.get_applied_migrations()
print(f"Applied migrations: {applied}")
```

### Symptom: "Too many connections"

**Possible causes:**
1. Creating multiple pools to same database
2. Not closing connections
3. Connection leaks in error paths

**Debug checklist:**
```python
# Check for multiple pools
# Look for this warning in logs:
"⚠️  Creating another connection pool to..."

# Check pool stats
stats = await pool.get_pool_stats()
print(f"Used: {stats['used_size']}/{stats['size']}")

# Verify cleanup in shutdown
# Make sure you have:
await pool.close()  # Or await db.disconnect()
```

### Symptom: "Migration already applied" or conflicts

**Possible causes:**
1. Not using unique `module_name`
2. Same module_name for different schemas
3. Multiple services using default module name

**Debug checklist:**
```python
# Check module_name is unique
migrations = AsyncMigrationManager(
    db,
    "migrations",
    module_name="myservice"  # Should be unique per service/schema
)

# For dual-mode libraries
module_name = f"mylib_{schema}"  # Include schema in name
```

## Before You Code Checklist

Run through this before implementing pgdbm:

- [ ] Have I created more than one `AsyncDatabaseManager(DatabaseConfig(...))` to same database?
- [ ] Am I using `{{tables.tablename}}` in ALL queries and migrations?
- [ ] Have I specified unique `module_name` for each service/schema?
- [ ] Am I closing connections conditionally (only if I created them)?
- [ ] Have I avoided hardcoding schema names?
- [ ] Am I creating managers per schema (not switching schema at runtime)?
- [ ] If using shared pool, am I NOT calling .connect() on managers?

**If you answered YES to first question or NO to any others:** Review the pattern skills.

## Testing Your Understanding

**Quick self-test:** What's wrong with each?

```python
# 1. What's wrong?
db1 = AsyncDatabaseManager(DatabaseConfig(connection_string="postgresql://localhost/app"))
db2 = AsyncDatabaseManager(DatabaseConfig(connection_string="postgresql://localhost/app"))

# 2. What's wrong?
await db.execute("INSERT INTO users (email) VALUES ($1)", email)

# 3. What's wrong?
migrations = AsyncMigrationManager(db, "migrations")

# 4. What's wrong?
db = AsyncDatabaseManager(pool=pool, schema="service1")
await db.connect()

# 5. What's wrong?
db.schema = "different_schema"
```

**Answers:**
1. Two pools to same database - use `create_shared_pool()`
2. Hardcoded table name - use `{{tables.users}}`
3. No module_name specified - add `module_name="myservice"`
4. Can't call connect() with external pool - just use db
5. Never change schema at runtime - create new manager

## The Bottom Line

**If pgdbm is fighting you, you're using it wrong.**

The library is designed for specific patterns:
- One pool, many schemas
- Template syntax everywhere
- Module name always specified
- Conditional resource management

Follow these patterns and pgdbm works smoothly. Fight them and you get errors, warnings, and bugs.

## Related Skills

- For mental model: `pgdbm:using-pgdbm`
- For pattern selection: `pgdbm:choosing-pattern`
- For implementation: `pgdbm:shared-pool-pattern`, `pgdbm:dual-mode-library`
