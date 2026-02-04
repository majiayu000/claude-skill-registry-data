---
name: redis-modules
description: Master Redis modules - RedisJSON, RediSearch, RedisTimeSeries, RedisBloom, and extending Redis functionality
sasmp_version: "1.3.0"
bonded_agent: 08-redis-production
bond_type: SECONDARY_BOND

# Production Configuration
version: "2.1.0"
last_updated: "2025-01"

# Parameters
parameters:
  module:
    type: string
    required: true
    enum: [json, search, timeseries, bloom, graph]

# Observability
observability:
  metrics:
    - module_loaded
    - json_document_count
    - search_query_latency
    - timeseries_samples
---

# Redis Modules Skill

## RedisJSON

JSON document storage and manipulation.

```redis
# Set document
JSON.SET user:1 $ '{"name":"John","age":30,"tags":["redis"]}'

# Get path
JSON.GET user:1 $.name              # "John"
JSON.GET user:1 $                   # Full document

# Modify
JSON.NUMINCRBY user:1 $.age 1       # Increment
JSON.ARRAPPEND user:1 $.tags '"new"' # Add to array
JSON.SET user:1 $.email '"john@example.com"'
```

## RediSearch

Full-text search and secondary indexing.

```redis
# Create index
FT.CREATE idx:users ON JSON PREFIX 1 user:
  SCHEMA
    $.name AS name TEXT SORTABLE
    $.email AS email TAG
    $.age AS age NUMERIC SORTABLE

# Search
FT.SEARCH idx:users "@name:John"
FT.SEARCH idx:users "@age:[25 35]"
FT.SEARCH idx:users "@email:{john@example.com}"

# Aggregate
FT.AGGREGATE idx:users "*"
  GROUPBY 1 @age
  REDUCE COUNT 0 AS count
```

## RedisTimeSeries

Time-series data with aggregations.

```redis
# Create series
TS.CREATE sensor:temp RETENTION 86400000 LABELS type temperature location office

# Add samples
TS.ADD sensor:temp * 23.5
TS.MADD sensor:temp * 23.5 sensor:humidity * 45

# Query
TS.RANGE sensor:temp - + AGGREGATION avg 3600000  # Hourly avg
TS.MRANGE - + FILTER location=office
```

## RedisBloom

Probabilistic data structures.

```redis
# Bloom filter
BF.ADD filter:emails "user@example.com"
BF.EXISTS filter:emails "user@example.com"  # 1 (might exist)
BF.EXISTS filter:emails "other@example.com" # 0 (definitely not)

# Cuckoo filter (allows delete)
CF.ADD filter:users "user123"
CF.DEL filter:users "user123"

# Count-Min Sketch
CMS.INCRBY sketch item1 5 item2 3
CMS.QUERY sketch item1  # ~5
```

## Loading Modules

```conf
# redis.conf
loadmodule /opt/redis-stack/lib/rejson.so
loadmodule /opt/redis-stack/lib/redisearch.so
loadmodule /opt/redis-stack/lib/redistimeseries.so
loadmodule /opt/redis-stack/lib/redisbloom.so
```

### Docker (Redis Stack)
```bash
docker run -p 6379:6379 redis/redis-stack:latest
```

## Assets
- `docker-compose-stack.yml` - Redis Stack with modules

## References
- `MODULES_GUIDE.md` - Complete guide

---

## Troubleshooting

### Module Not Loaded
```redis
MODULE LIST  # Check loaded modules
```
**Fix:** Check loadmodule path

### Index Not Found
```redis
FT._LIST  # List indexes
```
**Fix:** Create index first

---

## Error Codes

| Code | Name | Recovery |
|------|------|----------|
| MOD001 | NOT_LOADED | Check loadmodule |
| MOD002 | NO_INDEX | FT.CREATE index |
| MOD003 | SCHEMA_ERR | Fix schema definition |
