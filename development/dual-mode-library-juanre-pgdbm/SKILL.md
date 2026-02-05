---
name: dual-mode-library
description: Use when building reusable PyPI package with pgdbm - provides complete pattern for libraries that work standalone or embedded without needing examples
---

# Dual-Mode Library Pattern: Complete Implementation

## Overview

**Core Principle:** Accept connection_string OR db_manager, always run own migrations, clean up conditionally.

This pattern makes your library work both standalone (creates own pool) AND embedded (uses shared pool) without code changes.

## When to Use This

From `pgdbm:choosing-pattern` skill - use when:
- Publishing to PyPI
- Building internal shared library
- Code will be used by other developers
- Library might be used alongside other pgdbm libraries

## Complete Implementation Template

```python
from typing import Optional
from pathlib import Path
from pgdbm import AsyncDatabaseManager, DatabaseConfig, AsyncMigrationManager

class MyLibrary:
    """Library supporting dual-mode operation.

    Standalone: MyLibrary(connection_string='postgresql://...')
    Shared pool: MyLibrary(db_manager=shared_db)
    """

    def __init__(
        self,
        connection_string: Optional[str] = None,
        db_manager: Optional[AsyncDatabaseManager] = None,
        schema: Optional[str] = None,
    ):
        # Validation
        if not connection_string and not db_manager:
            raise ValueError("Either connection_string or db_manager required")

        # Track ownership
        self._external_db = db_manager is not None
        self.db = db_manager
        self._connection_string = connection_string
        self._schema = schema or "mylib"

    async def initialize(self):
        # Create connection only if not provided
        if not self._external_db:
            config = DatabaseConfig(
                connection_string=self._connection_string,
                min_connections=5,
                max_connections=20,
            )
            self.db = AsyncDatabaseManager(config)
            await self.db.connect()

        # ALWAYS run migrations (both modes!)
        migrations_path = Path(__file__).parent / "migrations"
        migrations = AsyncMigrationManager(
            self.db,
            migrations_path=str(migrations_path),
            module_name=f"mylib_{self._schema}",  # Unique per schema
        )
        await migrations.apply_pending_migrations()

    async def close(self):
        # Only close if we created the connection
        if self.db and not self._external_db:
            await self.db.disconnect()

    # Library methods (always use {{tables.}})
    async def create_record(self, data: dict):
        return await self.db.fetch_one(
            "INSERT INTO {{tables.records}} (data) VALUES ($1) RETURNING *",
            data
        )
```

## Critical Implementation Details

### 1. Parameter Validation

```python
def __init__(self, connection_string=None, db_manager=None):
    if not connection_string and not db_manager:
        raise ValueError(
            "Either connection_string or db_manager required.\n\n"
            "Standalone: MyLib(connection_string='postgresql://...')\n"
            "Shared pool: MyLib(db_manager=shared_db)"
        )
```

**Why:** Catch misconfiguration immediately with helpful error message.

### 2. Track Ownership

```python
self._external_db = db_manager is not None
```

**Why:** Determines who owns lifecycle. If `True`, caller owns pool. If `False`, we own it.

### 3. Conditional Connection Creation

```python
async def initialize(self):
    if not self._external_db:
        # We need to create connection
        self.db = AsyncDatabaseManager(config)
        await self.db.connect()

    # ALWAYS run migrations (external or not)
    await self._apply_migrations()
```

**Why:** Don't create pool if one was provided. But ALWAYS run migrations.

### 4. Unique Module Name Per Schema

```python
module_name = f"mylib_{self._schema}"  # "mylib_schema1", "mylib_schema2"
```

**Why:** Same library can be used multiple times with different schemas. Each needs unique migration tracking.

### 5. Conditional Cleanup

```python
async def close(self):
    if self.db and not self._external_db:
        await self.db.disconnect()
```

**Why:** Only close connections we created. External connections belong to caller.

## Usage Patterns

### Standalone Mode

```python
from mylib import MyLibrary

# User provides connection string
lib = MyLibrary(connection_string="postgresql://localhost/mydb")
await lib.initialize()

# Use library
result = await lib.create_record({"key": "value"})

# Clean up
await lib.close()
```

### Shared Pool Mode

```python
from pgdbm import AsyncDatabaseManager, DatabaseConfig
from mylib import MyLibrary

# App creates shared pool
config = DatabaseConfig(connection_string="postgresql://localhost/app")
shared_pool = await AsyncDatabaseManager.create_shared_pool(config)

# Create schema-isolated manager for library
lib_db = AsyncDatabaseManager(pool=shared_pool, schema="mylib")

# Pass to library
lib = MyLibrary(db_manager=lib_db)
await lib.initialize()

# Use library
result = await lib.create_record({"key": "value"})

# Don't call lib.close() - app owns the pool
await shared_pool.close()
```

### Multi-Library Composition

```python
# Parent app using multiple dual-mode libraries
from mylib import MyLibrary
from otherlib import OtherLibrary

# One shared pool
pool = await AsyncDatabaseManager.create_shared_pool(config)

# Each library gets own schema
mylib_db = AsyncDatabaseManager(pool=pool, schema="mylib")
otherlib_db = AsyncDatabaseManager(pool=pool, schema="otherlib")

# Initialize both
mylib = MyLibrary(db_manager=mylib_db)
otherlib = OtherLibrary(db_manager=otherlib_db)

await mylib.initialize()  # Runs mylib migrations in mylib schema
await otherlib.initialize()  # Runs otherlib migrations in otherlib schema

# Libraries can reference each other's data if needed
# (but each owns its own tables in separate schemas)
```

## Migration Files

Always use `{{tables.}}` syntax:

```sql
-- mylib/migrations/001_initial.sql
CREATE TABLE IF NOT EXISTS {{tables.records}} (
    id SERIAL PRIMARY KEY,
    data JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS records_created
    ON {{tables.records}} (created_at);
```

**Why templates matter:**
- Standalone mode: `{{tables.records}}` → `records`
- Shared pool with schema: `{{tables.records}}` → `"mylib".records`

Same migration file works in both modes.

## Common Mistakes

### ❌ Not Supporting db_manager Parameter

```python
# WRONG: Forces standalone mode only
def __init__(self, connection_string: str):
    self.db = AsyncDatabaseManager(DatabaseConfig(connection_string=connection_string))
```

**Fix:** Accept both `connection_string` and `db_manager`.

### ❌ Skipping Migrations in Shared Mode

```python
# WRONG: Assumes migrations already run
async def initialize(self):
    if self._external_db:
        return  # Skip migrations!
```

**Fix:** ALWAYS run migrations. Your module owns its schema/tables.

### ❌ Always Calling close()

```python
# WRONG: Closes external pool
await lib.close()  # Disconnects pool owned by parent app!
```

**Fix:** Check `_external_db` flag in `close()` method.

### ❌ Hardcoding Schema/Table Names

```python
# WRONG: Only works in one schema
await db.execute("INSERT INTO mylib.records ...")
```

**Fix:** Use `{{tables.records}}` - works in any schema.

### ❌ Not Including Schema in module_name

```python
# WRONG: Conflicts if library used twice
module_name = "mylib"
```

**Fix:** Include schema: `module_name = f"mylib_{schema}"`.

## FastAPI Integration

For libraries providing FastAPI apps:

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

def create_app(
    db_manager: Optional[AsyncDatabaseManager] = None,
    connection_string: Optional[str] = None,
) -> FastAPI:
    """Create app supporting both modes."""

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Initialize library
        lib = MyLibrary(
            connection_string=connection_string,
            db_manager=db_manager,
        )
        await lib.initialize()
        app.state.lib = lib

        yield

        # Clean up only if we own it
        await lib.close()

    return FastAPI(lifespan=lifespan)

# Standalone usage
app = create_app(connection_string="postgresql://...")

# Parent app usage
parent = FastAPI()
lib_app = create_app(db_manager=shared_db)
parent.mount("/lib", lib_app)
```

## Testing Both Modes

```python
# tests/conftest.py
import pytest
from mylib import MyLibrary

@pytest.fixture(params=["standalone", "shared"])
async def lib(request, test_db_factory):
    """Test both modes."""
    mode = request.param

    if mode == "standalone":
        lib = MyLibrary(connection_string="postgresql://localhost/test")
    else:
        db = await test_db_factory.create_db(schema="mylib")
        lib = MyLibrary(db_manager=db)

    await lib.initialize()
    yield lib
    await lib.close()

# tests/test_lib.py
async def test_create_record(lib):
    # This test runs in BOTH modes
    result = await lib.create_record({"key": "value"})
    assert result["id"] is not None
```

## Package Structure for PyPI

```
mylib/
├── pyproject.toml
├── README.md
├── src/
│   └── mylib/
│       ├── __init__.py           # Export MyLibrary
│       ├── core.py              # Implementation
│       └── migrations/
│           ├── 001_initial.sql
│           └── 002_indexes.sql
└── tests/
    ├── conftest.py
    └── test_mylib.py
```

```toml
# pyproject.toml
[project]
name = "mylib"
dependencies = ["pgdbm>=0.2.0"]

[project.optional-dependencies]
dev = ["pytest>=7.0", "pytest-asyncio>=0.21"]
```

## Why This Pattern Exists

**Problem:** Users have different deployment contexts:
- Solo developer: wants simple `connection_string` setup
- Enterprise app: has shared pool, needs schema isolation
- Microservices: each service creates own pool
- Multi-tenant: needs dynamic schema creation

**Solution:** Dual-mode pattern handles all cases with same code.

**Benefits:**
- Library works in any context
- No forced architecture decisions
- Efficient resource sharing when possible
- Complete isolation when needed

## Checklist

Before publishing dual-mode library:

- [ ] Accept both `connection_string` and `db_manager` parameters
- [ ] Validate at least one is provided
- [ ] Track ownership with `_external_db` flag
- [ ] Create connection only if not provided
- [ ] ALWAYS run migrations in both modes
- [ ] Use `{{tables.}}` in all SQL
- [ ] Use unique `module_name` including schema
- [ ] Close connection only if you created it
- [ ] Test both modes with parametrized fixtures
- [ ] Document both usage modes in README

## Complete Minimal Example

```python
from typing import Optional
from pathlib import Path
from pgdbm import AsyncDatabaseManager, DatabaseConfig, AsyncMigrationManager

class MyLibrary:
    def __init__(self, connection_string=None, db_manager=None):
        if not connection_string and not db_manager:
            raise ValueError("Either connection_string or db_manager required")
        self._external_db = db_manager is not None
        self.db = db_manager
        self._connection_string = connection_string

    async def initialize(self):
        if not self._external_db:
            config = DatabaseConfig(connection_string=self._connection_string)
            self.db = AsyncDatabaseManager(config)
            await self.db.connect()

        migrations = AsyncMigrationManager(
            self.db,
            str(Path(__file__).parent / "migrations"),
            module_name="mylib"
        )
        await migrations.apply_pending_migrations()

    async def close(self):
        if self.db and not self._external_db:
            await self.db.disconnect()
```

That's the complete dual-mode pattern.

## Related Skills

- For pattern selection: `pgdbm:choosing-pattern`
- For mental model: `pgdbm:using-pgdbm`
- For shared pool usage: `pgdbm:shared-pool-pattern`
- For testing: `pgdbm:testing-database-code`
