---
name: database-optimization
description: Optimize SQL queries, indexes, and identify N+1 problems. Use for database performance and migration review.
context: fork
globs: ["**/models/**", "**/queries/**"]
alwaysApply: false
---

# Database Optimization Skill

## When to Use

Use this skill when:
- Optimizing slow SQL queries
- Analyzing missing or redundant indexes
- Reviewing Alembic migrations for safety
- Identifying N+1 query problems
- Designing database schemas
- Planning data migrations
- Reviewing query execution plans

## Optimization Checklist

### 1. Index Analysis

```sql
-- Check missing indexes
SELECT schemaname, tablename, indexname, indexdef
FROM pg_indexes
WHERE tablename = 'your_table';

-- Identify unused indexes
SELECT * FROM pg_stat_user_indexes
WHERE idx_scan = 0;
```

**Index Recommendations:**
```
✅ Always index:
- Primary keys (automatic)
- Foreign keys
- Columns in WHERE clauses
- Columns in ORDER BY
- Columns in JOIN conditions

❌ Avoid indexing:
- Low cardinality columns (boolean, status)
- Frequently updated columns
- Small tables (<1000 rows)
```

### 2. N+1 Query Detection

```python
# ❌ N+1 Problem
users = await session.execute(select(User))
for user in users:
    # This triggers N additional queries!
    orders = await session.execute(
        select(Order).where(Order.user_id == user.id)
    )

# ✅ Solution: Eager loading
from sqlalchemy.orm import selectinload

users = await session.execute(
    select(User).options(selectinload(User.orders))
)
```

### 3. Query Optimization Patterns

```python
# ✅ Use pagination
from sqlalchemy import select
from app.models import Product

async def get_products(skip: int = 0, limit: int = 20):
    query = select(Product).offset(skip).limit(limit)
    result = await session.execute(query)
    return result.scalars().all()

# ✅ Use specific columns (not SELECT *)
query = select(Product.id, Product.name, Product.price)

# ✅ Use exists() for existence checks
from sqlalchemy import exists
query = select(exists().where(User.email == email))
```

### 4. Migration Safety

```python
# ✅ Safe migration patterns
def upgrade():
    # Add column with default (no table lock)
    op.add_column('users', sa.Column('status', sa.String(20), 
                                      server_default='active'))

# ❌ Dangerous patterns
def upgrade():
    # Avoid: Rename column (breaks app)
    op.alter_column('users', 'name', new_column_name='full_name')
    
    # Avoid: Change column type (data loss risk)
    op.alter_column('users', 'age', type_=sa.String())
```

### 5. Async Best Practices

```python
# ✅ Proper async session handling
from sqlalchemy.ext.asyncio import AsyncSession

async def get_user(session: AsyncSession, user_id: int):
    result = await session.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalar_one_or_none()

# ✅ Bulk operations
async def bulk_insert(session: AsyncSession, items: list):
    session.add_all(items)
    await session.commit()
```

## Output Format

```markdown
## Database Optimization Report

### Query Analysis
- Queries analyzed: X
- Slow queries (>100ms): X
- N+1 problems: X

### Index Recommendations
| Table | Column | Type | Reason |
|-------|--------|------|--------|
| users | email | UNIQUE | WHERE clause filter |
| orders | user_id | INDEX | Foreign key JOIN |

### Optimization Suggestions
1. [Query] - [Current time] - [Optimized time] - [How]

### Migration Review
- ✅ Safe to run
- ⚠️ Requires maintenance window
- ❌ Breaking change detected
```

## Example Usage

```
@database Optimize the slow query in order_service.py:120
@database Review the new migration for safety issues
@database Find N+1 problems in the user module
@database Suggest indexes for the products table
```

## LLM-Assisted Index Optimization

### Automatic Index Discovery from EXPLAIN ANALYZE

```python
import re
from dataclasses import dataclass, field

@dataclass
class IndexRecommendation:
    table: str
    columns: list[str]
    reason: str
    estimated_impact: str  # HIGH / MEDIUM / LOW
    query_pattern: str

class LLMIndexAdvisor:
    """Uses LLM to analyze EXPLAIN ANALYZE output and recommend indexes."""
    
    INDEX_PROMPT = """Analyze this PostgreSQL EXPLAIN ANALYZE output and recommend indexes:
    
{explain_output}

The query was:
{query}

Rules:
1. Sequential scans on large tables -> recommend index
2. Missing composite indexes for multi-column WHERE clauses
3. Partial indexes for filtered queries (WHERE status = 'active')
4. Covering indexes for SELECT * queries with many columns
5. Consider existing indexes to avoid duplicates

Return recommendations as JSON array with: table, columns, reason, estimated_impact
"""
    
    @classmethod
    async def analyze(cls, explain_output: str, query: str) -> list[IndexRecommendation]:
        """Generate index recommendations from EXPLAIN ANALYZE output."""
        # Uses LLM (via the configured model tier) to analyze the plan
        # Returns structured recommendations
        pass
    
    @classmethod
    async def validate_index_impact(cls, index_ddl: str) -> str:
        """Validate an index by running EXPLAIN ANALYZE before and after."""
        # Run EXPLAIN ANALYZE with the query
        # Create the index
        # Run EXPLAIN ANALYZE again
        # Compare costs and return diff
        pass
```

### Real-Time Query Pattern Detection

```python
@dataclass
class QueryPattern:
    fingerprint: str  # Normalized query form
    frequency: int    # Times executed
    avg_time_ms: float
    table_scans: bool
    missing_index_score: float  # 0-1

class PatternAnalyzer:
    """Detect query patterns and suggest optimizations using LLM."""
    
    @staticmethod
    async def detect_patterns(pg_stat_statements: list[dict]) -> list[QueryPattern]:
        """Analyze pg_stat_statements output for optimization opportunities."""
        # Group by normalized query
        # Sort by total_time descending
        # Flag sequential scans on large result sets
        # Use LLM to suggest index strategies
        pass
```

### Migration Safety Review with LLM

```python
class MigrationSafetyReviewer:
    """Review Alembic migrations for safety concerns using LLM."""
    
    REVIEW_PROMPT = """Review this Alembic migration for safety:
    
{migration_code}

Check for:
1. Long-running locks (ADD COLUMN DEFAULT, ALTER TYPE)
2. Blocking operations (DROP COLUMN without expand-contract)
3. Data loss potential (DROP TABLE, TRUNCATE)
4. Missing indexes on new foreign key columns
5. Nullability changes that could break existing code
"""
    
    @classmethod
    async def review(cls, migration_sql: str) -> list[dict]:
        """Review migration for safety issues."""
        # Pass migration to LLM for safety analysis
        # Return structured findings with severity
        pass
```

---

## Appendix: General Performance Optimization

Additional performance optimization patterns beyond database-specific concerns.

### Caching Strategy

```python
class CachingService:
    def __init__(self, redis_client):
        self.redis = redis_client
    
    async def get_user(self, user_id: int):
        # Try cache first
        cached = await self.redis.get(f"user:{user_id}")
        if cached:
            return json.loads(cached)
        
        # Cache miss - fetch from DB
        user = await db.query(User).filter(User.id == user_id).first()
        
        # Cache for 1 hour
        await self.redis.setex(
            f"user:{user_id}",
            3600,
            json.dumps(user.dict())
        )
        return user

# Cache invalidation on update
async def update_user(user_id: int, data):
    user = await db.query(User).filter(User.id == user_id).first()
    user.update(data)
    await db.commit()
    
    # Invalidate cache
    await self.redis.delete(f"user:{user_id}")
```

### Monitoring Performance

```python
# Add timing middleware
@app.middleware("http")
async def add_timing_header(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    response.headers["X-Process-Time"] = str(duration)
    logger.info(f"{request.url.path} took {duration:.3f}s")
    return response
```

### Performance Checklist

- [ ] Identified slow queries (with EXPLAIN ANALYZE)
- [ ] Indexes added on WHERE/JOIN/ORDER BY columns
- [ ] N+1 queries fixed (eager loading)
- [ ] Caching implemented for hot data
- [ ] Pagination added to list endpoints
- [ ] Batch operations where possible
- [ ] Connection pooling configured
- [ ] Monitoring/alerting in place
