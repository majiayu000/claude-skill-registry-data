---
name: choosing-pattern
description: Use when deciding which pgdbm pattern to use (standalone, dual-mode library, or shared pool) - provides decision tree based on deployment context without requiring doc exploration
---

# Choosing the Right pgdbm Pattern

## Overview

**Core Principle:** Choose pattern based on deployment context and reusability needs.

pgdbm supports three main patterns. This skill helps you choose the right one in <30 seconds without reading multiple docs.

## Quick Decision Tree

```
What are you building?
│
├─ Reusable library/package for PyPI?
│  └─ → DUAL-MODE LIBRARY pattern
│     • Accept connection_string OR db_manager
│     • Works standalone AND embedded
│
├─ Single application with multiple services/modules?
│  └─ → SHARED POOL pattern
│     • ONE pool, many schema-isolated managers
│     • Most efficient for production
│
└─ Simple standalone service/microservice?
   └─ → STANDALONE pattern
      • AsyncDatabaseManager(DatabaseConfig(...))
      • Simplest setup
```

## Pattern Selection Table

| If you have... | Use this pattern | Key indicator |
|----------------|------------------|---------------|
| Library published to PyPI | Dual-Mode | Code needs to work in someone else's app |
| FastAPI monolith with routers | Shared Pool | Multiple services, same process |
| Multiple services, same app | Shared Pool | Need connection efficiency |
| Background worker (separate process) | Standalone | Different OS process |
| Simple microservice | Standalone | One service, own database |
| Multi-tenant SaaS | Shared Pool | Many tenants, schema isolation |

## Detailed Decision Criteria

### Use DUAL-MODE LIBRARY When:

**Triggers:**
- You're publishing to PyPI
- You're building internal shared library
- Code will be used by other developers
- Library might be used alongside other pgdbm libraries

**Key characteristics:**
- Unknown deployment context
- Must work standalone OR embedded
- Always runs own migrations
- Schema-agnostic via `{{tables.}}`

**Red flags you need this:**
- [ ] You're writing `import mylib` in your README
- [ ] Someone else's app will import your code
- [ ] You don't control the database configuration

**Example minimal setup:**
```python
class MyLibrary:
    def __init__(
        self,
        connection_string: Optional[str] = None,
        db_manager: Optional[AsyncDatabaseManager] = None,
    ):
        if not connection_string and not db_manager:
            raise ValueError("Provide one or the other")
        self._external_db = db_manager is not None
        self.db = db_manager
        self._connection_string = connection_string

    async def initialize(self):
        if not self._external_db:
            config = DatabaseConfig(connection_string=self._connection_string)
            self.db = AsyncDatabaseManager(config)
            await self.db.connect()

        # ALWAYS run migrations
        migrations = AsyncMigrationManager(
            self.db, "migrations", module_name="mylib"
        )
        await migrations.apply_pending_migrations()
```

**For complete implementation:** See `pgdbm:dual-mode-library` skill

### Use SHARED POOL When:

**Triggers:**
- Multiple services in same Python process
- FastAPI app with multiple routers
- Monolith with logical service separation
- Multi-tenant SaaS application

**Key characteristics:**
- Services share database connection pool
- Each service gets own schema
- Connection efficiency critical
- All services in same application

**Red flags you need this:**
- [ ] You're creating multiple `AsyncDatabaseManager(DatabaseConfig(...))` in same app
- [ ] You're hitting PostgreSQL connection limits
- [ ] You have >2 routers/services needing database

**Example minimal setup:**
```python
# In lifespan
config = DatabaseConfig(connection_string="postgresql://...")
shared_pool = await AsyncDatabaseManager.create_shared_pool(config)

# Each service gets schema-isolated manager
users_db = AsyncDatabaseManager(pool=shared_pool, schema="users")
orders_db = AsyncDatabaseManager(pool=shared_pool, schema="orders")

# Run migrations for each
for db, path, name in [(users_db, "migrations/users", "users"), ...]:
    migrations = AsyncMigrationManager(db, path, name)
    await migrations.apply_pending_migrations()
```

**For complete implementation:** See `pgdbm:shared-pool-pattern` skill

### Use STANDALONE When:

**Triggers:**
- Single service, dedicated database
- Background worker (separate process)
- Simple microservice
- Development/testing
- Service can't share connections

**Key characteristics:**
- Creates own connection pool
- Controls full database lifecycle
- Simplest pattern
- Most straightforward

**Red flags you need this:**
- [ ] Separate OS process (can't share pool anyway)
- [ ] Only one logical service
- [ ] Development environment
- [ ] Learning pgdbm

**Example minimal setup:**
```python
config = DatabaseConfig(connection_string="postgresql://...")
db = AsyncDatabaseManager(config)
await db.connect()

migrations = AsyncMigrationManager(db, "migrations", module_name="myservice")
await migrations.apply_pending_migrations()

# Use db
user_id = await db.fetch_value(
    "INSERT INTO {{tables.users}} (email) VALUES ($1) RETURNING id",
    email
)

await db.disconnect()
```

**For complete implementation:** See `pgdbm:standalone-service` skill

## Wrong Pattern Red Flags

### 🚫 You Chose WRONG Pattern If:

**Using Standalone but should use Shared Pool:**
- [ ] You create multiple `AsyncDatabaseManager(DatabaseConfig(...))` to same database
- [ ] You see warning: "Creating another connection pool to..."
- [ ] You're hitting PostgreSQL `max_connections` limit
- [ ] All services run in same Python process

**Using Shared Pool but should use Dual-Mode:**
- [ ] Your code will be imported by other apps
- [ ] You're publishing to PyPI
- [ ] Users need to provide their own database

**Using Dual-Mode but should use Standalone:**
- [ ] You control entire deployment
- [ ] Code never used as library
- [ ] Adding unnecessary complexity

## Common Ambiguous Cases

### "Background worker, same database as main app"

**Question to ask:** Same process or different process?

- **Same process** (threads/asyncio tasks): Use Shared Pool
- **Different process** (separate Python process): Use Standalone
  - Each process creates own pool (can't share across processes)
  - Use schema isolation to prevent table conflicts
  - Worker uses schema="worker", main uses schema="main"

### "Multiple microservices, containerized"

**Answer:** Each container = Standalone pattern

- Containers are separate processes
- Can't share pools across containers
- Use schema isolation if sharing same database
- Each service: `AsyncDatabaseManager(DatabaseConfig(...))`

### "Library used internally, not published"

**Answer:** Still use Dual-Mode if used by multiple apps

- "Internal" doesn't mean "standalone"
- If imported by different projects, use Dual-Mode
- If only used in one app, can use Shared Pool

## Pattern Comparison

| Aspect | Standalone | Dual-Mode | Shared Pool |
|--------|-----------|-----------|-------------|
| **Complexity** | Low | Medium | Medium |
| **Flexibility** | Low | High | Medium |
| **Connection Efficiency** | Low | Varies | High |
| **Use Case** | Simple services | Reusable libraries | Multi-service apps |
| **Pool Creation** | Creates own | Conditional | Uses provided |
| **Migration Management** | Owns | Always runs own | Each service runs own |
| **Best For** | Microservices, workers | PyPI packages | Monoliths, multi-tenant |

## Decision Process Example

**Scenario:** "I'm building a FastAPI app with user authentication, blog posts, and comments"

**Decision process:**
1. Multiple services? **Yes** (auth, blog, comments)
2. Same Python process? **Yes** (all in FastAPI app)
3. Will be reused as library? **No** (application code)

**Answer:** **Shared Pool Pattern**

**Why:**
- Multiple services = need isolation
- Same process = can share pool
- Not reusable = don't need dual-mode flexibility

## Quick Self-Check

Before implementing, ask:

1. **Who creates the database manager?**
   - Me = Standalone or Shared Pool
   - Could be me or someone else = Dual-Mode

2. **How many services need database access?**
   - 1 = Standalone (probably)
   - 2+ in same process = Shared Pool
   - 2+ in different processes = Standalone each

3. **Will my code be imported by other projects?**
   - Yes = Dual-Mode
   - No = Standalone or Shared Pool

## Next Steps

Once you've chosen:

- **Dual-Mode**: See `pgdbm:dual-mode-library` for full implementation
- **Shared Pool**: See `pgdbm:shared-pool-pattern` for full implementation
- **Standalone**: See `pgdbm:standalone-service` for full implementation

All patterns use:
- `{{tables.}}` syntax (mandatory)
- Unique `module_name` in migrations (mandatory)
- Schema isolation for multi-service (recommended)

## The Iron Rule

**Whatever pattern you choose, NEVER:**
- Create multiple pools to same database in same process
- Hardcode schema names in SQL
- Skip `module_name` in AsyncMigrationManager
- Switch `db.schema` at runtime

These violations break pgdbm's core assumptions.
