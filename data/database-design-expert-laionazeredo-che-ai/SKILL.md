---
name: "database-design-expert"
description: "Master guide for database architecture and schema design. Covers normalization, indexing, migration patterns, and performance optimization for SQL and NoSQL."
---

# Database Design Expert Guide

This skill provides the architectural standards for designing robust, scalable, and performant data layers.

## 🏗 Schema Modeling
- **Relational (SQL)**: Follow 3NF for consistency. Use denormalization only for proven performance bottlenecks.
- **NoSQL**: Model for access patterns. Optimize for read/write ratios and data locality.
- **Entities**: Define clear primary keys (UUIDs preferred for distributed systems) and foreign key constraints.

## 🚀 Performance & Indexing
- **Indexing**: Use B-tree for range/equality, GIN for search, and covering indexes to avoid table lookups.
- **Query Optimization**: Use `EXPLAIN` to identify sequential scans and costly joins.
- **Partitioning**: Implement table partitioning for large datasets (time-series or categorical).

## ⚡ Migrations & Lifecycle
- **Declarative Migrations**: Use version-controlled migrations. Ensure migrations are reversible (Up/Down).
- **Zero-Downtime**: Design schema changes that don't block reads/writes (e.g., adding nullable columns first).
- **Data Integrity**: Enforce rules at the database level via constraints and triggers.

## 🔗 References
- [Database Design Patterns](https://microservices.io/patterns/data/database-per-service.html)
- [Postgres Performance Wiki](https://wiki.postgresql.org/wiki/Performance_Optimization)
