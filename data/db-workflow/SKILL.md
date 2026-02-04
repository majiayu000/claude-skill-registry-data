---
name: db-workflow
description: Database migration workflow helper. Use when creating database migrations, modifying SQLAlchemy models, or managing Alembic migrations. Automatically handles model changes, migration creation, and database upgrades.
---

# Database Migration Workflow

This skill helps with the complete database migration workflow in this project.

## When to use this skill

- Modifying SQLAlchemy models in `backend/app/models/`
- Creating new database tables or columns
- Changing relationships between models
- Running database migrations
- Checking migration status

## Workflow Steps

1. **Before modifying models**: Check current migration status
   ```bash
   make db-upgrade  # Ensure all migrations are applied
   ```

2. **After modifying models**: Create migration
   ```bash
   make db-migrate  # Auto-generate migration from model changes
   ```

3. **Review migration**: Always read the generated migration file in `backend/alembic/versions/`
   - Verify upgrade() and downgrade() operations
   - Check for data migrations if needed
   - Ensure no data loss operations

4. **Apply migration**:
   ```bash
   make db-upgrade  # Apply to local database
   ```

5. **Test migration**: Run tests to verify schema changes
   ```bash
   make test
   ```

## Critical Rules

- NEVER delete the Docker volume `pgdata` - local database must persist
- Always review auto-generated migrations before applying
- Test both upgrade AND downgrade paths
- For production: coordinate with team before running migrations
- Row-level security (RLS) policies may need manual updates in migrations

## Common Tasks

### Add new model field
1. Add field to SQLAlchemy model
2. Run `make db-migrate`
3. Review generated migration
4. Run `make db-upgrade`
5. Run `make test`

### Create new table
1. Create new model class in appropriate module
2. Import model in `backend/app/models/__init__.py`
3. Run `make db-migrate`
4. Review generated migration
5. Run `make db-upgrade`
6. Run `make test`

### Check migration status
```bash
cd backend
uv run alembic current     # Show current revision
uv run alembic heads       # Show latest revision
uv run alembic history     # Show all migrations
```

## Troubleshooting

- **Migration conflict**: Multiple heads exist, merge with `alembic merge`
- **Auto-generation missed changes**: Check model imports and table metadata
- **Test database issues**: Use `DATABASE_URL="postgresql://postgres:postgres@localhost:5433/manageros_test" make db-upgrade`
