---
name: cool-mysql
description: Use this skill when working with the cool-mysql library for Go. This skill provides comprehensive guidance on using cool-mysql's MySQL helper functions, including dual connection pools, named parameters, template syntax, caching strategies, and advanced query patterns. Apply when writing database code, optimizing queries, setting up caching, or migrating from database/sql.
---

# cool-mysql MySQL Helper Library

## Overview

`cool-mysql` is a MySQL helper library for Go that wraps `database/sql` with MySQL-specific conveniences while keeping the underlying interfaces intact. The library reduces boilerplate code for common database operations while providing advanced features like caching, automatic retries, and dual read/write connection pools.

**Core Philosophy:**
- Keep `database/sql` interfaces intact
- Provide conveniences without hiding MySQL behavior
- Focus on productivity without sacrificing control
- Type-safe operations with flexible result mapping

## When to Use This Skill

Use this skill when:
- Writing MySQL database operations in Go
- Setting up database connections with read/write separation
- Implementing caching strategies for queries
- Working with struct mappings and MySQL columns
- Migrating from `database/sql` to `cool-mysql`
- Optimizing query performance
- Handling transactions with proper context management
- Debugging query issues or understanding error handling
- Implementing CRUD operations, upserts, or batch inserts

## Core Concepts

### 1. Dual Connection Pools

`cool-mysql` maintains separate connection pools for reads and writes to optimize for read-heavy workloads.

**Default Behavior:**
- `Select()`, `SelectJSON()`, `Count()`, `Exists()` → Read pool
- `Insert()`, `Upsert()`, `Exec()` → Write pool
- `SelectWrites()`, `ExistsWrites()` → Write pool (for read-after-write consistency)

**When to use SelectWrites():**
Use immediately after writing data when you need consistency:
```go
db.Insert("users", user)
// Need immediate consistency - use write pool
db.SelectWrites(&user, "SELECT `id`, `name`, `email`, `age`, `active`, `created_at`, `updated_at` FROM `users` WHERE `id` = @@id", 0, user.ID)
```

### 2. Named Parameters

cool-mysql uses `@@paramName` syntax instead of positional `?` placeholders.

**Key Points:**
- Parameters are case-insensitive when merged
- Structs can be used directly as parameters (field names → parameter names)
- Use `mysql.Params{"key": value}` for explicit parameters
- Use `mysql.Raw()` to inject literal SQL (not escaped)

**Example:**
```go
// Named parameters
db.Select(&users, "SELECT `id`, `name`, `email`, `age`, `active`, `created_at`, `updated_at` FROM `users` WHERE `age` > @@minAge AND `status` = @@status", 0,
    mysql.Params{"minAge": 18, "status": "active"})

// Struct as parameters
user := User{ID: 1, Name: "Alice"}
db.Exec("UPDATE `users` SET `name` = @@Name WHERE `id` = @@ID", user)

// Raw SQL injection
db.Select(&users, "SELECT `id`, `name`, `email`, `age`, `active`, `created_at`, `updated_at` FROM `users` WHERE @@condition", 0,
    mysql.Raw("created_at > NOW() - INTERVAL 1 DAY"))
```

### 3. Template Syntax

cool-mysql supports Go template syntax for conditional query logic.

**Important Distinctions:**
- Template variables use **field names** (`.Name`), not column names from tags
- Template processing happens **before** parameter interpolation
- Access parameters directly as fields: `.ParamName`

**CRITICAL: Marshaling Template Values**

When injecting VALUES (not identifiers) via templates, you MUST use the `marshal` pipe:

```go
// ✅ CORRECT - Use @@param for values (automatically marshaled)
query := "SELECT `id`, `name`, `email`, `age`, `active`, `created_at`, `updated_at` FROM `users` WHERE {{ if .MinAge }}`age` > @@minAge{{ end }}"

// ✅ CORRECT - Use | marshal when injecting value directly in template
query := "SELECT `id`, `name`, `email`, `age`, `active`, `created_at`, `updated_at` FROM `users` WHERE `name` = {{ .Name | marshal }}"

// ❌ WRONG - Direct injection without marshal causes syntax errors
query := "SELECT `id`, `name`, `email`, `age`, `active`, `created_at`, `updated_at` FROM `users` WHERE `name` = {{ .Name }}"  // BROKEN!

// ✅ CORRECT - Identifiers (column names) validated, then injected
if !allowedColumns[sortBy] { return errors.New("invalid column") }
query := "SELECT `id`, `name`, `email`, `age`, `active`, `created_at`, `updated_at` FROM `users` ORDER BY {{ .SortBy }}"  // OK - validated identifier
```

**Best Practice:** Use `@@param` syntax for values. Only use template injection with `| marshal` when you need conditional value logic.

**Example:**
```go
db.Select(&users,
    "SELECT `id`, `name`, `email`, `age`, `active`, `created_at`, `updated_at` FROM `users` WHERE 1=1"+
    " {{ if .MinAge }}AND `age` > @@minAge{{ end }}"+
    " {{ if .Status }}AND `status` = @@status{{ end }}",
    0,
    mysql.Params{"minAge": 18, "status": "active"})
```

### 4. Caching

cool-mysql provides pluggable caching with support for Redis, Memcached, or in-memory storage.

**Cache TTL:**
- `0` = No caching (always query database)
- `> 0` = Cache for specified duration (e.g., `5*time.Minute`)

**Cache Setup:**
```go
// Redis (with distributed locking)
db.EnableRedis(redisClient)

// Memcached
db.EnableMemcache(memcacheClient)

// In-memory (weak pointers, GC-managed)
db.UseCache(mysql.NewWeakCache())

// Layered caching (fast local + shared distributed)
db.UseCache(mysql.NewMultiCache(
    mysql.NewWeakCache(),      // L1: Fast local cache
    mysql.NewRedisCache(redis), // L2: Shared distributed cache
))
```

**Only SELECT operations are cached** - writes always hit the database.

### 5. Struct Tag Mapping

Control column mapping and behavior with `mysql` struct tags.

**Tag Options:**
- `mysql:"column_name"` - Map to database column
- `mysql:"column_name,defaultzero"` - Write `DEFAULT(column_name)` for zero values
- `mysql:"column_name,omitempty"` - Same as `defaultzero`
- `mysql:"column_name,insertDefault"` - Same as `defaultzero`
- `mysql:"-"` - Completely ignore this field
- `mysql:"column0x2cname"` - Hex encoding for special characters (becomes `column,name`)

**Example:**
```go
type User struct {
    ID        int       `mysql:"id"`
    Name      string    `mysql:"name"`
    Email     string    `mysql:"email"`
    CreatedAt time.Time `mysql:"created_at,defaultzero"` // Use DB default on zero value
    UpdatedAt time.Time `mysql:"updated_at,defaultzero"`
    Password  string    `mysql:"-"` // Never include in queries
}
```

## Quick Start Guide

### Creating a Database Connection

**From connection parameters:**
```go
db, err := mysql.New(
    wUser, wPass, wSchema, wHost, wPort,  // Write connection
    rUser, rPass, rSchema, rHost, rPort,  // Read connection
    collation,                             // e.g., "utf8mb4_unicode_ci"
    timeZone,                              // e.g., "America/New_York"
)
```

**From DSN strings:**
```go
db, err := mysql.NewFromDSN(writesDSN, readsDSN)
```

**From existing connections:**
```go
db, err := mysql.NewFromConn(writesConn, readsConn)
```

### Basic Query Patterns

**Select into struct slice:**
```go
var users []User
err := db.Select(&users, "SELECT `id`, `name`, `email`, `age`, `active`, `created_at`, `updated_at` FROM `users` WHERE `age` > @@minAge", 0, 18)
```

**Select single value:**
```go
var name string
err := db.Select(&name, "SELECT `name` FROM `users` WHERE `id` = @@id", 0, 1)
// Returns sql.ErrNoRows if not found
```

**Count records:**
```go
count, err := db.Count("SELECT COUNT(*) FROM `users` WHERE `active` = @@active", 0, 1)
```

**Check existence:**
```go
exists, err := db.Exists("SELECT 1 FROM `users` WHERE `email` = @@email", 0, "user@example.com")
```

**Insert data:**
```go
// Single insert
user := User{Name: "Alice", Email: "alice@example.com"}
err := db.Insert("users", user)

// Batch insert (automatically chunked)
users := []User{{Name: "Bob"}, {Name: "Charlie"}}
err := db.Insert("users", users)
```

**Upsert (INSERT ... ON DUPLICATE KEY UPDATE):**
```go
err := db.Upsert(
    "users",                      // table
    []string{"email"},           // unique columns
    []string{"name", "updated_at"}, // columns to update on conflict
    "",                          // optional WHERE clause
    user,                        // data
)
```

**Execute query:**
```go
err := db.Exec("UPDATE `users` SET `active` = 1 WHERE `id` = @@id", 1)
```

## Migration Guide from database/sql

### Key Differences

| database/sql | cool-mysql | Notes |
|--------------|------------|-------|
| `?` placeholders | `@@paramName` | Named parameters are case-insensitive |
| `db.Query()` + `rows.Scan()` | `db.Select(&result, query, cacheTTL, params)` | Automatic scanning into structs |
| Manual connection pools | Dual pools (read/write) | Automatic routing based on operation |
| No caching | Built-in caching | Pass TTL as second parameter |
| `sql.ErrNoRows` always | `sql.ErrNoRows` for single values only | Slices return empty, not error |
| Manual chunking | Automatic chunking | Insert operations respect `max_allowed_packet` |
| No retry logic | Automatic retries | Handles deadlocks, timeouts, connection losses |

### Migration Pattern

**Before (database/sql):**
```go
rows, err := db.Query("SELECT `id`, `name`, `email` FROM `users` WHERE `age` > ?", 18)
if err != nil {
    return err
}
defer rows.Close()

var users []User
for rows.Next() {
    var u User
    if err := rows.Scan(&u.ID, &u.Name, &u.Email); err != nil {
        return err
    }
    users = append(users, u)
}
return rows.Err()
```

**After (cool-mysql):**
```go
var users []User
return db.Select(&users, "SELECT `id`, `name`, `email`, `age`, `active`, `created_at`, `updated_at` FROM `users` WHERE `age` > @@minAge", 0, 18)
```

## Best Practices

### Parameter Handling

**DO:**
- Use `@@paramName` syntax consistently
- Use `mysql.Params{}` for clarity
- Use structs as parameters when appropriate
- Use `mysql.Raw()` for literal SQL that shouldn't be escaped

**DON'T:**
- Mix `?` and `@@` syntax (use `@@` exclusively)
- Assume parameters are case-sensitive (they're normalized)
- Inject user input with `mysql.Raw()` (SQL injection risk)

### Template Usage

**DO:**
- Use templates for conditional query logic
- Use `@@param` for values (preferred - automatically marshaled)
- Use `{{.Field | marshal}}` when injecting values directly in templates
- Validate/whitelist identifiers (column names) before template injection
- Reference parameters by field name: `.ParamName`
- Add custom template functions with `db.AddTemplateFuncs()`

**DON'T:**
- Inject values without marshal: `{{.Name}}` causes syntax errors
- Use column names in templates (use field names)
- Forget that templates process before parameter interpolation
- Use templates when named parameters suffice
- Inject user-controlled identifiers without validation

### Caching Strategy

**DO:**
- Use `0` TTL for frequently-changing data
- Use longer TTLs (5-60 minutes) for stable reference data
- Use `SelectWrites()` immediately after writes for consistency
- Consider `MultiCache` for high-traffic applications
- Enable Redis distributed locking to prevent cache stampedes

**DON'T:**
- Cache writes (they're automatically skipped)
- Use same TTL for all queries (tune based on data volatility)
- Forget that cache keys include query + parameters

### Struct Tags

**DO:**
- Use `defaultzero` for timestamp columns with DB defaults
- Use `mysql:"-"` to exclude sensitive fields
- Use hex encoding for column names with special characters
- Implement `Zeroer` interface for custom zero-value detection

**DON'T:**
- Forget that tag column names override field names
- Mix `json` tags with `mysql` tags without testing

### Error Handling

**DO:**
- Check for `sql.ErrNoRows` when selecting single values
- Rely on automatic retries for transient errors (deadlocks, timeouts)
- Use `ExecResult()` when you need `LastInsertId()` or `RowsAffected()`

**DON'T:**
- Expect `sql.ErrNoRows` when selecting into slices (returns empty slice)
- Implement manual retry logic (already built-in)

### Performance Optimization

**DO:**
- Use channels for memory-efficient streaming of large datasets
- Use `SelectWrites()` sparingly (only when consistency required)
- Enable caching for expensive or frequent queries
- Use batch operations (slices/channels) for large inserts

**DON'T:**
- Load entire large result sets into memory when streaming is possible
- Use `SelectWrites()` as default (defeats read pool optimization)
- Cache everything (tune TTL based on access patterns)

## Advanced Patterns

### Streaming with Channels

**Select into channel:**
```go
userCh := make(chan User)
go func() {
    defer close(userCh)
    db.Select(userCh, "SELECT `id`, `name`, `email`, `age`, `active`, `created_at`, `updated_at` FROM `users`", 0)
}()

for user := range userCh {
    // Process user
}
```

**Insert from channel:**
```go
userCh := make(chan User)
go func() {
    for _, u := range users {
        userCh <- u
    }
    close(userCh)
}()

err := db.Insert("users", userCh)
```

### Function Receivers

```go
err := db.Select(func(u User) {
    log.Printf("Processing user: %s", u.Name)
}, "SELECT `id`, `name`, `email`, `age`, `active`, `created_at`, `updated_at` FROM `users`", 0)
```

### Transaction Management

```go
tx, commit, cancel, err := mysql.GetOrCreateTxFromContext(ctx)
defer cancel()
if err != nil {
    return err
}

// Store transaction in context
ctx = mysql.NewContextWithTx(ctx, tx)

// Do database operations...

if err := commit(); err != nil {
    return err
}
```

### Custom Interfaces

**Custom zero detection:**
```go
type CustomTime struct {
    time.Time
}

func (ct CustomTime) IsZero() bool {
    return ct.Time.IsZero() || ct.Time.Unix() == 0
}
```

**Custom value conversion:**
```go
type Point struct {
    X, Y float64
}

func (p Point) Values() []any {
    return []any{p.X, p.Y}
}
```

## Environment Variables

Configure behavior via environment variables:

- `COOL_MAX_EXECUTION_TIME_TIME` - Max query execution time (default: 27s)
- `COOL_MAX_ATTEMPTS` - Max retry attempts (default: unlimited)
- `COOL_REDIS_LOCK_RETRY_DELAY` - Lock retry delay (default: 0.020s)
- `COOL_MYSQL_MAX_QUERY_LOG_LENGTH` - Max query length in logs (default: 4096 bytes)

## Bundled Resources

This skill includes comprehensive reference documentation and working examples:

### Reference Documentation (`references/`)

- **api-reference.md** - Complete API documentation for all methods
- **query-patterns.md** - Query pattern examples and best practices
- **caching-guide.md** - Detailed caching strategies and configuration
- **struct-tags.md** - Comprehensive struct tag reference
- **testing-patterns.md** - Testing approaches with sqlmock

To access reference documentation:
```
Read references/api-reference.md for complete API documentation
Read references/query-patterns.md for query examples
Read references/caching-guide.md for caching strategies
Read references/struct-tags.md for struct tag details
Read references/testing-patterns.md for testing patterns
```

### Working Examples (`examples/`)

- **basic-crud.go** - Simple CRUD operations
- **advanced-queries.go** - Templates, channels, function receivers
- **caching-setup.go** - Cache configuration examples
- **transaction-patterns.go** - Transaction handling patterns
- **upsert-examples.go** - Upsert use cases

To access examples:
```
Read examples/basic-crud.go for basic patterns
Read examples/advanced-queries.go for advanced usage
Read examples/caching-setup.go for cache setup
Read examples/transaction-patterns.go for transactions
Read examples/upsert-examples.go for upsert patterns
```

## Common Gotchas

1. **Empty Result Handling**: Selecting into slice returns empty slice (not `sql.ErrNoRows`); selecting into single value returns `sql.ErrNoRows`

2. **Template vs Column Names**: Templates use field names (`.Name`), not column names from tags

3. **Cache Keys**: Include both query and parameters, so identical queries with different params cache separately

4. **Read/Write Consistency**: Use `SelectWrites()` immediately after writes, not `Select()`

5. **Struct Tag Priority**: `mysql` tag overrides field name for column mapping

6. **Parameter Case**: Parameters are case-insensitive when merged (normalized to lowercase)

7. **Automatic Chunking**: Large inserts automatically chunk based on `max_allowed_packet`

8. **Retry Behavior**: Automatic retries for error codes 1213 (deadlock), 1205 (lock timeout), 2006 (server gone), 2013 (connection lost)

## Next Steps

- Read `references/api-reference.md` for complete API documentation
- Check `examples/basic-crud.go` to see common patterns in action
- Review `references/caching-guide.md` for caching best practices
- Study `references/struct-tags.md` for advanced struct mapping
- Explore `examples/advanced-queries.go` for complex query patterns
