---
name: alembic-workflow
description: Create and manage Alembic database migrations in ettametta. Use when adding/modifying database tables, resolving migration conflicts, or fixing schema drift. Covers autogenerate, merge heads, introspection-based migrations, and the CI bypass issue.
---

# Alembic Migration Workflow

Skill for creating and managing database migrations in ettametta — autogenerate, merge heads, introspection patterns, and the CI bypass problem.

## Quick Commands

### Generate a new migration
```bash
alembic revision --autogenerate -m "description_of_change"
```

### Apply migrations
```bash
alembic upgrade head
```

### Check current state
```bash
alembic current
alembic history --verbose
alembic heads  # should be exactly 1
```

### Downgrade
```bash
alembic downgrade -1  # one step back
alembic downgrade base  # all the way
```

## Architecture Reference

### Configuration

| File | Purpose |
|------|---------|
| `alembic.ini` | Config — `sqlalchemy.url` is placeholder, overridden at runtime |
| `alembic/env.py` | Runtime — imports `Base.metadata` from `src.api.utils.models`, reads `settings.DATABASE_URL` |
| `alembic/script.py.mako` | Template for generated migration files |

### Model Import Chain

`env.py` imports `Base` from `src.api.utils.models`. This pulls in all models transitively:

```
env.py
  → src.api.utils.models (Base, all table models)
    → src.api.utils.database (Base = declarative_base())
    → src.api.utils.user_models (UserDB, SubscriptionTier, UserRole)
    → src.api.utils.credit_models (UserCreditDB, CreditTransactionDB)
```

**Important:** All model modules must be imported for autogenerate to detect them. If you add a new model module, ensure it's imported in `src/api/utils/models.py`.

### Migration History (16 migrations, 2 merge points)

```
a4b1aaadd072 (initial)
  ├─ 001_create_user_table ──────────────┐
  ├─ add_user_id_monitored_niches ───────┤
  └─ b2c3d4e5f6g7_add_is_google_oauth ──┤
                                          ├─ merge_heads_2026
                                          │
c8d2e4f5g6h7 ─→ 2aa1c8c2bf49 ─→ 86ebe6287aea ─→ a1b2c3d4e5f
                                                        │
a1b2c3d4e5f6 ──┐                                       │
                ├─ efb25ef5b164 (merge) ─→ 260bae1bf65b ─→ f1b2c3d4e5f6
ee8627d8341b ──┘                                            │
                                                            ▼
                                          g1b2c3d4e5f7 ─→ d410fb0d40a9
                                                                │
                                                                ▼
                                          83a4ab83e579 ─→ e7b99c2d1f4a
```

### Introspection-Based Migrations

Newer migrations (`83a4ab83e579`, `e7b99c2d1f4a`) use `Inspector.from_engine()` to conditionally apply changes. This is a defensive pattern for databases that may be in different states:

```python
from sqlalchemy import inspect as sa_inspect

def upgrade():
    bind = op.get_bind()
    inspector = sa_inspect(bind)
    columns = [c['name'] for c in inspector.get_columns('my_table')]
    
    if 'new_column' not in columns:
        op.add_column('my_table', sa.Column('new_column', sa.String))
```

Use this pattern when:
- The database may already have the column (manual addition or different environment)
- You're fixing a previous migration that may have partially applied
- Multiple developers may have different schema states

## Common Issues & Fixes

### CI/CD bypasses Alembic entirely

**Critical issue:** The CI/CD pipeline uses `Base.metadata.create_all(bind=engine)` instead of `alembic upgrade head`. This means migrations are never validated in CI, and schema drift can accumulate silently.

`scripts/init_db.py` also uses `drop_all()` + `create_all()` — no Alembic.

**Impact:** Migrations that work against a fresh database may fail against production (which was built incrementally). Always test migrations against a copy of the production schema.

### Multiple heads

```bash
# Check for multiple heads
alembic heads

# If multiple heads exist, create a merge migration
alembic merge -m "merge_heads" head1 head2
```

### Migration fails against existing database

Use introspection to make migrations idempotent:

```python
def upgrade():
    bind = op.get_bind()
    inspector = sa_inspect(bind)
    
    # Check table exists
    if 'my_table' not in inspector.get_table_names():
        op.create_table('my_table', ...)
    
    # Check column exists
    columns = [c['name'] for c in inspector.get_columns('existing_table')]
    if 'new_col' not in columns:
        op.add_column('existing_table', sa.Column('new_col', sa.String))
    
    # Check index exists
    indexes = [i['name'] for i in inspector.get_indexes('existing_table')]
    if 'ix_new_col' not in indexes:
        op.create_index('ix_new_col', 'existing_table', ['new_col'])
```

### autogenerate doesn't detect changes

1. Ensure all model modules are imported in `src/api/utils/models.py`
2. Ensure `target_metadata = Base.metadata` in `env.py`
3. Check that the model class inherits from `Base` (not a different Base)
4. Run `alembic revision --autogenerate` and review the generated diff

### Database URL not resolving

`env.py` overrides `sqlalchemy.url` from `settings.DATABASE_URL`. If it fails:
- Check `src/api/config/settings.py` for the `DATABASE_URL` field
- Default is SQLite (`sqlite:///./data/db/ettametta.db`)
- Production uses PostgreSQL via `DATABASE_URL` env var

### Downgrade fails

Not all migrations implement `downgrade()`. The Mako template generates a `pass` placeholder. If you need reversible migrations, implement both `upgrade()` and `downgrade()`.

## Best Practices

1. **Always review autogenerate output** — it can miss renames, detect false positives for constraints
2. **Use introspection for safety** — especially in shared databases or when deploying to environments with unknown state
3. **One logical change per migration** — don't bundle unrelated schema changes
4. **Test against production-like data** — `create_all` in CI doesn't catch migration bugs
5. **Keep migrations small** — large migrations are harder to debug and roll back
6. **Name migrations clearly** — the `-m` message should describe what changes, not why

## References

- [Migration History Details](references/migration-history.md)
- [Introspection Patterns](references/introspection-patterns.md)
