---
name: redis-transactions
description: Master Redis transactions - MULTI/EXEC, WATCH for optimistic locking, Lua scripting, and atomic operation patterns
sasmp_version: "1.3.0"
bonded_agent: 03-redis-operations
bond_type: PRIMARY_BOND

# Production Configuration
version: "2.1.0"
last_updated: "2025-01"

# Parameters
parameters:
  transaction_type:
    type: string
    required: true
    enum: [multi_exec, watch, lua_script]
  watch_keys:
    type: array
    required: false
    items:
      type: string
  lua_script:
    type: string
    required: false
    max_length: 65535
  timeout_ms:
    type: integer
    required: false
    default: 5000

# Retry Configuration
retry_config:
  max_retries: 5
  backoff_strategy: exponential
  backoff_base_ms: 100
  retryable_errors:
    - EXECABORT
    - BUSY
    - connection_timeout

# Observability
observability:
  logging:
    level: info
    log_watch_failures: true
  metrics:
    - transaction_duration_ms
    - watch_abort_rate
    - lua_execution_time_ms

# Validation Rules
validation:
  lua_scripts:
    require_keys_param: true
    max_execution_time_ms: 5000
  transactions:
    max_commands: 1000
    max_watch_keys: 100
---

# Redis Transactions Skill

## Overview

Production-grade transaction handling for Redis. Master MULTI/EXEC for atomic command batches, WATCH for optimistic locking, and Lua scripting for complex atomic operations.

## Transaction Types Comparison

| Feature | MULTI/EXEC | WATCH+MULTI | Lua Script |
|---------|------------|-------------|------------|
| Atomicity | ✅ | ✅ | ✅ |
| Isolation | Partial | Partial | ✅ Full |
| Conditional logic | ❌ | ❌ | ✅ |
| Read-modify-write | ❌ | ✅ | ✅ |
| Cluster support | ⚠️ Same slot | ⚠️ Same slot | ⚠️ Same slot |
| Debugging | Easy | Medium | Harder |

## MULTI/EXEC Transactions

### Basic Transaction
```redis
MULTI                                # Start transaction
SET user:123:balance 100
INCR user:123:login_count
LPUSH user:123:actions "login"
EXEC                                 # Execute atomically
# Returns: [OK, 1, 1]
```

### Discard Transaction
```redis
MULTI
SET key1 "value1"
SET key2 "value2"
DISCARD                              # Abort, nothing executed
```

### Transaction Guarantees
- ✅ **Atomic execution**: All commands execute without interruption
- ✅ **All or nothing**: If EXEC fails, nothing is applied
- ❌ **No rollback**: Individual command failures don't rollback others
- ❌ **No read-modify-write**: Can't use previous values in transaction

## WATCH (Optimistic Locking)

### Pattern: Check-and-Set
```redis
WATCH user:123:balance               # Start watching
balance = GET user:123:balance       # Read current value

# Client-side logic
if balance >= 50:
    MULTI
    DECRBY user:123:balance 50
    INCRBY merchant:456:balance 50
    EXEC                             # nil if balance changed
else:
    UNWATCH                          # Release watch
```

### Multiple Keys
```redis
WATCH key1 key2 key3                 # Watch multiple keys
# ... read values ...
MULTI
# ... modify values ...
EXEC                                 # nil if ANY watched key changed
UNWATCH                              # Always call after failed EXEC
```

### Watch Retry Pattern (Python)
```python
MAX_RETRIES = 5
for attempt in range(MAX_RETRIES):
    try:
        pipe = r.pipeline(True)      # True = use MULTI
        pipe.watch('user:123:balance')

        balance = int(pipe.get('user:123:balance') or 0)
        if balance < 50:
            pipe.unwatch()
            raise InsufficientFunds()

        pipe.multi()
        pipe.decrby('user:123:balance', 50)
        pipe.incrby('merchant:456:balance', 50)
        pipe.execute()
        break  # Success

    except redis.WatchError:
        continue  # Retry
    finally:
        pipe.reset()
```

## Lua Scripting

### Basic Script
```lua
-- Atomic increment with cap
local current = tonumber(redis.call('GET', KEYS[1]) or 0)
local max = tonumber(ARGV[1])

if current < max then
    return redis.call('INCR', KEYS[1])
else
    return current
end
```

### Execute Script
```redis
EVAL "return redis.call('GET', KEYS[1])" 1 mykey

# Load and execute by hash (faster for repeated calls)
SCRIPT LOAD "return redis.call('GET', KEYS[1])"
# Returns: "a42059b356c875f0717db19a51f6aaa9161e77a2"

EVALSHA a42059b356c875f0717db19a51f6aaa9161e77a2 1 mykey
```

### Script Management
```redis
SCRIPT EXISTS <sha1> [sha1 ...]      # Check if loaded
SCRIPT FLUSH [ASYNC|SYNC]            # Clear cache
SCRIPT KILL                          # Kill running (if no writes)
SCRIPT DEBUG YES|SYNC|NO             # Enable debugging
```

## Production Patterns

### Pattern 1: Fund Transfer
```lua
-- transfer.lua
local from = KEYS[1]
local to = KEYS[2]
local amount = tonumber(ARGV[1])

local from_balance = tonumber(redis.call('GET', from) or 0)

if from_balance >= amount then
    redis.call('DECRBY', from, amount)
    redis.call('INCRBY', to, amount)
    return 1  -- Success
else
    return 0  -- Insufficient funds
end
```

### Pattern 2: Distributed Lock
```lua
-- acquire_lock.lua
local lock_key = KEYS[1]
local holder = ARGV[1]
local ttl = tonumber(ARGV[2])

if redis.call('SET', lock_key, holder, 'NX', 'EX', ttl) then
    return 1
else
    return 0
end

-- release_lock.lua
local lock_key = KEYS[1]
local holder = ARGV[1]

if redis.call('GET', lock_key) == holder then
    return redis.call('DEL', lock_key)
else
    return 0
end
```

### Pattern 3: Rate Limiter
```lua
-- rate_limit.lua
local key = KEYS[1]
local limit = tonumber(ARGV[1])
local window = tonumber(ARGV[2])

local current = tonumber(redis.call('GET', key) or 0)

if current < limit then
    redis.call('INCR', key)
    if current == 0 then
        redis.call('EXPIRE', key, window)
    end
    return 1  -- Allowed
else
    return 0  -- Denied
end
```

## Lua Best Practices

```lua
-- ✅ GOOD: Always use KEYS and ARGV
local value = redis.call('GET', KEYS[1])
redis.call('SET', KEYS[2], ARGV[1])

-- ❌ BAD: Dynamic key names break cluster
local key = 'user:' .. ARGV[1]  -- Don't!
redis.call('GET', key)

-- ✅ GOOD: Early return for efficiency
if not redis.call('EXISTS', KEYS[1]) then
    return nil
end

-- ✅ GOOD: Use pcall for error handling
local ok, result = pcall(redis.call, 'GET', KEYS[1])
if not ok then
    return redis.error_reply("Operation failed")
end
```

## Assets

- `distributed-lock.lua` - Production-ready lock implementation
- `config.yaml` - Transaction configuration

## Scripts

- `lua-loader.sh` - Load and manage Lua scripts
- `helper.py` - Python transaction utilities

## References

- `TRANSACTION_PATTERNS.md` - Best practices guide
- `GUIDE.md` - Complete reference

---

## Troubleshooting Guide

### Common Issues & Solutions

#### 1. EXECABORT
```
EXECABORT Transaction discarded because of previous errors
```

**Cause:** Syntax error in queued command

**Diagnosis:**
```redis
MULTI
SET key                              # Missing value!
EXEC
# (error) EXECABORT...
```

**Fix:** Validate commands before queueing

#### 2. Watch Keeps Failing
**Cause:** High contention on watched key

**Solutions:**
- Reduce transaction time
- Use Lua script instead
- Implement exponential backoff
- Consider different data model

#### 3. BUSY Script Error
```
BUSY Redis is busy running a script
```

**Cause:** Lua script running too long (>lua-time-limit)

**Recovery:**
```redis
# Kill script (only if no writes performed)
SCRIPT KILL

# If script performed writes
# Must restart Redis or wait
```

**Prevention:**
```conf
# redis.conf
lua-time-limit 5000  # 5 seconds
```

#### 4. NOSCRIPT Error
```
NOSCRIPT No matching script
```

**Cause:** Script not loaded (cache cleared or different node)

**Fix:**
```python
# Always handle NOSCRIPT
try:
    result = r.evalsha(sha, 1, key)
except redis.NoScriptError:
    result = r.eval(script, 1, key)
```

### Debug Checklist

```markdown
□ All keys in same hash slot (cluster)?
□ WATCH before read operations?
□ UNWATCH after failed EXEC?
□ Lua script uses KEYS/ARGV properly?
□ Script execution time reasonable?
□ Handling NOSCRIPT error?
□ Retry logic for WatchError?
```

### Transaction Performance

| Operation | Time | Notes |
|-----------|------|-------|
| MULTI | O(1) | Start transaction |
| Queue command | O(1) | Add to queue |
| EXEC | O(N) | Execute N commands |
| WATCH | O(1) | Per key |
| EVAL | O(N) | Script complexity |
| EVALSHA | O(N) | Same as EVAL (no load overhead) |

---

## Error Codes Reference

| Code | Name | Description | Recovery |
|------|------|-------------|----------|
| T001 | EXECABORT | Syntax error in queue | Fix command syntax |
| T002 | WATCH_FAILED | Key modified | Retry transaction |
| T003 | BUSY | Script timeout | SCRIPT KILL or wait |
| T004 | NOSCRIPT | Script not loaded | Re-EVAL or LOAD |
| T005 | CROSSSLOT | Keys in different slots | Use hash tags |

---

## Test Template

```python
# test_redis_transactions.py
import redis
import pytest

@pytest.fixture
def r():
    return redis.Redis(decode_responses=True)

def test_multi_exec(r):
    pipe = r.pipeline()
    pipe.set("tx:key1", "value1")
    pipe.set("tx:key2", "value2")
    results = pipe.execute()
    assert results == [True, True]
    r.delete("tx:key1", "tx:key2")

def test_watch_success(r):
    r.set("tx:balance", "100")
    pipe = r.pipeline(True)
    pipe.watch("tx:balance")
    balance = int(pipe.get("tx:balance"))
    pipe.multi()
    pipe.set("tx:balance", balance - 50)
    results = pipe.execute()
    assert results == [True]
    assert r.get("tx:balance") == "50"
    r.delete("tx:balance")

def test_lua_script(r):
    script = "return redis.call('GET', KEYS[1])"
    r.set("tx:lua", "test_value")
    result = r.eval(script, 1, "tx:lua")
    assert result == "test_value"
    r.delete("tx:lua")
```
