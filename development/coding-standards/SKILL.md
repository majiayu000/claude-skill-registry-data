---
name: coding-standards
description: Rust coding standards (Japanese comments required, error handling, logging, naming conventions). Use when writing new code, adding error handling, logging, fixing errors, asking about coding style, thiserror, tracing, naming conventions, or code review.
---

# Coding Standards

## Language Rules

### Comments and Documentation

**All comments, documentation, and error messages must be in Japanese**

```rust
// ✅ Correct
/// ユーザーを作成する
pub async fn create_user() -> Result<()> {
    // ユーザー情報をバリデーション
}

// ❌ Wrong
/// Create a user
pub async fn create_user() -> Result<()> {
    // Validate user info
}
```

### Naming Conventions

- Structs/Enums/Type Aliases: `PascalCase`
- Functions/Methods/Variables: `snake_case`
- Constants: `SCREAMING_SNAKE_CASE`

```rust
// ✅ Correct
struct UserData { }
const MAX_RETRIES: u32 = 3;
fn create_user() { }

// ❌ Wrong
struct user_data { }
const maxRetries: u32 = 3;
fn CreateUser() { }
```

## Error Handling

### Using thiserror

Define appropriate error types per layer

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ServiceError {
    #[error("ユーザーが見つかりません: {0}")]
    UserNotFound(String),

    #[error("バリデーションエラー: {0}")]
    ValidationError(String),

    #[error("データベースエラー")]
    DatabaseError(#[from] DbErr),
}
```

### Error Conversion

Use `#[from]` attribute for cross-layer error conversion

```rust
#[derive(Error, Debug)]
pub enum FacadeError {
    #[error("サービスエラー")]
    ServiceError(#[from] ServiceError),

    #[error("リポジトリエラー")]
    RepositoryError(#[from] RepositoryError),
}
```

### Prohibited

- **Prohibited**: `unwrap()` in production code
- `panic!()` only for unrecoverable situations

```rust
// ❌ Prohibited
let user = find_user().unwrap();

// ✅ Correct
let user = find_user().map_err(|e| ServiceError::UserNotFound(e.to_string()))?;
```

## Logging

### Using tracing

Use structured logging

```rust
use tracing::{error, warn, info, debug};

// ERROR: System errors, unexpected exceptions
error!(error = %e, user_id = %user_id, "ユーザー作成に失敗しました");

// WARN: Business exceptions, retryable errors
warn!(recruitment_id = %id, "募集が満員のため参加を拒否しました");

// INFO: Important business operations start/end
info!(quest_name = %quest_name, "募集作成を開始しました");

// DEBUG: Debug information
debug!(params = ?params, "リクエストパラメータ");
```

### Log Levels

| Level | Purpose | Examples |
|-------|---------|----------|
| ERROR | System errors, unexpected exceptions | DB connection failure, external API failure |
| WARN | Business exceptions, retryable errors | Validation errors, permission denied |
| INFO | Important business operations start/end | Recruitment creation, user registration |
| DEBUG | Debug information | Parameter details, internal state |

## Performance

### Ownership and Borrowing

Avoid unnecessary `clone()`, use borrowing

```rust
// ❌ Avoid
fn process(data: String) {
    let copied = data.clone();
    // ...
}

// ✅ Recommended
fn process(data: &str) {
    // ...
}
```

### Arc Usage

Minimize `Arc<T>` usage

```rust
// ❌ Avoid (unnecessary Arc)
fn process(data: Arc<String>) {
    // ...
}

// ✅ Recommended (borrowing is enough)
fn process(data: &str) {
    // ...
}
```

## Code Quality

### Function Length

- **Prohibited**: Functions over 100 lines
- **Prohibited**: Nesting deeper than 5 levels

```rust
// ❌ Avoid
fn complex_function() {
    if condition1 {
        if condition2 {
            if condition3 {
                if condition4 {
                    if condition5 {
                        // Too deep
                    }
                }
            }
        }
    }
}

// ✅ Recommended (early return)
fn simple_function() -> Result<()> {
    if !condition1 { return Ok(()); }
    if !condition2 { return Ok(()); }
    if !condition3 { return Ok(()); }
    // Flat structure
    Ok(())
}
```

### Concurrency

Use `futures` for concurrent operations

```rust
use futures::future::try_join_all;

// ✅ Concurrent processing
let futures = items.iter().map(|item| process_item(item));
let results = try_join_all(futures).await?;
```
