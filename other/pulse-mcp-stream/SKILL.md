---
name: pulse-mcp-stream
description: ' Layer 1: Real-Time Social Stream Monitoring via MCP'
version: 1.0.0
---


# pulse-mcp-stream

> Layer 1: Real-Time Social Stream Monitoring via MCP

**Version**: 1.0.0  
**Trit**: +1 (Generator - produces live data)  
**Bundle**: acquisition  

## Overview

Pulse-MCP-stream provides real-time monitoring of social interactions, enabling the cognitive surrogate system to stay updated with the latest patterns. It streams mentions, engagement changes, and trending topics.

## Capabilities

### 1. subscribe-actor

Subscribe to real-time updates for a user.

```python
from pulse_mcp_stream import PulseClient

client = PulseClient(seed=0xf061ebbc2ca74d78)

async for event in client.subscribe_actor("barton.bsky.social"):
    match event.type:
        case "post":
            print(f"New post: {event.text[:50]}...")
        case "reply":
            print(f"Reply from {event.actor}: {event.text[:30]}...")
        case "like":
            print(f"Liked by {event.actor}")
        case "repost":
            print(f"Reposted by {event.actor}")
        case "mention":
            print(f"Mentioned by {event.actor}")
```

### 2. monitor-engagement-delta

Track engagement changes in real-time.

```python
async for delta in client.monitor_engagement_delta("barton.bsky.social"):
    # delta = {
    #   post_id: "at://...",
    #   likes_delta: +5,
    #   reposts_delta: +2,
    #   replies_delta: +1,
    #   timestamp: "2024-12-22T05:00:00Z",
    #   velocity: 2.3  # engagements per minute
    # }
    
    if delta.velocity > 5.0:
        print(f"🔥 Viral post detected: {delta.post_id}")
```

### 3. trend-detect-network

Detect trending topics in a user's network.

```python
trends = await client.trend_detect_network(
    center_user="barton.bsky.social",
    time_window_minutes=60,
    min_mentions=3
)

# Returns:
# [
#   {topic: "category theory", mentions: 12, velocity: 0.2/min},
#   {topic: "Gay.jl", mentions: 8, velocity: 0.13/min},
#   {topic: "MCP servers", mentions: 5, velocity: 0.08/min}
# ]
```

### 4. firehose-filter

Connect to Bluesky firehose with filters.

```python
async for record in client.firehose_filter(
    collections=["app.bsky.feed.post"],
    authors=["barton.bsky.social", "friend1.bsky.social"],
    text_contains=["GF(3)", "category", "topos"]
):
    await process_record(record)
```

### 5. batch-export

Export stream data to DuckDB for analysis.

```python
exporter = client.batch_exporter(
    db_path="pulse_stream.duckdb",
    batch_size=100,
    flush_interval_seconds=30
)

async with exporter:
    async for event in client.subscribe_actor("barton.bsky.social"):
        await exporter.write(event)
```

## MCP Server Integration

```typescript
// pulse-mcp-server/src/index.ts
import { Server } from "@modelcontextprotocol/sdk/server";

const server = new Server({
  name: "pulse-mcp-stream",
  version: "1.0.0"
});

server.setRequestHandler("subscribe", async (params) => {
  const { actor, filters } = params;
  
  // Connect to Bluesky firehose
  const stream = await connectFirehose({
    actor,
    collections: filters?.collections ?? ["app.bsky.feed.post"],
  });
  
  return {
    streamId: stream.id,
    status: "connected"
  };
});

server.setRequestHandler("poll", async (params) => {
  const { streamId, maxEvents } = params;
  const events = await getBufferedEvents(streamId, maxEvents);
  return { events };
});
```

## DuckDB Schema

```sql
CREATE TABLE pulse_events (
    event_id VARCHAR PRIMARY KEY,
    event_type VARCHAR,  -- 'post', 'reply', 'like', 'repost', 'mention'
    actor_did VARCHAR,
    actor_handle VARCHAR,
    subject_uri VARCHAR,
    text TEXT,
    created_at TIMESTAMP,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    engagement_snapshot JSON
);

CREATE TABLE engagement_deltas (
    delta_id VARCHAR PRIMARY KEY,
    post_uri VARCHAR,
    likes_delta INT,
    reposts_delta INT,
    replies_delta INT,
    velocity FLOAT,
    measured_at TIMESTAMP
);

CREATE TABLE network_trends (
    trend_id VARCHAR PRIMARY KEY,
    topic VARCHAR,
    mention_count INT,
    velocity FLOAT,
    first_seen TIMESTAMP,
    last_seen TIMESTAMP,
    peak_velocity FLOAT
);
```

## GF(3) Triad Integration

| Trit | Skill | Role |
|------|-------|------|
| -1 | influence-propagation | Validates network patterns |
| 0 | bisimulation-game | Coordinates equivalence |
| +1 | **pulse-mcp-stream** | Generates live data |

**Conservation**: (-1) + (0) + (+1) = 0 ✓

## Configuration

```yaml
# pulse-mcp-stream.yaml
connection:
  firehose_url: "wss://bsky.network/xrpc/com.atproto.sync.subscribeRepos"
  reconnect_delay_ms: 1000
  max_reconnect_attempts: 10

filters:
  collections:
    - app.bsky.feed.post
    - app.bsky.feed.like
    - app.bsky.feed.repost
  
buffering:
  max_buffer_size: 10000
  flush_interval_seconds: 30

export:
  db_path: "pulse_stream.duckdb"
  batch_size: 100

reproducibility:
  seed: 0xf061ebbc2ca74d78
```

## Justfile Recipes

```makefile
# Start pulse stream
pulse-start actor="barton.bsky.social":
    python3 -m pulse_mcp_stream subscribe "{{actor}}"

# Monitor engagement
pulse-engagement actor="barton.bsky.social":
    python3 -m pulse_mcp_stream engagement "{{actor}}"

# Detect trends
pulse-trends actor="barton.bsky.social" window="60":
    python3 -m pulse_mcp_stream trends "{{actor}}" --window "{{window}}"

# Export to DuckDB
pulse-export db="pulse.duckdb":
    python3 -m pulse_mcp_stream export --db "{{db}}"
```

## Related Skills

- `atproto-ingest` (Layer 1) - Batch data collection
- `influence-propagation` (Layer 7) - Network analysis
- `cognitive-surrogate` (Layer 6) - Pattern consumption
- `duckdb-timetravel` (Layer 3) - Data storage



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb

## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.