---
name: MongoDB Aggregation Pipeline Optimization
description: General MongoDB aggregation pipeline optimization techniques including early filtering, index usage, array operators vs $unwind, $lookup optimization, and performance debugging. Use when writing aggregation queries for ANY MongoDB project, debugging slow pipelines, or analyzing query performance. For M32RIMM-specific patterns, use mongodb-m32rimm-patterns skill.
allowed-tools: [Read, Grep, Bash]
---

# MongoDB Aggregation Pipeline Optimization

General optimization patterns for MongoDB aggregation pipelines. Applicable to ANY MongoDB project, regardless of domain or schema.

**Companion Documents**:
- **reference.md**: Detailed examples, benchmarks, and debugging workflows (in this skill directory)
- **mongodb-m32rimm-patterns**: M32RIMM/FISIO-specific patterns (subscription isolation, businessObjects queries)

---

## 1. Pipeline Stage Ordering (MOST CRITICAL)

**Early filtering rule**: Place `$match` as early as possible to reduce data volume.

**Optimal stage order**:
```
$match → $project → $addFields → $lookup → $unwind → $group → $sort → $limit
```

**Why this matters**: MongoDB processes pipeline stages sequentially. Filtering 1M docs to 10K BEFORE $lookup saves 990K unnecessary joins.

### Performance Impact

| Optimization | Speedup | Example |
|--------------|---------|---------|
| Early $match | 10-100x | Filter by tenant/status first |
| Project before lookup | 5-20x | Reduce field count before join |
| Covered queries | 5-10x | Return data from index only |
| Array operators vs $unwind | 5-10x | Filter arrays without unwinding |
| Indexed $lookup | 10-50x | Join on indexed fields |

### Stage Ordering Examples

```javascript
// BAD - filters AFTER expensive operations
db.orders.aggregate([
    {$lookup: {from: 'customers', ...}},  // Joins ALL docs
    {$unwind: '$items'},
    {$match: {status: 'pending'}}         // Filters last
])

// GOOD - filters early, reduces data before expensive ops
db.orders.aggregate([
    {$match: {status: 'pending'}},        // Filter first
    {$project: {_id: 1, items: 1}},       // Reduce fields
    {$lookup: {from: 'customers', ...}}   // Join smaller set
])
```

### MongoDB's Automatic Optimization

MongoDB can move `$match` before `$project` when safe:
```javascript
// Written as:
[
    {$project: {_id: 1, status: 1, amount: 1}},
    {$match: {status: 'pending', amount: {$gt: 100}}}
]

// MongoDB optimizes to:
[
    {$match: {status: 'pending', amount: {$gt: 100}}},
    {$project: {_id: 1, status: 1, amount: 1}}
]
```

**BUT**: Don't rely on this. Write explicit early $match for clarity.

---

## 2. Index Usage & Covered Queries

### Check Index Usage

```javascript
// Explain aggregation execution
db.collection.explain('executionStats').aggregate([
    {$match: {status: 'active', category: 'electronics'}},
    {$project: {_id: 1, name: 1}}
])

// Key fields to check:
// - totalDocsExamined (should be close to nReturned)
// - executionTimeMillis (lower is better)
// - winningPlan.stage (IXSCAN = good, COLLSCAN = bad)
```

### Covered Queries

**Definition**: Query returns all data from index (no document fetch).

**Requirements**:
1. All queried fields are in the index
2. All returned fields are in the index
3. Query doesn't exclude `_id` unless `{_id: 0}` in projection

**Example**:
```javascript
// Index
db.products.createIndex({
    category: 1,
    status: 1,
    updated_at: -1
})

// Covered query - returns only indexed fields
db.products.aggregate([
    {$match: {
        category: 'electronics',
        status: 'active'
    }},
    {$project: {
        _id: 1,
        category: 1,
        status: 1,
        updated_at: 1
    }},
    {$sort: {updated_at: -1}}
])
```

**Performance**: 5-10x faster than document scans.

### Index Strategy Best Practices

1. **Filter fields first**: Most selective filters at start of compound index
2. **Sort fields last**: Include sort fields at end of compound index
3. **Include projection fields**: Add projected fields for covered queries
4. **Avoid index bloat**: Don't index every field (diminishing returns)

```javascript
// Good compound index design
db.orders.createIndex({
    tenant_id: 1,        // Filter: highest selectivity
    status: 1,           // Filter: medium selectivity
    created_at: -1       // Sort field last
})

// Query uses index efficiently
db.orders.aggregate([
    {$match: {
        tenant_id: 'abc123',
        status: 'pending'
    }},
    {$sort: {created_at: -1}}
])
```

---

## 3. Array Operators vs $unwind/$group Anti-Pattern

**AVOID**: `$unwind → $group` for array transformations (blocking stage, slow).

**USE**: Array operators (`$filter`, `$map`, `$reduce`, `$arrayElemAt`, `$size`).

### Quick Example

```javascript
// BAD - explodes documents
db.products.aggregate([
    {$unwind: '$tags'},
    {$match: {'tags': 'sale'}},
    {$group: {_id: '$_id', sale_tags: {$push: '$tags'}}}
])

// GOOD - filter in place
db.products.aggregate([
    {$match: {category: 'electronics'}},
    {$project: {
        sale_tags: {$filter: {input: '$tags', cond: {$eq: ['$$this', 'sale']}}}
    }}
])
```

### Common Array Operators

```javascript
{$filter: {input: '$items', cond: {$eq: ['$$this.status', 'active']}}}
{$map: {input: '$products', in: {id: '$$this._id', price: '$$this.price'}}}
{$arrayElemAt: ['$items', 0]}  // First element
{$size: '$items'}  // Array length
{$reduce: {input: '$items', initialValue: 0, in: {$add: ['$$value', '$$this.price']}}}
```

**Performance**: 5-10x faster for large arrays. See reference.md for detailed examples.

---

## 4. $lookup Optimization

**Critical**: Index foreign collection on lookup field (10-50x speedup).

### Basic vs Optimized Lookup

```javascript
// Basic lookup
{$lookup: {from: 'customers', localField: 'customer_id', foreignField: '_id', as: 'customer'}}

// Optimized with pipeline (filter + project)
{$lookup: {
    from: 'customers',
    let: {customer_id: '$customer_id'},
    pipeline: [
        {$match: {$expr: {$eq: ['$_id', '$$customer_id']}, status: 'active'}},
        {$project: {_id: 1, name: 1, email: 1}}  // Only needed fields
    ],
    as: 'customer'
}}
```

### Required Index

```javascript
// CRITICAL: Index on foreign field
db.customers.createIndex({_id: 1, status: 1})
```

### Multiple Lookups

```javascript
// AVOID: Sequential lookups on multiple collections
// BETTER: Nest related lookups, use pipeline to filter
// BEST: Denormalize if data rarely changes
```

See reference.md for detailed multiple lookup patterns and benchmarks.

---

## 5. $group Optimization

**Key principles**: Group before sort, use $first/$last instead of $push, enable allowDiskUse for large datasets.

### Efficient Grouping

```javascript
// BAD - accumulates entire documents
{$group: {_id: '$customer_id', orders: {$push: '$$ROOT'}}}

// GOOD - accumulate only needed metrics
{$group: {
    _id: '$customer_id',
    count: {$sum: 1},
    first_order_id: {$first: '$_id'},
    last_order_date: {$max: '$created_at'}
}}
```

### Memory Limit (100MB)

```javascript
// Enable disk usage for large aggregations
db.collection.aggregate(pipeline, {allowDiskUse: true})
```

See reference.md for nested grouping patterns and detailed examples.

---

## 6. Materialized Views with $merge/$out

**Use case**: Heavy aggregations run frequently (dashboards, reports).

### $merge vs $out

| Feature | $merge | $out |
|---------|--------|------|
| Behavior | Upserts into target | Replaces entire collection |
| Use when | Incremental updates | Full refresh |

### Quick Example

```javascript
// Incremental update with $merge
{$merge: {into: 'dailySales', on: '_id', whenMatched: 'replace', whenNotMatched: 'insert'}}

// Full replace with $out
{$out: 'productsByCategory'}
```

See reference.md for detailed patterns, update strategies, and scheduling examples.

---

## 7. MongoDB Version Features

**MongoDB 5.0+**: Slot-based execution engine (automatic optimization), $setWindowFields.
**MongoDB 6.0+**: Improved $lookup performance, better memory management.

Check version: `db.version()`

---

## 8. Debugging Slow Pipelines

### 1. Explain Query

```javascript
db.collection.explain('executionStats').aggregate([...])
```

**Check**: `totalDocsExamined` (should be close to `nReturned`), `executionTimeMillis`, `stage` (IXSCAN good, COLLSCAN bad).

### 2. Profile Slow Queries

```javascript
db.setProfilingLevel(1, {slowms: 100})  // Enable
db.system.profile.find().sort({ts: -1}).limit(10)  // Check
db.setProfilingLevel(0)  // Disable
```

### 3. Iterative Testing

Test pipeline stages one at a time to find bottleneck. Add stages incrementally and measure time/doc count.

### 4. MongoDB Compass

Use visual explain in Compass to identify COLLSCAN stages and memory bottlenecks.

See reference.md for detailed debugging workflow with examples.

---

## 9. Common Patterns (Quick Reference)

```javascript
// Count by category
{$group: {_id: '$category', count: {$sum: 1}, avg_price: {$avg: '$price'}}}

// Top N results
{$sort: {order_count: -1}}, {$limit: 10}

// Time-based grouping
{$group: {_id: {year: {$year: '$created_at'}, week: {$week: '$created_at'}}, count: {$sum: 1}}}

// Conditional aggregation
{$group: {
    _id: null,
    pending: {$sum: {$cond: [{$eq: ['$status', 'pending']}, 1, 0]}},
    completed: {$sum: {$cond: [{$eq: ['$status', 'completed']}, 1, 0]}}
}}
```

See reference.md for complete pattern implementations with context.

---

## 10. Anti-Patterns to Avoid

**DON'T**:
- $match after $lookup (filter before lookup)
- $unwind → $group for array transformations (use array operators)
- Querying without indexes (collection scans are slow)
- Multiple sequential $lookup stages (denormalize or combine)
- Bare $group without $match (groups entire collection)
- $sort before $limit without index (sorts everything)
- Projecting all fields before $lookup (transfer unnecessary data)
- Ignoring allowDiskUse for large aggregations (100MB memory limit)

**DO**:
- Filter early (smallest dataset possible)
- Use indexed fields in $match
- Project only needed fields
- Use array operators for array manipulation
- Combine lookups when possible
- Enable allowDiskUse for large aggregations
- Check explain() output before deploying
- Create compound indexes for common query patterns

---

## Performance Checklist

Before deploying aggregation pipeline:

1. **Early filtering**: $match with most selective filters first
2. **Index usage**: Check explain() shows IXSCAN (not COLLSCAN)
3. **Projection**: Reduce fields before expensive operations
4. **Array operators**: Use $filter/$map instead of $unwind/$group
5. **Lookup indexes**: Ensure foreign collection has index on join field
6. **allowDiskUse**: Enable for large aggregations (>100MB)
7. **Testing**: Run explain() on production-sized data

**Performance targets** (1M doc collection):
- Early $match: 90x speedup
- Covered query: 11x speedup
- Array operators: 9x speedup
- Indexed $lookup: 50x speedup

See reference.md for detailed benchmarks.

---

## Quick Reference Card

```javascript
// 1. Filter early (most selective filters first)
{$match: {tenant_id: 'abc', status: 'active'}}

// 2. Project before expensive operations
{$project: {_id: 1, needed_field: 1}}

// 3. Use array operators (not $unwind/$group)
{$filter: {input: '$items', cond: {...}}}

// 4. Optimize lookups with pipeline
{$lookup: {
    from: 'collection',
    let: {...},
    pipeline: [
        {$match: {$expr: {...}, status: 'active'}}
    ],
    as: 'result'
}}

// 5. Check performance
db.collection.explain('executionStats').aggregate([...])

// 6. Enable disk usage for large aggregations
db.collection.aggregate(pipeline, {allowDiskUse: true})

// 7. Use covered queries when possible
// Only project indexed fields

// 8. Group before sort (reduce data volume)
{$group: {...}}, {$sort: {...}}
```

---

## Remember

**Core priorities**:
1. Filter early (smallest dataset before expensive ops)
2. Use indexes (IXSCAN not COLLSCAN)
3. Test with explain() on production-sized data
4. Profile slow queries in production

**When stuck**: Check explain() → Profile → Test stages incrementally → Use Compass visual explain.

**Documentation**: [MongoDB Aggregation Optimization](https://docs.mongodb.com/manual/core/aggregation-pipeline-optimization/)

**Related skills**: `mongodb-m32rimm-patterns` for M32RIMM/FISIO-specific patterns.
