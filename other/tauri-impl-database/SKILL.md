---
name: tauri-impl-database
description: >
  Use when adding database storage, implementing key-value persistence, or integrating SQL databases in Tauri 2 apps.
  Prevents data loss from missing store auto-save configuration and SQL injection from unparameterized queries.
  Covers SQLite via tauri-plugin-sql, key-value storage via tauri-plugin-store, and custom DB integration with sqlx/diesel/rusqlite.
  Keywords: tauri database, SQLite, tauri-plugin-sql, tauri-plugin-store, key-value storage, sqlx, diesel, rusqlite.
license: MIT
compatibility: "Designed for Claude Code. Requires Tauri 2.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# tauri-impl-database

## Decision Tree: Which Storage Approach

```
Need persistent data in Tauri 2?
|
+-- Simple key-value pairs (settings, preferences, cache)?
|   --> tauri-plugin-store (Section 1)
|
+-- Relational data with SQL queries?
|   |
|   +-- Frontend-driven queries (JS/TS calls SQL directly)?
|   |   --> tauri-plugin-sql (Section 2)
|   |
|   +-- Backend-driven queries (Rust owns the data layer)?
|       --> Custom DB via Rust commands (Section 3)
|
+-- Encrypted storage for secrets?
    --> tauri-plugin-stronghold (out of scope, see plugin docs)
```

---

## Section 1: tauri-plugin-store (Key-Value Storage)

### When to Use

Use `tauri-plugin-store` for user preferences, application settings, small cache data, and any scenario where you need persistent key-value pairs without relational queries.

### Setup

**Rust side** (`src-tauri/Cargo.toml`):
```toml
[dependencies]
tauri-plugin-store = "2"
```

**Register the plugin** (`src-tauri/src/lib.rs`):
```rust
tauri::Builder::default()
    .plugin(tauri_plugin_store::Builder::default().build())
    .run(tauri::generate_context!())
    .expect("error while running tauri application");
```

**Frontend side** (`package.json`):
```json
{
  "dependencies": {
    "@tauri-apps/plugin-store": "^2"
  }
}
```

**Permissions** (`src-tauri/capabilities/default.json`):
```json
{
  "permissions": ["store:default"]
}
```

### Eager Loading Pattern

ALWAYS use eager loading when you need the store immediately at component mount or app startup.

```typescript
import { load } from '@tauri-apps/plugin-store';

// Eager: loads from disk immediately, awaits until ready
const store = await load('settings.json', { autoSave: true });

// CRUD operations
await store.set('theme', 'dark');
await store.set('user', { name: 'Alice', prefs: { lang: 'en' } });

const theme = await store.get<string>('theme');
// Returns undefined if key does not exist -- ALWAYS handle this
const hasKey = await store.has('theme');

// Enumeration
const allKeys = await store.keys();
const allValues = await store.values();
const allEntries = await store.entries();
const count = await store.length();

// Deletion
await store.delete('theme');
await store.clear();

// Manual persistence (only needed when autoSave is false)
await store.save();

// Reload from disk (discard in-memory changes)
await store.reload();

// Reset to default values
await store.reset();
```

### Lazy Loading Pattern

Use `LazyStore` when the store is referenced in multiple places but first access timing is uncertain. The store initializes on first operation.

```typescript
import { LazyStore } from '@tauri-apps/plugin-store';

// Does NOT load from disk yet
const store = new LazyStore('cache.json');

// First operation triggers disk load automatically
await store.set('lastSync', Date.now());
const lastSync = await store.get<number>('lastSync');
```

### Critical Rules

**NEVER** assume `store.get()` returns a value. It returns `undefined` for missing keys.

**NEVER** store large binary data in the store. It serializes to JSON on disk. Use the filesystem plugin for binary files.

**ALWAYS** call `await store.save()` if `autoSave` is `false`. Data loss occurs on app exit without save.

**ALWAYS** use `await load(...)` before calling store methods when using eager loading. Calling methods on an unloaded store causes runtime errors.

---

## Section 2: tauri-plugin-sql (SQLite from Frontend)

### When to Use

Use `tauri-plugin-sql` when the frontend needs direct SQL access for relational data, and you prefer writing queries in TypeScript rather than exposing individual Rust commands for each operation.

### Setup

**Rust side** (`src-tauri/Cargo.toml`):
```toml
[dependencies]
tauri-plugin-sql = { version = "2", features = ["sqlite"] }
```

**Register the plugin** (`src-tauri/src/lib.rs`):
```rust
use tauri_plugin_sql::{Migration, MigrationKind};

let migrations = vec![
    Migration {
        version: 1,
        description: "create_initial_tables",
        sql: "CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );",
        kind: MigrationKind::Up,
    },
    Migration {
        version: 2,
        description: "add_settings_table",
        sql: "CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );",
        kind: MigrationKind::Up,
    },
];

tauri::Builder::default()
    .plugin(
        tauri_plugin_sql::Builder::default()
            .add_migrations("sqlite:app.db", migrations)
            .build(),
    )
    .run(tauri::generate_context!())
    .expect("error while running tauri application");
```

**Frontend side** (`package.json`):
```json
{
  "dependencies": {
    "@tauri-apps/plugin-sql": "^2"
  }
}
```

**Permissions** (`src-tauri/capabilities/default.json`):
```json
{
  "permissions": ["sql:default"]
}
```

### Frontend CRUD Operations

```typescript
import Database from '@tauri-apps/plugin-sql';

// Connect (creates file if it does not exist)
const db = await Database.load('sqlite:app.db');

// INSERT with parameters (ALWAYS use parameterized queries)
await db.execute(
  'INSERT INTO users (name, email) VALUES ($1, $2)',
  ['Alice', 'alice@example.com']
);

// SELECT
const users = await db.select<Array<{
  id: number;
  name: string;
  email: string;
}>>('SELECT * FROM users WHERE name = $1', ['Alice']);

// UPDATE
const result = await db.execute(
  'UPDATE users SET name = $1 WHERE id = $2',
  ['Bob', 1]
);
console.log(`Rows affected: ${result.rowsAffected}`);

// DELETE
await db.execute('DELETE FROM users WHERE id = $1', [1]);

// Close connection when done
await db.close();
```

### Critical Rules

**ALWAYS** use parameterized queries (`$1`, `$2`, ...). NEVER concatenate user input into SQL strings.

**ALWAYS** define migrations in Rust before the app starts. The plugin runs migrations on first connection.

**NEVER** use `Database.load()` with an absolute file path. Use the `sqlite:` prefix with a relative name. The plugin resolves the path to the app data directory.

**ALWAYS** close the database connection when the component or page unmounts to prevent connection leaks.

---

## Section 3: Custom Database via Rust Commands

### When to Use

Use custom Rust commands when you need full control over the database layer: connection pooling, complex transactions, custom ORM (diesel), type-safe queries (sqlx), or when the database logic belongs in the backend.

### Pattern: sqlx with SQLite

**Rust side** (`src-tauri/Cargo.toml`):
```toml
[dependencies]
sqlx = { version = "0.8", features = ["runtime-tokio", "sqlite"] }
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
thiserror = "2"
```

**Database state and connection** (`src-tauri/src/db.rs`):
```rust
use sqlx::sqlite::{SqlitePool, SqlitePoolOptions};
use std::path::PathBuf;

pub struct DbState {
    pub pool: SqlitePool,
}

pub async fn init_db(db_path: PathBuf) -> Result<SqlitePool, sqlx::Error> {
    let db_url = format!("sqlite:{}?mode=rwc", db_path.display());
    let pool = SqlitePoolOptions::new()
        .max_connections(5)
        .connect(&db_url)
        .await?;

    // Run migrations
    sqlx::query(
        "CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )"
    )
    .execute(&pool)
    .await?;

    Ok(pool)
}
```

**Commands** (`src-tauri/src/commands.rs`):
```rust
use crate::db::DbState;
use serde::Serialize;

#[derive(Debug, thiserror::Error)]
pub enum Error {
    #[error(transparent)]
    Sqlx(#[from] sqlx::Error),
    #[error("item not found: {0}")]
    NotFound(i64),
}

impl serde::Serialize for Error {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where S: serde::ser::Serializer {
        serializer.serialize_str(self.to_string().as_ref())
    }
}

#[derive(Serialize, sqlx::FromRow)]
pub struct Item {
    id: i64,
    title: String,
    done: bool,
}

#[tauri::command]
pub async fn create_item(
    state: tauri::State<'_, DbState>,
    title: String,
) -> Result<i64, Error> {
    let result = sqlx::query("INSERT INTO items (title) VALUES (?)")
        .bind(&title)
        .execute(&state.pool)
        .await?;
    Ok(result.last_insert_rowid())
}

#[tauri::command]
pub async fn get_items(
    state: tauri::State<'_, DbState>,
) -> Result<Vec<Item>, Error> {
    let items = sqlx::query_as::<_, Item>("SELECT * FROM items")
        .fetch_all(&state.pool)
        .await?;
    Ok(items)
}

#[tauri::command]
pub async fn toggle_item(
    state: tauri::State<'_, DbState>,
    id: i64,
) -> Result<(), Error> {
    let rows = sqlx::query("UPDATE items SET done = NOT done WHERE id = ?")
        .bind(id)
        .execute(&state.pool)
        .await?
        .rows_affected();
    if rows == 0 {
        return Err(Error::NotFound(id));
    }
    Ok(())
}
```

**App setup** (`src-tauri/src/lib.rs`):
```rust
mod commands;
mod db;

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .setup(|app| {
            let db_path = app.path().app_data_dir()?.join("data.db");
            // Ensure parent directory exists
            if let Some(parent) = db_path.parent() {
                std::fs::create_dir_all(parent)?;
            }

            let pool = tauri::async_runtime::block_on(async {
                db::init_db(db_path).await
            })?;

            app.manage(db::DbState { pool });
            Ok(())
        })
        .invoke_handler(tauri::generate_handler![
            commands::create_item,
            commands::get_items,
            commands::toggle_item,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

**Frontend call**:
```typescript
import { invoke } from '@tauri-apps/api/core';

const id = await invoke<number>('create_item', { title: 'Buy groceries' });
const items = await invoke<Array<{ id: number; title: string; done: boolean }>>('get_items');
await invoke('toggle_item', { id: 1 });
```

### Critical Rules

**ALWAYS** initialize the database in the `setup()` hook and manage the pool as state. NEVER create connections inside individual commands.

**ALWAYS** ensure the database directory exists before connecting. Use `app.path().app_data_dir()` for the correct platform-specific path.

**ALWAYS** use `async` commands for all database operations. Sync database calls block the main thread and freeze the UI.

**NEVER** wrap the pool in `Arc`. Tauri already wraps managed state in `Arc` internally. `SqlitePool` is also internally `Arc`-wrapped.

**ALWAYS** use the `thiserror` + manual `Serialize` impl pattern for error types. See [references/methods.md](references/methods.md) for the full pattern.

**ALWAYS** define custom command permissions when using this approach. See tauri-errors-permissions skill for the permission setup flow.

---

## Reference Links

- [references/methods.md](references/methods.md) -- API signatures for store, sql plugin, and sqlx patterns
- [references/examples.md](references/examples.md) -- Complete working examples for each approach
- [references/anti-patterns.md](references/anti-patterns.md) -- Common database integration mistakes

### Official Sources

- https://v2.tauri.app/plugin/sql/
- https://v2.tauri.app/plugin/store/
- https://docs.rs/tauri-plugin-sql/latest/tauri_plugin_sql/
- https://docs.rs/tauri-plugin-store/latest/tauri_plugin_store/
