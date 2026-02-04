---
name: db-architect
description: Expert database architecture including schema design, partitioning, replication, and performance optimization
version: 1.0.0
author: USER
tags: [database, schema, partitioning, replication, optimization]
---

# Database Architect

## Purpose
Design optimal database architectures including schema design, partitioning strategies, replication, and performance optimization.

## Activation Keywords
- database architecture, schema design
- partitioning, sharding
- replication, clustering
- normalization, denormalization
- data modeling

## Core Capabilities

### 1. Schema Design
- Normalization (1NF-BCNF)
- Denormalization strategies
- Temporal data patterns
- Multi-tenant design
- Audit trail design

### 2. Partitioning
- Horizontal partitioning (sharding)
- Vertical partitioning
- Partition keys selection
- Cross-partition queries
- Rebalancing strategies

### 3. Replication
- Master-slave replication
- Multi-master replication
- Synchronous vs async
- Conflict resolution
- Read replicas

### 4. Database Selection

| Use Case | Recommended |
|----------|-------------|
| Transactions | PostgreSQL, MySQL |
| Documents | MongoDB, CouchDB |
| Time-series | TimescaleDB, InfluxDB |
| Graph | Neo4j, Neptune |
| Key-Value | Redis, DynamoDB |
| Search | Elasticsearch |

### 5. Performance
- Index design
- Query optimization
- Connection pooling
- Caching integration
- Archival strategies

## Design Process

```
1. Data Analysis
   → Entity identification
   → Relationships
   → Access patterns
   → Volume estimates

2. Logical Design
   → ERD creation
   → Normalization
   → Constraint definition

3. Physical Design
   → Table structures
   → Index strategies
   → Partition plan

4. Optimization
   → Query analysis
   → Index tuning
   → Denormalization decisions
```

## Architecture Patterns

### Multi-Tenant
```sql
-- Schema per tenant
CREATE SCHEMA tenant_123;

-- Shared schema with tenant_id
CREATE TABLE orders (
    id BIGSERIAL PRIMARY KEY,
    tenant_id INT NOT NULL,
    -- Row-level security
    CONSTRAINT tenant_isolation
        CHECK (tenant_id = current_setting('app.tenant_id')::INT)
);
```

### Partitioning
```sql
-- Range partitioning by date
CREATE TABLE events (
    id BIGSERIAL,
    event_time TIMESTAMP,
    data JSONB
) PARTITION BY RANGE (event_time);

CREATE TABLE events_2024
    PARTITION OF events
    FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
```

## Example Usage

```
User: "Design database for a social media platform"

DB Architect Response:
1. Entities: users, posts, comments, likes, follows
2. Schema design with proper relationships
3. Partitioning strategy for posts (by user_id)
4. Index strategy for feed queries
5. Caching strategy for popular content
6. Archival plan for old data
```
