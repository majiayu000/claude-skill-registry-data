---
name: rust-backend-database
description: Implements database integration patterns for Rust backends using SQLx and SeaORM. Use when setting up database connections, writing queries, defining entities, managing migrations, or configuring connection pools. Covers compile-time checked SQL, ORM patterns, and N+1 prevention.
---

<objective>
Provides comprehensive guidance for database integration in Rust backend applications. Covers SQLx for compile-time verified SQL queries and SeaORM for complex domain models requiring ORM patterns.
</objective>

<essential_principles>
**1. Type Safety First** - SQLx validates queries at compile time. SeaORM uses derive macros for type-safe entities.

**2. Connection Pooling is Mandatory** - Never create individual connections per request.

**3. Migrations are Code** - Treat migrations as first-class code. Version control, review, test.

**4. Choose the Right Tool**
- SQLx: Simple to medium complexity, direct SQL control
- SeaORM: Complex relations, dynamic queries, ActiveRecord patterns
</essential_principles>

<decision_matrix>
| Scenario | Use |
|----------|-----|
| Simple CRUD, direct SQL | SQLx query_as!() |
| Complex entity relationships | SeaORM Smart Entity Loader |
| Performance-critical | SQLx (minimal overhead) |
| N+1 prevention | SeaORM data loaders |
</decision_matrix>

<patterns>
<pattern name="sqlx_pool">
**SQLx Pool Configuration**

```rust
use sqlx::postgres::PgPoolOptions;

pub async fn create_pool(database_url: &str) -> Result<PgPool, sqlx::Error> {
    PgPoolOptions::new()
        .max_connections(10)
        .min_connections(2)
        .acquire_timeout(Duration::from_secs(3))
        .max_lifetime(Duration::from_secs(30 * 60))
        .connect(database_url)
        .await
}
```
</pattern>

<pattern name="sqlx_queries">
**Compile-Time Checked Queries**

```rust
#[derive(FromRow)]
struct User {
    id: i64,
    email: String,
    name: Option<String>,
}

async fn get_user(pool: &PgPool, id: i64) -> Result<User, sqlx::Error> {
    sqlx::query_as!(User, "SELECT id, email, name FROM users WHERE id = $1", id)
        .fetch_one(pool)
        .await
}
```
</pattern>

<pattern name="transactions">
**Transactions**

```rust
let mut tx = pool.begin().await?;

sqlx::query!("UPDATE accounts SET balance = balance - $1 WHERE id = $2", amount, from_id)
    .execute(&mut *tx)
    .await?;

sqlx::query!("UPDATE accounts SET balance = balance + $1 WHERE id = $2", amount, to_id)
    .execute(&mut *tx)
    .await?;

tx.commit().await?;
```
</pattern>

<pattern name="seaorm_n_plus_1">
**N+1 Prevention (SeaORM)**

```rust
// GOOD: Smart Entity Loader
let users_with_posts = user::Entity::load()
    .filter(user::Column::Active.eq(true))
    .with(post::Entity)           // 1-N: uses data loader
    .with(profile::Entity)        // 1-1: uses JOIN
    .all(&db)
    .await?;
```
</pattern>
</patterns>

<success_criteria>
- [ ] Connection pool configured with appropriate limits
- [ ] Migrations run successfully on startup
- [ ] Queries compile without errors (SQLx compile-time check)
- [ ] N+1 queries prevented for relations
- [ ] Transactions used for multi-step operations
- [ ] Pool integrated into Axum AppState
</success_criteria>
