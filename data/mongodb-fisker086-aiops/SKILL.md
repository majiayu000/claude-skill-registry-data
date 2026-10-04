---
name: mongodb
description: Query MongoDB databases, collections, and documents
activation_keywords: [mongodb, mongo, database, document, nosql]
execution_mode: client
---

# MongoDB Skill

Provides read-only MongoDB operations via local CLI:
- List databases and collections
- Find documents with filters
- Count documents
- Explain query execution plans
- Get collection stats and indexes

Use `builtin_mongodb` tool with fields:
- `operation`: one of "list_dbs", "list_collections", "find", "count", "explain", "stats", "indexes"
- `connection_string`: MongoDB connection string (default: "mongodb://localhost:27017")
- `database`: database name (required for list_collections/find/count/explain/stats/indexes)
- `collection`: collection name (required for find/count/explain/stats/indexes)
- `filter`: JSON filter document (for find, default: "{}")
- `limit`: max documents to return (default: 20)
- `sort`: JSON sort document (for find)

Note: Requires mongosh CLI installed.
All operations are read-only.
