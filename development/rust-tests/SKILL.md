---
name: rust-tests
description: Run and debug Rust tests for glhf. Use when running tests, fixing test failures, or adding new test cases.
---

# Rust Testing Guide

## Running Tests

### All Tests
```bash
cargo test
```

### Embedding Tests (require model download)
```bash
cargo test embed -- --ignored
```

### Specific Tests
```bash
cargo test test_name           # Run tests matching name
cargo test --lib               # Only library tests
cargo test --test integration  # Only integration tests
cargo test -- --nocapture      # Show println output
```

## Test Structure

```
tests/
├── integration.rs      # End-to-end tests
└── common/
    └── mod.rs          # Test utilities (TestEnv, fixtures)

src/
├── db/mod.rs          # Unit tests in #[cfg(test)] mod tests
├── embed.rs           # Embedding tests (#[ignore] for CI)
└── document.rs        # Document struct tests
```

## Test Utilities

### TestEnv (tests/common/mod.rs)
```rust
let env = TestEnv::new();                    // Creates temp directory
let project = env.create_project("path");    // Creates project dir
let jsonl = env.write_jsonl(&project, "file.jsonl", &lines);
```

### Fixtures
```rust
fn user_message(content: &str, session: &str) -> String
fn assistant_message(content: &str, session: &str) -> String
fn assistant_with_blocks(texts: &[&str], session: &str) -> String
fn file_history_snapshot() -> String
fn malformed_json() -> String
```

## Test Categories

| Category | Location | Run Command |
|----------|----------|-------------|
| Unit tests | `src/**/*.rs` | `cargo test --lib` |
| Integration | `tests/integration.rs` | `cargo test --test integration` |
| Doc tests | `src/**/*.rs` | `cargo test --doc` |
| Embedding | `src/embed.rs` | `cargo test embed -- --ignored` |
| Benchmarks | `benches/indexing.rs` | `cargo bench` |

## Writing Tests

### Database Tests
```rust
#[test]
fn test_database_operation() {
    let env = TestEnv::new();
    let db_path = env.index_dir.join("test.db");

    let mut db = Database::open(&db_path).unwrap();

    let doc = Document::new(
        ChunkKind::Message,
        "test content".to_string(),
        PathBuf::from("/test"),
    );

    db.insert_documents(&[doc]).unwrap();

    let results = db.search_fts("test", 10).unwrap();
    assert_eq!(results.len(), 1);
}
```

### Embedding Tests (ignored by default)
```rust
#[test]
#[ignore = "Requires model download"]
fn test_embedding() {
    let embedder = Embedder::new().unwrap();
    let embedding = embedder.embed_query("test").unwrap();
    assert_eq!(embedding.len(), 512);  // Potion-base-32M dimension
}
```

## Common Failures

| Error | Cause | Fix |
|-------|-------|-----|
| `Failed to load model` | Missing/corrupted model | Delete HF cache, re-run |
| `sqlite-vec not loaded` | Init order | Call init_sqlite_vec() before open |
| `FTS5 match failed` | Bad query syntax | Escape special chars |
