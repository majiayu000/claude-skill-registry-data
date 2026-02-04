---
name: sqlite-best-practices
description: SQLite best practices, optimization, and common patterns for Go applications
triggers: [sqlite, database, sql, query, index, transaction, schema]
---

# SQLite Best Practices Skill

## Overview

SQLite is a lightweight, embedded database perfect for applications like the Budget app. This skill covers best practices for using SQLite effectively in Go.

## Connection Setup

### Basic Connection

```go
import (
    "database/sql"
    _ "github.com/mattn/go-sqlite3"
)

func OpenDatabase(path string) (*sql.DB, error) {
    db, err := sql.Open("sqlite3", path)
    if err != nil {
        return nil, err
    }

    // Test connection
    if err := db.Ping(); err != nil {
        return nil, err
    }

    return db, nil
}
```

### Connection with Pragmas

```go
func OpenDatabase(path string) (*sql.DB, error) {
    // Add pragmas to connection string
    dsn := path + "?_journal_mode=WAL&_busy_timeout=5000&_foreign_keys=on"

    db, err := sql.Open("sqlite3", dsn)
    if err != nil {
        return nil, err
    }

    // Or set pragmas after connection
    pragmas := []string{
        "PRAGMA journal_mode = WAL",           // Write-Ahead Logging for better concurrency
        "PRAGMA synchronous = NORMAL",         // Balance safety and speed
        "PRAGMA foreign_keys = ON",            // Enable foreign key constraints
        "PRAGMA busy_timeout = 5000",          // Wait 5s on lock
        "PRAGMA cache_size = -64000",          // 64MB cache
    }

    for _, pragma := range pragmas {
        if _, err := db.Exec(pragma); err != nil {
            return nil, fmt.Errorf("failed to set pragma: %w", err)
        }
    }

    return db, nil
}
```

## Schema Design

### Data Types

SQLite has 5 storage classes:
- `NULL`
- `INTEGER`: For whole numbers, booleans, dates
- `REAL`: For floating point (avoid for money!)
- `TEXT`: For strings, dates (ISO8601)
- `BLOB`: For binary data

**Budget App Convention:**
```sql
CREATE TABLE accounts (
    id TEXT PRIMARY KEY,              -- UUID as text
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    balance INTEGER NOT NULL DEFAULT 0,  -- Cents (integer)
    created_at DATETIME NOT NULL,     -- ISO8601 text
    updated_at DATETIME NOT NULL
);
```

### Money Storage

**Always use INTEGER for money (cents):**

```sql
-- GOOD: Store as cents
balance INTEGER NOT NULL DEFAULT 0  -- $100.00 = 10000

-- BAD: Never use REAL for money
balance REAL  -- Floating point errors!
```

**Conversion:**
```go
// Dollars to cents
cents := int(dollars * 100)

// Cents to dollars
dollars := float64(cents) / 100.0
```

### Foreign Keys

**Enable foreign keys:**
```sql
PRAGMA foreign_keys = ON;
```

**Define foreign keys:**
```sql
CREATE TABLE transactions (
    id TEXT PRIMARY KEY,
    account_id TEXT NOT NULL,
    category_id TEXT NOT NULL,
    amount INTEGER NOT NULL,
    FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);
```

### Constraints

```sql
CREATE TABLE accounts (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL CHECK(type IN ('checking', 'savings', 'credit_card')),
    balance INTEGER NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);

-- Unique constraints
CREATE TABLE allocations (
    id TEXT PRIMARY KEY,
    category_id TEXT NOT NULL,
    period TEXT NOT NULL,
    amount INTEGER NOT NULL,
    UNIQUE(category_id, period)  -- One allocation per category per period
);

-- Or as separate constraint
CREATE UNIQUE INDEX idx_unique_allocation ON allocations(category_id, period);
```

### Indexes

**When to index:**
- Foreign key columns
- Columns used in WHERE clauses
- Columns used in ORDER BY
- Columns used in JOINs

```sql
-- Foreign key indexes
CREATE INDEX idx_transactions_account_id ON transactions(account_id);
CREATE INDEX idx_transactions_category_id ON transactions(category_id);

-- Query filter indexes
CREATE INDEX idx_transactions_date ON transactions(date);

-- Composite indexes for common queries
CREATE INDEX idx_transactions_account_date ON transactions(account_id, date);
```

**Don't over-index:**
- Indexes slow down writes
- Indexes take up space
- Only index columns actually used in queries

## SQL Injection Prevention

### Always Use Parameterized Queries

```go
// GOOD: Parameterized query
query := "SELECT * FROM accounts WHERE name = ?"
rows, err := db.Query(query, userInput)

// BAD: String concatenation - SQL INJECTION VULNERABILITY!
query := fmt.Sprintf("SELECT * FROM accounts WHERE name = '%s'", userInput)
rows, err := db.Query(query)
```

### Named Parameters

```go
// Alternative: Named parameters (sqlite3 driver supports)
query := "INSERT INTO accounts (id, name, type, balance) VALUES (?, ?, ?, ?)"
_, err := db.Exec(query, account.ID, account.Name, account.Type, account.Balance)
```

## Query Patterns

### Insert

```go
func (r *Repository) Create(account *Account) error {
    query := `
        INSERT INTO accounts (id, name, type, balance, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
    `

    _, err := r.db.Exec(
        query,
        account.ID,
        account.Name,
        account.Type,
        account.Balance,
        time.Now().UTC(),
        time.Now().UTC(),
    )

    if err != nil {
        return fmt.Errorf("failed to create account: %w", err)
    }

    return nil
}
```

### Query Single Row

```go
func (r *Repository) GetByID(id string) (*Account, error) {
    query := `
        SELECT id, name, type, balance, created_at, updated_at
        FROM accounts
        WHERE id = ?
    `

    var account Account
    err := r.db.QueryRow(query, id).Scan(
        &account.ID,
        &account.Name,
        &account.Type,
        &account.Balance,
        &account.CreatedAt,
        &account.UpdatedAt,
    )

    if err == sql.ErrNoRows {
        return nil, ErrNotFound
    }
    if err != nil {
        return nil, fmt.Errorf("failed to get account: %w", err)
    }

    return &account, nil
}
```

### Query Multiple Rows

```go
func (r *Repository) GetAll() ([]*Account, error) {
    query := `
        SELECT id, name, type, balance, created_at, updated_at
        FROM accounts
        ORDER BY name
    `

    rows, err := r.db.Query(query)
    if err != nil {
        return nil, fmt.Errorf("failed to query accounts: %w", err)
    }
    defer rows.Close()  // IMPORTANT: Always close rows

    var accounts []*Account
    for rows.Next() {
        var account Account
        err := rows.Scan(
            &account.ID,
            &account.Name,
            &account.Type,
            &account.Balance,
            &account.CreatedAt,
            &account.UpdatedAt,
        )
        if err != nil {
            return nil, fmt.Errorf("failed to scan account: %w", err)
        }
        accounts = append(accounts, &account)
    }

    // Check for errors during iteration
    if err := rows.Err(); err != nil {
        return nil, fmt.Errorf("error iterating rows: %w", err)
    }

    return accounts, nil
}
```

### Update

```go
func (r *Repository) Update(account *Account) error {
    query := `
        UPDATE accounts
        SET name = ?, type = ?, balance = ?, updated_at = ?
        WHERE id = ?
    `

    result, err := r.db.Exec(
        query,
        account.Name,
        account.Type,
        account.Balance,
        time.Now().UTC(),
        account.ID,
    )

    if err != nil {
        return fmt.Errorf("failed to update account: %w", err)
    }

    // Check if row was actually updated
    rowsAffected, err := result.RowsAffected()
    if err != nil {
        return fmt.Errorf("failed to get rows affected: %w", err)
    }

    if rowsAffected == 0 {
        return ErrNotFound
    }

    return nil
}
```

### Delete

```go
func (r *Repository) Delete(id string) error {
    query := "DELETE FROM accounts WHERE id = ?"

    result, err := r.db.Exec(query, id)
    if err != nil {
        return fmt.Errorf("failed to delete account: %w", err)
    }

    rowsAffected, err := result.RowsAffected()
    if err != nil {
        return fmt.Errorf("failed to get rows affected: %w", err)
    }

    if rowsAffected == 0 {
        return ErrNotFound
    }

    return nil
}
```

### Upsert (Insert or Update)

```go
func (r *Repository) Upsert(allocation *Allocation) error {
    query := `
        INSERT INTO allocations (id, category_id, period, amount, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(category_id, period)
        DO UPDATE SET
            amount = excluded.amount,
            updated_at = excluded.updated_at
    `

    _, err := r.db.Exec(
        query,
        allocation.ID,
        allocation.CategoryID,
        allocation.Period,
        allocation.Amount,
        time.Now().UTC(),
        time.Now().UTC(),
    )

    return err
}
```

## Transactions

### Basic Transaction

```go
func (r *Repository) CreateWithTransaction(account *Account, transaction *Transaction) error {
    tx, err := r.db.Begin()
    if err != nil {
        return fmt.Errorf("failed to begin transaction: %w", err)
    }

    // Rollback on error
    defer func() {
        if err != nil {
            tx.Rollback()
        }
    }()

    // Insert account
    _, err = tx.Exec(
        "INSERT INTO accounts (id, name, type, balance) VALUES (?, ?, ?, ?)",
        account.ID, account.Name, account.Type, account.Balance,
    )
    if err != nil {
        return fmt.Errorf("failed to insert account: %w", err)
    }

    // Insert transaction
    _, err = tx.Exec(
        "INSERT INTO transactions (id, account_id, amount) VALUES (?, ?, ?)",
        transaction.ID, transaction.AccountID, transaction.Amount,
    )
    if err != nil {
        return fmt.Errorf("failed to insert transaction: %w", err)
    }

    // Commit
    if err = tx.Commit(); err != nil {
        return fmt.Errorf("failed to commit: %w", err)
    }

    return nil
}
```

### Transaction Helper

```go
func (r *Repository) withTransaction(fn func(tx *sql.Tx) error) error {
    tx, err := r.db.Begin()
    if err != nil {
        return fmt.Errorf("begin transaction: %w", err)
    }

    defer func() {
        if p := recover(); p != nil {
            tx.Rollback()
            panic(p)
        } else if err != nil {
            tx.Rollback()
        } else {
            err = tx.Commit()
        }
    }()

    err = fn(tx)
    return err
}

// Usage
func (r *Repository) CreateAccount(account *Account) error {
    return r.withTransaction(func(tx *sql.Tx) error {
        _, err := tx.Exec("INSERT INTO accounts (...) VALUES (...)", ...)
        return err
    })
}
```

## Query Building

### Dynamic Filters

```go
func (r *Repository) GetTransactions(filters TransactionFilters) ([]*Transaction, error) {
    query := "SELECT * FROM transactions WHERE 1=1"
    args := []interface{}{}

    if filters.AccountID != "" {
        query += " AND account_id = ?"
        args = append(args, filters.AccountID)
    }

    if filters.CategoryID != "" {
        query += " AND category_id = ?"
        args = append(args, filters.CategoryID)
    }

    if !filters.StartDate.IsZero() {
        query += " AND date >= ?"
        args = append(args, filters.StartDate)
    }

    if !filters.EndDate.IsZero() {
        query += " AND date <= ?"
        args = append(args, filters.EndDate)
    }

    query += " ORDER BY date DESC"

    rows, err := r.db.Query(query, args...)
    // ... scan rows
}
```

### Aggregation

```go
func (r *Repository) GetAccountSummary() (int, error) {
    query := "SELECT COALESCE(SUM(balance), 0) FROM accounts"

    var total int
    err := r.db.QueryRow(query).Scan(&total)
    if err != nil {
        return 0, fmt.Errorf("failed to get total: %w", err)
    }

    return total, nil
}
```

## Error Handling

```go
import "errors"

var (
    ErrNotFound      = errors.New("not found")
    ErrDuplicate     = errors.New("duplicate entry")
    ErrForeignKey    = errors.New("foreign key constraint")
)

func (r *Repository) Create(account *Account) error {
    _, err := r.db.Exec("INSERT INTO accounts (...) VALUES (...)", ...)

    if err != nil {
        // Check for specific SQLite errors
        if strings.Contains(err.Error(), "UNIQUE constraint failed") {
            return ErrDuplicate
        }
        if strings.Contains(err.Error(), "FOREIGN KEY constraint failed") {
            return ErrForeignKey
        }
        return fmt.Errorf("database error: %w", err)
    }

    return nil
}
```

## Testing with SQLite

### In-Memory Database

```go
func setupTestDB(t *testing.T) *sql.DB {
    db, err := sql.Open("sqlite3", ":memory:")
    if err != nil {
        t.Fatalf("Failed to open test database: %v", err)
    }

    // Initialize schema
    schema := `
        CREATE TABLE accounts (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            balance INTEGER NOT NULL DEFAULT 0
        );
    `

    if _, err := db.Exec(schema); err != nil {
        t.Fatalf("Failed to create schema: %v", err)
    }

    return db
}

func TestRepository(t *testing.T) {
    db := setupTestDB(t)
    defer db.Close()

    repo := NewRepository(db)
    // ... test with repo
}
```

## Common Patterns

### Batch Insert

```go
func (r *Repository) CreateBatch(accounts []*Account) error {
    tx, err := r.db.Begin()
    if err != nil {
        return err
    }
    defer tx.Rollback()

    stmt, err := tx.Prepare("INSERT INTO accounts (id, name, type, balance) VALUES (?, ?, ?, ?)")
    if err != nil {
        return err
    }
    defer stmt.Close()

    for _, account := range accounts {
        _, err := stmt.Exec(account.ID, account.Name, account.Type, account.Balance)
        if err != nil {
            return err
        }
    }

    return tx.Commit()
}
```

### Count Rows

```go
func (r *Repository) Count() (int, error) {
    var count int
    err := r.db.QueryRow("SELECT COUNT(*) FROM accounts").Scan(&count)
    return count, err
}
```

### Check Existence

```go
func (r *Repository) Exists(id string) (bool, error) {
    var exists bool
    query := "SELECT EXISTS(SELECT 1 FROM accounts WHERE id = ?)"
    err := r.db.QueryRow(query, id).Scan(&exists)
    return exists, err
}
```

## Performance Tips

1. **Use Indexes**: Index foreign keys and filter columns
2. **Use Transactions**: Batch writes in transactions (much faster)
3. **Use Prepared Statements**: For repeated queries
4. **Enable WAL Mode**: Better concurrent read/write
5. **Optimize Cache Size**: Increase for read-heavy workloads
6. **Analyze Queries**: Use `EXPLAIN QUERY PLAN`

```sql
-- Analyze query performance
EXPLAIN QUERY PLAN
SELECT * FROM transactions WHERE account_id = ? AND date > ?;
```

## Common Pitfalls

### ❌ Not Closing Rows

```go
// BAD: rows never closed
rows, _ := db.Query("SELECT * FROM accounts")
for rows.Next() {
    // ...
}
// Missing: defer rows.Close()

// GOOD: Always close
rows, _ := db.Query("SELECT * FROM accounts")
defer rows.Close()  // ✓
for rows.Next() {
    // ...
}
```

### ❌ Not Checking rows.Err()

```go
// BAD: Not checking iteration errors
for rows.Next() {
    rows.Scan(...)
}
// Missing: rows.Err() check

// GOOD: Check for errors
for rows.Next() {
    rows.Scan(...)
}
if err := rows.Err(); err != nil {  // ✓
    return err
}
```

### ❌ Using REAL for Money

```go
// BAD: Floating point for money
balance REAL

// GOOD: Integer cents
balance INTEGER
```

### ❌ Not Enabling Foreign Keys

```go
// BAD: Foreign keys not enforced by default
db, _ := sql.Open("sqlite3", "budget.db")

// GOOD: Enable foreign keys
db, _ := sql.Open("sqlite3", "budget.db")
db.Exec("PRAGMA foreign_keys = ON")
```

## Budget App Specific

### Atomic Balance Updates

```go
func (r *TransactionRepository) CreateWithBalanceUpdate(txn *Transaction) error {
    return r.withTransaction(func(tx *sql.Tx) error {
        // Insert transaction
        _, err := tx.Exec(
            "INSERT INTO transactions (...) VALUES (...)",
            txn.ID, txn.AccountID, txn.Amount, ...,
        )
        if err != nil {
            return err
        }

        // Update account balance atomically
        _, err = tx.Exec(
            "UPDATE accounts SET balance = balance + ? WHERE id = ?",
            txn.Amount,
            txn.AccountID,
        )
        return err
    })
}
```

### Calculating Aggregates

```go
func (r *AllocationRepository) GetTotalAllocated() (int, error) {
    query := "SELECT COALESCE(SUM(amount), 0) FROM allocations"
    var total int
    err := r.db.QueryRow(query).Scan(&total)
    return total, err
}
```
