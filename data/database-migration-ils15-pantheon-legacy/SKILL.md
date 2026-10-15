---
name: database-migration
description: "Database migrations with Alembic, rollbacks, and zero-downtime deployment. Use for schema changes."
globs: ["**/alembic/**", "**/migrations/**"]
alwaysApply: false
---

# Database Migration Skill

## Migration Lifecycle

### 1. Generate Migration
```bash
alembic revision --autogenerate -m "Add user preferences"
```

### 2. Review Generated Script
```python
# File: alembic/versions/001_add_user_preferences.py

def upgrade():
    op.create_table('user_preferences',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('theme', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id']),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('user_preferences')
```

### 3. Add Indexes
```python
def upgrade():
    op.create_table(...)
    # Add indexes for performance
    op.create_index(
        'ix_user_preferences_user_id',
        'user_preferences',
        ['user_id']
    )

def downgrade():
    op.drop_index('ix_user_preferences_user_id')
    op.drop_table('user_preferences')
```

### 4. Test Locally
```bash
# Test upgrade
alembic upgrade head

# Verify data integrity
SELECT * FROM user_preferences;

# Test downgrade
alembic downgrade -1

# Verify
SELECT COUNT(*) FROM user_preferences;  # Should error
```

### 5. Test on Production-like Data
```bash
# Backup production
pg_dump production > backup.sql

# Load to staging
psql staging < backup.sql

# Run migration
alembic upgrade head

# Performance test
EXPLAIN ANALYZE SELECT * FROM user_preferences WHERE user_id = 123;
```

### 6. Deploy with Zero Downtime
```python
# Strategy 1: Expand-Contract
# 1. Add new column (backward compatible)
# 2. Backfill data
# 3. Deploy code to use new column
# 4. Drop old column

# Strategy 2: Blue-Green
# 1. Deploy new schema to green DB
# 2. Sync data
# 3. Switch traffic to green
# 4. Keep blue as rollback option
```

## Backward Compatibility Rules
- ✅ Add columns with defaults
- ✅ Add tables
- ✅ Add indexes
- ✅ Change column types (with care)
- ❌ Drop columns without deprecation
- ❌ Rename columns without alias
- ❌ Change constraints abruptly

## Versioning
- Never edit old migrations
- Always create new migration
- Migrations are immutable
- Name clearly: `001_initial_schema.py`

## Rollback Procedure
ALWAYS test downgrade first:
```bash
alembic current  # See current version
alembic downgrade -1  # Go back 1 version
alembic upgrade +2  # Forward 2 versions
```
