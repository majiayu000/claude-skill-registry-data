---
name: clean-architecture
description: Clean architecture 4-layer structure (events/facades/services/repository), transaction management, dependency rules. Use when creating events, facades, services, repositories, managing transactions, asking about layer responsibilities, architectural questions, or refactoring code.
---

# Clean Architecture Guide

## Layer Flow

```
events (Presentation) → facades (Application) → services (Business Logic) → repository (Data Access)
```

## Layer Responsibilities

### events/
Discord event handlers (slash commands, buttons, reactions)

- Call facades (1:1 relationship)
- **Prohibited**: Direct access to Service/Repository layers

### facades/
Coordinate multiple services, manage transaction boundaries

- **Only layer responsible for transaction management** (begin/commit/rollback)
- Compose services to implement use cases

### services/
Single business operations, domain rules

- Call repositories
- Receive transactions as arguments, pass to repositories only
- **Prohibited**: Direct dependency on other services

### repository/
Data persistence and retrieval abstraction

- DB operations with transactions (`create_with_txn`, etc.)
- **Prohibited**: Business logic implementation

## Transaction Management (Critical)

**Only Facade layer can manage transactions**

### Facade Layer
```rust
let txn = app_state.db().begin().await?;
let result = async {
    service_layer_call(&txn).await?;
    Ok(())
}.await;
match result {
    Ok(_) => txn.commit().await?,
    Err(e) => txn.rollback().await?,
}
```

### Service Layer
```rust
pub async fn service_function(txn: &DatabaseTransaction) -> Result<()> {
    repository.create_with_txn(txn, ...).await?;
    Ok(())  // No commit/rollback
}
```

### Repository Layer
```rust
pub async fn create_with_txn(&self, txn: &DatabaseTransaction, ...) -> Result<()> {
    entity.insert(txn).await?;
    Ok(())  // No commit/rollback
}
```

## Dependency Injection

AppState pattern (Rust-idiomatic approach, not DI container)

- Initialize single DB connection and AppState in `main.rs`
- Share across all layers via PoiseData
- Constructor injection for dependencies
- **Prohibited**: Creating individual DB connections per layer

## Architecture Constraints

### Prohibited

- Cross-layer direct access (e.g., Facade → Repository direct call)
- DB operations outside transactions
- Transaction creation/commit/rollback in Service/Repository layers
- Long-held transactions
- Global variables

### Code Quality Constraints

- No functions over 100 lines
- No nesting deeper than 5 levels
- Avoid unnecessary `clone()`, use borrowing
- Minimize `Arc<T>` usage

## Performance

- Use `futures::future::try_join_all` for concurrent operations
