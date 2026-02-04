---
name: static-data
description: Bulk insert optimization pattern for static/reference data sync
---
# Static Data Sync Pattern

Use this pattern when syncing large volumes of reference/static data from external APIs to a database.

## Key Principles

### 1. Bulk INSERT with Multi-Row VALUES

Instead of individual INSERT statements, batch rows into single queries:

```go
// Bad: N queries for N rows
for _, item := range items {
    db.Exec("INSERT INTO items (...) VALUES ($1, $2, ...)", item.A, item.B)
}

// Good: 1 query for N rows (batch size 500)
valueStrings := make([]string, 0, len(batch))
valueArgs := make([]interface{}, 0, len(batch)*numCols)
for i, item := range batch {
    base := i * numCols
    valueStrings = append(valueStrings, fmt.Sprintf(
        "($%d, $%d, $%d, NOW())", base+1, base+2, base+3))
    valueArgs = append(valueArgs, item.A, item.B, item.C)
}
query := fmt.Sprintf(`INSERT INTO items (...) VALUES %s
    ON CONFLICT (pk) DO UPDATE SET ...`,
    strings.Join(valueStrings, ", "))
db.ExecContext(ctx, query, valueArgs...)
```

### 2. Batch Size

- **500 rows per query** is a good default for PostgreSQL
- Balances query size vs network round trips
- Adjust based on column count and data size

### 3. Pre-Filter for Foreign Keys

When child records reference parent records, pre-filter to avoid FK violations:

```go
// Collect unique parent IDs from batch
parentIDs := collectUniqueParentIDs(childRecords)

// Query which parents exist
rows, _ := db.Query(
    "SELECT id FROM parents WHERE id = ANY($1) AND deleted_at IS NULL",
    pq.Array(parentIDs))

existingParents := make(map[string]struct{})
for rows.Next() {
    var id string
    rows.Scan(&id)
    existingParents[id] = struct{}{}
}

// Filter children to only those with existing parents
validChildren := filterByExistingParents(childRecords, existingParents)
```

### 4. API Rate Limiting

Match the external API's rate limits:

```go
const (
    DefaultRateDelay = 250 * time.Millisecond  // 4 req/sec
    Min429Wait       = 5 * time.Second         // Min wait on 429
    Max429Wait       = 120 * time.Second       // Cap wait time
    MaxRetries       = 10
)
```

### 5. Progress Logging

Log batch progress for visibility:

```go
result, _ := db.ExecContext(ctx, query, valueArgs...)
rows, _ := result.RowsAffected()
fmt.Printf("[DB] batch: %d attempted, %d affected\n", len(batch), rows)
```

## Performance Impact

- **500x fewer queries** (from 22K individual INSERTs to 44 batch queries)
- **Faster sync times** (minutes vs hours)
- **Lower database load** (fewer connections, less parsing overhead)

## When to Use

- Syncing reference data from external APIs (markets, products, users)
- Bulk imports from files
- Any scenario with thousands of rows to upsert

## Example Implementation

See: `ssmd/internal/secmaster/store.go`
- `bulkUpsertEvents()` - bulk INSERT for events
- `bulkUpsertMarkets()` - bulk INSERT with FK pre-filtering
- `UpsertMarketBatch()` - orchestrates pre-filter + batch INSERT
