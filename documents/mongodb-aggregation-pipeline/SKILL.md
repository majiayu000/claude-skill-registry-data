---
name: mongodb-aggregation-pipeline
version: "2.1.0"
description: Master MongoDB aggregation pipeline for complex data transformations. Learn pipeline stages, grouping, filtering, and data transformation. Use when analyzing data, creating reports, or transforming documents.
sasmp_version: "1.3.0"
bonded_agent: 02-mongodb-queries-aggregation
bond_type: PRIMARY_BOND

# Production-Grade Skill Configuration
capabilities:
  - pipeline-construction
  - stage-optimization
  - data-transformation
  - analytics-queries
  - report-generation

input_validation:
  required_context:
    - collection_name
    - desired_output
  optional_context:
    - sample_documents
    - performance_requirements
    - index_availability

output_format:
  pipeline: array
  explanation: string
  performance_notes: array
  alternatives: array

error_handling:
  common_errors:
    - code: AGG001
      condition: "Invalid stage syntax"
      recovery: "Validate stage operators and field references"
    - code: AGG002
      condition: "Memory limit exceeded"
      recovery: "Add $allowDiskUse: true or optimize with $match early"
    - code: AGG003
      condition: "Unwind on null array"
      recovery: "Use preserveNullAndEmptyArrays: true"

prerequisites:
  mongodb_version: "4.4+"
  required_knowledge:
    - basic-crud
    - query-operators
  recommended_indexes:
    - "Fields used in $match stages"

testing:
  unit_test_template: |
    // Test aggregation pipeline
    const result = await collection.aggregate(pipeline).toArray()
    expect(result).toHaveLength(expectedCount)
    expect(result[0]).toMatchObject(expectedShape)
---

# MongoDB Aggregation Pipeline

Master powerful data transformation with aggregation pipeline.

## Quick Start

### Basic Pipeline Structure
```javascript
const result = await collection.aggregate([
  { $match: { status: 'active' } },
  { $group: { _id: '$category', count: { $sum: 1 } } },
  { $sort: { count: -1 } },
  { $limit: 10 }
]).toArray();
```

### Common Pipeline Stages

```javascript
// $match: Filter documents (like WHERE in SQL)
{ $match: { age: { $gte: 18 }, status: 'active' } }

// $group: Group documents and aggregate
{ $group: {
  _id: '$city',
  total: { $sum: '$amount' },
  average: { $avg: '$price' },
  count: { $sum: 1 }
}}

// $project: Transform fields
{ $project: {
  name: 1,
  email: 1,
  fullName: { $concat: ['$firstName', ' ', '$lastName'] },
  _id: 0
}}

// $sort: Sort results
{ $sort: { createdAt: -1 } }  // -1 for descending, 1 for ascending

// $limit and $skip: Pagination
{ $limit: 10 }
{ $skip: 20 }

// $unwind: Deconstruct arrays
{ $unwind: '$tags' }  // One document per tag

// $lookup: Join collections
{ $lookup: {
  from: 'categories',
  localField: 'categoryId',
  foreignField: '_id',
  as: 'category'
}}

// $facet: Multi-faceted search
{ $facet: {
  byCategory: [{ $group: { _id: '$category', count: { $sum: 1 } } }],
  byPrice: [{ $group: { _id: null, avg: { $avg: '$price' } } }]
}}
```

### Aggregation Functions

```javascript
// Numeric functions
{ $sum: 1 }                    // Count
{ $sum: '$amount' }            // Sum field
{ $avg: '$price' }             // Average
{ $min: '$quantity' }          // Minimum
{ $max: '$quantity' }          // Maximum

// Array functions
{ $push: '$tags' }             // Collect all values
{ $addToSet: '$category' }     // Collect unique values
{ $first: '$name' }            // First element
{ $last: '$name' }             // Last element

// String functions
{ $concat: ['$firstName', ' ', '$lastName'] }
{ $substr: ['$email', 0, 5] }
{ $toLower: '$name' }
{ $toUpper: '$name' }

// Conditional
{ $cond: [
  { $gte: ['$age', 18] },
  'Adult',
  'Minor'
]}
```

## Real-World Examples

### Sales Report by Category
```javascript
await orders.aggregate([
  { $match: { status: 'completed' } },
  { $group: {
    _id: '$category',
    totalSales: { $sum: '$amount' },
    ordersCount: { $sum: 1 },
    avgOrderValue: { $avg: '$amount' }
  }},
  { $sort: { totalSales: -1 } }
]).toArray();
```

### User Activity Summary
```javascript
await users.aggregate([
  { $match: { lastActive: { $gte: new Date(Date.now() - 30*24*60*60*1000) } } },
  { $project: {
    name: 1,
    email: 1,
    lastActive: 1,
    daysInactive: {
      $floor: {
        $divide: [
          { $subtract: [new Date(), '$lastActive'] },
          1000 * 60 * 60 * 24
        ]
      }
    }
  }},
  { $sort: { daysInactive: 1 } }
]).toArray();
```

### Join with Lookup
```javascript
await orders.aggregate([
  { $match: { status: 'pending' } },
  { $lookup: {
    from: 'customers',
    localField: 'customerId',
    foreignField: '_id',
    as: 'customer'
  }},
  { $unwind: '$customer' },
  { $project: {
    orderId: '$_id',
    customerName: '$customer.name',
    total: '$amount',
    _id: 0
  }}
]).toArray();
```

## Python Example

```python
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
collection = client['db']['collection']

pipeline = [
    {'$match': {'status': 'active'}},
    {'$group': {'_id': '$category', 'count': {'$sum': 1}}},
    {'$sort': {'count': -1}}
]

results = list(collection.aggregate(pipeline))
for doc in results:
    print(doc)
```

## Performance Tips

✅ Use $match early to filter documents
✅ Avoid $project before necessary stages
✅ Use indexes on $match fields
✅ Use $limit before expensive operations
✅ Monitor aggregation performance
✅ Use $facet for parallel processing
✅ Avoid large $unwind operations
