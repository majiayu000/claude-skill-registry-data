---
name: redis-master
description: "Leverage Redis for caching, sessions, pub/sub, queues, rate limiting, and real-time features. Design Redis data structures for optimal performance."
category: php-frameworks
tags: ['redis', 'cache', 'pub-sub', 'session', 'queue']
complexity: advanced
risk: low
compatibility: [claude-code, antigravity, gemini-cli, cursor, copilot, codex-cli, autohand, kiro]
source: antigravity-official
version: "1.0.0"
date_added: "2026-07-10"
last_updated: "2026-07-10"
---

# Redis Master

## Purpose
Use Redis effectively as a cache, message broker, session store, queue, and real-time data structure server.

## Operating Mode
You are a **Redis expert** who selects appropriate data structures, implements patterns correctly, and avoids common pitfalls like memory bloat and cache stampedes.

## The Process

### 1️⃣ Data Structure Selection
| Structure | Best For | Example Use Case |
|---|---|---|
| String | Simple values, counters | Cache, rate limiting |
| Hash | Objects, records | User sessions, config |
| List | Queues, activity feeds | Job queues, recent items |
| Set | Unique collections | Tags, permissions |
| Sorted Set | Ranked data | Leaderboards, rate windows |
| Stream | Event log | Activity stream, audit log |
| Bitmap | Boolean flags at scale | Feature flags, presence |
| HyperLogLog | Cardinality estimates | Unique visitor counts |

### 2️⃣ Caching Patterns
```php
// Cache-Aside (Lazy Loading) - Most common
$user = Cache::remember("user:{$id}", 3600, function () use ($id) {
    return User::find($id);
});

// Write-Through: Update cache on every write
public function updateUser(User $user, array $data): User
{
    $user->update($data);
    Cache::put("user:{$user->id}", $user, 3600);
    return $user;
}

// Cache stampede prevention (atomically set cache)
$value = Cache::lock("lock:user:{$id}", 10)->block(5, function () use ($id) {
    return Cache::remember("user:{$id}", 3600, fn() => User::find($id));
});

// Tagging for bulk invalidation
Cache::tags(['posts', 'user:123'])->put("post:{$postId}", $post, 3600);
Cache::tags(['user:123'])->flush(); // Invalidate all user's cached data
```

### 3️⃣ Rate Limiting with Redis
```php
// Sliding window rate limiter using Sorted Set
function checkRateLimit(string $key, int $limit, int $windowSeconds): bool
{
    $now = microtime(true);
    $windowStart = $now - $windowSeconds;
    
    $redis = Redis::connection();
    $redis->zRemRangeByScore($key, '-inf', $windowStart);
    $count = $redis->zCard($key);
    
    if ($count >= $limit) {
        return false; // Rate limited
    }
    
    $redis->zAdd($key, $now, $now);
    $redis->expire($key, $windowSeconds);
    return true;
}

// Laravel rate limiter
RateLimiter::for('api', function (Request $request) {
    return Limit::perMinute(60)->by($request->user()?->id ?: $request->ip());
});
```

### 4️⃣ Pub/Sub for Real-time
```php
// Publisher (broadcasting events)
Redis::publish('notifications', json_encode([
    'user_id' => $userId,
    'type'    => 'order_ready',
    'message' => 'Your order #123 is ready!',
]));

// Subscriber (in a separate process)
Redis::subscribe(['notifications'], function ($message, $channel) {
    $data = json_decode($message, true);
    // Process notification...
    WebSocket::send($data['user_id'], $data);
});
```

### 5️⃣ Leaderboard with Sorted Sets
```php
// Add/update player score
Redis::zAdd('leaderboard:weekly', $score, $userId);

// Get top 10 with scores
$leaderboard = Redis::zRevRangeWithScores('leaderboard:weekly', 0, 9);

// Get player rank
$rank = Redis::zRevRank('leaderboard:weekly', $userId);

// Get player score
$score = Redis::zScore('leaderboard:weekly', $userId);
```

### 6️⃣ Session Storage
```env
SESSION_DRIVER=redis
SESSION_LIFETIME=120
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_PASSWORD=null
```

### 7️⃣ Redis Best Practices
- Always set TTL on cached keys — never use `SET key value` without expiry
- Use namespaced keys: `app:users:123` not just `user`
- Monitor memory: `redis-cli info memory`
- Set `maxmemory-policy allkeys-lru` for cache-only Redis instances
- Use pipelining for bulk operations
- Enable persistence (RDB + AOF) for non-cache data
- Use Redis Cluster or Sentinel for HA

## Outputs
1. Caching layer implementation
2. Rate limiting configuration
3. Session storage setup
4. Pub/sub patterns
5. Leaderboard/ranking implementation
6. Redis configuration for production
