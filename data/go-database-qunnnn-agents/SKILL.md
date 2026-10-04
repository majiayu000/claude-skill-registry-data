---
name: go-database
description: "Best practices for Go database access. Covers parameterized queries, struct scanning, transactions, error handling, and connection pooling."
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 06 May 2026 04:35:00 GMT
---

## Best Practices

1. **Use sqlx or pgx** — Avoid ORMs like GORM for complex production systems. They hide SQL and cause performance issues.
2. **Parameterized queries** — NEVER concatenate strings into SQL. Use `?` or `$1` placeholders.
3. **Propagate Context** — Always use `*Context` methods (`QueryContext`, `ExecContext`) to respect timeouts and cancellation.
4. **Handle `sql.ErrNoRows`** — Distinguish between "no data found" and an actual database error.
5. **Always close rows** — Use `defer rows.Close()` immediately after checking the error from `QueryContext`.
6. **Transactions for atomicity** — Wrap multi-statement updates in a transaction.
7. **Handle NULLs** — Use pointers (e.g., `*string`) or `sql.NullString` for columns that can be null.
8. **Connection pooling** — Configure `SetMaxOpenConns` and `SetMaxIdleConns` based on your load.

## Query Examples

### Selecting a single row (sqlx)
```go
var user User
err := db.GetContext(ctx, &user, "SELECT * FROM users WHERE id = $1", id)
if errors.Is(err, sql.ErrNoRows) {
    return nil, ErrNotFound
}
```

### Selecting multiple rows (sqlx)
```go
var users []User
err := db.SelectContext(ctx, &users, "SELECT * FROM users WHERE status = $1", "active")
```

### Executing an update
```go
result, err := db.ExecContext(ctx, "UPDATE users SET status = $1 WHERE id = $2", "inactive", id)
if err != nil {
    return err
}
rowsAffected, _ := result.RowsAffected()
```

## Transactions

```go
tx, err := db.BeginTxx(ctx, nil)
if err != nil {
    return err
}
defer tx.Rollback() // Safe to call even if committed

if _, err := tx.ExecContext(ctx, ...); err != nil {
    return err
}

return tx.Commit()
```

## Connection Pool Configuration

```go
db.SetMaxOpenConns(25)
db.SetMaxIdleConns(25)
db.SetConnMaxLifetime(5 * time.Minute)
```

## Anti-patterns

- ❌ **SQL Injection**: `fmt.Sprintf("SELECT * FROM users WHERE name='%s'", name)`.
- ❌ **Leaking connections**: Forgetting `rows.Close()`.
- ❌ **Ignoring `rows.Err()`**: Always check `rows.Err()` after the `for rows.Next()` loop.
- ❌ **ORMs for everything**: Resulting in N+1 query problems.
- ❌ **Long-running transactions**: Holding locks too long and blocking other operations.
