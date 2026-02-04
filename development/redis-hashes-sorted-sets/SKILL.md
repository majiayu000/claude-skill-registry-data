---
name: redis-hashes-sorted-sets
description: Master Redis Hashes and Sorted Sets - object storage, field operations, leaderboards, rankings, and scoring systems
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
    enum: [hset, hget, hgetall, zadd, zrange, zrank, zincrby]
  score:
    type: float
    required: false
  range_options:
    type: object
    required: false
    properties:
      start: { type: integer }
      stop: { type: integer }
      withscores: { type: boolean }

# Retry Configuration
retry_config:
  max_retries: 3
  backoff_strategy: exponential
  backoff_base_ms: 100

# Observability
observability:
  metrics:
    - hash_field_count
    - zset_cardinality
    - operation_latency_ms
    - rank_query_count
---

# Redis Hashes and Sorted Sets Skill

## Hashes Overview

Redis Hashes are maps between string fields and string values - perfect for object storage.

### Hash Commands
```redis
# Basic operations
HSET key field value [field value ...]  # O(N)
HGET key field                          # O(1)
HGETALL key                             # O(N)
HDEL key field [field ...]              # O(N)
HEXISTS key field                       # O(1)

# Bulk operations
HMSET key field value [field value ...]  # Deprecated, use HSET
HMGET key field [field ...]              # O(N)

# Numeric operations
HINCRBY key field increment              # O(1)
HINCRBYFLOAT key field increment         # O(1)

# Metadata
HLEN key                                 # O(1)
HKEYS key                                # O(N)
HVALS key                                # O(N)
HSCAN key cursor [MATCH pattern] [COUNT count]

# Advanced (Redis 7.4+)
HSETEX key seconds field value           # Set with TTL
HGETEX key field EX seconds              # Get with TTL refresh
```

## Sorted Sets Overview

Sorted Sets combine Sets with scores, enabling ranked collections.

### Sorted Set Commands
```redis
# Add with scores
ZADD key [NX|XX] [GT|LT] [CH] [INCR] score member [score member ...]

# Range queries by index
ZRANGE key start stop [BYSCORE|BYLEX] [REV] [LIMIT offset count] [WITHSCORES]
ZREVRANGE key start stop [WITHSCORES]  # Deprecated, use ZRANGE REV

# Range by score
ZRANGEBYSCORE key min max [WITHSCORES] [LIMIT offset count]  # Deprecated
ZRANGE key min max BYSCORE [WITHSCORES] [LIMIT offset count]

# Ranking
ZRANK key member              # 0-based rank (lowest first)
ZREVRANK key member           # 0-based rank (highest first)
ZSCORE key member             # Get score

# Modifications
ZINCRBY key increment member  # Increment score - O(log N)
ZREM key member [member ...]  # Remove - O(M*log N)

# Cardinality
ZCARD key                     # Total count - O(1)
ZCOUNT key min max            # Count in range - O(log N)

# Set operations
ZINTER numkeys key [key ...]  # Intersection
ZUNION numkeys key [key ...]  # Union
ZDIFF numkeys key [key ...]   # Difference
```

## Production Patterns

### Pattern 1: User Profile Storage
```redis
# Store user as hash
HSET user:123 name "John" email "john@example.com" age "30" status "active"

# Get specific fields (efficient)
HMGET user:123 name email

# Update single field
HSET user:123 status "premium"

# Atomic counter in hash
HINCRBY user:123 login_count 1
HINCRBY user:123 points 100

# Check field exists
HEXISTS user:123 email
```

### Pattern 2: Leaderboard System
```redis
# Add/Update scores
ZADD leaderboard 1000 "player:1"
ZADD leaderboard 1500 "player:2"
ZADD leaderboard 800 "player:3"

# Increment score (game points)
ZINCRBY leaderboard 50 "player:1"

# Get top 10 (highest scores)
ZRANGE leaderboard 0 9 REV WITHSCORES

# Get player rank (0-indexed)
ZREVRANK leaderboard "player:1"

# Get player score
ZSCORE leaderboard "player:1"

# Get players around a rank
ZRANGE leaderboard 5 15 REV WITHSCORES

# Count players above threshold
ZCOUNT leaderboard 1000 +inf
```

### Pattern 3: Time-Based Scoring (Activity Feed)
```redis
# Add items with timestamp as score
ZADD feed:user:123 1704067200 "post:456"
ZADD feed:user:123 1704153600 "post:789"

# Get recent items
ZRANGE feed:user:123 0 19 REV

# Get items from time range
ZRANGE feed:user:123 1704000000 1704200000 BYSCORE

# Remove old items
ZREMRANGEBYSCORE feed:user:123 -inf 1703980800
```

### Pattern 4: Rate Limiting with Sorted Set
```redis
# Sliding window rate limiter
-- Add request with timestamp
ZADD ratelimit:user:123 1704067200.123 "req:uuid1"

-- Remove old entries (outside window)
ZREMRANGEBYSCORE ratelimit:user:123 -inf 1704067140.123

-- Count requests in window
ZCARD ratelimit:user:123

-- Check if under limit
-- If ZCARD < 100, allow request
```

### Pattern 5: Product Inventory with Hash
```redis
# Store product
HSET product:sku:ABC123 \
    name "Redis T-Shirt" \
    price "29.99" \
    stock "100" \
    category "apparel"

# Decrement stock atomically
HINCRBY product:sku:ABC123 stock -1

# Get product info
HGETALL product:sku:ABC123

# Update price
HSET product:sku:ABC123 price "24.99"
```

### Pattern 6: Session Storage
```redis
# Store session data
HSET session:abc123 \
    user_id "123" \
    created "1704067200" \
    ip "192.168.1.1" \
    user_agent "Mozilla/5.0"

# Set session TTL
EXPIRE session:abc123 3600

# Update last access
HSET session:abc123 last_access "1704070800"

# Get specific session data
HMGET session:abc123 user_id created
```

## Command Complexity

| Command | Complexity | Notes |
|---------|------------|-------|
| HSET/HGET | O(1) | Single field |
| HMSET/HMGET | O(N) | N = fields |
| HGETALL | O(N) | Returns all |
| HINCRBY | O(1) | Atomic |
| ZADD | O(log N) | Per member |
| ZRANGE | O(log N + M) | M = returned |
| ZRANK | O(log N) | Binary search |
| ZINCRBY | O(log N) | Update + reorder |
| ZCARD | O(1) | Stored metadata |

## Memory Optimization

### Hash Ziplist Encoding
```conf
# redis.conf - Use ziplist for small hashes
hash-max-ziplist-entries 512
hash-max-ziplist-value 64
```

### Sorted Set Ziplist
```conf
zset-max-ziplist-entries 128
zset-max-ziplist-value 64
```

## Assets

- `leaderboard.lua` - Atomic leaderboard operations
- `hash-ttl.lua` - Per-field TTL simulation

## Scripts

- `hash-migration.py` - Hash data migration script

## References

- `HASH_ZSET_PATTERNS.md` - Pattern guide

---

## Troubleshooting Guide

### Common Issues & Solutions

#### 1. HGETALL on Large Hash
```redis
# Can block for seconds
HGETALL huge:hash  # 100K+ fields
```

**Fix:**
```redis
# Use HSCAN instead
HSCAN huge:hash 0 COUNT 1000
```

#### 2. WRONGTYPE Error
```
WRONGTYPE Operation against a key holding the wrong kind of value
```

**Diagnosis:**
```redis
TYPE mykey
```

**Prevention:** Consistent key naming (`hash:*`, `zset:*`)

#### 3. Score Precision Issues
```redis
ZADD scores 1.7976931348623157e+308 "item"  # Max float
ZADD scores 0.1 "a"
ZADD scores 0.2 "b"
# 0.1 + 0.1 may not equal 0.2 exactly
```

**Fix:** Use integer scores when possible (multiply by 100 for cents)

#### 4. Leaderboard Tie-Breaking
**Problem:** Same score = arbitrary order

**Fix:** Use composite score
```redis
# score = points * 1000000 + (MAX_TIME - timestamp)
ZADD leaderboard 1000000000 "player:1"  # 1000 pts at time 0
ZADD leaderboard 1000999999 "player:2"  # 1000 pts later (lower rank)
```

#### 5. Memory Bloat with Hashes
**Cause:** Large field values or too many fields

**Diagnosis:**
```redis
DEBUG OBJECT user:123
MEMORY USAGE user:123
```

**Fix:**
- Compress large values
- Split into multiple hashes
- Use appropriate encoding thresholds

### Debug Checklist

```markdown
□ Key exists? (EXISTS key)
□ Correct type? (TYPE key)
□ Hash field exists? (HEXISTS key field)
□ Score within valid range?
□ Encoding efficient? (DEBUG OBJECT key)
□ Memory usage acceptable? (MEMORY USAGE key)
```

### Performance Considerations

| Scenario | Issue | Solution |
|----------|-------|----------|
| HGETALL large hash | Blocking | Use HSCAN |
| ZRANGE 0 -1 large set | High memory | Paginate |
| Many ZINCRBY | Hot key | Shard by key |
| String values in hash | Memory waste | Consider MessagePack |

---

## Error Codes Reference

| Code | Name | Description | Recovery |
|------|------|-------------|----------|
| HZ001 | WRONGTYPE | Type mismatch | Check TYPE |
| HZ002 | FIELD_NOT_FOUND | Hash field missing | Check HEXISTS |
| HZ003 | NAN_SCORE | Invalid score value | Validate number |
| HZ004 | MEMBER_NOT_FOUND | ZSet member missing | Check membership |
| HZ005 | OVERFLOW | Integer overflow | Use float or reset |

---

## Test Template

```python
# test_redis_hashes_zsets.py
import redis
import pytest

@pytest.fixture
def r():
    return redis.Redis(decode_responses=True)

class TestHashes:
    def test_user_profile(self, r):
        r.delete("test:user:1")
        r.hset("test:user:1", mapping={
            "name": "John",
            "email": "john@example.com",
            "age": "30"
        })
        assert r.hget("test:user:1", "name") == "John"
        assert r.hlen("test:user:1") == 3
        r.delete("test:user:1")

    def test_hincrby(self, r):
        r.delete("test:counter")
        r.hset("test:counter", "visits", "10")
        r.hincrby("test:counter", "visits", 5)
        assert r.hget("test:counter", "visits") == "15"
        r.delete("test:counter")

    def test_hmget(self, r):
        r.delete("test:hash")
        r.hset("test:hash", mapping={"a": "1", "b": "2", "c": "3"})
        result = r.hmget("test:hash", "a", "c")
        assert result == ["1", "3"]
        r.delete("test:hash")

class TestSortedSets:
    def test_leaderboard(self, r):
        r.delete("test:leaderboard")
        r.zadd("test:leaderboard", {"player:1": 100, "player:2": 200})

        # Top player
        top = r.zrange("test:leaderboard", 0, 0, desc=True)
        assert top == ["player:2"]

        # Rank
        rank = r.zrevrank("test:leaderboard", "player:1")
        assert rank == 1  # 0-indexed, second place

        r.delete("test:leaderboard")

    def test_zincrby(self, r):
        r.delete("test:scores")
        r.zadd("test:scores", {"player:1": 100})
        r.zincrby("test:scores", 50, "player:1")
        assert r.zscore("test:scores", "player:1") == 150
        r.delete("test:scores")

    def test_zrangebyscore(self, r):
        r.delete("test:zset")
        r.zadd("test:zset", {"a": 1, "b": 2, "c": 3, "d": 4})
        result = r.zrangebyscore("test:zset", 2, 3)
        assert result == ["b", "c"]
        r.delete("test:zset")

    def test_zcount(self, r):
        r.delete("test:zset")
        r.zadd("test:zset", {"a": 1, "b": 2, "c": 3})
        assert r.zcount("test:zset", 2, "+inf") == 2
        r.delete("test:zset")
```
