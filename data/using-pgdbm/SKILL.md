---
name: using-pgdbm
description: Use when setting up pgdbm database connections, migrations, or multi-service architecture - provides mental model of one pool/many schemas/template syntax and complete API reference without needing to read docs
---

# Using pgdbm: Mental Model and Core Patterns

## Overview

**Core Principle:** One shared connection pool, multiple schema-isolated managers, template-based queries.

pgdbm is designed so code can run standalone (creates own pool) OR embedded (uses shared pool) without changes. This flexibility comes from three key patterns:

1. **ONE pool to rule them all** - Never create multiple pools to the same database
2. **Schema isolation** - Each service/module gets its own PostgreSQL schema
3. **Template syntax** - `{{tables.tablename}}` works across all deployment modes

## Quick Decision Tree

```
Need database access?
├─ Multiple services/modules in same app?
│  └─ Use SHARED POOL pattern
│     • Create ONE pool with create_shared_pool()
│     • Each service gets AsyncDatabaseManager(pool=shared_pool, schema="service_name")
│     • Each runs own migrations with unique module_name
│
├─ Building reusable library/package?
│  └─ Use DUAL-MODE pattern
│     • Accept EITHER connection_string OR db_manager parameter
│     • Create own pool if standalone, use provided if embedded
│     • ALWAYS run own migrations regardless
│
└─ Simple standalone service?
   └─ Use STANDALONE pattern
      • AsyncDatabaseManager(DatabaseConfig(...))
      • Run migrations with AsyncMigrationManager
```

## Complete API Quick Reference

### Creating Connections

```python
# Shared pool (for multi-service apps)
from pgdbm import AsyncDatabaseManager, DatabaseConfig

config = DatabaseConfig(
    connection_string="postgresql://user:pass@host/db",
    min_connections=10,
    max_connections=50,
)
shared_pool = await AsyncDatabaseManager.create_shared_pool(config)

# Schema-isolated managers (share the pool)
users_db = AsyncDatabaseManager(pool=shared_pool, schema="users")
orders_db = AsyncDatabaseManager(pool=shared_pool, schema="orders")

# Standalone (creates own pool)
db = AsyncDatabaseManager(config)
await db.connect()
```

### Running Migrations

```python
from pgdbm import AsyncMigrationManager

migrations = AsyncMigrationManager(
    db,                              # AsyncDatabaseManager instance
    migrations_path="./migrations",  # Directory with SQL files
    module_name="myservice"          # REQUIRED: unique identifier
)
result = await migrations.apply_pending_migrations()
```

### Writing Queries

```python
# ALWAYS use {{tables.}} syntax
user_id = await db.fetch_value(
    "INSERT INTO {{tables.users}} (email) VALUES ($1) RETURNING id",
    "user@example.com"
)

# With transactions
async with db.transaction() as tx:
    user_id = await tx.fetch_value(
        "INSERT INTO {{tables.users}} (email) VALUES ($1) RETURNING id",
        email
    )
    await tx.execute(
        "INSERT INTO {{tables.profiles}} (user_id, bio) VALUES ($1, $2)",
        user_id,
        "Bio text"
    )
    # Auto-commits on success, rolls back on exception
```

### Migration File Format

```sql
-- migrations/001_create_users.sql
CREATE TABLE IF NOT EXISTS {{tables.users}} (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS users_email
    ON {{tables.users}} (email);
```

## Why These Patterns Exist

### Why ONE Shared Pool?

**Problem:** PostgreSQL has hard connection limits (typically 100-400). Each connection consumes:
- 5-10MB server memory
- File descriptors
- Authentication overhead

**With pool-per-service:**
- 5 services × (min=10, max=50) = capacity for 250 connections
- Most sit idle, but you hit database limits anyway
- Wastes resources

**With shared pool:**
- One pool (min=20, max=100) serves all 5 services
- Connections allocated dynamically based on actual demand
- Never exceeds database limits

**Key insight:** Services don't hit peak load simultaneously. Dynamic allocation beats static pre-allocation.

### Why Schema Isolation?

**Three options for multi-tenancy/multi-service:**

| Approach | Security | Complexity | Use When |
|----------|----------|------------|----------|
| **Separate DBs** | Strongest (PostgreSQL enforced) | High | Regulatory requirements, <1000 tenants |
| **Separate Schemas** | Good (application enforced) | Medium | 100-10,000 tenants, B2B SaaS |
| **Row-level (tenant_id)** | Weakest (code must filter) | Low | Millions of tenants, consumer apps |

**pgdbm optimizes for schemas** because:
- PostgreSQL-native isolation
- Shared connection pool (efficient)
- Can't accidentally query across tenants (different schema = error)
- Simpler than separate databases, safer than row-level

### Why Template Syntax?

**Problem:** Hardcoding table names locks code to ONE deployment mode.

```python
# ❌ WRONG: Hardcoded - only works in "myapp" schema
await db.execute('INSERT INTO "myapp".users (email) VALUES ($1)', email)

# ✅ CORRECT: Template - works everywhere
await db.execute('INSERT INTO {{tables.users}} (email) VALUES ($1)', email)
```

**How it works:**
- With `schema="myapp"`: `{{tables.users}}` → `"myapp".users`
- Without schema: `{{tables.users}}` → `users`
- At **query preparation time** (not connection init for shared pools)

**Benefits:**
- Same code works standalone, shared pool, multi-tenant
- Can't forget schema qualification (template does it)
- Migrations portable across deployments
- Libraries can be composed (each uses own schema)

## Common Patterns

### FastAPI Integration

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create ONE shared pool
    config = DatabaseConfig(connection_string="postgresql://localhost/myapp")
    shared_pool = await AsyncDatabaseManager.create_shared_pool(config)

    # Schema-isolated managers
    app.state.dbs = {
        'users': AsyncDatabaseManager(pool=shared_pool, schema="users"),
        'orders': AsyncDatabaseManager(pool=shared_pool, schema="orders"),
    }

    # Run migrations for each
    for name, db in app.state.dbs.items():
        migrations = AsyncMigrationManager(
            db,
            migrations_path=f"migrations/{name}",
            module_name=name
        )
        await migrations.apply_pending_migrations()

    yield
    await shared_pool.close()

app = FastAPI(lifespan=lifespan)

@app.post("/users")
async def create_user(email: str, request: Request):
    db = request.app.state.dbs['users']
    user_id = await db.fetch_value(
        "INSERT INTO {{tables.users}} (email) VALUES ($1) RETURNING id",
        email
    )
    return {"id": user_id}
```

### Dual-Mode Library Pattern

```python
from typing import Optional
from pgdbm import AsyncDatabaseManager, DatabaseConfig

class MyLibrary:
    """Library that works standalone OR embedded."""

    def __init__(
        self,
        connection_string: Optional[str] = None,
        db_manager: Optional[AsyncDatabaseManager] = None,
    ):
        if not connection_string and not db_manager:
            raise ValueError("Provide connection_string OR db_manager")

        self._external_db = db_manager is not None
        self.db = db_manager
        self._connection_string = connection_string

    async def initialize(self):
        # Create pool only if not provided
        if not self._external_db:
            config = DatabaseConfig(connection_string=self._connection_string)
            self.db = AsyncDatabaseManager(config)
            await self.db.connect()

        # ALWAYS run own migrations
        migrations = AsyncMigrationManager(
            self.db,
            migrations_path="./migrations",
            module_name="mylib"  # Unique!
        )
        await migrations.apply_pending_migrations()

    async def close(self):
        # Only close if WE created the connection
        if self.db and not self._external_db:
            await self.db.disconnect()
```

## Red Flags - STOP and Reconsider

If you're about to do any of these, you're missing the mental model:

- [ ] Creating multiple `AsyncDatabaseManager` instances with `DatabaseConfig` to same database
- [ ] Hardcoding schema names in SQL: `INSERT INTO "myschema".users`
- [ ] Not using `{{tables.}}` syntax in queries or migrations
- [ ] Passing `schema` parameter to `AsyncMigrationManager` (it reads from db)
- [ ] Not specifying `module_name` in migrations (causes conflicts)
- [ ] Switching `db.schema` at runtime (create separate managers instead)
- [ ] Using bare table names: `INSERT INTO users` (not schema-safe)

**All of these mean:** Review the mental model. You're fighting the library instead of using its design.

## Complete API Reference

**For COMPLETE AsyncDatabaseManager API:** See `pgdbm:core-api-reference` skill

Includes ALL methods:
- `execute`, `executemany`, `execute_and_return_id`
- `fetch_one`, `fetch_all`, `fetch_value`
- `fetch_as_model`, `fetch_all_as_model` (Pydantic)
- `copy_records_to_table` (bulk operations)
- `table_exists`, `get_pool_stats`
- `transaction`, `acquire`
- Complete DatabaseConfig parameters (SSL, timeouts, retry, etc.)

**For COMPLETE AsyncMigrationManager API:** See `pgdbm:migrations-api-reference` skill

Includes ALL methods:
- `apply_pending_migrations`, `get_applied_migrations`
- `get_pending_migrations`, `find_migration_files`
- `create_migration`, `rollback_migration`
- `get_migration_history`
- Migration file format and naming conventions
- Checksum validation

**Quick reference for most common operations:**

```python
# Query methods
count = await db.fetch_value("SELECT COUNT(*) FROM {{tables.users}}")
user = await db.fetch_one("SELECT * FROM {{tables.users}} WHERE id = $1", user_id)
users = await db.fetch_all("SELECT * FROM {{tables.users}}")
await db.execute("DELETE FROM {{tables.users}} WHERE id = $1", user_id)
user_id = await db.execute_and_return_id("INSERT INTO {{tables.users}} ...", ...)

# Transactions
async with db.transaction() as tx:
    await tx.execute(...)
    await tx.fetch_value(...)

# Migrations
migrations = AsyncMigrationManager(db, "migrations", module_name="myapp")
result = await migrations.apply_pending_migrations()
```

## Template Syntax Reference

Available in all SQL queries and migration files:

```sql
{{tables.tablename}}  -- Expands to: "schema".tablename (or just tablename if no schema)
{{schema}}            -- Expands to: "schema" (or empty if no schema)
```

**How expansion works:**

```python
# With schema="myapp"
"SELECT * FROM {{tables.users}}" → "SELECT * FROM \"myapp\".users"

# Without schema
"SELECT * FROM {{tables.users}}" → "SELECT * FROM users"
```

## Complete Working Example

```python
# app.py - Complete production setup
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pgdbm import AsyncDatabaseManager, DatabaseConfig, AsyncMigrationManager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ONE shared pool
    config = DatabaseConfig(
        connection_string="postgresql://localhost/myapp",
        min_connections=10,
        max_connections=50,
    )
    shared_pool = await AsyncDatabaseManager.create_shared_pool(config)

    # Schema-isolated managers
    app.state.users_db = AsyncDatabaseManager(pool=shared_pool, schema="users")
    app.state.orders_db = AsyncDatabaseManager(pool=shared_pool, schema="orders")

    # Run migrations
    for db, path, name in [
        (app.state.users_db, "migrations/users", "users"),
        (app.state.orders_db, "migrations/orders", "orders"),
    ]:
        migrations = AsyncMigrationManager(db, path, name)
        await migrations.apply_pending_migrations()

    yield
    await shared_pool.close()

app = FastAPI(lifespan=lifespan)
```

## When to Use What

| Scenario | Pattern | Key Points |
|----------|---------|------------|
| FastAPI app with 3 services | Shared pool | ONE `create_shared_pool()`, each service gets schema |
| Building PyPI package | Dual-mode library | Accept `db_manager` OR `connection_string` |
| Simple microservice | Standalone | `AsyncDatabaseManager(config)` |
| Multi-tenant SaaS | Shared pool + schemas | Each tenant = separate schema |
| Testing | Use fixtures | Import from `pgdbm.fixtures.conftest` |

## Related Skills

**For pattern selection:**
- `pgdbm:choosing-pattern` - Which pattern for your use case

**For implementation:**
- `pgdbm:shared-pool-pattern` - Multi-service apps
- `pgdbm:dual-mode-library` - PyPI packages
- `pgdbm:standalone-service` - Simple services

**For complete API:**
- `pgdbm:core-api-reference` - ALL AsyncDatabaseManager methods
- `pgdbm:migrations-api-reference` - ALL AsyncMigrationManager methods

**For testing and quality:**
- `pgdbm:testing-database-code` - Test fixtures
- `pgdbm:common-mistakes` - Anti-patterns
