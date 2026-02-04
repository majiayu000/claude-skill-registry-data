---
name: sqlite-test-validator
description: Test and validate SQLite database migrations and schema changes
type: skill
language: python
---

# SQLite Test Validator

Test database migrations and validate schema integrity.

## Capabilities
- Test migration scripts
- Validate schema changes
- Check data integrity after migrations
- Compare database schemas
- Generate test databases
- Verify foreign key constraints
- Test triggers and indexes
- Validate data types
- Check for breaking changes

## Tools
`sqlite_validator.py` - Test and validate databases

## Commands
```bash
# Test migration
./sqlite_validator.py test-migration --from old.db --to new.db --script migrate.sql

# Compare schemas
./sqlite_validator.py compare --db1 v1.XRose --db2 v2.XRose

# Validate schema
./sqlite_validator.py validate schema.sql

# Check integrity
./sqlite_validator.py check-integrity database.XRose
```

## Test Types
- **Schema Migration** - Verify DDL changes
- **Data Migration** - Verify data transforms
- **Integrity** - Check constraints/triggers
- **Performance** - Query performance
- **Rollback** - Test migration reversibility

## Complementary To
`database-migration-helper` (generates migrations)
`xrose-database-reader` (reads XRose files)
