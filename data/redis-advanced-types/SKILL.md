---
name: redis-advanced-types
description: Master Redis advanced data types - Bitmaps, HyperLogLog, Streams, and Geospatial indexes for specialized use cases
sasmp_version: "1.3.0"
bonded_agent: 02-redis-data-structures
bond_type: SECONDARY_BOND

# Production Configuration
version: "2.1.0"
last_updated: "2025-01"

# Parameters
parameters:
  data_type:
    type: string
    required: true
    enum: [bitmap, hyperloglog, stream, geo]
  operation:
    type: string
    required: true
  precision:
    type: string
    required: false
    description: "HyperLogLog precision level"

# Retry Configuration
retry_config:
  max_retries: 3
  backoff_strategy: exponential
  backoff_base_ms: 100

# Observability
observability:
  metrics:
    - bitmap_cardinality
    - hll_estimated_count
    - stream_length
    - geo_query_radius
---

# Redis Advanced Types Skill

## Bitmaps

Memory-efficient bit operations for flags and counters. 512MB max = 2^32 bits.

### Bitmap Commands
```redis
SETBIT key offset value           # Set bit - O(1)
GETBIT key offset                 # Get bit - O(1)
BITCOUNT key [start end [BYTE|BIT]]  # Count 1s - O(N)
BITOP AND|OR|XOR|NOT destkey key [key ...]  # Bitwise ops - O(N)
BITPOS key bit [start [end [BYTE|BIT]]]     # Find position - O(N)
BITFIELD key [GET type offset] [SET type offset value] [INCRBY type offset increment]
```

### Pattern 1: User Activity Tracking
```redis
# Track daily logins (1 bit per day)
SETBIT user:123:logins:2024 0 1   # Jan 1
SETBIT user:123:logins:2024 4 1   # Jan 5
SETBIT user:123:logins:2024 9 1   # Jan 10

# Count login days in January
BITCOUNT user:123:logins:2024 0 3  # First 4 bytes = 31 days

# Check specific day
GETBIT user:123:logins:2024 4  # Returns 1
```

### Pattern 2: Feature Flags
```redis
# Bit positions represent features
# 0=dark_mode, 1=notifications, 2=beta_features
SETBIT user:123:features 0 1  # Enable dark mode
SETBIT user:123:features 2 1  # Enable beta

# Check feature
GETBIT user:123:features 0  # 1 = enabled
```

### Pattern 3: Daily Active Users
```redis
# Track DAU with bitmap
SETBIT dau:2024-01-15 123 1  # User 123 active
SETBIT dau:2024-01-15 456 1  # User 456 active

# Count DAU
BITCOUNT dau:2024-01-15

# Weekly active (OR across days)
BITOP OR wau:2024-w3 dau:2024-01-15 dau:2024-01-16 dau:2024-01-17
BITCOUNT wau:2024-w3

# Users active all 7 days (AND)
BITOP AND daily-active:week dau:2024-01-15 dau:2024-01-16 ...
```

## HyperLogLog

Probabilistic cardinality estimation with 0.81% standard error. Only 12KB per key!

### HyperLogLog Commands
```redis
PFADD key element [element ...]    # Add - O(1)
PFCOUNT key [key ...]              # Count - O(1) per key
PFMERGE destkey sourcekey [sourcekey ...]  # Merge - O(N)
```

### Pattern 1: Unique Visitors
```redis
# Track hourly unique visitors
PFADD visitors:2024-01-15:10 "user:1" "user:2" "user:3"
PFADD visitors:2024-01-15:11 "user:2" "user:4"

# Count unique for hour
PFCOUNT visitors:2024-01-15:10  # ~3

# Daily unique (merge hours)
PFMERGE visitors:2024-01-15 visitors:2024-01-15:10 visitors:2024-01-15:11
PFCOUNT visitors:2024-01-15  # ~4
```

### Pattern 2: Unique Search Queries
```redis
PFADD searches:2024-01 "redis tutorial" "redis commands"
PFCOUNT searches:2024-01
```

## Streams

Append-only log with consumer groups for reliable message processing.

### Stream Commands
```redis
# Writing
XADD stream [NOMKSTREAM] [MAXLEN|MINID [=|~] threshold] *|id field value [field value ...]
XLEN stream                        # Get length - O(1)

# Reading
XREAD [COUNT count] [BLOCK ms] STREAMS stream [stream ...] id [id ...]
XRANGE stream start end [COUNT count]
XREVRANGE stream end start [COUNT count]

# Consumer Groups
XGROUP CREATE stream group id|$ [MKSTREAM] [ENTRIESREAD n]
XREADGROUP GROUP group consumer [COUNT count] [BLOCK ms] [NOACK] STREAMS stream [stream ...] id [id ...]
XACK stream group id [id ...]
XPENDING stream group [[IDLE min-idle-time] start end count [consumer]]
XCLAIM stream group consumer min-idle-time id [id ...]
XAUTOCLAIM stream group consumer min-idle-time start [COUNT count]

# Management
XTRIM stream MAXLEN|MINID [=|~] threshold
XDEL stream id [id ...]
XINFO STREAM|GROUPS|CONSUMERS stream [group]
```

### Pattern 1: Event Sourcing
```redis
# Add events
XADD orders:events * event_type "created" order_id "123" amount "99.99"
XADD orders:events * event_type "paid" order_id "123" payment_id "pay_456"
XADD orders:events * event_type "shipped" order_id "123" tracking "TRK789"

# Read all events for replay
XRANGE orders:events - +

# Read new events only
XREAD BLOCK 5000 STREAMS orders:events $
```

### Pattern 2: Consumer Group Processing
```redis
# Create consumer group
XGROUP CREATE orders:events processors $ MKSTREAM

# Consumer 1 reads
XREADGROUP GROUP processors consumer-1 COUNT 10 BLOCK 5000 STREAMS orders:events >

# Acknowledge processed
XACK orders:events processors 1704067200000-0

# Check pending (unacked)
XPENDING orders:events processors

# Claim stale messages (consumer died)
XAUTOCLAIM orders:events processors consumer-2 60000 0-0 COUNT 10
```

### Pattern 3: Capped Stream (Logs)
```redis
# Add with auto-trim
XADD logs MAXLEN ~ 10000 * level "error" message "Connection failed"

# Manual trim
XTRIM logs MAXLEN ~ 10000
```

## Geospatial

Location-based data with distance and radius queries.

### Geo Commands
```redis
GEOADD key [NX|XX] [CH] longitude latitude member [longitude latitude member ...]
GEOPOS key member [member ...]
GEODIST key member1 member2 [M|KM|FT|MI]
GEOHASH key member [member ...]
GEOSEARCH key FROMMEMBER member|FROMLONLAT lon lat BYRADIUS radius M|KM|FT|MI|BYBOX width height M|KM|FT|MI [ASC|DESC] [COUNT count [ANY]] [WITHCOORD] [WITHDIST] [WITHHASH]
GEOSEARCHSTORE dest src FROMMEMBER member|FROMLONLAT lon lat BYRADIUS radius unit|BYBOX width height unit [ASC|DESC] [COUNT count [ANY]] [STOREDIST]
```

### Pattern 1: Store Locator
```redis
# Add store locations
GEOADD stores -122.4194 37.7749 "store:sf"
GEOADD stores -118.2437 34.0522 "store:la"
GEOADD stores -73.9857 40.7484 "store:nyc"

# Find stores within 50km
GEOSEARCH stores FROMLONLAT -122.4 37.8 BYRADIUS 50 km WITHCOORD WITHDIST

# Distance between stores
GEODIST stores "store:sf" "store:la" km  # ~559 km
```

### Pattern 2: Nearby Users
```redis
# Update user location
GEOADD users:location -122.4194 37.7749 "user:123"

# Find nearby users
GEOSEARCH users:location FROMMEMBER "user:123" BYRADIUS 5 km COUNT 10 WITHDIST

# Store results for caching
GEOSEARCHSTORE nearby:user:123 users:location FROMMEMBER "user:123" BYRADIUS 5 km
```

### Pattern 3: Delivery Zone Check
```redis
# Define delivery zones (store + radius)
GEOADD zones -122.4194 37.7749 "zone:downtown"

# Check if address in delivery zone
GEODIST zones "zone:downtown" "customer:addr" km
# If < 10, can deliver
```

## Command Complexity

| Command | Complexity | Notes |
|---------|------------|-------|
| SETBIT/GETBIT | O(1) | Constant |
| BITCOUNT | O(N) | N = byte range |
| BITOP | O(N) | N = string length |
| PFADD | O(1) | Amortized |
| PFCOUNT | O(1)/O(N) | 1 key/N keys |
| XADD | O(1) | With MAXLEN ~ O(N) |
| XREAD | O(N) | N = returned |
| XRANGE | O(N) | N = returned |
| GEOADD | O(log N) | Per member |
| GEOSEARCH | O(N+log M) | N=radius, M=elements |

## Assets
- `stream-consumer.py` - Stream consumer implementation
- `geo-search.lua` - Atomic geo operations

## References
- `ADVANCED_TYPES_GUIDE.md` - Complete guide

---

## Troubleshooting Guide

### Common Issues & Solutions

#### 1. Bitmap Memory Explosion
**Cause:** Setting high offset creates sparse bitmap
```redis
SETBIT sparse 100000000 1  # Creates ~12MB
```

**Fix:** Use hash with bitmap segments
```redis
# Instead of SETBIT user:flags 1000000 1
HSET user:flags segment:1000 "\x01"
```

#### 2. HyperLogLog Accuracy
**Issue:** Count varies on repeated PFCOUNT

**Expected:** 0.81% standard error is normal
```redis
# For 1M unique elements
# Expected range: 991,900 - 1,008,100
```

#### 3. Stream Consumer Lag
**Diagnosis:**
```redis
XINFO GROUPS mystream
# Check lag field
```

**Fix:**
- Add more consumers
- Increase batch size
- Check consumer processing time

#### 4. Pending Messages Growing
```redis
XPENDING mystream mygroup
```

**Cause:** Consumers crashing without ACK

**Fix:**
```redis
# Claim and reprocess
XAUTOCLAIM mystream mygroup new-consumer 300000 0-0 COUNT 100
```

#### 5. Geo Precision Issues
**Issue:** Geohash precision ~0.6m max

**Fix:** Store exact coords in hash if needed
```redis
HSET location:123 lat "37.7749000000" lon "-122.4194000000"
```

### Debug Checklist

```markdown
□ Data type correct? (TYPE key)
□ Bitmap offset reasonable? (< 2^32)
□ Stream consumer group exists? (XINFO GROUPS)
□ Pending messages cleared? (XPENDING)
□ HLL merged correctly? (PFMERGE)
□ Geo coordinates valid? (-180 to 180, -85.05 to 85.05)
```

---

## Error Codes Reference

| Code | Name | Description | Recovery |
|------|------|-------------|----------|
| ADV001 | BIT_OFFSET | Offset too large | Use smaller offset |
| ADV002 | STREAM_NOGROUP | Consumer group missing | XGROUP CREATE |
| ADV003 | STREAM_NOENT | Entry ID not found | Check ID format |
| ADV004 | GEO_INVALID | Invalid coordinates | Validate lat/lon |
| ADV005 | HLL_MERGE | Merge failure | Check source keys |

---

## Test Template

```python
# test_redis_advanced.py
import redis
import pytest
import time

@pytest.fixture
def r():
    return redis.Redis(decode_responses=True)

class TestBitmaps:
    def test_user_activity(self, r):
        r.delete("test:activity")
        r.setbit("test:activity", 0, 1)
        r.setbit("test:activity", 5, 1)
        assert r.bitcount("test:activity") == 2
        assert r.getbit("test:activity", 0) == 1
        assert r.getbit("test:activity", 1) == 0
        r.delete("test:activity")

class TestHyperLogLog:
    def test_unique_count(self, r):
        r.delete("test:hll")
        r.pfadd("test:hll", "a", "b", "c", "a")  # 'a' duplicate
        count = r.pfcount("test:hll")
        assert 2 <= count <= 4  # Allow HLL variance
        r.delete("test:hll")

    def test_merge(self, r):
        r.delete("test:hll1", "test:hll2", "test:merged")
        r.pfadd("test:hll1", "a", "b")
        r.pfadd("test:hll2", "b", "c")
        r.pfmerge("test:merged", "test:hll1", "test:hll2")
        count = r.pfcount("test:merged")
        assert 2 <= count <= 4
        r.delete("test:hll1", "test:hll2", "test:merged")

class TestStreams:
    def test_basic_stream(self, r):
        r.delete("test:stream")
        msg_id = r.xadd("test:stream", {"event": "test"})
        assert msg_id is not None

        messages = r.xrange("test:stream", "-", "+")
        assert len(messages) == 1
        assert messages[0][1]["event"] == "test"
        r.delete("test:stream")

    def test_consumer_group(self, r):
        r.delete("test:stream")
        r.xadd("test:stream", {"data": "test"})

        try:
            r.xgroup_create("test:stream", "testgroup", "$", mkstream=True)
        except redis.ResponseError:
            pass  # Group exists

        r.xadd("test:stream", {"data": "new"})
        msgs = r.xreadgroup("testgroup", "consumer1",
                           {"test:stream": ">"}, count=1)
        assert len(msgs) > 0
        r.delete("test:stream")

class TestGeo:
    def test_store_locator(self, r):
        r.delete("test:geo")
        r.geoadd("test:geo", (-122.4194, 37.7749, "sf"))
        r.geoadd("test:geo", (-118.2437, 34.0522, "la"))

        # Distance
        dist = r.geodist("test:geo", "sf", "la", unit="km")
        assert 550 < dist < 570

        # Nearby
        nearby = r.geosearch("test:geo",
                            longitude=-122.4, latitude=37.8,
                            radius=100, unit="km")
        assert "sf" in nearby
        r.delete("test:geo")
```
