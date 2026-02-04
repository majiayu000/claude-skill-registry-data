---
name: shared-pool-pattern
description: Use when implementing shared connection pool for multiple services in same application - provides complete setup steps for FastAPI/multi-service apps without needing examples
---

# Shared Pool Pattern: Complete Implementation

## Overview

**Core Principle:** ONE pool created at startup, multiple schema-isolated managers, each runs own migrations.

This is the **production-recommended pattern** for applications with multiple services/modules sharing a database.

## When to Use This

From `pgdbm:choosing-pattern` skill - use when:
- Multiple services in same Python process (FastAPI with routers)
- Need connection efficiency (avoid multiple pools)
- Want schema isolation between services
- Building monolith with logical service separation

## Critical Setup Steps

### Step 1: Create Shared Pool (ONCE at startup)

```python
from pgdbm import AsyncDatabaseManager, DatabaseConfig

# In your FastAPI lifespan or app startup
config = DatabaseConfig(
    connection_string="postgresql://localhost/myapp",
    min_connections=5,    # Start small, tune based on metrics
    max_connections=20,   # Shared across ALL services - keep under DB max_connections
)

shared_pool = await AsyncDatabaseManager.create_shared_pool(config)
```

**CRITICAL:** Only call `create_shared_pool()` once. Store the pool somewhere accessible (app state, global, etc).

### Step 2: Create Schema-Isolated Managers

```python
# Each service gets own manager with dedicated schema
users_db = AsyncDatabaseManager(pool=shared_pool, schema="users")
orders_db = AsyncDatabaseManager(pool=shared_pool, schema="orders")
payments_db = AsyncDatabaseManager(pool=shared_pool, schema="payments")
```

**CRITICAL:**
- Never call `.connect()` on these managers (pool already exists)
- Each manager's schema is permanent (don't try to change it)

### Step 3: Run Migrations for Each Service

```python
from pgdbm import AsyncMigrationManager

for db, path, module in [
    (users_db, "migrations/users", "users"),
    (orders_db, "migrations/orders", "orders"),
    (payments_db, "migrations/payments", "payments"),
]:
    migrations = AsyncMigrationManager(
        db,
        migrations_path=path,
        module_name=module  # MUST be unique per service
    )
    await migrations.apply_pending_migrations()
```

**CRITICAL:** Each service uses unique `module_name` to prevent migration conflicts.

## FastAPI Integration (Complete Example)

### Pattern: Lifespan Handler

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from pgdbm import AsyncDatabaseManager, DatabaseConfig, AsyncMigrationManager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create shared pool
    config = DatabaseConfig(connection_string="postgresql://localhost/myapp")
    shared_pool = await AsyncDatabaseManager.create_shared_pool(config)

    # Create schema-isolated managers
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

    # Shutdown: Close pool
    await shared_pool.close()

app = FastAPI(lifespan=lifespan)

# Use in routes
@app.post("/users")
async def create_user(email: str, request: Request):
    db = request.app.state.dbs['users']
    user_id = await db.fetch_value(
        "INSERT INTO {{tables.users}} (email) VALUES ($1) RETURNING id",
        email
    )
    return {"id": user_id}
```

### Pattern: Dependency Injection (Cleaner)

```python
# dependencies.py
from typing import Annotated
from fastapi import Depends, Request

async def get_users_db(request: Request):
    return request.app.state.dbs['users']

async def get_orders_db(request: Request):
    return request.app.state.dbs['orders']

UsersDB = Annotated[AsyncDatabaseManager, Depends(get_users_db)]
OrdersDB = Annotated[AsyncDatabaseManager, Depends(get_orders_db)]

# routes.py
@app.post("/users")
async def create_user(email: str, db: UsersDB):
    user_id = await db.fetch_value(
        "INSERT INTO {{tables.users}} (email) VALUES ($1) RETURNING id",
        email
    )
    return {"id": user_id}
```

## Migration File Structure

```
migrations/
├── users/
│   ├── 001_create_users.sql
│   └── 002_add_profiles.sql
├── orders/
│   ├── 001_create_orders.sql
│   └── 002_add_items.sql
└── payments/
    └── 001_create_payments.sql
```

Each migration MUST use `{{tables.}}` syntax:

```sql
-- migrations/users/001_create_users.sql
CREATE TABLE IF NOT EXISTS {{tables.users}} (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS users_email
    ON {{tables.users}} (email);
```

This automatically becomes `"users".users` table in users schema.

## Pool Sizing Guide

Start small and tune based on metrics:

```python
# Start with conservative defaults
config = DatabaseConfig(
    connection_string="...",
    min_connections=5,    # Floor - connections opened eagerly
    max_connections=20,   # Cap - tune based on DB max_connections and traffic
)

# For high-traffic apps, tune upward based on:
# - Your DB's max_connections (typically 100-400)
# - Observed pool exhaustion in metrics
# - Number of concurrent requests
```

**Key insight:** Shared pool uses LESS connections than separate pools because services don't peak simultaneously. The pool dynamically allocates connections based on actual demand.

**Important:** Keep `max_connections` well under your database's `max_connections` setting to leave room for admin connections and other clients.

## Common Mistakes

### ❌ Creating Multiple Pools

```python
# WRONG: Each service creates own pool
users_db = AsyncDatabaseManager(DatabaseConfig(...))  # Pool 1
orders_db = AsyncDatabaseManager(DatabaseConfig(...)) # Pool 2
```

You'll see warning: `"⚠️ Creating another connection pool to..."`

**Fix:** Use `create_shared_pool()` once, pass to all managers.

### ❌ Calling connect() on Pool-Based Managers

```python
# WRONG
users_db = AsyncDatabaseManager(pool=shared_pool, schema="users")
await users_db.connect()  # ERROR: "Cannot call connect() when using external pool"
```

**Fix:** Don't call `.connect()` - the pool already exists.

### ❌ Forgetting module_name

```python
# WRONG: All services use default module name
migrations = AsyncMigrationManager(users_db, "migrations/users")
migrations = AsyncMigrationManager(orders_db, "migrations/orders")
# Migration conflicts!
```

**Fix:** Always specify unique `module_name`:
```python
AsyncMigrationManager(users_db, "migrations/users", module_name="users")
AsyncMigrationManager(orders_db, "migrations/orders", module_name="orders")
```

### ❌ Not Using {{tables.}} Syntax

```python
# WRONG: Hardcoded table name
await db.execute("INSERT INTO users (email) VALUES ($1)", email)
# Goes to wrong schema or fails!
```

**Fix:** Always use templates:
```python
await db.execute("INSERT INTO {{tables.users}} (email) VALUES ($1)", email)
```

### ❌ Trying to Change Schema at Runtime

```python
# WRONG: Schema is permanent on manager
db.schema = "different_schema"  # Don't do this!
```

**Fix:** Create separate manager for each schema:
```python
schema1_db = AsyncDatabaseManager(pool=shared_pool, schema="schema1")
schema2_db = AsyncDatabaseManager(pool=shared_pool, schema="schema2")
```

## Singleton Pattern (Alternative)

For more complex apps, create singleton manager:

```python
# shared/database.py
import asyncio
from typing import Optional
import asyncpg
from pgdbm import AsyncDatabaseManager, DatabaseConfig

class SharedDatabaseManager:
    _instance: Optional["SharedDatabaseManager"] = None
    _pool: Optional[asyncpg.Pool] = None
    _initialized: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def initialize(self, database_url: str):
        if self._initialized:
            return

        config = DatabaseConfig(connection_string=database_url)
        self._pool = await AsyncDatabaseManager.create_shared_pool(config)
        self._initialized = True

    def get_pool(self) -> asyncpg.Pool:
        if not self._initialized:
            raise RuntimeError("Not initialized")
        return self._pool

    async def close(self):
        if self._pool:
            await self._pool.close()

# Usage
db_mgr = SharedDatabaseManager()
await db_mgr.initialize("postgresql://...")
users_db = AsyncDatabaseManager(pool=db_mgr.get_pool(), schema="users")
```

## Multi-Tenant Extension

For multi-tenant SaaS, create managers dynamically:

```python
# tenant_manager.py
class TenantManager:
    def __init__(self, shared_pool):
        self.shared_pool = shared_pool
        self.tenant_dbs = {}

    async def get_tenant_db(self, tenant_id: str):
        if tenant_id not in self.tenant_dbs:
            schema = f"tenant_{tenant_id}"

            # Create schema
            admin_db = AsyncDatabaseManager(pool=self.shared_pool)
            await admin_db.execute(f'CREATE SCHEMA IF NOT EXISTS "{schema}"')

            # Create tenant manager
            tenant_db = AsyncDatabaseManager(pool=self.shared_pool, schema=schema)

            # Run migrations
            migrations = AsyncMigrationManager(
                tenant_db,
                migrations_path="tenant_migrations",
                module_name=f"tenant_{tenant_id}"
            )
            await migrations.apply_pending_migrations()

            self.tenant_dbs[tenant_id] = tenant_db

        return self.tenant_dbs[tenant_id]

# Usage
tenant_mgr = TenantManager(shared_pool)
tenant_db = await tenant_mgr.get_tenant_db("customer_123")
```

## Monitoring Pool Usage

```python
# Check pool health
stats = await shared_pool.get_pool_stats()

usage = stats['used_size'] / stats['size']
if usage > 0.8:
    logger.warning(f"High pool usage: {usage:.1%}")

# Metrics
print(f"Total connections: {stats['size']}")
print(f"Active: {stats['used_size']}")
print(f"Idle: {stats['free_size']}")
```

## Quick Checklist

Before deploying shared pool pattern:

- [ ] Create pool with `create_shared_pool()` ONCE at startup
- [ ] Each service gets `AsyncDatabaseManager(pool=shared_pool, schema="service_name")`
- [ ] Never call `.connect()` on pool-based managers
- [ ] Each service runs migrations with unique `module_name`
- [ ] All SQL uses `{{tables.}}` syntax
- [ ] Pool closed in shutdown/finally block
- [ ] Pool size calculated based on total service needs

## Complete Minimal Example

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pgdbm import AsyncDatabaseManager, DatabaseConfig, AsyncMigrationManager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create ONE pool
    config = DatabaseConfig(connection_string="postgresql://localhost/myapp")
    pool = await AsyncDatabaseManager.create_shared_pool(config)

    # Schema-isolated managers
    app.state.users_db = AsyncDatabaseManager(pool=pool, schema="users")
    app.state.orders_db = AsyncDatabaseManager(pool=pool, schema="orders")

    # Migrations
    for db, path, name in [
        (app.state.users_db, "migrations/users", "users"),
        (app.state.orders_db, "migrations/orders", "orders"),
    ]:
        await AsyncMigrationManager(db, path, name).apply_pending_migrations()

    yield
    await pool.close()

app = FastAPI(lifespan=lifespan)
```

That's it. This is the complete shared pool pattern.

## Related Skills

- For pattern selection: `pgdbm:choosing-pattern`
- For mental model: `pgdbm:using-pgdbm`
- For complete API: `pgdbm:core-api-reference`
- For testing: `pgdbm:testing-database-code`
