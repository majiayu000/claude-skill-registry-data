---
name: redis-lists-sets
description: Master Redis Lists and Sets - queues, stacks, unique collections, set operations, and real-world implementation patterns
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
  operation:
    type: string
    required: true
    enum: [push, pop, range, members, add, remove, set_ops]
  blocking:
    type: boolean
    required: false
    default: false
  timeout_seconds:
    type: integer
    required: false
    default: 30
    max: 300

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
  metrics:
    - list_length
    - set_cardinality
    - operation_latency_ms
    - blocking_wait_time
---

# Redis Lists and Sets Skill

## Lists Overview

Redis Lists are linked lists of string values, perfect for queues and stacks.

### List Commands
```redis
# Push operations
LPUSH key value [value ...]   # Push to head - O(1) per element
RPUSH key value [value ...]   # Push to tail - O(1) per element

# Pop operations
LPOP key [count]              # Pop from head - O(N)
RPOP key [count]              # Pop from tail - O(N)
BLPOP key [key ...] timeout   # Blocking pop - O(1)
BRPOP key [key ...] timeout   # Blocking pop from tail

# Range operations
LRANGE key start stop         # Get range - O(S+N)
LINDEX key index              # Get by index - O(N)
LLEN key                      # Get length - O(1)

# Manipulation
LMOVE source dest LEFT|RIGHT LEFT|RIGHT
LINSERT key BEFORE|AFTER pivot value
LSET key index value          # Set by index
LTRIM key start stop          # Trim list
LPOS key element              # Find position (Redis 6.0.6+)
```

## Sets Overview

Redis Sets are unordered collections of unique strings.

### Set Commands
```redis
# Basic operations
SADD key member [member ...]   # Add members - O(N)
SREM key member [member ...]   # Remove members - O(N)
SMEMBERS key                   # Get all members - O(N)
SISMEMBER key member           # Check membership - O(1)
SMISMEMBER key member [member ...]  # Multi-check (Redis 6.2+)
SCARD key                      # Get cardinality - O(1)

# Random operations
SRANDMEMBER key [count]        # Random members
SPOP key [count]               # Pop random members

# Set operations
SINTER key [key ...]           # Intersection - O(N*M)
SUNION key [key ...]           # Union - O(N)
SDIFF key [key ...]            # Difference - O(N)
SINTERSTORE dest key [key ...] # Store intersection
SUNIONSTORE dest key [key ...] # Store union
SDIFFSTORE dest key [key ...]  # Store difference

# Scanning
SSCAN key cursor [MATCH pattern] [COUNT count]
```

## Production Patterns

### Pattern 1: Reliable Message Queue
```redis
# Producer
RPUSH queue:tasks '{"id":1,"action":"process","retry":0}'

# Consumer with reliability (move to processing)
LMOVE queue:tasks queue:processing LEFT RIGHT

# After processing complete
LREM queue:processing 1 '{"id":1,"action":"process","retry":0}'

# Dead letter queue for failures
RPUSH queue:dlq '{"id":1,"action":"process","error":"timeout"}'
```

### Pattern 2: Priority Queue
```redis
# High priority
LPUSH queue:tasks:high '{"priority":"high"}'

# Normal priority
RPUSH queue:tasks:normal '{"priority":"normal"}'

# Consumer checks high first
BLPOP queue:tasks:high queue:tasks:normal 30
```

### Pattern 3: Unique Visitors Tracking
```redis
# Track unique visitors per day
SADD visitors:2024-01-15 "user:123"
SADD visitors:2024-01-15 "user:456"

# Count unique
SCARD visitors:2024-01-15

# Weekly unique visitors (union)
SUNIONSTORE visitors:week:3 visitors:2024-01-15 visitors:2024-01-16 visitors:2024-01-17
SCARD visitors:week:3

# Set TTL for automatic cleanup
EXPIRE visitors:2024-01-15 604800  # 7 days
```

### Pattern 4: Tag System
```redis
# Add tags to items
SADD item:123:tags "redis" "database" "cache"
SADD item:456:tags "redis" "nosql"

# Find items with specific tag
SADD tag:redis:items "item:123" "item:456"

# Find items with ALL tags (intersection)
SINTER tag:redis:items tag:database:items

# Find items with ANY tag (union)
SUNION tag:redis:items tag:nosql:items
```

### Pattern 5: Social Features
```redis
# User follows
SADD user:123:following "user:456" "user:789"
SADD user:456:followers "user:123"

# Mutual friends
SINTER user:123:following user:456:following

# Friend suggestions (friends of friends)
SDIFF user:456:following user:123:following
```

## Command Complexity

| Command | Complexity | Notes |
|---------|------------|-------|
| LPUSH/RPUSH | O(1) | Per element |
| LPOP/RPOP | O(N) | N = count |
| LRANGE | O(S+N) | S = start offset |
| LINDEX | O(N) | N = index |
| LLEN | O(1) | Stored metadata |
| SADD/SREM | O(N) | N = members |
| SISMEMBER | O(1) | Hash lookup |
| SMEMBERS | O(N) | Returns all |
| SINTER | O(N*M) | Smallest set first |

## Assets

- `queue-config.yaml` - Queue configuration template
- `reliable-queue.lua` - Atomic queue operations

## Scripts

- `queue-consumer.py` - Python queue consumer example

## References

- `LIST_SET_PATTERNS.md` - Common patterns guide

---

## Troubleshooting Guide

### Common Issues & Solutions

#### 1. WRONGTYPE Error
```
WRONGTYPE Operation against a key holding the wrong kind of value
```

**Cause:** Using list command on set or vice versa

**Diagnosis:**
```redis
TYPE mykey  # Check actual type
```

**Prevention:** Use consistent naming conventions (e.g., `list:*`, `set:*`)

#### 2. Blocking Operation Timeout
```redis
# Returns nil after timeout
BLPOP queue:empty 5
```

**Cause:** No elements in list within timeout

**Fix:**
- Increase timeout for low-traffic queues
- Check if producers are running
- Use non-blocking LPOP with retry logic

#### 3. Large Set Operations Blocking
```redis
# Can block for seconds on large sets
SMEMBERS huge:set  # 1M+ members
```

**Fix:**
```redis
# Use SSCAN instead
SSCAN huge:set 0 COUNT 1000
```

#### 4. Memory Issues with Long Lists
**Cause:** Unbounded list growth

**Fix:**
```redis
# Cap list length
LTRIM queue:logs 0 9999  # Keep last 10000

# Or use RPUSH with LTRIM atomically
MULTI
RPUSH queue:logs "entry"
LTRIM queue:logs -10000 -1
EXEC
```

### Debug Checklist

```markdown
□ Key exists? (EXISTS key)
□ Correct type? (TYPE key)
□ List/Set not empty? (LLEN/SCARD)
□ Blocking timeout appropriate?
□ Memory usage acceptable? (MEMORY USAGE key)
□ Consumer running?
□ Producer running?
```

### Performance Considerations

| Scenario | Issue | Solution |
|----------|-------|----------|
| LRANGE 0 -1 | Full list scan | Paginate with LRANGE |
| SMEMBERS large set | High memory | Use SSCAN |
| Many small lists | Memory overhead | Consolidate or use Streams |
| SINTER large sets | CPU spike | Pre-compute or cache |

---

## Error Codes Reference

| Code | Name | Description | Recovery |
|------|------|-------------|----------|
| LS001 | WRONGTYPE | Type mismatch | Check TYPE, fix key |
| LS002 | EMPTY | List/Set empty | Check producers |
| LS003 | INDEX_OOB | Index out of bounds | Validate index |
| LS004 | TIMEOUT | Blocking timeout | Increase timeout |
| LS005 | MEMORY | Large collection | LTRIM or SSCAN |

---

## Test Template

```python
# test_redis_lists_sets.py
import redis
import pytest

@pytest.fixture
def r():
    return redis.Redis(decode_responses=True)

class TestLists:
    def test_queue_pattern(self, r):
        r.delete("test:queue")
        r.rpush("test:queue", "task1", "task2")
        assert r.llen("test:queue") == 2
        assert r.lpop("test:queue") == "task1"
        r.delete("test:queue")

    def test_stack_pattern(self, r):
        r.delete("test:stack")
        r.lpush("test:stack", "a", "b", "c")
        assert r.lpop("test:stack") == "c"  # LIFO
        r.delete("test:stack")

    def test_lrange(self, r):
        r.delete("test:list")
        r.rpush("test:list", *range(10))
        assert len(r.lrange("test:list", 0, 4)) == 5
        r.delete("test:list")

class TestSets:
    def test_unique_members(self, r):
        r.delete("test:set")
        r.sadd("test:set", "a", "b", "a")  # Duplicate ignored
        assert r.scard("test:set") == 2
        r.delete("test:set")

    def test_set_operations(self, r):
        r.delete("test:set1", "test:set2")
        r.sadd("test:set1", "a", "b", "c")
        r.sadd("test:set2", "b", "c", "d")

        assert r.sinter("test:set1", "test:set2") == {"b", "c"}
        assert r.sunion("test:set1", "test:set2") == {"a", "b", "c", "d"}
        assert r.sdiff("test:set1", "test:set2") == {"a"}

        r.delete("test:set1", "test:set2")

    def test_membership(self, r):
        r.delete("test:set")
        r.sadd("test:set", "member1")
        assert r.sismember("test:set", "member1") == 1
        assert r.sismember("test:set", "nonexistent") == 0
        r.delete("test:set")
```
