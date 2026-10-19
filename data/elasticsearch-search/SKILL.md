---
name: elasticsearch-search
description: >
  Architect, index, query, and optimize Elasticsearch and OpenSearch distributed
  search clusters. Use when defining explicit schema mappings, configuring custom text
  analyzers (tokenizers and filters), authoring complex Query DSL searches (bool,
  multi_match, aggregations), tuning shard routing and bulk indexing throughput,
  managing Index Lifecycle Management (ILM) data tiers, or diagnosing cluster health.
compatibility: >
  Agent Skills-compatible coding agents administering or querying Elasticsearch 8+
  or OpenSearch 2+ distributed clusters via REST API or client libraries. Tooling is
  required only for executable validation.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "elasticsearch, opensearch, search, indexing, fulltext, aggregations, ilm, query-dsl, inverted-index"
  topics: "databases"
---

# Elasticsearch & OpenSearch Engineering

Elasticsearch and OpenSearch are distributed, JSON-based search and analytics engines built on Apache Lucene. They deliver near real-time full-text search, high-scale structured filtering, and multi-dimensional aggregations through inverted indexes, columnar doc values, and block k-d trees.

## Purpose & Overview

Search clusters suffer from common architectural failure modes: "mapping explosions" caused by unconstrained dynamic typing, unroutable or unassigned shards that degrade cluster health to yellow or red, inefficient queries triggering full cluster scatter-gather operations, and out-of-memory heap exhaustion during high-cardinality aggregations.

This skill equips agents with principles and production recipes to:
- Structure explicit index mappings with strict typing (`text`, `keyword`, `date`, `numeric`, `nested`).
- Build custom text analysis pipelines with specialized character filters, tokenizers, and token filters.
- Author robust search queries using the **Query DSL** (`bool`, `match`, `term`, `multi_match`, `fuzzy`, `range`).
- Execute multi-bucket and metric **aggregations** (`terms`, `date_histogram`, `percentiles`) while avoiding memory exhaustion.
- Optimize search latency and cluster load through explicit **routing keys** (`_routing`).
- Automate index retention, compression, and storage cost reduction with **Index Lifecycle Management (ILM)** across hot, warm, and cold tiers.
- Maximize write throughput with batched bulk indexing (`_bulk`) and tuned `refresh_interval` settings.
- Diagnose and resolve shard allocation failures and cluster state health degradation.

---

## Core Principles & Rules

1. **Disable Dynamic Field Mapping in Production**: Dynamic mapping converts unexpected incoming JSON keys into new index fields. This leads directly to "mapping explosion" (exceeding `index.mapping.total_fields.limit`), consuming JVM heap and crashing master nodes. Always set `"dynamic": "strict"` or `"dynamic": false` on production indices.
2. **Distinguish `text` from `keyword` Types**:
   - `text`: Analyzed through a tokenizer pipeline for full-text search. Cannot be sorted or aggregated on without expensive fielddata enabled.
   - `keyword`: Exact-value string stored unchanged into doc values. Used for filtering, sorting, and aggregations.
   - For multi-purpose string fields, use multi-fields (mapping the field as `text` with a `.keyword` sub-field).
3. **Keep Shard Sizes Between 20GB and 50GB**:
   - For search-intensive workloads: aim for 10GB to 30GB per shard.
   - For log/time-series workloads: aim for 30GB to 50GB per shard.
   - Avoid creating hundreds of small (< 1GB) shards: each shard consumes Lucene metadata overhead, open file handles, and JVM heap.
4. **Prefer Filter Context over Query Context**: Clauses inside `"filter"` or `"must_not"` compute boolean matches without calculating Lucene relevance scores (`_score`). Filter queries are automatically cached in node memory, drastically reducing CPU usage and response latency.
5. **Tune Refresh Intervals for Bulk Ingest**: The default `refresh_interval: 1s` creates a new Lucene segment every second, degrading indexing throughput and triggering constant segment merges. During high-throughput bulk ingestion, set `"refresh_interval": "30s"` or `"-1"`, and re-enable it after ingestion completes.
6. **Beware of High-Cardinality Terms Aggregations**: Aggregating on unbounded strings (e.g., UUIDs, transaction hashes, arbitrary URLs) without circuit breakers causes JVM heap exhaustion and cluster instability.

---

## Standard Workflows & Procedures

### Workflow 1: Creating an Explicit Mapping with Custom Analyzers

```
Raw Text Stream: "The Fast WiFi-6 Router (Model: AX-3000)!"
       │
       ▼ HTML Strip / Char Filters: Removes markup & replaces custom chars
       │
       ▼ Tokenizer: Breaks text into individual tokens (e.g., standard, whitespace)
       │ ["The", "Fast", "WiFi", "6", "Router", "Model", "AX", "3000"]
       │
       ▼ Token Filters: lowercase, remove stop words, apply synonyms, stem
       │ ["fast", "wifi", "6", "router", "model", "ax", "3000"]
       │
       ▼ Inverted Index Storage
```

```json
PUT /products_v1
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1,
    "analysis": {
      "filter": {
        "autocomplete_ngram": {
          "type": "edge_ngram",
          "min_gram": 2,
          "max_gram": 15
        }
      },
      "analyzer": {
        "product_search_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase", "asciifolding"]
        },
        "autocomplete_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase", "asciifolding", "autocomplete_ngram"]
        }
      }
    }
  },
  "mappings": {
    "dynamic": "strict",
    "properties": {
      "product_id": { "type": "keyword" },
      "tenant_id": { "type": "keyword" },
      "title": {
        "type": "text",
        "analyzer": "product_search_analyzer",
        "fields": {
          "autocomplete": {
            "type": "text",
            "analyzer": "autocomplete_analyzer",
            "search_analyzer": "product_search_analyzer"
          },
          "raw": { "type": "keyword" }
        }
      },
      "description": { "type": "text", "analyzer": "product_search_analyzer" },
      "price_cents": { "type": "integer" },
      "in_stock": { "type": "boolean" },
      "categories": { "type": "keyword" },
      "created_at": { "type": "date" }
    }
  }
}
```

### Workflow 2: Authoring Production Query DSL (Bool, Match, Filter)

A production search query combining relevance scoring on textual fields with strict, cached filtering on structured attributes:

```json
POST /products_v1/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "multi_match": {
            "query": "mesh router wifi 6",
            "fields": ["title^3", "description"],
            "type": "best_fields",
            "fuzziness": "AUTO",
            "prefix_length": 2
          }
        }
      ],
      "filter": [
        { "term": { "tenant_id": "tenant_eu_01" } },
        { "term": { "in_stock": true } },
        {
          "range": {
            "price_cents": {
              "gte": 5000,
              "lte": 30000
            }
          }
        }
      ]
    }
  },
  "sort": [
    { "_score": { "order": "desc" } },
    { "price_cents": { "order": "asc" } }
  ],
  "from": 0,
  "size": 20
}
```

### Workflow 3: Shard Allocation & Cluster Diagnostics

When cluster health degrades to `YELLOW` (missing replicas) or `RED` (missing primary shards):

1. **Inspect High-Level Cluster Health**:
   ```bash
   GET /_cluster/health?pretty
   ```
2. **List Problematic Shards**:
   ```bash
   GET /_cat/shards?v=true&h=index,shard,prirep,state,unassigned.reason,node
   ```
3. **Diagnose Unassigned Shard Root Cause**:
   ```json
   POST /_cluster/allocation/explain
   {
     "index": "products_v1",
     "shard": 0,
     "primary": true
   }
   ```
   Common root causes:
   - `DISK_LIMIT_WATERMARK`: Shards cannot allocate because disk usage exceeded low/high watermarks (85% / 90%).
   - `ALLOCATION_DELAYED`: Node briefly restarted, waiting on `delayed_timeout`.
   - `SAME_HOST_RULE`: Replica cannot be placed on the same physical host as its primary.

---

## Real-World Examples & Patterns

### Pattern 1: High-Performance Bulk Ingestion

Ingest documents using NDJSON batches with optimal batch size (typically 5MB to 15MB or 1,000 to 5,000 documents per batch):

```python
import json
import requests

def stream_bulk_index(es_url: str, index_name: str, documents: list[dict], batch_size: int = 1000):
    lines = []
    for doc in documents:
        # Action metadata header
        action = {"index": {"_index": index_name, "_id": doc["product_id"]}}
        # Optional routing: action["index"]["routing"] = doc["tenant_id"]
        lines.append(json.dumps(action))
        lines.append(json.dumps(doc))

        if len(lines) >= batch_size * 2:
            _send_bulk(es_url, lines)
            lines = []

    if lines:
        _send_bulk(es_url, lines)

def _send_bulk(es_url: str, lines: list[str]):
    payload = "\n".join(lines) + "\n"
    res = requests.post(
        f"{es_url}/_bulk",
        data=payload,
        headers={"Content-Type": "application/x-ndjson"},
        timeout=30,
    )
    res.raise_for_status()
    body = res.json()
    if body.get("errors"):
        for item in body.get("items", []):
            op = item.get("index") or item.get("create")
            if op and op.get("error"):
                print(f"Failed doc {op.get('_id')}: {op.get('error')}")
```

### Pattern 2: Multi-Bucket Aggregations (Time-Series Histogram + Metric)

Aggregating order volumes by date, computing total revenue, and calculating percentile latencies:

```json
POST /orders/_search
{
  "size": 0,
  "query": {
    "range": {
      "created_at": {
        "gte": "now-30d/d",
        "lte": "now/d"
      }
    }
  },
  "aggs": {
    "orders_over_time": {
      "date_histogram": {
        "field": "created_at",
        "calendar_interval": "day",
        "format": "yyyy-MM-dd"
      },
      "aggs": {
        "daily_revenue": {
          "sum": {
            "field": "total_cents"
          }
        },
        "order_percentiles": {
          "percentiles": {
            "field": "total_cents",
            "percents": [50.0, 95.0, 99.0]
          }
        }
      }
    }
  }
}
```

### Pattern 3: Multi-Tier Index Lifecycle Management (ILM)

Automate transitioning indices from high-IOPS NVMe nodes (Hot) down to cost-efficient object storage (Cold/Frozen):

```json
PUT /_ilm/policy/time_series_lifecycle
{
  "policy": {
    "phases": {
      "hot": {
        "min_age": "0ms",
        "actions": {
          "rollover": {
            "max_primary_shard_size": "40gb",
            "max_age": "7d"
          },
          "set_priority": { "priority": 100 }
        }
      },
      "warm": {
        "min_age": "14d",
        "actions": {
          "forcemerge": { "max_num_segments": 1 },
          "allocate": { "number_of_replicas": 1 },
          "set_priority": { "priority": 50 }
        }
      },
      "cold": {
        "min_age": "60d",
        "actions": {
          "allocate": { "number_of_replicas": 0 },
          "set_priority": { "priority": 0 }
        }
      },
      "delete": {
        "min_age": "180d",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}
```

---

## Common Anti-Patterns & Pitfalls

| Anti-Pattern | Operational Hazard | Correct Engineering Approach |
|:---|:---|:---|
| **Relying on Dynamic Field Mapping** | New arbitrary JSON keys inflate schema fields, resulting in master node OOM cluster crashes. | Set `"dynamic": "strict"` or `"dynamic": false` on production mappings. |
| **Over-Sharding (thousands of tiny shards)** | Excessive JVM memory consumption on Lucene metadata, high GC pressure, slow query coordination. | Size shards between 20GB and 50GB; consolidate small indices via ILM or Reindex. |
| **Searching with deep pagination (`from: 10000`)** | Coordinating node must collect and rank `from + size` results from every shard, exhausting heap. | Use `search_after` with point-in-time (`PIT`) for deep paging workflows. |
| **Enabling `fielddata: true` on `text` fields** | Loads entire inverted index terms into JVM heap for aggregation, frequently crashing data nodes. | Use `.keyword` sub-fields (doc values) for sorting and aggregations. |
| **Omitting Routing Key on Multi-Tenant Indices** | Every search scatters across all cluster shards, limiting throughput. | Index and query with `?routing=tenant_id` to constrain searches to a single shard. |
| **Unbounded `terms` Aggregations** | Running aggregations on high-cardinality fields (e.g. UUIDs) consumes gigabytes of heap memory. | Set moderate `"size"` parameters and ensure terms circuit breakers (`indices.breaker.fielddata`) are configured. |

---

## Verification Checklist

- [ ] Production index template defines explicit mappings with `"dynamic": "strict"`.
- [ ] Multi-fields configured with both `text` (analyzed search) and `keyword` (doc values aggregation/sort) where needed.
- [ ] Shard sizing validated to target 20GB-50GB per shard in production.
- [ ] Structured filter criteria are placed inside `filter` or `must_not` clauses to leverage query bitset caching.
- [ ] Deep pagination avoids large `from` offsets, using `search_after` with Point in Time (`PIT`).
- [ ] High-volume bulk indexing pipelines use the `_bulk` API with tuned `refresh_interval`.
- [ ] Multi-tenant data models evaluate `_routing` keys to avoid full cluster scatter-gather overhead.
- [ ] Index Lifecycle Management (ILM) configured for time-series indices (hot, warm, cold, delete phases).
- [ ] Cluster health returns `GREEN`, with zero unassigned shards and safe disk watermark thresholds.

---

## Tooling & Reference Guides

- **Elasticsearch Query DSL Guide**: Canonical reference for boolean queries, compound filters, and match expressions.
- **OpenSearch Core Documentation**: Architecture, indexing, search APIs, and performance tuning.
- **Cat APIs & Cluster APIs**: Diagnostic commands (`_cat/indices`, `_cat/shards`, `_cat/nodes`, `_cluster/allocation/explain`).
- **Elasticsearch / OpenSearch Official Clients**: Idiomatic SDKs for Python (`elasticsearch-py`), Node.js (`@elastic/elasticsearch`), and Go (`go-elasticsearch`).
- **Search Profiler API**: Query profiling tool (`"profile": true`) to measure per-shard Lucene execution time and component bottlenecks.
