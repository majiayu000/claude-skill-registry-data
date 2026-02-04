---
name: "SQL Development"
description: "Design efficient database schemas, write optimized queries with proper indexes, and manage data operations following best practices"
category: "database"
required_tools: ["Read", "Write", "Edit", "Bash"]
---

# SQL Development

## Purpose
Design efficient database schemas, write optimized SQL queries, and manage data operations following database best practices and performance patterns.

## When to Use
- Designing database schemas
- Writing data queries
- Optimizing slow queries
- Creating database migrations
- Managing data relationships

## Key Capabilities
1. **Schema Design** - Create normalized, efficient table structures
2. **Query Optimization** - Write performant SELECT, INSERT, UPDATE, DELETE
3. **Index Strategy** - Design indexes for query performance

## Approach
1. Design schema following normalization principles
2. Define primary keys, foreign keys, and constraints
3. Write queries using proper JOINs and WHERE clauses
4. Create indexes for frequently queried columns
5. Use EXPLAIN to analyze query performance
6. Test with realistic data volumes

## Example
**Context**: Task management database
````sql
-- Schema Design
CREATE TABLE tasks (
    id VARCHAR(50) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    assigned_agent VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL,
    priority VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP NULL,
    completed_at TIMESTAMP NULL,
    INDEX idx_status (status),
    INDEX idx_agent_status (assigned_agent, status),
    INDEX idx_created (created_at)
);

-- Optimized Query
SELECT t.id, t.title, t.status, a.name as agent_name
FROM tasks t
JOIN agents a ON t.assigned_agent = a.agent_file
WHERE t.status IN ('pending', 'active')
  AND t.priority = 'high'
ORDER BY t.created_at DESC
LIMIT 10;
````

## Best Practices
- ✅ Use indexes on frequently queried columns
- ✅ Avoid SELECT * - specify needed columns
- ✅ Use prepared statements to prevent SQL injection
- ✅ Normalize data to reduce redundancy
- ❌ Avoid: N+1 query problems
- ❌ Avoid: Missing WHERE clause on large tables

