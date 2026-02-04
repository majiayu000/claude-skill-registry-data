---
name: database-analyzer
description: Analyze and optimize database schemas, identify performance issues, and suggest improvements. Use when working with database structure, indexes, or query performance.
---

# Database Analyzer Skill

This skill helps you analyze database schemas, identify optimization opportunities, and understand table relationships.

## Instructions

1. **Identify the target:** Determine which table or schema to analyze
2. **Gather context:** Understand the current usage patterns and performance concerns
3. **Analyze structure:** Examine table definitions, indexes, and relationships
4. **Identify issues:** Look for missing indexes, improper data types, or inefficient structures
5. **Suggest improvements:** Provide specific, actionable recommendations

## Examples

### Example 1: Basic Table Analysis

**User request:** "Analyze the users table for optimization opportunities"

**Approach:**
- Check table structure and data types
- Verify indexes on frequently queried columns
- Look for redundant or missing indexes
- Suggest appropriate data types for columns

**Analysis Steps:**
```sql
-- 1. Get table structure
DESCRIBE users;

-- 2. Check existing indexes
SHOW INDEX FROM users;

-- 3. Analyze table statistics
ANALYZE TABLE users;
```

**Common Issues to Check:**
- Missing indexes on foreign keys
- Text columns that should be ENUM or SET
- Missing or excessive indexes
- Improper data types (e.g., VARCHAR when INT would suffice)

### Example 2: Performance Investigation

**User request:** "Why are queries on the orders table slow?"

**Approach:**
- Identify frequently executed queries
- Check for missing indexes on WHERE/JOIN columns
- Analyze table size and growth patterns
- Suggest partitioning if appropriate

**Investigation Steps:**
```sql
-- 1. Check table size
SELECT
    table_name,
    round(((data_length + index_length) / 1024 / 1024), 2) AS 'Size (MB)'
FROM information_schema.TABLES
WHERE table_name = 'orders';

-- 2. Identify slow queries
SHOW PROCESSLIST;

-- 3. Check query execution plan
EXPLAIN SELECT * FROM orders WHERE customer_id = 123;
```

**Optimization Recommendations:**
- Add composite indexes for common query patterns
- Consider partitioning by date for large historical tables
- Archive old data to separate tables
- Optimize data types to reduce row size

### Example 3: Index Optimization

**User request:** "Review indexes on the products table"

**Approach:**
- List all current indexes
- Identify unused or redundant indexes
- Check for missing indexes on query patterns
- Calculate index selectivity

**Review Process:**
```sql
-- 1. Show all indexes
SHOW INDEX FROM products;

-- 2. Check index usage (MySQL 5.6+)
SELECT * FROM sys.schema_unused_indexes
WHERE object_schema = 'your_database'
  AND object_name = 'products';

-- 3. Analyze query patterns
SELECT DISTINCT column_name
FROM information_schema.statistics
WHERE table_name = 'products';
```

## Requirements

- Access to database schema information
- Understanding of SQL and database design principles
- Ability to read EXPLAIN query plans (if available)
- Knowledge of the application's query patterns

## Best Practices

- **Always explain the reasoning** behind suggestions
- **Consider both read and write performance** impacts
- **Account for data volume** and growth patterns
- **Suggest incremental improvements** when possible
- **Document assumptions** made during analysis
- **Provide migration scripts** for proposed changes
- **Test recommendations** in a non-production environment first

## Common Patterns

### Pattern 1: E-commerce Database
- Heavy read operations on product catalog
- Frequent JOIN operations between products, categories, and prices
- Date-based queries for orders
- **Key optimizations:** Composite indexes, query caching, read replicas

### Pattern 2: User Management System
- Frequent lookups by email or username
- Session management with expiration
- Role-based access control queries
- **Key optimizations:** Unique indexes, covering indexes, denormalization

### Pattern 3: Analytics Database
- Large aggregation queries
- Time-series data
- Reporting queries with multiple JOINs
- **Key optimizations:** Partitioning, summary tables, columnstore indexes

## Troubleshooting

### No Slow Queries Detected
- Check slow query log settings
- Verify logging is enabled
- Look for queries with high execution count (not just slow time)

### Index Not Being Used
- Check index selectivity (should be high)
- Verify query uses indexed columns in WHERE clause
- Consider forcing index with USE INDEX hint for testing
- Check for implicit type conversions preventing index use

### Table Lock Contention
- Identify long-running transactions
- Consider using InnoDB over MyISAM for row-level locking
- Optimize batch operations to reduce lock time

## Resources

Bundled resources in this skill package:
- `references/schema-patterns.sql` - Common schema patterns
- `scripts/analyze-table.php` - Automated analysis script
- `assets/optimization-checklist.md` - Comprehensive checklist

Use base directory from `composer read-skill` output to locate these files.

## Notes

- Always backup before making schema changes
- Test in development environment first
- Monitor performance before and after changes
- Document all modifications for team awareness
