---
name: postgresql-database
description: Expert PostgreSQL database development skill covering schema design, normalization, Alembic migrations, SQLAlchemy ORM patterns, query optimization, index strategies, JSONB for flexible data, and full-text search. Use when designing database schemas, creating migrations, optimizing queries, implementing full-text search, or working with PostgreSQL-specific features like JSONB.
---

# PostgreSQL Database Development

## Overview

Master PostgreSQL database development with comprehensive guidance on schema design, migrations, ORM patterns, and advanced PostgreSQL features. This skill provides best practices, reference documentation, and automation scripts for building high-performance, well-structured PostgreSQL databases.

## When to Use This Skill

Use this skill when working on:
- Database schema design and normalization
- Creating or reviewing Alembic migrations
- Defining SQLAlchemy models and relationships
- Optimizing slow queries or improving database performance
- Choosing and implementing index strategies
- Working with JSONB for semi-structured data
- Implementing full-text search functionality
- Analyzing database performance issues
- Setting up database projects from scratch

## Core Capabilities

### 1. Schema Design and Normalization

Consult `references/schema_design.md` for:
- Database normalization (1NF, 2NF, 3NF) with practical examples
- Common design patterns (one-to-many, many-to-many, self-referential)
- Polymorphic associations and inheritance patterns
- Audit trail and temporal data patterns
- Soft delete implementation
- Anti-patterns to avoid (EAV, god tables, etc.)

**When to read this reference:**
- Designing new database schemas
- Reviewing existing schema for normalization issues
- Implementing common relationship patterns
- Adding audit trails or soft deletes

**Example usage:**
```
When designing a new user management system, reference schema_design.md for:
- Proper normalization of user attributes
- Many-to-many relationship patterns for user roles
- Audit trail implementation to track user changes
```

### 2. Alembic Migration Workflows

Consult `references/alembic_migrations.md` for:
- Initial Alembic setup and configuration
- Auto-generating migrations from SQLAlchemy models
- Manual migration creation for complex changes
- Adding/modifying columns, indexes, and constraints
- Data migrations and transformations
- PostgreSQL-specific features (ENUM, JSONB, extensions)
- Production-safe migration practices (CONCURRENTLY)
- Branching and merging strategies
- Common issues and solutions

**Automation script:** `scripts/init_alembic.py`
- Initializes Alembic with best practices
- Configures environment variable support
- Creates custom migration templates
- Generates comprehensive README

**When to use:**
```bash
# Initialize new project with Alembic
python scripts/init_alembic.py --models-path app/models.py
```

**When to read this reference:**
- Creating database migrations
- Troubleshooting migration issues
- Migrating production databases safely
- Understanding Alembic best practices

### 3. SQLAlchemy Model Definitions

Consult `references/sqlalchemy_models.md` for:
- Basic and modern (2.0+) model syntax
- Relationship patterns (one-to-many, many-to-many, self-referential)
- Column types and constraints
- Advanced patterns (mixins, hybrid properties, events)
- Table inheritance strategies
- Association proxies and composite columns
- Model validation

**When to read this reference:**
- Defining new SQLAlchemy models
- Implementing complex relationships
- Using advanced SQLAlchemy features
- Migrating to SQLAlchemy 2.0 syntax

**Example usage:**
```
When creating models for a blog platform, reference sqlalchemy_models.md for:
- One-to-many relationship between User and Post
- Many-to-many relationship between Post and Tag
- Hybrid properties for computed fields
- Timestamp mixins for created_at/updated_at
```

### 4. Query Optimization Techniques

Consult `references/query_optimization.md` for:
- Understanding EXPLAIN and EXPLAIN ANALYZE
- Different scan types (index-only, index, bitmap, sequential)
- Solving N+1 query problems with eager loading
- Join optimization strategies
- Efficient pagination (keyset vs offset)
- Aggregation and grouping optimization
- Subquery optimization (EXISTS vs IN)
- Batch operations for bulk inserts/updates
- Avoiding common anti-patterns

**Analysis script:** `scripts/analyze_queries.py`
- Analyzes slow queries using pg_stat_statements
- Identifies most time-consuming queries
- Finds queries with high variability
- Provides optimization recommendations

**When to use:**
```bash
# Analyze query performance
python scripts/analyze_queries.py postgresql://user:pass@localhost/db --limit 20
```

**When to read this reference:**
- Diagnosing slow queries
- Improving application performance
- Reviewing query patterns
- Understanding query execution plans

### 5. Index Strategies

Consult `references/indexes.md` for:
- Index types (B-tree, Hash, GIN, GiST, BRIN, SP-GiST)
- When to use each index type
- Composite indexes and column ordering
- Partial indexes for conditional indexing
- Expression indexes for computed values
- Covering indexes with INCLUDE clause
- Index maintenance and monitoring
- Best practices and common pitfalls

**Analysis script:** `scripts/analyze_indexes.py`
- Finds unused indexes
- Detects duplicate indexes
- Identifies missing indexes on foreign keys
- Shows most-used indexes
- Provides actionable recommendations

**When to use:**
```bash
# Analyze index usage and health
python scripts/analyze_indexes.py postgresql://user:pass@localhost/db
```

**When to read this reference:**
- Adding new indexes to improve query performance
- Choosing the right index type for your use case
- Optimizing existing indexes
- Understanding index trade-offs

### 6. JSONB for Flexible Data

Consult `references/jsonb_usage.md` for:
- JSONB vs JSON comparison
- Basic JSONB operations and operators
- Querying and filtering JSONB data
- Modifying JSONB fields
- JSONB functions and aggregations
- Indexing strategies for JSONB (GIN, expression indexes)
- Advanced patterns (validation, combining with structured data)
- Performance considerations
- SQLAlchemy JSONB usage

**When to read this reference:**
- Storing semi-structured or flexible data
- Working with user-generated attributes
- Implementing schema-less fields
- Querying or updating JSON data
- Optimizing JSONB performance

**Example usage:**
```
When building a product catalog with varying attributes, reference jsonb_usage.md for:
- Storing product attributes in JSONB
- Querying products by specific attributes
- Indexing JSONB for fast lookups
- Validating JSONB structure with constraints
```

### 7. Full-Text Search Implementation

Consult `references/fulltext_search.md` for:
- Full-text search basics (tsvector, tsquery)
- Creating efficient full-text search indexes
- Query syntax (AND, OR, NOT, phrases, prefix matching)
- Ranking and sorting search results
- Highlighting search results
- Multi-language support
- Fuzzy search with trigrams
- Performance optimization
- Advanced patterns (multi-table search, autocomplete)
- SQLAlchemy integration

**When to read this reference:**
- Implementing search functionality
- Optimizing existing search queries
- Supporting multiple languages
- Adding autocomplete or fuzzy matching
- Combining full-text with other filters

**Example usage:**
```
When adding search to a blog platform, reference fulltext_search.md for:
- Creating tsvector column with weighted title and content
- Building search queries from user input
- Ranking results by relevance
- Highlighting matching terms in snippets
```

## Utility Scripts

### Schema Inspector
**Script:** `scripts/schema_inspector.py`

Generate comprehensive documentation of your database schema.

**Usage:**
```bash
# Generate markdown documentation for entire database
python scripts/schema_inspector.py postgresql://user:pass@localhost/db

# Inspect specific table
python scripts/schema_inspector.py postgresql://user:pass@localhost/db --table users

# Output as JSON
python scripts/schema_inspector.py postgresql://user:pass@localhost/db --output json
```

**When to use:**
- Documenting existing databases
- Understanding inherited codebases
- Reviewing schema structure
- Generating schema documentation

## Workflow Examples

### Starting a New Database Project

1. **Design the schema**
   - Read `references/schema_design.md` for normalization guidance
   - Sketch out table relationships
   - Identify common patterns (audit trails, soft deletes)

2. **Set up SQLAlchemy models**
   - Read `references/sqlalchemy_models.md` for model patterns
   - Define Base and create model classes
   - Implement relationships and constraints

3. **Initialize Alembic**
   ```bash
   python scripts/init_alembic.py --models-path app/models.py
   export DATABASE_URL="postgresql://user:pass@localhost/db"
   ```

4. **Create initial migration**
   - Read `references/alembic_migrations.md` for best practices
   - Generate migration: `alembic revision --autogenerate -m "Initial schema"`
   - Review and adjust the generated migration
   - Apply migration: `alembic upgrade head`

5. **Add indexes**
   - Read `references/indexes.md` for index strategies
   - Add indexes for foreign keys and frequently queried columns
   - Create migration for indexes: `alembic revision -m "Add indexes"`

### Optimizing Database Performance

1. **Identify slow queries**
   ```bash
   python scripts/analyze_queries.py postgresql://user:pass@localhost/db --limit 20
   ```

2. **Analyze query execution**
   - Use EXPLAIN ANALYZE on identified slow queries
   - Read `references/query_optimization.md` for optimization techniques
   - Check for N+1 queries, missing indexes, or inefficient joins

3. **Review index usage**
   ```bash
   python scripts/analyze_indexes.py postgresql://user:pass@localhost/db
   ```

4. **Implement optimizations**
   - Add missing indexes on foreign keys
   - Remove unused indexes
   - Optimize queries based on recommendations
   - Use appropriate eager loading strategies

5. **Verify improvements**
   - Re-run analysis scripts
   - Compare query execution times
   - Monitor production metrics

### Adding Full-Text Search

1. **Read the reference**
   - Consult `references/fulltext_search.md` for implementation patterns

2. **Choose an approach**
   - Generated column (PostgreSQL 12+) - recommended
   - Trigger-based update
   - Expression index

3. **Implement search vector**
   ```python
   # Example using generated column
   search_vector = Column(
       TSVECTOR,
       Computed("to_tsvector('english', coalesce(title, '') || ' ' || coalesce(content, ''))")
   )
   ```

4. **Create migration**
   - Generate Alembic migration
   - Add GIN index on search_vector
   - Review migration for correctness

5. **Implement search queries**
   - Use websearch_to_tsquery for user input
   - Add ranking and highlighting
   - Test with various queries

## Best Practices

### Schema Design
- Normalize to 3NF unless there's a specific reason not to
- Use appropriate data types (don't store everything as TEXT)
- Add constraints (NOT NULL, CHECK, UNIQUE) at the database level
- Use foreign keys with ON DELETE/ON UPDATE actions
- Consider partial indexes for frequently filtered queries

### Migrations
- Always review auto-generated migrations
- Test migrations on development data first
- Write reversible migrations (proper downgrade implementations)
- Use CONCURRENTLY for index operations in production
- Add data migrations separately from schema changes

### Query Optimization
- Index foreign keys and frequently queried columns
- Use appropriate eager loading to avoid N+1 queries
- Prefer keyset pagination over OFFSET for large datasets
- Use EXPLAIN ANALYZE to verify index usage
- Monitor query performance with pg_stat_statements

### Indexes
- Don't over-index - each index has overhead on writes
- Create indexes CONCURRENTLY in production
- Remove unused indexes
- Use partial indexes when only subset needs indexing
- Choose appropriate index type for your query patterns

### JSONB
- Use JSONB over JSON for better performance
- Index JSONB columns with GIN for containment queries
- Use expression indexes for specific JSONB fields
- Combine structured columns with JSONB for flexibility
- Validate JSONB structure with CHECK constraints

## Additional Resources

All reference files contain extensive code examples, best practices, and anti-patterns to avoid. Read the relevant reference file when working on tasks in that domain.

The automation scripts provide practical tools for common database tasks:
- `init_alembic.py` - Set up Alembic with best practices
- `analyze_indexes.py` - Find optimization opportunities
- `analyze_queries.py` - Identify performance bottlenecks
- `schema_inspector.py` - Generate schema documentation

For production deployments, always:
- Test migrations in staging environment first
- Use CONCURRENTLY for index operations
- Monitor query performance
- Keep statistics up to date with ANALYZE
- Review execution plans with EXPLAIN
