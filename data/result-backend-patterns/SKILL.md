---
name: result-backend-patterns
description: Result backend configuration patterns for Celery including Redis, Database, and RPC backends with serialization, expiration policies, and performance optimization. Use when configuring result storage, troubleshooting result persistence, implementing custom serializers, migrating between backends, optimizing result expiration, or when user mentions result backends, task results, Redis backend, PostgreSQL results, result serialization, or backend migration.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Result Backend Patterns

**Purpose:** Configure and optimize Celery result backends for reliable task result storage and retrieval.

**Activation Triggers:**
- Setting up result backend for first time
- Migrating from one backend to another
- Result retrieval failures or timeouts
- Serialization errors with complex objects
- Performance issues with result storage
- Expired result cleanup problems
- Custom serialization requirements

**Key Resources:**
- `templates/redis-backend.py` - Redis result backend configuration
- `templates/db-backend.py` - Database (SQLAlchemy) backend setup
- `templates/rpc-backend.py` - RPC (AMQP) backend configuration
- `templates/result-expiration.py` - Expiration and cleanup policies
- `templates/custom-serializers.py` - Custom serialization patterns
- `scripts/test-backend.sh` - Backend connection and functionality testing
- `scripts/migrate-backend.sh` - Safe backend migration with data preservation
- `examples/` - Complete setup guides for each backend type

## Backend Selection Guide

### Redis Backend (Recommended for Most Cases)
**Best for:**
- High-performance applications
- Frequent result access
- Short to medium result retention (minutes to days)
- Real-time status updates

**Characteristics:**
- Fast in-memory storage
- Automatic expiration support
- Connection pooling built-in
- TTL-based cleanup

**Use template:** `templates/redis-backend.py`

### Database Backend (PostgreSQL/MySQL)
**Best for:**
- Long-term result storage (weeks to months)
- Applications with existing database infrastructure
- Complex result queries and reporting
- Audit trail requirements

**Characteristics:**
- Persistent disk storage
- SQL query capabilities
- Automatic table creation
- Transaction support

**Use template:** `templates/db-backend.py`

### RPC Backend (Message Broker)
**Best for:**
- Transient results consumed immediately
- Microservice architectures
- Results used only by initiating client
- Minimal infrastructure requirements

**Characteristics:**
- No additional backend service needed
- Results as AMQP messages
- Single-retrieval pattern
- Optional persistence mode

**Use template:** `templates/rpc-backend.py`

## Configuration Workflow

### 1. Choose Backend Based on Requirements

**Decision Matrix:**
```
Performance Priority + Short Retention → Redis
Long-term Storage + Query Needs → Database
Immediate Consumption Only → RPC
Existing Redis Infrastructure → Redis
Existing Database Infrastructure → Database
```

### 2. Apply Base Configuration Template

```bash
# Copy appropriate template to your celeryconfig.py or settings
cp templates/redis-backend.py your_project/celeryconfig.py
# OR
cp templates/db-backend.py your_project/celeryconfig.py
# OR
cp templates/rpc-backend.py your_project/celeryconfig.py
```

### 3. Configure Connection Settings

**Redis Example:**
```python
# Security: Use environment variables, never hardcode
import os

result_backend = f'redis://:{os.getenv("REDIS_PASSWORD", "")}@' \
                 f'{os.getenv("REDIS_HOST", "localhost")}:' \
                 f'{os.getenv("REDIS_PORT", "6379")}/0'
```

**Database Example:**
```python
# Security: Use environment variables for credentials
import os

db_user = os.getenv("DB_USER", "celery")
db_pass = os.getenv("DB_PASSWORD", "your_password_here")
db_host = os.getenv("DB_HOST", "localhost")
db_name = os.getenv("DB_NAME", "celery_results")

result_backend = f'db+postgresql://{db_user}:{db_pass}@{db_host}/{db_name}'
```

### 4. Set Serialization Options

Reference `templates/custom-serializers.py` for advanced patterns:

```python
# JSON (default, secure, cross-language)
result_serializer = 'json'
result_accept_content = ['json']

# Enable compression for large results
result_compression = 'gzip'

# Store extended metadata (task name, args, retries)
result_extended = True
```

### 5. Configure Expiration Policy

Reference `templates/result-expiration.py`:

```python
# Expire after 24 hours (default: 1 day)
result_expires = 86400

# Disable expiration for critical results
result_expires = None

# Enable automatic cleanup (requires celery beat)
beat_schedule = {
    'cleanup-results': {
        'task': 'celery.backend_cleanup',
        'schedule': crontab(hour=4, minute=0),
    }
}
```

### 6. Test Backend Connection

```bash
# Verify backend is reachable and functional
./scripts/test-backend.sh redis
# OR
./scripts/test-backend.sh postgresql
# OR
./scripts/test-backend.sh rpc
```

## Backend-Specific Configurations

### Redis Optimization

**Connection Pooling:**
```python
redis_max_connections = 50  # Adjust based on worker count
redis_socket_timeout = 120
redis_socket_keepalive = True
redis_retry_on_timeout = True
```

**Persistence vs Performance:**
```python
# For critical results, ensure Redis persistence
# Configure in redis.conf:
# save 900 1      # Save after 900s if 1 key changed
# save 300 10     # Save after 300s if 10 keys changed
# appendonly yes  # Enable AOF for durability
```

### Database Optimization

**Connection Management:**
```python
database_engine_options = {
    'pool_size': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True,  # Verify connections before use
}

# Resolve stale connections
database_short_lived_sessions = True
```

**Table Customization:**
```python
database_table_names = {
    'task': 'celery_taskmeta',
    'group': 'celery_groupmeta',
}

# Auto-create tables at startup (Celery 5.5+)
database_create_tables_at_setup = True
```

**MySQL Transaction Isolation:**
```python
# CRITICAL for MySQL
database_engine_options = {
    'isolation_level': 'READ COMMITTED',
}
```

### RPC Configuration

**Persistent Messages:**
```python
# Make results survive broker restarts
result_persistent = True

# Configure result exchange
result_exchange = 'celery_results'
result_exchange_type = 'direct'
```

## Serialization Patterns

### JSON (Recommended Default)

**Advantages:**
- Human-readable
- Cross-language compatible
- Secure (no code execution)
- Widely supported

**Limitations:**
- Cannot serialize complex Python objects
- No datetime support (use ISO strings)
- Limited binary data support

**Example:** See `templates/custom-serializers.py`

### Custom Serializers

**When to Use:**
- Complex domain objects
- Binary data (images, files)
- Custom data types
- Performance optimization

**Implementation:**
```python
from kombu.serialization import register

def custom_encoder(obj):
    # Your encoding logic
    return serialized_data

def custom_decoder(data):
    # Your decoding logic
    return deserialized_obj

register(
    'myformat',
    custom_encoder,
    custom_decoder,
    content_type='application/x-myformat',
    content_encoding='utf-8'
)

# Use in config
result_serializer = 'myformat'
result_accept_content = ['myformat', 'json']
```

## Migration Between Backends

### Safe Migration Process

```bash
# Use migration script for zero-downtime migration
./scripts/migrate-backend.sh redis postgresql

# Process:
# 1. Configure new backend alongside old
# 2. Dual-write to both backends
# 3. Verify new backend functionality
# 4. Switch reads to new backend
# 5. Deprecate old backend
```

### Manual Migration Steps

**1. Add new backend configuration:**
```python
# Keep old backend active
result_backend = 'redis://localhost:6379/0'

# Add new backend (not active yet)
# new_result_backend = 'db+postgresql://...'
```

**2. Deploy with dual-write capability:**
```python
# Custom backend that writes to both
class DualBackend:
    def __init__(self):
        self.old_backend = RedisBackend(...)
        self.new_backend = DatabaseBackend(...)

    def store_result(self, task_id, result, state):
        # Write to both backends
        self.old_backend.store_result(task_id, result, state)
        self.new_backend.store_result(task_id, result, state)
```

**3. Verify and switch:**
```bash
# Test new backend
./scripts/test-backend.sh postgresql

# Update config to use new backend
result_backend = 'db+postgresql://...'
```

## Performance Optimization

### Disable Results When Not Needed

```python
# Global setting
task_ignore_result = True

# Per-task override
@app.task(ignore_result=True)
def fire_and_forget_task():
    # Results not stored
    pass
```

### Connection Pooling

**Redis:**
```python
redis_max_connections = None  # No limit (use with caution)
# OR
redis_max_connections = worker_concurrency * 2  # Rule of thumb
```

**Database:**
```python
database_engine_options = {
    'pool_size': 20,
    'max_overflow': 10,
}
```

### Result Compression

```python
# Compress large results
result_compression = 'gzip'  # or 'bzip2'

# Only compress results over threshold
result_compression = 'gzip'
result_compression_level = 6  # 1-9, higher = more compression
```

### Batch Result Retrieval

```python
# Retrieve multiple results efficiently
from celery.result import GroupResult

job = group(task.s(i) for i in range(100))()
results = job.get(timeout=10, propagate=False)
```

## Troubleshooting

### Results Not Persisting

**Check:**
1. Backend connection string format
2. Backend service is running
3. Credentials are correct
4. `ignore_result` is not set globally
5. Task completed without errors

**Debug:**
```bash
./scripts/test-backend.sh <backend-type>
```

### Serialization Errors

**Symptoms:**
- `TypeError: Object of type X is not JSON serializable`
- `pickle.PicklingError`

**Solutions:**
1. Use JSON-compatible types only
2. Implement custom serializer (see `templates/custom-serializers.py`)
3. Convert complex objects before returning
4. Use `result_serializer = 'pickle'` (security risk!)

### Performance Degradation

**Redis:**
- Increase `redis_max_connections`
- Enable connection pooling
- Monitor Redis memory usage
- Implement aggressive expiration

**Database:**
- Add indexes on `task_id` column
- Enable `database_short_lived_sessions`
- Increase connection pool size
- Archive old results periodically

### Expired Results

**Check expiration settings:**
```python
# View current setting
print(app.conf.result_expires)

# Extend retention
result_expires = 7 * 86400  # 7 days
```

**Enable automatic cleanup:**
```python
# Requires celery beat
beat_schedule = {
    'cleanup-results': {
        'task': 'celery.backend_cleanup',
        'schedule': crontab(hour=4, minute=0),
    }
}
```

## Security Best Practices

**Connection Credentials:**
- Store in environment variables, never hardcode
- Use `.env.example` with placeholders
- Add `.env` to `.gitignore`
- Rotate credentials regularly

**Network Security:**
- Use TLS/SSL for Redis connections (`rediss://`)
- Enable SSL for database connections
- Restrict backend access by IP/firewall
- Use authentication for all backends

**Serialization:**
- Avoid pickle serializer (code execution risk)
- Use JSON for cross-language compatibility
- Validate deserialized data
- Implement content type whitelisting

## Examples

All backend configurations have complete examples in `examples/`:

- `redis-backend-setup.md` - Complete Redis setup with sentinel and cluster
- `postgresql-backend.md` - PostgreSQL configuration with migrations
- `result-expiration-policies.md` - Expiration strategies and cleanup patterns

## Resources

**Templates:** Complete configuration files in `templates/` directory
**Scripts:** Testing and migration tools in `scripts/` directory
**Examples:** Real-world setup guides in `examples/` directory

---

**Backend Support:** Redis, PostgreSQL, MySQL, SQLite, MongoDB, RPC (AMQP)
**Celery Version:** 5.0+
**Last Updated:** 2025-11-16
