---
name: db-comparison
description: Database selection — strengths and use-case mapping by type.
---

### Relational
| Database | Strengths | Watch out for |
|----------|-----------|---------------|
| **PostgreSQL** | Full SQL, JSONB, extensions, ACID | Config tuning needed for performance |
| **MySQL / MariaDB** | Wide support, simple ops | Less feature-rich than Postgres |
| **SQL Server** | Enterprise features, .NET integration | Licensing cost |
| **SQLite** | Zero config, embedded | Not for concurrent writes |

### Document
| Database | Strengths | Watch out for |
|----------|-----------|---------------|
| **MongoDB** | Flexible schema, horizontal scale | No joins, eventual consistency tradeoffs |
| **Firestore** | Real-time, serverless-friendly | Query limitations, cost at scale |
| **Cosmos DB** | Multi-model, global distribution | Complex pricing, learning curve |

### Key-Value / Cache
| Database | Use case |
|----------|----------|
| **Redis** | Cache, sessions, queues, pub/sub, leaderboards |
| **Memcached** | Simple distributed cache |
| **ElastiCache / Memorystore / Azure Cache** | Managed Redis/Memcached |

### Column-Family
| Database | Use case |
|----------|----------|
| **Cassandra / Keyspaces** | High-write, time-series, distributed |
| **Bigtable** | Analytics, IoT, wide-column |

### Vector / AI
| Database | Use case |
|----------|----------|
| **pgvector** (PostgreSQL ext.) | Semantic search, embeddings, RAG pipelines — load `skills/architecture/llm-integration/SKILL.md` |
| **Dedicated vector DBs** | Pinecone, Weaviate, Qdrant — when Postgres can't scale the vector workload |

### Managed Cloud (defer to cloud specialists when infra decisions needed)
- **AWS**: RDS, Aurora, DynamoDB, ElastiCache, DocumentDB, Redshift
- **GCP**: Cloud SQL, Spanner, Firestore, Bigtable, Memorystore, BigQuery
- **Azure**: Azure SQL, Cosmos DB, Cache for Redis, Synapse Analytics
