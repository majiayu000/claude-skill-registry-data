---
name: core-api-reference
description: Use when implementing pgdbm database operations - provides complete AsyncDatabaseManager and DatabaseConfig API with all methods and parameters
---

# pgdbm Core API Reference

## Overview

**Complete API reference for AsyncDatabaseManager, DatabaseConfig, and TransactionManager.**

All signatures, parameters, return types, and usage examples. No documentation lookup needed.

## AsyncDatabaseManager

### Initialization

```python
# Pattern 1: Create own pool
AsyncDatabaseManager(config: DatabaseConfig)

# Pattern 2: Use external pool
AsyncDatabaseManager(
    pool: asyncpg.Pool,
    schema: Optional[str] = None
)
```

**Rules:**
- Cannot provide both `config` and `pool`
- `schema` only valid with external pool
- Must call `connect()` if using config
- Never call `connect()` if using external pool

### Connection Lifecycle

```python
# Create shared pool (class method)
pool = await AsyncDatabaseManager.create_shared_pool(config: DatabaseConfig) -> asyncpg.Pool

# Connect (only for config-based init)
await db.connect() -> None
# Raises PoolError if using external pool

# Disconnect (only for config-based init)
await db.disconnect() -> None
# Does nothing if using external pool
```

### Query Methods

All methods automatically apply `{{tables.}}` template substitution.

```python
# Execute without return
await db.execute(
    query: str,
    *args: Any,
    timeout: Optional[float] = None
) -> str
# Returns: asyncpg status string like "INSERT 0 1"

# Execute and return generated ID
await db.execute_and_return_id(
    query: str,
    *args: Any
) -> Any
# Automatically appends RETURNING id if not present
# Returns: The id value

# Fetch single value
await db.fetch_value(
    query: str,
    *args: Any,
    column: int = 0,
    timeout: Optional[float] = None
) -> Any
# Returns: Single value from result (or None)

# Fetch single row
await db.fetch_one(
    query: str,
    *args: Any,
    timeout: Optional[float] = None
) -> Optional[dict[str, Any]]
# Returns: Dictionary of column->value (or None if no results)

# Fetch all rows
await db.fetch_all(
    query: str,
    *args: Any,
    timeout: Optional[float] = None
) -> list[dict[str, Any]]
# Returns: List of dictionaries

# Batch execute (multiple parameter sets)
await db.executemany(
    query: str,
    args_list: list[tuple]
) -> None
# Executes same query with different parameter sets
# More efficient than looping execute()
```

**Examples:**

```python
# execute_and_return_id - Common for inserts
user_id = await db.execute_and_return_id(
    "INSERT INTO {{tables.users}} (email, name) VALUES ($1, $2)",
    "alice@example.com",
    "Alice"
)
# Automatically becomes: ... RETURNING id

# fetch_value with column parameter
email = await db.fetch_value(
    "SELECT email, name FROM {{tables.users}} WHERE id = $1",
    user_id,
    column=0  # Get first column (email)
)

# executemany for batch inserts
users = [
    ("alice@example.com", "Alice"),
    ("bob@example.com", "Bob"),
    ("charlie@example.com", "Charlie"),
]
await db.executemany(
    "INSERT INTO {{tables.users}} (email, name) VALUES ($1, $2)",
    users
)
```

### Bulk Operations

```python
# Copy records (MUCH faster than INSERT for bulk data)
await db.copy_records_to_table(
    table_name: str,
    records: list[tuple],
    columns: Optional[list[str]] = None
) -> int
# Uses PostgreSQL COPY command
# Returns: Number of records copied

# Example
records = [
    ("alice@example.com", "Alice"),
    ("bob@example.com", "Bob"),
]
count = await db.copy_records_to_table(
    "users",  # Don't use {{tables.}} here - just table name
    records=records,
    columns=["email", "name"]
)
# Returns: 2
```

### Pydantic Integration

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    email: str
    name: str

# Fetch single row as model
user = await db.fetch_as_model(
    User,
    query: str,
    *args: Any,
    timeout: Optional[float] = None
) -> Optional[User]

# Fetch all rows as models
users = await db.fetch_all_as_model(
    User,
    query: str,
    *args: Any,
    timeout: Optional[float] = None
) -> list[User]

# Example
user = await db.fetch_as_model(
    User,
    "SELECT * FROM {{tables.users}} WHERE id = $1",
    user_id
)
# Returns: User(id=1, email="alice@example.com", name="Alice")
```

### Schema Operations

```python
# Check if table exists
exists = await db.table_exists(table_name: str) -> bool

# Examples
exists = await db.table_exists("users")  # Check in current schema
exists = await db.table_exists("other_schema.users")  # Check in specific schema
```

### Transaction Management

```python
# Create transaction context
async with db.transaction() as tx:
    # tx has same API as db (execute, fetch_one, fetch_all, etc.)
    user_id = await tx.fetch_value(
        "INSERT INTO {{tables.users}} (email) VALUES ($1) RETURNING id",
        email
    )
    await tx.execute(
        "INSERT INTO {{tables.profiles}} (user_id) VALUES ($1)",
        user_id
    )
    # Auto-commits on success, rolls back on exception

# Nested transactions (savepoints)
async with db.transaction() as tx:
    await tx.execute("INSERT INTO {{tables.users}} ...")

    async with tx.transaction() as nested:
        await nested.execute("UPDATE {{tables.users}} ...")
        # Nested transaction uses SAVEPOINT
```

### Monitoring and Performance

```python
# Get pool statistics
stats = await db.get_pool_stats() -> dict[str, Any]
# Returns: {
#     "status": "connected",
#     "min_size": 10,
#     "max_size": 50,
#     "size": 15,              # Current total connections
#     "free_size": 10,         # Idle connections
#     "used_size": 5,          # Active connections
#     "database": "myapp",
#     "schema": "myschema",
#     "pid": 12345,
#     "version": "PostgreSQL 15.3"
# }

# Add prepared statement (performance optimization)
db.add_prepared_statement(
    name: str,
    query: str
) -> None
# Prepared statements created on all connections in pool
# Improves performance for frequently-used queries
```

### Advanced Operations

```python
# Acquire connection directly (advanced)
async with db.acquire() as conn:
    # conn is raw asyncpg connection
    # Use for operations not covered by AsyncDatabaseManager
    await conn.execute("...")
```

## DatabaseConfig

### Complete Parameter Reference

```python
from pgdbm import DatabaseConfig

config = DatabaseConfig(
    # Connection (either connection_string OR individual params)
    connection_string: Optional[str] = None,  # e.g., "postgresql://user:pass@host/db"
    host: str = "localhost",
    port: int = 5432,
    database: str = "postgres",
    user: str = "postgres",
    password: Optional[str] = None,
    schema: Optional[str] = None,  # Alias: schema_name

    # Connection Pool
    min_connections: int = 10,
    max_connections: int = 20,
    max_queries: int = 50000,  # Queries per connection before recycling
    max_inactive_connection_lifetime: float = 300.0,  # Seconds
    command_timeout: float = 60.0,  # Default query timeout (seconds)

    # Connection Initialization
    server_settings: Optional[dict[str, str]] = None,  # PostgreSQL settings
    init_commands: Optional[list[str]] = None,  # Run on each connection

    # TLS/SSL Configuration
    ssl_enabled: bool = False,
    ssl_mode: Optional[str] = None,  # 'require', 'verify-ca', 'verify-full'
    ssl_ca_file: Optional[str] = None,  # Path to CA certificate
    ssl_cert_file: Optional[str] = None,  # Path to client certificate
    ssl_key_file: Optional[str] = None,  # Path to client key
    ssl_key_password: Optional[str] = None,  # Key password if encrypted

    # Server-Side Timeouts (milliseconds, None to disable)
    statement_timeout_ms: Optional[int] = 60000,  # Abort long queries
    idle_in_transaction_session_timeout_ms: Optional[int] = 60000,  # Abort idle transactions
    lock_timeout_ms: Optional[int] = 5000,  # Abort lock waits

    # Retry Configuration
    retry_attempts: int = 3,
    retry_delay: float = 1.0,  # Initial delay (seconds)
    retry_backoff: float = 2.0,  # Exponential backoff multiplier
    retry_max_delay: float = 30.0,  # Maximum delay (seconds)
)
```

### Common Configurations

**Development:**
```python
config = DatabaseConfig(
    connection_string="postgresql://localhost/myapp_dev",
    min_connections=2,
    max_connections=10,
)
```

**Production with TLS:**
```python
config = DatabaseConfig(
    connection_string="postgresql://db.example.com/myapp",
    min_connections=20,
    max_connections=100,
    ssl_enabled=True,
    ssl_mode="verify-full",
    ssl_ca_file="/etc/ssl/certs/ca.pem",
    statement_timeout_ms=30000,  # 30 second timeout
    lock_timeout_ms=5000,  # 5 second lock timeout
)
```

**Custom initialization:**
```python
config = DatabaseConfig(
    connection_string="postgresql://localhost/myapp",
    init_commands=[
        "SET timezone TO 'UTC'",
        "SET statement_timeout TO '30s'",
    ],
    server_settings={
        "jit": "off",  # Disable JIT compilation
        "application_name": "myapp",
    },
)
```

## TransactionManager

Same API as AsyncDatabaseManager but within transaction context:

```python
async with db.transaction() as tx:
    # All methods available
    await tx.execute(query, *args, timeout=None) -> str
    await tx.executemany(query, args_list) -> None
    await tx.fetch_one(query, *args, timeout=None) -> Optional[dict]
    await tx.fetch_all(query, *args, timeout=None) -> list[dict]
    await tx.fetch_value(query, *args, column=0, timeout=None) -> Any

    # Nested transactions (savepoints)
    async with tx.transaction() as nested_tx:
        ...

    # Access underlying connection
    conn = tx.connection  # Property, not method
```

## Complete Method Summary

### AsyncDatabaseManager - All Methods

| Method | Parameters | Returns | Use Case |
|--------|------------|---------|----------|
| `execute` | query, *args, timeout | str | No results needed |
| `execute_and_return_id` | query, *args | Any | INSERT with auto RETURNING id |
| `executemany` | query, args_list | None | Batch execute same query |
| `fetch_value` | query, *args, column, timeout | Any | Single value |
| `fetch_one` | query, *args, timeout | dict\|None | Single row |
| `fetch_all` | query, *args, timeout | list[dict] | Multiple rows |
| `fetch_as_model` | model, query, *args, timeout | Model\|None | Single row as Pydantic |
| `fetch_all_as_model` | model, query, *args, timeout | list[Model] | Rows as Pydantic |
| `copy_records_to_table` | table, records, columns | int | Bulk COPY (fast) |
| `table_exists` | table_name | bool | Schema checking |
| `transaction` | - | TransactionManager | Transaction context |
| `get_pool_stats` | - | dict | Pool monitoring |
| `add_prepared_statement` | name, query | None | Performance optimization |
| `acquire` | - | Connection | Advanced: raw connection |
| `connect` | - | None | Initialize pool (config-based only) |
| `disconnect` | - | None | Close pool (config-based only) |
| `create_shared_pool` | config | asyncpg.Pool | Class method: create shared pool |

**Compatibility aliases**
- `fetch_val(...)` → `fetch_value(...)`
- `execute_many(...)` → `executemany(...)`

### TransactionManager - All Methods

| Method | Parameters | Returns |
|--------|------------|---------|
| `execute` | query, *args, timeout | str |
| `executemany` | query, args_list | None |
| `fetch_value` | query, *args, column, timeout | Any |
| `fetch_one` | query, *args, timeout | dict\|None |
| `fetch_all` | query, *args, timeout | list[dict] |
| `transaction` | - | TransactionManager (nested) |
| `connection` | - | Connection (property) |

**Note:** TransactionManager does NOT have:
- execute_and_return_id
- copy_records_to_table
- fetch_as_model
- table_exists
- Pool management methods

Use regular fetch_value for IDs within transactions.

## Template Syntax

All query methods support template substitution:

```python
# Available templates
{{tables.tablename}}   # → "schema".tablename (or tablename if no schema)
{{schema}}             # → "schema" (or empty)

# Example
query = "SELECT * FROM {{tables.users}} WHERE created_at > $1"

# With schema="myapp"
# Becomes: SELECT * FROM "myapp".users WHERE created_at > $1

# Without schema
# Becomes: SELECT * FROM users WHERE created_at > $1
```

## Usage Examples

### Basic Queries

```python
# Insert and get ID
user_id = await db.execute_and_return_id(
    "INSERT INTO {{tables.users}} (email, name) VALUES ($1, $2)",
    "alice@example.com",
    "Alice"
)

# Fetch single value
count = await db.fetch_value(
    "SELECT COUNT(*) FROM {{tables.users}}"
)

# Fetch with specific column
email = await db.fetch_value(
    "SELECT email, name FROM {{tables.users}} WHERE id = $1",
    user_id,
    column=0  # Get email (first column)
)

# Fetch one row
user = await db.fetch_one(
    "SELECT * FROM {{tables.users}} WHERE id = $1",
    user_id
)
# user = {"id": 1, "email": "...", "name": "..."}

# Fetch all rows
users = await db.fetch_all(
    "SELECT * FROM {{tables.users}} WHERE is_active = $1",
    True
)
# users = [{"id": 1, ...}, {"id": 2, ...}]

# Execute without results
await db.execute(
    "DELETE FROM {{tables.users}} WHERE id = $1",
    user_id
)

# Check table exists
if await db.table_exists("users"):
    print("Users table exists")
```

### Batch Operations

```python
# executemany - same query, different params
users = [
    ("alice@example.com", "Alice"),
    ("bob@example.com", "Bob"),
    ("charlie@example.com", "Charlie"),
]

await db.executemany(
    "INSERT INTO {{tables.users}} (email, name) VALUES ($1, $2)",
    users
)

# copy_records_to_table - fastest for bulk data
records = [
    ("alice@example.com", "Alice"),
    ("bob@example.com", "Bob"),
    # ... thousands more
]

count = await db.copy_records_to_table(
    "users",  # Just table name (template applied internally)
    records=records,
    columns=["email", "name"]
)
# Much faster than executemany for >1000 rows
```

### Pydantic Models

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    email: str
    name: str
    is_active: bool = True

# Fetch as model
user = await db.fetch_as_model(
    User,
    "SELECT * FROM {{tables.users}} WHERE id = $1",
    user_id
)
# user is User instance (typed)

# Fetch all as models
users = await db.fetch_all_as_model(
    User,
    "SELECT * FROM {{tables.users}} WHERE is_active = $1",
    True
)
# users is list[User] (typed)
```

### Transactions

```python
# Basic transaction
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
    # Commits on success, rolls back on exception

# Nested transaction (savepoint)
async with db.transaction() as tx:
    await tx.execute("INSERT INTO {{tables.users}} ...")

    try:
        async with tx.transaction() as nested:
            await nested.execute("UPDATE {{tables.users}} SET risky_field = $1", value)
            # This can rollback without affecting outer transaction
    except Exception:
        # Nested rolled back, outer transaction continues
        pass
```

### Monitoring

```python
# Get pool statistics
stats = await db.get_pool_stats()

print(f"Total connections: {stats['size']}")
print(f"Active: {stats['used_size']}")
print(f"Idle: {stats['free_size']}")
print(f"Usage: {stats['used_size'] / stats['size']:.1%}")

# Monitor pool health
usage = stats['used_size'] / stats['size']
if usage > 0.8:
    logger.warning(f"High pool usage: {usage:.1%}")
```

### Prepared Statements

```python
# Add frequently-used query as prepared statement
db.add_prepared_statement(
    "get_user_by_email",
    "SELECT * FROM {{tables.users}} WHERE email = $1"
)

# Prepared statements are created on all pool connections
# Improves performance for queries executed repeatedly
```

## DatabaseConfig Complete Reference

### Connection Parameters

```python
# Use connection_string (recommended)
config = DatabaseConfig(
    connection_string="postgresql://user:pass@host:port/database"
)

# OR use individual parameters
config = DatabaseConfig(
    host="localhost",
    port=5432,
    database="myapp",
    user="postgres",
    password="secret",
    schema="myschema",  # Optional schema
)
```

### Pool Configuration

```python
config = DatabaseConfig(
    connection_string="...",

    # Pool sizing
    min_connections=10,      # Minimum idle connections
    max_connections=50,      # Maximum total connections

    # Connection lifecycle
    max_queries=50000,       # Queries before recycling connection
    max_inactive_connection_lifetime=300.0,  # Seconds before closing idle
    command_timeout=60.0,    # Default query timeout (seconds)
)
```

### SSL/TLS Configuration

```python
config = DatabaseConfig(
    connection_string="postgresql://db.example.com/myapp",

    # Enable SSL
    ssl_enabled=True,
    ssl_mode="verify-full",  # 'require', 'verify-ca', 'verify-full'

    # Certificate files
    ssl_ca_file="/etc/ssl/certs/ca.pem",
    ssl_cert_file="/etc/ssl/certs/client.crt",  # For mutual TLS
    ssl_key_file="/etc/ssl/private/client.key",
    ssl_key_password="keypass",  # If key is encrypted
)
```

**SSL Modes:**
- `require`: Encrypt connection (don't verify certificate)
- `verify-ca`: Verify certificate is signed by trusted CA
- `verify-full`: Verify certificate AND hostname match

### Server-Side Timeouts

Prevent runaway queries and stuck transactions:

```python
config = DatabaseConfig(
    connection_string="...",

    # Timeouts in milliseconds (None to disable)
    statement_timeout_ms=30000,  # Abort queries >30 seconds
    idle_in_transaction_session_timeout_ms=60000,  # Abort idle transactions >1 minute
    lock_timeout_ms=5000,  # Abort lock waits >5 seconds
)
```

**Default values:**
- `statement_timeout_ms`: 60000 (60 seconds)
- `idle_in_transaction_session_timeout_ms`: 60000
- `lock_timeout_ms`: 5000

Set to `None` to disable.

### Connection Initialization

```python
config = DatabaseConfig(
    connection_string="...",

    # Custom server settings
    server_settings={
        "jit": "off",  # Disable JIT (prevents latency spikes)
        "application_name": "myapp",
        "timezone": "UTC",
    },

    # Commands run on each new connection
    init_commands=[
        "SET timezone TO 'UTC'",
        "SET work_mem TO '256MB'",
    ],
)
```

### Retry Configuration

```python
config = DatabaseConfig(
    connection_string="...",

    # Connection retry settings
    retry_attempts=3,  # Number of retries
    retry_delay=1.0,  # Initial delay (seconds)
    retry_backoff=2.0,  # Exponential backoff multiplier
    retry_max_delay=30.0,  # Maximum delay between retries
)
```

## Related Skills

- For patterns: `pgdbm:using-pgdbm`, `pgdbm:choosing-pattern`
- For migrations: `pgdbm:migrations-api-reference`
- For testing: `pgdbm:testing-database-code`
