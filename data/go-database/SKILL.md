---
name: go-database
description: Go database operations - SQL, ORMs, transactions, migrations
sasmp_version: "1.3.0"
bonded_agent: 04-go-database
bond_type: PRIMARY_BOND
---

# Go Database Skill

Production database patterns with Go including SQL, ORMs, and data access layer design.

## Overview

Best practices for database operations covering connection pooling, transactions, migrations, and query optimization.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| database | string | yes | - | Database: "postgres", "mysql", "sqlite" |
| orm | string | no | "sqlx" | ORM: "none", "sqlx", "gorm" |
| pool_size | int | no | 25 | Max open connections |

## Core Topics

### Connection Setup
```go
func NewDB(dsn string) (*sqlx.DB, error) {
    db, err := sqlx.Connect("postgres", dsn)
    if err != nil {
        return nil, fmt.Errorf("connect: %w", err)
    }

    db.SetMaxOpenConns(25)
    db.SetMaxIdleConns(5)
    db.SetConnMaxLifetime(5 * time.Minute)
    db.SetConnMaxIdleTime(1 * time.Minute)

    if err := db.Ping(); err != nil {
        return nil, fmt.Errorf("ping: %w", err)
    }

    return db, nil
}
```

### Repository Pattern
```go
type UserRepository struct {
    db *sqlx.DB
}

func (r *UserRepository) FindByID(ctx context.Context, id int64) (*User, error) {
    var user User
    err := r.db.GetContext(ctx, &user,
        `SELECT id, name, email, created_at FROM users WHERE id = $1`, id)
    if err != nil {
        if errors.Is(err, sql.ErrNoRows) {
            return nil, ErrUserNotFound
        }
        return nil, fmt.Errorf("find user %d: %w", id, err)
    }
    return &user, nil
}

func (r *UserRepository) Create(ctx context.Context, user *User) error {
    query := `INSERT INTO users (name, email) VALUES ($1, $2) RETURNING id, created_at`
    return r.db.QueryRowxContext(ctx, query, user.Name, user.Email).
        Scan(&user.ID, &user.CreatedAt)
}
```

### Transactions
```go
func (r *OrderRepository) CreateOrder(ctx context.Context, order *Order, items []OrderItem) error {
    tx, err := r.db.BeginTxx(ctx, nil)
    if err != nil {
        return fmt.Errorf("begin: %w", err)
    }
    defer tx.Rollback()

    // Insert order
    err = tx.QueryRowxContext(ctx,
        `INSERT INTO orders (user_id, total) VALUES ($1, $2) RETURNING id`,
        order.UserID, order.Total).Scan(&order.ID)
    if err != nil {
        return fmt.Errorf("insert order: %w", err)
    }

    // Insert items
    stmt, err := tx.PreparexContext(ctx,
        `INSERT INTO order_items (order_id, product_id, quantity, price) VALUES ($1, $2, $3, $4)`)
    if err != nil {
        return fmt.Errorf("prepare: %w", err)
    }
    defer stmt.Close()

    for _, item := range items {
        if _, err := stmt.ExecContext(ctx, order.ID, item.ProductID, item.Quantity, item.Price); err != nil {
            return fmt.Errorf("insert item: %w", err)
        }
    }

    return tx.Commit()
}
```

### Migrations (goose)
```sql
-- +goose Up
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);

-- +goose Down
DROP TABLE users;
```

## Retry Logic

```go
func (r *Repository) withRetry(ctx context.Context, fn func() error) error {
    backoff := []time.Duration{100*time.Millisecond, 500*time.Millisecond, 2*time.Second}

    for i := 0; i <= len(backoff); i++ {
        err := fn()
        if err == nil {
            return nil
        }

        // Only retry on transient errors
        if !isRetryable(err) {
            return err
        }

        if i < len(backoff) {
            select {
            case <-ctx.Done():
                return ctx.Err()
            case <-time.After(backoff[i]):
            }
        }
    }
    return fmt.Errorf("max retries exceeded")
}

func isRetryable(err error) bool {
    var pgErr *pgconn.PgError
    if errors.As(err, &pgErr) {
        return pgErr.Code == "40001" || pgErr.Code == "40P01" // serialization/deadlock
    }
    return false
}
```

## Unit Test Template

```go
func TestUserRepository_FindByID(t *testing.T) {
    db := setupTestDB(t)
    repo := &UserRepository{db: db}

    // Setup
    user := &User{Name: "Test", Email: "test@example.com"}
    err := repo.Create(context.Background(), user)
    require.NoError(t, err)

    // Test
    found, err := repo.FindByID(context.Background(), user.ID)
    require.NoError(t, err)
    assert.Equal(t, user.Name, found.Name)

    // Test not found
    _, err = repo.FindByID(context.Background(), 99999)
    assert.ErrorIs(t, err, ErrUserNotFound)
}
```

## Troubleshooting

### Failure Modes
| Symptom | Cause | Fix |
|---------|-------|-----|
| Connection refused | Pool exhausted | Increase pool, fix leaks |
| Slow queries | Missing index | Run EXPLAIN ANALYZE |
| Deadlock | Competing tx | Review lock ordering |

### Debug Commands
```bash
# Check active connections
SELECT * FROM pg_stat_activity WHERE datname = 'mydb';

# Analyze query
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';
```

## Usage

```
Skill("go-database")
```
