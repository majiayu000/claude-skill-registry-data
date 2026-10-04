---
name: mongodb
description: Query and manage MongoDB databases via Atlas Data API (curl) or mongosh. Connect to MongoDB Atlas collections without installing heavy CLI tools.
version: 1.0.0
allowed-tools: Bash
metadata:
  credentials:
    - MONGODB_DATA_API_URL
    - MONGODB_API_KEY
    - MONGODB_URL
---

# MongoDB Skill

Query MongoDB databases using the Atlas Data API (curl) or `mongosh` fallback.

## Quick Start

```bash
# Find documents via Atlas Data API
curl -s -X POST "$MONGODB_DATA_API_URL/action/find" \
  -H "api-key: $MONGODB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "dataSource": "'"$MONGODB_CLUSTER"'",
    "database": "'"$MONGODB_DATABASE"'",
    "collection": "users",
    "filter": {},
    "limit": 10
  }'
```

## Prerequisites

### Option A: Atlas Data API (Recommended — no CLI install needed)

| Variable | Description | Example |
|----------|-------------|---------|
| `MONGODB_DATA_API_URL` | Atlas Data API endpoint | `https://data.mongodb-api.com/app/data-xxxxx/endpoint/data/v1` |
| `MONGODB_API_KEY` | Atlas Data API key | `abc123...` |
| `MONGODB_CLUSTER` | Cluster name | `Cluster0` |
| `MONGODB_DATABASE` | Default database name | `myapp` |

### Option B: Connection String (for mongosh fallback)

| Variable | Description | Example |
|----------|-------------|---------|
| `MONGODB_URL` | Full connection string | `mongodb+srv://user:pass@cluster.mongodb.net/mydb` |

### Enable Atlas Data API

1. Go to MongoDB Atlas — App Services — Create Application
2. Enable Data API — Choose your cluster
3. Create an API key
4. Copy the endpoint URL

### Verify Setup

```bash
curl -s -X POST "$MONGODB_DATA_API_URL/action/find" \
  -H "api-key: $MONGODB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "dataSource": "'"$MONGODB_CLUSTER"'",
    "database": "'"$MONGODB_DATABASE"'",
    "collection": "users",
    "limit": 1
  }' | jq .
```

## Data API Recipes

### Find Documents

```bash
curl -s -X POST "$MONGODB_DATA_API_URL/action/find" \
  -H "api-key: $MONGODB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "dataSource": "'"$MONGODB_CLUSTER"'",
    "database": "'"$MONGODB_DATABASE"'",
    "collection": "users",
    "filter": {"status": "active"},
    "sort": {"created_at": -1},
    "limit": 20
  }' | jq '.documents'
```

### Find One Document

```bash
curl -s -X POST "$MONGODB_DATA_API_URL/action/findOne" \
  -H "api-key: $MONGODB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "dataSource": "'"$MONGODB_CLUSTER"'",
    "database": "'"$MONGODB_DATABASE"'",
    "collection": "users",
    "filter": {"email": "john@example.com"}
  }' | jq '.document'
```

### Insert One Document

```bash
curl -s -X POST "$MONGODB_DATA_API_URL/action/insertOne" \
  -H "api-key: $MONGODB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "dataSource": "'"$MONGODB_CLUSTER"'",
    "database": "'"$MONGODB_DATABASE"'",
    "collection": "users",
    "document": {
      "name": "John",
      "email": "john@example.com",
      "created_at": {"$date": "'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'"}
    }
  }' | jq .
```

### Update One Document

```bash
curl -s -X POST "$MONGODB_DATA_API_URL/action/updateOne" \
  -H "api-key: $MONGODB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "dataSource": "'"$MONGODB_CLUSTER"'",
    "database": "'"$MONGODB_DATABASE"'",
    "collection": "users",
    "filter": {"email": "john@example.com"},
    "update": {"$set": {"status": "active"}}
  }' | jq .
```

### Delete One Document

```bash
curl -s -X POST "$MONGODB_DATA_API_URL/action/deleteOne" \
  -H "api-key: $MONGODB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "dataSource": "'"$MONGODB_CLUSTER"'",
    "database": "'"$MONGODB_DATABASE"'",
    "collection": "users",
    "filter": {"email": "john@example.com"}
  }' | jq .
```

### Aggregate Pipeline

```bash
curl -s -X POST "$MONGODB_DATA_API_URL/action/aggregate" \
  -H "api-key: $MONGODB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "dataSource": "'"$MONGODB_CLUSTER"'",
    "database": "'"$MONGODB_DATABASE"'",
    "collection": "orders",
    "pipeline": [
      {"$match": {"status": "completed"}},
      {"$group": {"_id": "$customer_id", "total": {"$sum": "$amount"}, "count": {"$sum": 1}}},
      {"$sort": {"total": -1}},
      {"$limit": 10}
    ]
  }' | jq '.documents'
```

## mongosh Fallback

If you need interactive shell access or the Data API isn't available:

```bash
# Install mongosh on the fly (not pre-installed to save ~100MB)
npx mongosh "$MONGODB_URL" --eval "db.users.find().limit(10).toArray()"
```

### Common mongosh Commands

```bash
# List databases
npx mongosh "$MONGODB_URL" --eval "show dbs"

# List collections
npx mongosh "$MONGODB_URL" --eval "show collections"

# Count documents
npx mongosh "$MONGODB_URL" --eval "db.users.countDocuments()"

# Find with filter
npx mongosh "$MONGODB_URL" --eval "db.users.find({status: 'active'}).limit(10).toArray()"
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `401 Unauthorized` | Invalid API key | Check MONGODB_API_KEY |
| `no app found` | Wrong Data API URL | Verify MONGODB_DATA_API_URL in Atlas |
| `no rule exists` | Collection not allowed | Enable collection in Atlas Data API settings |
| `cannot find dataSource` | Wrong cluster name | Check MONGODB_CLUSTER matches Atlas |
| `connection refused` (mongosh) | Wrong URL | Verify MONGODB_URL connection string |

## Tips

- **Use Data API for simple CRUD** — no install needed, just curl
- **Use mongosh for complex work** — aggregations, admin tasks, interactive exploration
- **Always use `jq`** to format JSON responses from the Data API
- **Use `$date` wrapper** for date fields in Data API requests
- **Projection** — add `"projection": {"_id": 0, "name": 1, "email": 1}` to limit returned fields
- **Atlas Data API has rate limits** — 10,000 requests/minute per project
