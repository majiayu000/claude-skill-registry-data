---
name: migration-runner
description: Run and verify SeaORM database migrations against in-memory SQLite. Use when applying migrations, verifying schema changes, or testing migration correctness.
---

# Migration Runner

Run and verify SeaORM database migrations for LibrAgent.

## Setup

```rust
use sqlx::sqlite::SqlitePoolOptions;
use sea_orm::SqlxSqliteConnector;
use tauri_mcp_agent_lib::migration::Migrator;
use sea_orm_migration::MigratorTrait;

async fn setup_db() -> sea_orm::DatabaseConnection {
    let pool = SqlitePoolOptions::new()
        .connect("sqlite::memory:")
        .await
        .unwrap();
    let db = SqlxSqliteConnector::from_sqlx_sqlite_pool(pool);
    Migrator::up(&db, None).await.unwrap();
    db
}
```

## Verification Patterns

### Schema Validation

```rust
let db = setup_db().await;
// Verify tables exist
let result = db.query_all(
    "SELECT name FROM sqlite_master WHERE type='table'"
).await.unwrap();
assert!(result.iter().any(|r| r["name"].to_string().contains("expected_table")));
```

### Migration Up/Down

```rust
let db = setup_db().await;
Migrator::up(&db, None).await.unwrap();
// Verify schema after up
Migrator::down(&db, None).await.unwrap();
// Verify schema after down
```

### Foreign Key Validation

```rust
let db = setup_db().await;
// Attempt invalid foreign key insertion
// Verify foreign key constraint is enforced
```

## Key Files

- `src-tauri/src/migration/` - Migration files
- `src-tauri/src/repositories/` - Repository implementations
- `scripts/verify_phase2_migration.sh` - Legacy migration verification
- `scripts/test_planning_module.sh` - Legacy module testing

## CI Integration

Tests must be in `src-tauri/tests/` as integration tests. Run with:

```bash
cargo test --tests
```
