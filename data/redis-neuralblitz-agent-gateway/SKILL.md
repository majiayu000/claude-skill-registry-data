---
name: redis
description: Redis in-memory data store for caching, pub/sub, and real-time features
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: databases
---
## What I do
- Implement caching strategies
- Use Redis for session storage
- Build pub/sub systems
- Create rate limiters
- Use sorted sets for rankings
- Implement distributed locks
- Work with Redis Streams

## When to use me
When building high-performance caching, real-time features, or pub/sub systems.

## Strings
```bash
# Set/Get
SET user:1 "John"
GET user:1

# With expiry
SET session:abc "data" EX 3600
SETEX cache:key 300 "value"

# Increment
INCR views:page:1
INCRBY counter 10

# Multiple
MSET key1 "val1" key2 "val2"
MGET key1 key2
```

## Hashes
```bash
# Hash operations
HSET user:1 name "John" email "john@example.com" age "30"
HGET user:1 name
HMGET user:1 name email
HGETALL user:1

# Increment
HINCRBY user:1 age 1

# Delete field
HDEL user:1 age
```

## Lists
```bash
# Push/Pop
LPUSH queue:tasks "task1"
LPUSH queue:tasks "task2"
RPOP queue:tasks

# Range
LRANGE mylist 0 -1

# Blocking (queue)
BLPOP queue:tasks 0  # Wait for item
```

## Sets
```bash
# Add/Members
SADD tags:post:1 "react" "javascript" "frontend"
SMEMBERS tags:post:1

# Set operations
SADD users:online "alice" "bob" "charlie"
SISMEMBER users:online "alice"

# Intersection
SINTER set1 set2

# Random
SRANDMEMBER myset 3
```

## Sorted Sets
```bash
# Leaderboard
ZADD leaderboard 100 "player1"
ZADD leaderboard 200 "player2"
ZADD leaderboard 150 "player3"

# Get rank (0 = highest)
ZRANK leaderboard player2
ZREVRANK leaderboard player1

# Range
ZRANGE leaderboard 0 10 WITHSCORES
ZREVRANGE leaderboard 0 9 WITHSCORES
```

## Pub/Sub
```bash
# Subscribe
SUBSCRIBE chat:room:1

# Publish
PUBLISH chat:room:1 "Hello everyone"
```

## Streams
```bash
# Add to stream
XADD mystream * field1 value1 field2 value2

# Read
XRANGE mystream - + COUNT 10
XREAD COUNT 10 STREAMS mystream 0

# Consumer groups
XGROUP CREATE mystream group1 0
XREADGROUP GROUP group1 consumer1 STREAMS mystream >
```

## Python
```python
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

# String
r.set('key', 'value', ex=3600)
r.get('key')

# Hash
r.hset('user:1', mapping={'name': 'John', 'email': 'john@example.com'})
r.hgetall('user:1')

# List
r.lpush('queue', 'task')
r.rpop('queue')

# Sorted set
r.zadd('leaderboard', {'player1': 100, 'player2': 200})
r.zrevrange('leaderboard', 0, 9, withscores=True)

# Pub/Sub
p = r.pubsub()
p.subscribe('chat')
for message in p.listen():
    print(message)
```

## Rate Limiter
```python
def is_rate_limited(key, limit, window):
    now = time.time()
    window_start = now - window
    
    pipe = r.pipeline()
    pipe.zremrangebyscore(key, 0, window_start)
    pipe.zadd(key, {str(now): now})
    pipe.zcard(key)
    pipe.expire(key, window)
    
    results = pipe.execute()
    count = results[2]
    
    return count > limit
```
