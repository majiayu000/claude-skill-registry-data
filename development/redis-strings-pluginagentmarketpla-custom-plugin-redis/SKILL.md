---
name: redis-strings
description: Master Redis Strings - SET, GET, INCR, DECR, atomic counters, binary-safe operations, and caching patterns
sasmp_version: "1.3.0"
bonded_agent: 02-redis-data-structures
bond_type: PRIMARY_BOND

# Production Configuration
version: "2.1.0"
last_updated: "2025-01"

# Parameters
parameters:
  key:
    type: string
    required: true
    pattern: "^[a-zA-Z0-9:_-]+$"
    max_length: 512
  value:
    type: string
    required: true
    max_size: "512MB"
  ttl_seconds:
    type: integer
    required: false
    min: 1
    max: 31536000
  nx_xx:
    type: string
    required: false
    enum: [NX, XX]
    description: "NX=only if not exists, XX=only if exists"

# Retry Configuration
retry_config:
  max_retries: 3
  backoff_strategy: exponential
  backoff_base_ms: 100
  retryable_errors:
    - connection_timeout
    - BUSY

# Observability
observability:
  logging:
    level: debug
    include_key_pattern: true
  metrics:
    - operation_latency_ms
    - cache_hit_ratio
    - key_size_bytes

# Validation Rules
validation:
  key_naming:
    pattern: "object:id:field"
    examples: ["user:123:profile", "cache:api:users"]
  value_limits:
    warn_size_kb: 100
    max_size_kb: 10240
---

# Redis Strings Skill

## Overview

Production-grade String operations for Redis. Master atomic counters, caching patterns, and binary-safe string manipulation.

## Core Commands

### Basic Operations
```redis
SET key value [EX seconds] [PX milliseconds] [NX|XX] [KEEPTTL]
GET key
GETEX key [EX seconds|PX ms|EXAT ts|PXAT ts|PERSIST]  # Get + set TTL
DEL key [key ...]
EXISTS key [key ...]
```

### Atomic Counters
```redis
INCR key                      # +1 (creates if missing, starts at 0)
DECR key                      # -1
INCRBY key increment          # +N
DECRBY key decrement          # -N
INCRBYFLOAT key increment     # Float increment
```

### String Manipulation
```redis
APPEND key value              # Append to value
STRLEN key                    # Get length
GETRANGE key start end        # Substring (0-indexed, inclusive)
SETRANGE key offset value     # Replace from offset
```

### Batch Operations
```redis
MSET key value [key value ...]      # Set multiple
MGET key [key ...]                  # Get multiple
MSETNX key value [key value ...]    # Set multiple if none exist
```

### Advanced Options (Redis 6.2+)
```redis
SET key value GET                   # Set and return old value
SET key value IFEQ oldvalue         # Set if current equals (Redis 7.4+)
GETDEL key                          # Get and delete
SETEX key seconds value             # Set with TTL (deprecated, use SET EX)
```

## Production Patterns

### Pattern 1: Cache with TTL
```redis
# Set with 1-hour TTL
SET cache:user:123 '{"name":"John","email":"john@example.com"}' EX 3600

# Get (returns nil if expired)
GET cache:user:123

# Refresh TTL on access
GETEX cache:user:123 EX 3600
```

### Pattern 2: Rate Limiter (Fixed Window)
```redis
# Increment counter, set TTL on first request
INCR ratelimit:user:123:minute
EXPIRE ratelimit:user:123:minute 60 NX

# Check count
GET ratelimit:user:123:minute
```

### Pattern 3: Distributed Lock
```redis
# Acquire lock (NX = only if not exists)
SET lock:resource:123 "holder-uuid" NX EX 30

# Release lock (only if we own it) - use Lua
EVAL "if redis.call('get',KEYS[1])==ARGV[1] then return redis.call('del',KEYS[1]) else return 0 end" 1 lock:resource:123 "holder-uuid"
```

### Pattern 4: Session Storage
```redis
# Create session
SET session:abc123 '{"user_id":1,"created":1704067200}' EX 86400

# Touch session (reset TTL)
GETEX session:abc123 EX 86400

# Invalidate session
DEL session:abc123
```

## Command Complexity

| Command | Complexity | Notes |
|---------|------------|-------|
| SET/GET | O(1) | Constant time |
| MSET/MGET | O(N) | N = number of keys |
| INCR/DECR | O(1) | Atomic |
| APPEND | O(1) | Amortized |
| GETRANGE | O(N) | N = returned length |
| STRLEN | O(1) | Stored metadata |

## Assets

- `rate-limiter.lua` - Atomic rate limiting script
- `config.yaml` - Pattern configuration

## Scripts

- `string-benchmark.sh` - Performance testing script
- `helper.py` - Python utilities

## References

- `STRING_PATTERNS.md` - Common patterns guide
- `GUIDE.md` - Complete reference

---

## Troubleshooting Guide

### Common Issues & Solutions

#### 1. WRONGTYPE Error
```
WRONGTYPE Operation against a key holding the wrong kind of value
```

**Cause:** Trying string operation on non-string key

**Diagnosis:**
```redis
TYPE mykey  # Check actual type
```

**Prevention:**
- Use consistent key naming conventions
- Check type before operations in scripts

#### 2. Value Too Large
```
string exceeds maximum allowed size (512MB)
```

**Fix:**
- Compress data before storing
- Split into multiple keys
- Use appropriate data structure (Hash for objects)

#### 3. INCR on Non-Integer
```
ERR value is not an integer or out of range
```

**Cause:** INCR/DECR on string that isn't a valid integer

**Fix:**
```redis
# Check current value
GET counter

# Reset if corrupted
SET counter 0
```

#### 4. NX/XX Not Working as Expected
```redis
# NX only sets if key doesn't exist
SET key value NX  # Returns nil if key exists

# XX only sets if key exists
SET key value XX  # Returns nil if key missing
```

### Debug Checklist

```markdown
□ Key exists? (EXISTS key)
□ Correct type? (TYPE key)
□ Value is valid integer for INCR? (GET key)
□ TTL set correctly? (TTL key)
□ Key pattern consistent?
□ Value size reasonable?
```

### Performance Considerations

| Scenario | Issue | Solution |
|----------|-------|----------|
| Large values | High latency | Compress or split |
| Many small keys | Memory overhead | Use Hash for related data |
| No TTL on cache | Memory leak | Always set TTL |
| MGET 1000+ keys | Blocking | Batch into smaller chunks |

---

## Error Codes Reference

| Code | Name | Description | Recovery |
|------|------|-------------|----------|
| S001 | WRONGTYPE | Type mismatch | Check TYPE, fix key |
| S002 | OVERFLOW | Integer overflow | Use INCRBYFLOAT or reset |
| S003 | NAN | Not a number | Validate before INCR |
| S004 | TOOLARGE | Value > 512MB | Compress or split |
| S005 | SYNTAX | Invalid command | Check syntax |

---

## Test Template

```python
# test_redis_strings.py
import redis
import pytest

@pytest.fixture
def r():
    return redis.Redis(decode_responses=True)

def test_set_get(r):
    r.set("test:string:1", "hello")
    assert r.get("test:string:1") == "hello"
    r.delete("test:string:1")

def test_incr(r):
    r.set("test:counter", "10")
    r.incr("test:counter")
    assert r.get("test:counter") == "11"
    r.delete("test:counter")

def test_set_nx(r):
    r.delete("test:nx")
    assert r.set("test:nx", "first", nx=True) == True
    assert r.set("test:nx", "second", nx=True) == None
    r.delete("test:nx")

def test_ttl(r):
    r.set("test:ttl", "value", ex=60)
    ttl = r.ttl("test:ttl")
    assert 55 < ttl <= 60
    r.delete("test:ttl")
```
