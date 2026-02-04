---
name: mongodb-index-creation
version: "2.1.0"
description: Master MongoDB index creation and types. Learn single-field, compound, unique, text, geospatial, and TTL indexes. Optimize query performance dramatically with proper indexing.
sasmp_version: "1.3.0"
bonded_agent: 04-mongodb-performance-indexing
bond_type: PRIMARY_BOND

# Production-Grade Skill Configuration
capabilities:
  - single-field-indexes
  - compound-indexes
  - unique-indexes
  - text-indexes
  - geospatial-indexes
  - ttl-indexes

input_validation:
  required_context:
    - collection_name
    - query_patterns
  optional_context:
    - existing_indexes
    - write_frequency
    - collection_size

output_format:
  index_definition: object
  creation_command: string
  impact_analysis: object
  maintenance_notes: array

error_handling:
  common_errors:
    - code: INDEX001
      condition: "Duplicate index"
      recovery: "Check existing indexes, drop duplicate before creating"
    - code: INDEX002
      condition: "Background index build failed"
      recovery: "Check disk space, memory, restart build with background: true"
    - code: INDEX003
      condition: "Index too large for memory"
      recovery: "Consider partial index or remove low-value indexes"

prerequisites:
  mongodb_version: "4.4+"
  required_knowledge:
    - query-patterns
    - esr-rule
  performance_baseline:
    - "Current query latencies documented"

testing:
  unit_test_template: |
    // Verify index created and used
    await collection.createIndex({ field: 1 })
    const indexes = await collection.indexes()
    expect(indexes.some(i => i.key.field === 1)).toBe(true)
    const explain = await collection.find({ field: value }).explain()
    expect(explain.queryPlanner.winningPlan.inputStage.stage).toBe('IXSCAN')
---

# MongoDB Index Creation & Types

Dramatically improve query performance with strategic indexing.

## Quick Start

### Create Indexes
```javascript
// Single field index
await collection.createIndex({ email: 1 })

// Compound index (order matters!)
await collection.createIndex({ status: 1, createdAt: -1 })

// Unique index
await collection.createIndex({ email: 1 }, { unique: true })

// Sparse index (skip null values)
await collection.createIndex({ phone: 1 }, { sparse: true })

// TTL index (auto-delete after 24 hours)
await collection.createIndex({ createdAt: 1 }, { expireAfterSeconds: 86400 })

// Text index (full-text search)
await collection.createIndex({ title: 'text', content: 'text' })

// Geospatial index
await collection.createIndex({ location: '2dsphere' })
```

## Index Types

### Single Field Index
```javascript
// Simple index for one field
db.users.createIndex({ email: 1 })

// Benefits:
// - Speeds up queries on email field
// - Speeds up sorts on email
// - Speeds up range queries: { $gt, $lt }

// When to use:
// - Frequently filtered/sorted field
// - High cardinality (many unique values)
```

### Compound Index
```javascript
// Multiple fields - ORDER MATTERS!
db.orders.createIndex({ status: 1, createdAt: -1 })

// Good for queries like:
// { status: 'completed', createdAt: {$gt: date} }
// { status: 'completed' } // Can use this index

// Bad for:
// { createdAt: {$gt: date} } // Won't use index well
```

### Unique Index
```javascript
// Ensure field uniqueness
db.users.createIndex({ email: 1 }, { unique: true })

// Prevents duplicates:
// - insertOne with duplicate email → ERROR
// - Can't insert if email already exists

// Sparse unique (allow multiple nulls)
db.users.createIndex({ phone: 1 }, { unique: true, sparse: true })
```

### Sparse Index
```javascript
// Skip documents where field is null/missing
db.users.createIndex({ phone: 1 }, { sparse: true })

// Benefits:
// - Smaller index (excludes nulls)
// - Matches queries with { $exists: true }

// When to use:
// - Optional fields (not all documents have it)
// - Reduce index size
```

### Text Index
```javascript
// Full-text search
db.articles.createIndex({
  title: 'text',
  content: 'text',
  tags: 'text'
})

// Query:
db.articles.find({ $text: { $search: 'mongodb' } })

// Weights (title more important than content)
db.articles.createIndex({
  title: 'text',
  content: 'text'
}, { weights: { title: 10, content: 5 } })
```

### Geospatial Index
```javascript
// 2D spherical (lat/long)
db.venues.createIndex({ location: '2dsphere' })

// Query nearby
db.venues.find({
  location: {
    $near: {
      type: 'Point',
      coordinates: [-73.97, 40.77]
    },
    $maxDistance: 5000  // 5km
  }
})
```

### TTL Index
```javascript
// Auto-delete documents after time period
db.sessions.createIndex({ createdAt: 1 }, {
  expireAfterSeconds: 3600  // 1 hour
})

// Use cases:
// - Sessions that expire
// - Temporary logs
// - Cache-like collections

// MongoDB checks once per minute
// Deletion might lag up to 1 minute
```

## Index Management

### List Indexes
```javascript
// Show all indexes
const indexes = await collection.indexes()
console.log(indexes)

// Shows: name, key, size, doc count
```

### Drop Index
```javascript
// Drop specific index
await collection.dropIndex('email_1')

// Drop all non-_id indexes
await collection.dropIndexes()
```

### Index Options
```javascript
await collection.createIndex({ email: 1 }, {
  unique: true,           // Enforce uniqueness
  sparse: true,          // Skip nulls
  background: true,      // Don't block writes
  expireAfterSeconds: 86400, // TTL
  collation: { locale: 'en' }, // Language-specific
  name: 'custom_name'    // Custom index name
})
```

## Index Design: ESR Rule

**Equality, Sort, Range** - optimal compound index order

```javascript
// Query: Find active users sorted by created date, age 18-65
db.users.find({
  status: 'active',          // Equality
  age: { $gte: 18, $lte: 65 } // Range
}).sort({ createdAt: -1 })     // Sort

// Optimal index:
db.users.createIndex({
  status: 1,         // Equality first
  createdAt: -1,    // Sort second
  age: 1            // Range last
})
```

## Covered Queries

### Make Query "Covered"
```javascript
// Query returns entirely from index, no documents fetched!

// Create index with all needed fields
db.users.createIndex({ email: 1, name: 1, age: 1 })

// Query (covered - no docs fetched)
db.users.find(
  { email: 'user@example.com' },
  { projection: { email: 1, name: 1, age: 1, _id: 0 } }
)

// Much faster than fetching documents!
```

## Monitoring Indexes

### Check Index Usage
```javascript
// MongoDB 4.4+
db.collection.aggregate([
  { $indexStats: {} }
])

// Shows:
// - accesses.ops: Number of operations using index
// - accesses.since: When index was created
```

### Remove Unused Indexes
```javascript
// Identify unused:
// - Low accesses.ops value
// - Recent accesses.since date

// Drop unused indexes:
await collection.dropIndex('unused_index_name')
```

## Best Practices

✅ **Index Design:**
1. **Index for queries** - Add on frequently filtered fields
2. **Use ESR rule** - Equality, Sort, Range order
3. **Avoid over-indexing** - Each index has cost
4. **Monitor index size** - Large indexes need memory
5. **Test impact** - Measure query performance

✅ **Performance:**
1. **Create indexes early** - Before data growth
2. **Use explain()** - Verify index usage (IXSCAN)
3. **Batch index creation** - If many needed
4. **Monitor index stats** - Remove unused
5. **Plan for growth** - Future query patterns

❌ **Avoid:**
1. **Index everything** - Wastes storage and memory
2. **Complex regex without index** - Always slow
3. **Sorting without index** - Memory-intensive
4. **Large text indexes** - Memory usage
5. **Outdated indexes** - Remove when no longer needed

## Next Steps

1. **Identify slow queries** - Use explain()
2. **Create strategic indexes** - For your access patterns
3. **Monitor performance** - Before/after metrics
4. **Optimize compound indexes** - ESR rule
5. **Remove unused indexes** - Keep lean

---

**Ready to speed up your MongoDB!** ⚡
