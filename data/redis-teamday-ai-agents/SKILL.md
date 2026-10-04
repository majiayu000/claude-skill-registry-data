---
name: redis
description: Read and write Redis cache/store data using redis-cli or Upstash REST API. Manage keys, lists, hashes, sets, and sorted sets.
version: 1.0.0
allowed-tools: Bash
metadata:
  credentials:
    - REDIS_URL
    - UPSTASH_REDIS_REST_URL
    - UPSTASH_REDIS_REST_TOKEN
---

# Redis Skill

Read and write data in Redis using `redis-cli` or the Upstash REST API.

## Quick Start

```bash
# Using redis-cli
redis-cli -u "$REDIS_URL" SET greeting "hello"
redis-cli -u "$REDIS_URL" GET greeting

# Using Upstash REST API
curl -s "$UPSTASH_REDIS_REST_URL/get/greeting" \
  -H "Authorization: Bearer $UPSTASH_REDIS_REST_TOKEN" | jq '.result'
```

## Prerequisites

### Option A: redis-cli (standard Redis)

| Variable | Description | Example |
|----------|-------------|---------|
| `REDIS_URL` | Redis connection URL | `redis://default:password@host:6379` |

### Option B: Upstash REST API (serverless Redis)

| Variable | Description | Example |
|----------|-------------|---------|
| `UPSTASH_REDIS_REST_URL` | Upstash REST endpoint | `https://us1-xxx.upstash.io` |
| `UPSTASH_REDIS_REST_TOKEN` | Upstash REST token | `AXxxBase64Token...` |

### Verify Connection

```bash
# redis-cli
redis-cli -u "$REDIS_URL" PING

# Upstash
curl -s "$UPSTASH_REDIS_REST_URL/ping" \
  -H "Authorization: Bearer $UPSTASH_REDIS_REST_TOKEN" | jq .
```

## redis-cli Recipes

### String Operations

```bash
# Set a value
redis-cli -u "$REDIS_URL" SET mykey "myvalue"

# Set with expiry (60 seconds)
redis-cli -u "$REDIS_URL" SET mykey "myvalue" EX 60

# Get a value
redis-cli -u "$REDIS_URL" GET mykey

# Delete a key
redis-cli -u "$REDIS_URL" DEL mykey

# Set multiple keys
redis-cli -u "$REDIS_URL" MSET key1 "val1" key2 "val2" key3 "val3"

# Get multiple keys
redis-cli -u "$REDIS_URL" MGET key1 key2 key3
```

### Key Management

```bash
# Scan keys (safe for production — non-blocking)
redis-cli -u "$REDIS_URL" SCAN 0 MATCH "prefix:*" COUNT 100

# Get key type
redis-cli -u "$REDIS_URL" TYPE mykey

# Get TTL (time to live)
redis-cli -u "$REDIS_URL" TTL mykey

# Set expiry on existing key
redis-cli -u "$REDIS_URL" EXPIRE mykey 3600
```

### Hash Operations

```bash
# Set hash fields
redis-cli -u "$REDIS_URL" HSET user:1 name "Alice" email "alice@example.com" role "admin"

# Get one field
redis-cli -u "$REDIS_URL" HGET user:1 name

# Get all fields
redis-cli -u "$REDIS_URL" HGETALL user:1
```

### List Operations

```bash
# Push to list
redis-cli -u "$REDIS_URL" RPUSH queue "task1" "task2" "task3"

# Pop from list
redis-cli -u "$REDIS_URL" LPOP queue

# Get list range
redis-cli -u "$REDIS_URL" LRANGE queue 0 -1

# List length
redis-cli -u "$REDIS_URL" LLEN queue
```

### Set Operations

```bash
# Add to set
redis-cli -u "$REDIS_URL" SADD tags "python" "javascript" "typescript"

# Get all members
redis-cli -u "$REDIS_URL" SMEMBERS tags

# Check membership
redis-cli -u "$REDIS_URL" SISMEMBER tags "python"
```

### Sorted Set Operations

```bash
# Add with scores
redis-cli -u "$REDIS_URL" ZADD leaderboard 100 "alice" 85 "bob" 92 "charlie"

# Get top scores
redis-cli -u "$REDIS_URL" ZREVRANGE leaderboard 0 9 WITHSCORES

# Increment score
redis-cli -u "$REDIS_URL" ZINCRBY leaderboard 5 "bob"
```

### Server Info

```bash
# Memory usage
redis-cli -u "$REDIS_URL" INFO memory

# Database size (key count)
redis-cli -u "$REDIS_URL" DBSIZE
```

## Upstash REST API Recipes

For serverless Redis (no redis-cli needed):

### GET / SET

```bash
# SET
curl -s "$UPSTASH_REDIS_REST_URL/set/mykey/myvalue" \
  -H "Authorization: Bearer $UPSTASH_REDIS_REST_TOKEN"

# SET with EX (expiry in seconds)
curl -s "$UPSTASH_REDIS_REST_URL/set/mykey/myvalue/ex/60" \
  -H "Authorization: Bearer $UPSTASH_REDIS_REST_TOKEN"

# GET
curl -s "$UPSTASH_REDIS_REST_URL/get/mykey" \
  -H "Authorization: Bearer $UPSTASH_REDIS_REST_TOKEN" | jq '.result'

# DEL
curl -s "$UPSTASH_REDIS_REST_URL/del/mykey" \
  -H "Authorization: Bearer $UPSTASH_REDIS_REST_TOKEN"
```

### Multi-Command Pipeline

```bash
curl -s "$UPSTASH_REDIS_REST_URL/pipeline" \
  -H "Authorization: Bearer $UPSTASH_REDIS_REST_TOKEN" \
  -H "Content-Type: application/json" \
  -d '[
    ["SET", "key1", "val1"],
    ["SET", "key2", "val2"],
    ["MGET", "key1", "key2"]
  ]' | jq .
```

## Managed Service Setup

### Upstash (Recommended for serverless)
1. Sign up at upstash.com
2. Create a Redis database
3. Copy REST URL and REST Token from dashboard
4. Set `UPSTASH_REDIS_REST_URL` and `UPSTASH_REDIS_REST_TOKEN`

### Redis Cloud
1. Sign up at redis.com/cloud
2. Create a database
3. Use the public endpoint as `REDIS_URL`: `redis://default:password@host:port`

### AWS ElastiCache
- Use VPC endpoint: `redis://host:6379`
- Note: Must be in same VPC (no public access by default)

### Self-Hosted
- `REDIS_URL=redis://localhost:6379` or `redis://:password@host:6379`

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Could not connect` | Host unreachable | Check REDIS_URL, firewall |
| `NOAUTH` | Auth required | Include password in URL (`redis://:pass@host:port`) |
| `WRONGTYPE` | Wrong operation for key type | Check key type with `TYPE key` first |
| `OOM` | Memory limit reached | Delete unused keys or increase memory |
| `401` (Upstash) | Invalid token | Check UPSTASH_REDIS_REST_TOKEN |

## Tips

- **Use `SCAN` instead of `KEYS`** in production — `KEYS` blocks the server
- **Set TTL on cache keys** — use `EX` to auto-expire keys and prevent memory bloat
- **Use hashes for objects** — more memory-efficient than serialized JSON strings
- **Upstash REST for serverless** — no persistent connection needed, HTTP-based
- **Pipeline commands** — batch multiple operations for better performance
- **Use `--no-auth-warning`** flag to suppress auth warnings: `redis-cli --no-auth-warning -u "$REDIS_URL"`
