---
name: elasticsearch
description: Query and manage Elasticsearch or OpenSearch clusters via REST API. Search, index, and aggregate data using curl.
version: 1.0.0
allowed-tools: Bash
metadata:
  credentials:
    - ELASTICSEARCH_URL
    - ES_API_KEY
---

# Elasticsearch Skill

Query and manage Elasticsearch/OpenSearch clusters using curl (REST API).

## Quick Start

```bash
# Check cluster health
curl -s "$ELASTICSEARCH_URL/_cluster/health?pretty"

# Search an index
curl -s "$ELASTICSEARCH_URL/users/_search?pretty" \
  -H "Content-Type: application/json" \
  -d '{"query": {"match_all": {}}, "size": 10}'
```

## Prerequisites

| Variable | Description | Example |
|----------|-------------|---------|
| `ELASTICSEARCH_URL` | Cluster URL (with auth) | `https://user:pass@my-cluster.es.io:9243` |
| `ES_API_KEY` | API key (alternative auth) | `base64encodedkey` |

### Auth Methods

```bash
# Method 1: Credentials in URL
export ELASTICSEARCH_URL="https://elastic:password@my-cluster.es.io:9243"
curl -s "$ELASTICSEARCH_URL/_cluster/health?pretty"

# Method 2: API Key header
curl -s "$ELASTICSEARCH_URL/_cluster/health?pretty" \
  -H "Authorization: ApiKey $ES_API_KEY"
```

### Verify Connection

```bash
curl -s "$ELASTICSEARCH_URL/?pretty"
```

## Cluster Information

### Cluster Health

```bash
curl -s "$ELASTICSEARCH_URL/_cluster/health?pretty"
```

### List Indices

```bash
curl -s "$ELASTICSEARCH_URL/_cat/indices?v&s=store.size:desc"
```

### Node Info

```bash
curl -s "$ELASTICSEARCH_URL/_cat/nodes?v"
```

## Search Recipes

### Match All (list documents)

```bash
curl -s "$ELASTICSEARCH_URL/users/_search?pretty" \
  -H "Content-Type: application/json" \
  -d '{"query": {"match_all": {}}, "size": 10}'
```

### Full-Text Search

```bash
curl -s "$ELASTICSEARCH_URL/articles/_search?pretty" \
  -H "Content-Type: application/json" \
  -d '{
    "query": {
      "match": {"title": "machine learning"}
    },
    "size": 10
  }'
```

### Multi-Field Search

```bash
curl -s "$ELASTICSEARCH_URL/articles/_search?pretty" \
  -H "Content-Type: application/json" \
  -d '{
    "query": {
      "multi_match": {
        "query": "elasticsearch tutorial",
        "fields": ["title^2", "body", "tags"]
      }
    }
  }'
```

### Filter by Field

```bash
curl -s "$ELASTICSEARCH_URL/users/_search?pretty" \
  -H "Content-Type: application/json" \
  -d '{
    "query": {
      "term": {"status": "active"}
    }
  }'
```

### Range Query

```bash
curl -s "$ELASTICSEARCH_URL/orders/_search?pretty" \
  -H "Content-Type: application/json" \
  -d '{
    "query": {
      "range": {
        "created_at": {
          "gte": "2024-01-01",
          "lt": "2024-02-01"
        }
      }
    }
  }'
```

### Bool Query (combine conditions)

```bash
curl -s "$ELASTICSEARCH_URL/users/_search?pretty" \
  -H "Content-Type: application/json" \
  -d '{
    "query": {
      "bool": {
        "must": [{"match": {"role": "admin"}}],
        "filter": [{"term": {"status": "active"}}],
        "must_not": [{"term": {"banned": true}}]
      }
    }
  }'
```

### Search with Sorting

```bash
curl -s "$ELASTICSEARCH_URL/users/_search?pretty" \
  -H "Content-Type: application/json" \
  -d '{
    "query": {"match_all": {}},
    "sort": [{"created_at": "desc"}],
    "size": 20
  }'
```

### Select Specific Fields

```bash
curl -s "$ELASTICSEARCH_URL/users/_search?pretty" \
  -H "Content-Type: application/json" \
  -d '{
    "query": {"match_all": {}},
    "_source": ["name", "email", "created_at"],
    "size": 10
  }'
```

## Aggregations

### Count by Field

```bash
curl -s "$ELASTICSEARCH_URL/users/_search?pretty" \
  -H "Content-Type: application/json" \
  -d '{
    "size": 0,
    "aggs": {
      "by_status": {
        "terms": {"field": "status.keyword"}
      }
    }
  }'
```

### Average Value

```bash
curl -s "$ELASTICSEARCH_URL/orders/_search?pretty" \
  -H "Content-Type: application/json" \
  -d '{
    "size": 0,
    "aggs": {
      "avg_amount": {"avg": {"field": "amount"}}
    }
  }'
```

### Date Histogram

```bash
curl -s "$ELASTICSEARCH_URL/orders/_search?pretty" \
  -H "Content-Type: application/json" \
  -d '{
    "size": 0,
    "aggs": {
      "orders_over_time": {
        "date_histogram": {
          "field": "created_at",
          "calendar_interval": "month"
        }
      }
    }
  }'
```

## Document Operations

### Get Document by ID

```bash
curl -s "$ELASTICSEARCH_URL/users/_doc/1?pretty"
```

### Index a Document

```bash
curl -s -X POST "$ELASTICSEARCH_URL/users/_doc" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John",
    "email": "john@example.com",
    "status": "active",
    "created_at": "'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'"
  }' | jq .
```

### Update a Document

```bash
curl -s -X POST "$ELASTICSEARCH_URL/users/_update/1" \
  -H "Content-Type: application/json" \
  -d '{"doc": {"status": "inactive"}}'
```

### Delete a Document

```bash
curl -s -X DELETE "$ELASTICSEARCH_URL/users/_doc/1"
```

### Bulk Insert

```bash
curl -s -X POST "$ELASTICSEARCH_URL/_bulk" \
  -H "Content-Type: application/x-ndjson" \
  -d '
{"index": {"_index": "users"}}
{"name": "Alice", "email": "alice@example.com"}
{"index": {"_index": "users"}}
{"name": "Bob", "email": "bob@example.com"}
'
```

## Index Management

### Create Index with Mapping

```bash
curl -s -X PUT "$ELASTICSEARCH_URL/users" \
  -H "Content-Type: application/json" \
  -d '{
    "mappings": {
      "properties": {
        "name": {"type": "text"},
        "email": {"type": "keyword"},
        "status": {"type": "keyword"},
        "age": {"type": "integer"},
        "created_at": {"type": "date"}
      }
    }
  }'
```

### Get Index Mapping

```bash
curl -s "$ELASTICSEARCH_URL/users/_mapping?pretty"
```

### Delete Index

```bash
curl -s -X DELETE "$ELASTICSEARCH_URL/users"
```

## Managed Service Setup

### Elastic Cloud
1. Sign up at cloud.elastic.co
2. Create a deployment
3. Copy the Elasticsearch endpoint URL
4. Create an API key: Kibana — Stack Management — API Keys

### AWS OpenSearch
- Use the domain endpoint from AWS Console
- Auth via IAM or master user credentials

### Self-Hosted
- Default: `http://localhost:9200`
- With auth: `https://elastic:password@localhost:9200`

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `401 Unauthorized` | Bad credentials | Check URL credentials or ES_API_KEY |
| `index_not_found` | Index doesn't exist | List indices with `_cat/indices` |
| `mapper_parsing_exception` | Wrong field type | Check mapping with `_mapping` |
| `search_phase_execution` | Query syntax error | Validate JSON body |
| Connection refused | Host unreachable | Check ELASTICSEARCH_URL |

## Tips

- **Use `?pretty`** for human-readable JSON output
- **Use `_source`** to limit returned fields — reduces response size
- **Use `size: 0`** for aggregations when you don't need documents
- **Use `.keyword`** suffix for exact match on text fields
- **Use `_cat` APIs** for quick overviews: `_cat/indices`, `_cat/nodes`, `_cat/health`
- **Pipe to `jq`** for JSON processing: `| jq '.hits.hits[]._source'`
- **Bulk API** is much faster than individual inserts for large datasets
