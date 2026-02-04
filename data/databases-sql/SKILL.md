---
name: databases-sql
description: SQL database querying, optimization, and data management for analytics
version: "2.0.0"
sasmp_version: "2.0.0"
bonded_agent: 02-sql-databases-expert
bond_type: PRIMARY_BOND

# Skill Configuration
config:
  atomic: true
  retry_enabled: true
  max_retries: 3
  backoff_strategy: exponential
  query_timeout: 120

# Parameter Validation
parameters:
  database_type:
    type: string
    required: true
    enum: [postgresql, mysql, sqlserver, sqlite, bigquery, snowflake]
    default: postgresql
  skill_level:
    type: string
    required: true
    enum: [beginner, intermediate, advanced, expert]
    default: beginner
  focus_area:
    type: string
    required: false
    enum: [queries, optimization, design, warehousing, all]
    default: all

# Observability
observability:
  logging_level: info
  metrics: [query_count, execution_time, optimization_score]
  query_logging: true
---

# Databases & SQL Skill

## Overview
Master SQL and database concepts essential for data analysts, from basic queries to advanced optimization and data warehousing.

## Core Topics

### SQL Fundamentals
- SELECT, FROM, WHERE, ORDER BY
- JOINs (INNER, LEFT, RIGHT, FULL)
- GROUP BY and aggregate functions
- Subqueries and CTEs

### Advanced SQL
- Window functions (ROW_NUMBER, RANK, LAG, LEAD)
- Recursive queries
- Query optimization and execution plans
- Index strategies

### Database Concepts
- Relational database design principles
- Normalization and denormalization
- Data warehousing concepts (star schema, snowflake)
- ETL processes

### Popular Platforms
- PostgreSQL
- MySQL
- SQL Server
- BigQuery, Redshift, Snowflake

## Learning Objectives
- Write efficient SQL queries for data extraction
- Understand database design and optimization
- Work with cloud data warehouses
- Implement ETL processes for analytics pipelines

## Error Handling

| Error Type | Cause | Recovery |
|------------|-------|----------|
| Syntax error | Invalid SQL | Validate query syntax before execution |
| Timeout | Long-running query | Add indexes, optimize query |
| Connection failed | Network/auth issue | Retry with exponential backoff |
| Permission denied | Access rights | Request appropriate permissions |
| Deadlock | Concurrent transactions | Retry transaction |

## Related Skills
- foundations (for data concepts)
- programming (for SQL with Python/R)
- advanced (for big data processing)
