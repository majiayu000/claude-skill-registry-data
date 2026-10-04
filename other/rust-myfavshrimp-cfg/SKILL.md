---
name: rust
description: Personal Rust guidelines. Use when writing or reviewing Rust code.
---

When using `thiserror`, do not add per-variant `#[error("...")]` messages on enum variants. Instead, define a separate error struct for each failure mode and reference it via `#[from]` on the variant. The enum gets a single top-level `#[error]` covering the whole operation.

**Example:**

```rust
#[derive(thiserror::Error, Debug)]
#[error("Could not load user")]
pub enum LoadUserError {
    NotFound(#[from] UserNotFoundError),
    Database(#[from] DatabaseError),
}

#[derive(thiserror::Error, Debug)]
#[error("User {user_id} not found")]
pub struct UserNotFoundError {
    pub user_id: UserId,
}
```

Not:

```rust
#[derive(thiserror::Error, Debug)]
pub enum LoadUserError {
    #[error("User {0} not found")]
    NotFound(UserId),
    #[error("Database error: {0}")]
    Database(#[from] sqlx::Error),
}
```

Each named error struct can be matched on, propagated, and reused independently. Inline messages on enum variants collapse the failure mode into a string and break traceable error chains.
