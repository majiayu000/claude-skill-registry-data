---
name: grokking-system-design-interview
description: Pattern-based system design interview preparation framework with reusable building blocks, question walkthroughs, and company-specific interview guides
triggers:
  - "help me prepare for a system design interview"
  - "show me system design patterns"
  - "design a scalable system"
  - "explain distributed system concepts"
  - "practice system design questions"
  - "what are common system design building blocks"
  - "how to approach system design interviews"
  - "show me cache and load balancing patterns"
---

# Grokking System Design Interview Skill

> Skill by [ara.so](https://ara.so) — Design Skills collection.

This skill provides expertise in using the Grokking System Design repository, a pattern-based approach to system design interviews. Learn reusable building blocks (caching, sharding, replication, consistency models) and apply them to any design question.

## What This Project Does

Grokking System Design is a free, open companion to the original course that teaches:
- **Pattern-based methodology**: Learn 24 reusable building blocks instead of memorizing answers
- **Interview framework**: A repeatable 7-step structure for any question
- **40+ question walkthroughs**: From TinyURL to ChatGPT, organized by difficulty
- **Company-specific guides**: How 58 companies run their system design rounds
- **Distributed systems deep dives**: Case studies of Dynamo, Cassandra, Kafka, etc.

## Installation

This is a knowledge repository, not code you install. Clone it for offline reference:

```bash
git clone https://github.com/design-gurus/grokking-system-design.git
cd grokking-system-design
```

Or browse online at: https://github.com/design-gurus/grokking-system-design

## Repository Structure

```
grokking-system-design/
├── patterns/              # 24 reusable building blocks
├── questions/            # 40+ system design walkthroughs
├── companies/            # 58 company-specific interview guides
├── cheat-sheets/         # Quick reference sheets
├── roadmaps/             # 1-week, 2-week, 6-week study plans
├── deep-dives/           # Distributed systems case studies
└── glossary.md           # System design vocabulary
```

## The 7-Step Interview Framework

Every system design question should follow this structure:

### 1. Clarify Requirements (3-5 minutes)

**Functional requirements** (what the system does):
```
Example for "Design Instagram":
- Users can upload photos
- Users can follow other users
- Users see a feed of photos from people they follow
- Users can like and comment on photos
```

**Non-functional requirements** (how the system performs):
```
- Scale: 500M users, 100M daily active users
- Availability: 99.99% uptime
- Latency: Feed loads in < 200ms
- Consistency: Eventual consistency is acceptable
```

### 2. Estimate Scale (5 minutes)

```
Traffic estimate:
- 100M DAU
- Each user views 50 photos/day = 5B photo views/day
- 5B / 86400 seconds ≈ 58K requests/second
- Peak traffic (3x average) = 174K RPS

Storage estimate:
- 2M new photos/day
- Average photo size: 2MB
- Daily storage: 2M × 2MB = 4TB/day
- 5-year storage: 4TB × 365 × 5 ≈ 7.3PB

Bandwidth estimate:
- Incoming: 4TB/day = 46MB/s
- Outgoing (views): 5B × 2MB / 86400 = 115GB/s
```

### 3. Define the API (5 minutes)

```python
# REST API example for Instagram

# Upload photo
POST /api/v1/photos
Content-Type: multipart/form-data
Body: { photo: file, caption: string, location: string }
Response: { photo_id: string, url: string }

# Get user feed
GET /api/v1/feed?user_id={id}&cursor={cursor}&limit=20
Response: { photos: [...], next_cursor: string }

# Follow user
POST /api/v1/users/{user_id}/follow
Body: { follower_id: string }
Response: { success: boolean }

# Like photo
POST /api/v1/photos/{photo_id}/like
Body: { user_id: string }
Response: { success: boolean, like_count: number }
```

### 4. Design the Data Model (5 minutes)

```sql
-- SQL schema example for Instagram

CREATE TABLE users (
    user_id BIGINT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    INDEX idx_username (username)
);

CREATE TABLE photos (
    photo_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    photo_url VARCHAR(500) NOT NULL,
    caption TEXT,
    location VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX idx_user_created (user_id, created_at)
);

CREATE TABLE follows (
    follower_id BIGINT NOT NULL,
    followee_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (follower_id, followee_id),
    INDEX idx_follower (follower_id),
    INDEX idx_followee (followee_id)
);

CREATE TABLE likes (
    photo_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (photo_id, user_id),
    INDEX idx_photo (photo_id)
);
```

For NoSQL (DynamoDB):
```json
// Users table
{
  "PK": "USER#12345",
  "SK": "METADATA",
  "username": "johndoe",
  "email": "john@example.com",
  "created_at": "2024-01-01T00:00:00Z"
}

// Photos table
{
  "PK": "USER#12345",
  "SK": "PHOTO#67890",
  "photo_id": "67890",
  "photo_url": "https://cdn.example.com/photos/67890.jpg",
  "caption": "Beautiful sunset",
  "created_at": "2024-01-15T18:30:00Z"
}

// Follows table (adjacency list)
{
  "PK": "USER#12345",
  "SK": "FOLLOWS#USER#99999",
  "created_at": "2024-01-10T12:00:00Z"
}
```

### 5. High-Level Architecture (10 minutes)

```
┌─────────────┐
│   Clients   │ (Web, iOS, Android)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│     CDN     │ (CloudFront, Cloudflare)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│Load Balancer│ (ELB, HAProxy, NGINX)
└──────┬──────┘
       │
       ▼
┌──────────────────────────────┐
│     API Gateway / BFF        │
└──────┬───────────────────────┘
       │
       ├─────────┬─────────┬─────────┐
       ▼         ▼         ▼         ▼
   ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
   │ User   │ │ Photo  │ │ Feed   │ │ Social │
   │Service │ │Service │ │Service │ │Service │
   └───┬────┘ └───┬────┘ └───┬────┘ └───┬────┘
       │          │          │          │
       ├──────────┼──────────┼──────────┤
       ▼          ▼          ▼          ▼
   ┌───────────────────────────────────────┐
   │          Message Queue (Kafka)        │
   └───────────────────────────────────────┘
       │          │          │          │
       ├──────────┼──────────┼──────────┤
       ▼          ▼          ▼          ▼
   ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
   │ Cache  │ │ SQL DB │ │ NoSQL  │ │ Object │
   │(Redis) │ │(Postgres)│ │(Cassandra)││Storage│
   └────────┘ └────────┘ └────────┘ │  (S3)  │
                                     └────────┘
```

### 6. Deep Dive (15 minutes)

Pick 1-2 components and go deep. Example: **Feed generation**

```python
# Feed generation service - approach 1: Fan-out on write

class FeedService:
    def __init__(self, cache, db, queue):
        self.cache = cache  # Redis
        self.db = db        # PostgreSQL
        self.queue = queue  # Kafka
    
    def publish_photo(self, user_id, photo_id):
        """
        When user posts a photo, push to all followers' feeds
        (Fan-out on write)
        """
        # Get all followers
        followers = self.db.query(
            "SELECT follower_id FROM follows WHERE followee_id = %s",
            (user_id,)
        )
        
        # Push to each follower's feed cache
        for follower in followers:
            feed_key = f"feed:{follower['follower_id']}"
            self.cache.zadd(
                feed_key,
                {photo_id: time.time()},  # Score = timestamp
                nx=True  # Only if not exists
            )
            # Keep only latest 1000 items
            self.cache.zremrangebyrank(feed_key, 0, -1001)
        
        # Publish event for async processing
        self.queue.publish('photo.published', {
            'user_id': user_id,
            'photo_id': photo_id,
            'timestamp': time.time()
        })
    
    def get_feed(self, user_id, cursor=None, limit=20):
        """
        Retrieve user's feed from cache
        """
        feed_key = f"feed:{user_id}"
        
        # Get from Redis sorted set (sorted by timestamp)
        if cursor:
            photo_ids = self.cache.zrevrangebyscore(
                feed_key,
                max=cursor,
                min='-inf',
                start=0,
                num=limit
            )
        else:
            photo_ids = self.cache.zrevrange(
                feed_key,
                start=0,
                end=limit-1
            )
        
        if not photo_ids:
            # Cache miss - generate from DB (fan-out on read)
            return self._generate_feed_from_db(user_id, limit)
        
        # Batch fetch photo metadata
        photos = self._batch_get_photos(photo_ids)
        
        return {
            'photos': photos,
            'next_cursor': photos[-1]['timestamp'] if photos else None
        }
    
    def _generate_feed_from_db(self, user_id, limit):
        """
        Fallback: Generate feed from database
        (Fan-out on read for cache misses)
        """
        photos = self.db.query("""
            SELECT p.photo_id, p.user_id, p.photo_url, p.caption, p.created_at
            FROM photos p
            JOIN follows f ON p.user_id = f.followee_id
            WHERE f.follower_id = %s
            ORDER BY p.created_at DESC
            LIMIT %s
        """, (user_id, limit))
        
        # Warm up cache
        feed_key = f"feed:{user_id}"
        for photo in photos:
            self.cache.zadd(
                feed_key,
                {photo['photo_id']: photo['created_at'].timestamp()}
            )
        
        return {'photos': photos, 'next_cursor': photos[-1]['created_at'] if photos else None}
```

**Trade-offs:**

| Approach | Pros | Cons | Use When |
|----------|------|------|----------|
| Fan-out on write | Fast reads, pre-computed | Slow writes, storage overhead | Most users have few followers |
| Fan-out on read | Fast writes, less storage | Slow reads, more DB load | Users have many followers (celebrities) |
| Hybrid | Best of both | Complex implementation | Production systems |

### 7. Bottlenecks & Trade-offs (5 minutes)

```
Bottleneck: Database writes (photo uploads)
Solutions:
1. Shard database by user_id (consistent hashing)
2. Use write-ahead log (WAL) for durability
3. Batch writes with message queue
4. Use object storage (S3) for photos, DB only for metadata

Bottleneck: Feed generation for celebrity users (millions of followers)
Solutions:
1. Hybrid approach: fan-out on read for users with > 100K followers
2. Limit fan-out, deliver celebrity posts on demand
3. Use real-time stream processing (Kafka + Flink)

Bottleneck: Hot partition (single shard receives too much traffic)
Solutions:
1. Re-shard using different hash function
2. Add secondary indexes
3. Cache popular content (80/20 rule)

Trade-off: Consistency vs Availability (CAP theorem)
- Strong consistency: Users always see latest data, but system may be unavailable during network partition
- Eventual consistency: System is always available, but users may see stale data temporarily
- Choice: Eventual consistency for social features (likes, follows), strong consistency for payments
```

## Core Patterns Reference

### 1. Caching

```python
# Redis caching pattern with TTL and cache-aside strategy

import redis
import json
from typing import Optional

class CacheService:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)
    
    def get(self, key: str) -> Optional[dict]:
        """Get from cache, return None if miss"""
        value = self.redis.get(key)
        return json.loads(value) if value else None
    
    def set(self, key: str, value: dict, ttl: int = 3600):
        """Set with TTL (default 1 hour)"""
        self.redis.setex(key, ttl, json.dumps(value))
    
    def delete(self, key: str):
        """Invalidate cache entry"""
        self.redis.delete(key)
    
    def get_or_compute(self, key: str, compute_fn, ttl: int = 3600):
        """Cache-aside pattern: get from cache or compute and store"""
        cached = self.get(key)
        if cached is not None:
            return cached
        
        # Cache miss - compute and store
        value = compute_fn()
        self.set(key, value, ttl)
        return value

# Usage
cache = CacheService(redis_url="redis://localhost:6379/0")

def get_user_profile(user_id: str):
    return cache.get_or_compute(
        key=f"user:{user_id}",
        compute_fn=lambda: db.fetch_user(user_id),
        ttl=1800  # 30 minutes
    )
```

**Cache eviction policies:**
- LRU (Least Recently Used) - default, good for general use
- LFU (Least Frequently Used) - good for access patterns with hot keys
- TTL (Time To Live) - expire after fixed time

### 2. Load Balancing

```nginx
# NGINX load balancer configuration

upstream api_servers {
    # Load balancing method
    least_conn;  # Route to server with fewest connections
    # Alternative: ip_hash (sticky sessions), round_robin (default)
    
    server api1.example.com:8080 weight=3 max_fails=3 fail_timeout=30s;
    server api2.example.com:8080 weight=2 max_fails=3 fail_timeout=30s;
    server api3.example.com:8080 weight=1 backup;  # Backup server
    
    # Health checks
    check interval=3000 rise=2 fall=3 timeout=1000;
}

server {
    listen 80;
    server_name api.example.com;
    
    location / {
        proxy_pass http://api_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        
        # Timeouts
        proxy_connect_timeout 5s;
        proxy_send_timeout 10s;
        proxy_read_timeout 10s;
        
        # Retries
        proxy_next_upstream error timeout http_500 http_502 http_503;
    }
}
```

### 3. Sharding / Partitioning

```python
# Consistent hashing for data partitioning

import hashlib
from bisect import bisect_right
from typing import List, Dict

class ConsistentHash:
    def __init__(self, nodes: List[str], virtual_nodes: int = 150):
        """
        nodes: List of server addresses
        virtual_nodes: Number of virtual nodes per physical node
        """
        self.virtual_nodes = virtual_nodes
        self.ring: Dict[int, str] = {}
        self.sorted_keys: List[int] = []
        
        for node in nodes:
            self.add_node(node)
    
    def _hash(self, key: str) -> int:
        """Hash function (MD5)"""
        return int(hashlib.md5(key.encode()).hexdigest(), 16)
    
    def add_node(self, node: str):
        """Add a node with virtual replicas"""
        for i in range(self.virtual_nodes):
            virtual_key = f"{node}:{i}"
            hash_val = self._hash(virtual_key)
            self.ring[hash_val] = node
            self.sorted_keys.append(hash_val)
        
        self.sorted_keys.sort()
    
    def remove_node(self, node: str):
        """Remove a node and its virtual replicas"""
        for i in range(self.virtual_nodes):
            virtual_key = f"{node}:{i}"
            hash_val = self._hash(virtual_key)
            del self.ring[hash_val]
            self.sorted_keys.remove(hash_val)
    
    def get_node(self, key: str) -> str:
        """Find the node responsible for this key"""
        if not self.ring:
            return None
        
        hash_val = self._hash(key)
        
        # Find the first node clockwise
        idx = bisect_right(self.sorted_keys, hash_val)
        if idx == len(self.sorted_keys):
            idx = 0
        
        return self.ring[self.sorted_keys[idx]]

# Usage
nodes = ["db1.example.com", "db2.example.com", "db3.example.com"]
ch = ConsistentHash(nodes)

# Route user data to appropriate shard
user_id = "user_12345"
shard = ch.get_node(user_id)
print(f"User {user_id} -> {shard}")

# Adding a new shard only affects ~1/N of keys
ch.add_node("db4.example.com")
```

### 4. Rate Limiting

```python
# Token bucket rate limiter

import time
from threading import Lock

class TokenBucket:
    def __init__(self, capacity: int, refill_rate: float):
        """
        capacity: Maximum tokens in bucket
        refill_rate: Tokens added per second
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.time()
        self.lock = Lock()
    
    def _refill(self):
        """Add tokens based on time elapsed"""
        now = time.time()
        elapsed = now - self.last_refill
        tokens_to_add = elapsed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill = now
    
    def consume(self, tokens: int = 1) -> bool:
        """
        Try to consume tokens. Returns True if allowed, False if rate limited.
        """
        with self.lock:
            self._refill()
            
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False

# Redis-based distributed rate limiter
class RedisRateLimiter:
    def __init__(self, redis_client, key_prefix: str = "rate_limit"):
        self.redis = redis_client
        self.key_prefix = key_prefix
    
    def is_allowed(self, user_id: str, limit: int, window: int) -> bool:
        """
        Sliding window rate limiter
        user_id: Identifier for the user/IP
        limit: Max requests allowed in window
        window: Time window in seconds
        """
        key = f"{self.key_prefix}:{user_id}"
        now = time.time()
        window_start = now - window
        
        pipe = self.redis.pipeline()
        
        # Remove old entries outside the window
        pipe.zremrangebyscore(key, 0, window_start)
        
        # Count requests in current window
        pipe.zcard(key)
        
        # Add current request
        pipe.zadd(key, {now: now})
        
        # Set expiry
        pipe.expire(key, window)
        
        results = pipe.execute()
        request_count = results[1]
        
        return request_count < limit

# Usage
limiter = TokenBucket(capacity=100, refill_rate=10)  # 10 req/sec

if limiter.consume():
    # Process request
    handle_request()
else:
    # Return 429 Too Many Requests
    return {"error": "Rate limit exceeded"}, 429
```

### 5. Message Queue Pattern

```python
# Kafka producer/consumer pattern

from kafka import KafkaProducer, KafkaConsumer
import json

class EventPublisher:
    def __init__(self, bootstrap_servers: list):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            acks='all',  # Wait for all replicas
            retries=3,
            max_in_flight_requests_per_connection=1  # Preserve order
        )
    
    def publish(self, topic: str, event: dict, key: str = None):
        """Publish event to Kafka topic"""
        future = self.producer.send(
            topic,
            key=key.encode('utf-8') if key else None,
            value=event
        )
        # Optionally wait for confirmation
        # result = future.get(timeout=10)
        return future
    
    def close(self):
        self.producer.flush()
        self.producer.close()

class EventConsumer:
    def __init__(self, bootstrap_servers: list, group_id: str, topics: list):
        self.consumer = KafkaConsumer(
            *topics,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',  # Start from beginning if no offset
            enable_auto_commit=False  # Manual commit for at-least-once delivery
        )
    
    def consume(self, handler):
        """Consume messages and process with handler function"""
        try:
            for message in self.consumer:
                try:
                    handler(message.value)
                    # Commit offset after successful processing
                    self.consumer.commit()
                except Exception as e:
                    print(f"Error processing message: {e}")
                    # Don't commit - message will be redelivered
        finally:
            self.consumer.close()

# Usage - Publisher
publisher = EventPublisher(['kafka1:9092', 'kafka2:9092'])
publisher.publish(
    topic='user.signup',
    event={
        'user_id': '12345',
        'email': 'user@example.com',
        'timestamp': time.time()
    },
    key='12345'  # Messages with same key go to same partition
)

# Usage - Consumer
def handle_signup(event):
    user_id = event['user_id']
    # Send welcome email
    send_email(event['email'], "Welcome!")
    # Update analytics
    analytics.track('user_signup', user_id)

consumer = EventConsumer(
    bootstrap_servers=['kafka1:9092', 'kafka2:9092'],
    group_id='signup-processor',
    topics=['user.signup']
)
consumer.consume(handle_signup)
```

## Common Question Patterns

### URL Shortener (Basic)

**Approach:**
1. Generate unique short code (base62 encoding of auto-increment ID or hash)
2. Store mapping in key-value store (Redis + persistent DB)
3. Handle collisions with retry or pre-generated pool
4. Implement redirect (302 temporary or 301 permanent)

```python
import hashlib
import base64

class URLShortener:
    BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    def __init__(self, db, cache):
        self.db = db
        self.cache = cache
    
    def shorten(self, long_url: str, custom_alias: str = None) -> str:
        """Create short URL"""
        # Check if URL already shortened
        existing = self.db.query(
            "SELECT short_code FROM urls WHERE long_url = %s",
            (long_url,)
        )
        if existing:
            return existing['short_code']
        
        if custom_alias:
            short_code = custom_alias
            # Check availability
            if self.db.query("SELECT 1 FROM urls WHERE short_code = %s", (short_code,)):
                raise ValueError("Alias already taken")
        else:
            # Generate short code from auto-increment ID
            url_id = self.db.insert("INSERT INTO urls (long_url) VALUES (%s)", (long_url,))
            short_code = self._encode_base62(url_id)
        
        # Store mapping
        self.db.execute(
            "UPDATE urls SET short_code = %s WHERE id = %s",
            (short_code, url_id)
        )
        
        # Cache the mapping
        self.cache.set(f"url:{short_code}", long_url, ttl=86400)
        
        return short_code
    
    def resolve(self, short_code: str) -> str:
        """Get original URL"""
        # Try cache first
        cached = self.cache.get(f"url:{short_code}")
        if cached:
            return cached
        
        # Cache miss - query DB
        result = self.db.query(
            "SELECT long_url FROM urls WHERE short_code = %s",
            (short_code,)
        )
        
        if not result:
            raise ValueError("URL not found")
        
        long_url = result['long_url']
        
        # Update cache
        self.cache.set(f"url:{short_code}", long_url, ttl=86400)
        
        # Track analytics asynchronously
        self._track_click(short_code)
        
        return long_url
    
    def _encode_base62(self, num: int) -> str:
        """Convert number to base62 string"""
        if num == 0:
            return self.BASE62[0]
        
        encoded = []
        while num > 0:
            encoded.append(self.BASE62[num % 62])
            num //= 62
        
        return ''.join(reversed(encoded))
    
    def _track_click(self, short_code: str):
        """Async analytics tracking"""
        # Push to message queue for processing
        self.queue.publish('url.clicked', {
            'short_code': short_code,
            'timestamp': time.time()
        })
```

### News Feed / Timeline (Advanced)

See detailed example in "Deep Dive" section above.

**Key decisions:**
- Fan-out on write vs read vs hybrid
- How to handle celebrity users (millions of followers)
- Cache strategy (Redis sorted sets)
- Pagination (cursor-based vs offset)

### Real-time Chat (Advanced)

**Architecture:**
- WebSocket connections for real-time delivery
- Message queue for reliability (Kafka)
- Presence service (Redis pub/sub)
- Message history (Cassandra or MongoDB)

```python
# WebSocket chat server with Socket.IO

from socketio import AsyncServer, ASGIApp
from aiohttp import web
import asyncio

sio = AsyncServer(async_mode='aiohttp', cors_allowed_origins='*')
app = web.Application()
sio.attach(app)

# In-memory store (use Redis in production)
connections = {}  # user_id -> set of socket IDs
rooms = {}        # room_id -> set of user_ids

@sio.event
async def connect(sid, environ):
    """Client connected"""
    print(f"Client {sid} connected")

@sio.event
async def authenticate(sid, data):
    """Authenticate user and join their rooms"""
    user_id = data['user_id']
    token = data['token']
    
    # Verify token (omitted)
    if not verify_token(token):
        await sio.disconnect(sid)
        return
    
    # Track connection
    if user_id not in connections:
        connections[user_id] = set()
    connections[user_id].add(sid)
    
    # Join user's chat rooms
    user_rooms = db.get_user_rooms(user_id)
    for room_id in user_rooms:
        await sio.enter_room(sid, room_id)
        if room_id not in rooms:
            rooms[room_id] = set()
        rooms[room_id].add(user_id)
    
    # Broadcast online status
    await sio.emit('user_online', {'user_id': user_id}, skip_sid=sid)

@sio.event
async def send_message(sid, data):
    """Receive and broadcast message"""
    room_id = data['room_id']
    user_id = data['user_id']
    content = data['content']
    
    # Save to database
    message_id = await db.save_message({
        'room_id': room_id,
        'user_id': user_id,
        'content': content,
        'timestamp': time.time()
    })
    
    # Publish to message queue for fan-out
    await queue.publish('chat.message', {
        'message
