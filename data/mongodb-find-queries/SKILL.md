---
name: mongodb-find-queries
version: "2.1.0"
description: Master MongoDB find queries with filters, projections, sorting, and pagination. Learn query operators, comparison, logical operators, and real-world query patterns. Use when retrieving data from MongoDB collections.
sasmp_version: "1.3.0"
bonded_agent: 02-mongodb-queries-aggregation
bond_type: PRIMARY_BOND

# Production-Grade Skill Configuration
capabilities:
  - query-construction
  - filter-operators
  - projection-design
  - sorting-pagination
  - text-search

input_validation:
  required_context:
    - collection_name
    - filter_criteria
  optional_context:
    - projection_fields
    - sort_order
    - pagination_params

output_format:
  query: object
  options: object
  explanation: string
  performance_tips: array

error_handling:
  common_errors:
    - code: FIND001
      condition: "Projection mixing include/exclude"
      recovery: "Use either inclusion or exclusion, not both (except _id)"
    - code: FIND002
      condition: "Sort memory limit exceeded"
      recovery: "Create index on sort field or use allowDiskUse"
    - code: FIND003
      condition: "Invalid regex pattern"
      recovery: "Validate regex syntax, escape special characters"

prerequisites:
  mongodb_version: "4.0+"
  required_knowledge:
    - mongodb-basics
    - query-operators
  index_requirements:
    - "Indexes on frequently filtered fields recommended"

testing:
  unit_test_template: |
    // Test find query
    const results = await collection.find(filter, { projection }).toArray()
    expect(results).toHaveLength(expectedCount)
    expect(results[0]).toHaveProperty('expectedField')
---

# MongoDB Find Queries

Master the find() method for powerful data retrieval.

## Quick Start

### Basic Query
```javascript
// Find one document
const user = await collection.findOne({ email: 'user@example.com' })

// Find multiple documents
const users = await collection.find({ status: 'active' }).toArray()

// Find with multiple conditions
const products = await collection.find({
  price: { $gt: 100 },
  category: 'electronics'
}).toArray()
```

### Query Operators Reference

**Comparison Operators:**
```javascript
{ field: { $eq: value } }      // Equal
{ field: { $ne: value } }      // Not equal
{ field: { $gt: value } }      // Greater than
{ field: { $gte: value } }     // Greater or equal
{ field: { $lt: value } }      // Less than
{ field: { $lte: value } }     // Less or equal
{ field: { $in: [val1, val2] } } // In array
{ field: { $nin: [val1, val2] } } // Not in array
```

**Logical Operators:**
```javascript
{ $and: [{field1: val1}, {field2: val2}] }  // AND
{ $or: [{field1: val1}, {field2: val2}] }   // OR
{ $not: {field: {$gt: 5}} }                // NOT
{ $nor: [{field1: val1}, {field2: val2}] }  // NOR
```

**Array Operators:**
```javascript
{ field: { $all: [val1, val2] } }    // All values in array
{ field: { $elemMatch: {...} } }     // Match array elements
{ field: { $size: 5 } }              // Array size exactly 5
```

## Projection (Select Fields)

```javascript
// Include fields
db.users.findOne({...}, { projection: { name: 1, email: 1 } })
// Returns: { _id, name, email }

// Exclude fields
db.users.findOne({...}, { projection: { password: 0 } })
// Returns: all fields except password

// Hide _id
db.users.findOne({...}, { projection: { _id: 0, name: 1 } })

// Computed fields
db.users.findOne({...}, {
  projection: {
    firstName: 1,
    lastName: 1,
    fullName: { $concat: ['$firstName', ' ', '$lastName'] }
  }
})
```

## Sorting

```javascript
// Sort ascending (1) or descending (-1)
db.products.find({}).sort({ price: 1 }).toArray()      // Price ascending
db.products.find({}).sort({ createdAt: -1 }).toArray() // Newest first

// Multi-field sort
db.orders.find({}).sort({
  status: 1,        // Active first
  createdAt: -1     // Then newest
}).toArray()

// Case-insensitive sort
db.users.find({}).collation({ locale: 'en', strength: 2 }).sort({ name: 1 })
```

## Pagination

```javascript
// Method 1: Skip and Limit
const pageSize = 10
const pageNumber = 2
const skip = (pageNumber - 1) * pageSize

const results = await collection
  .find({})
  .skip(skip)
  .limit(pageSize)
  .toArray()

// Method 2: Cursor-based (better for large datasets)
const lastId = objectIdOfLastDocument
const results = await collection
  .find({ _id: { $gt: lastId } })
  .limit(pageSize)
  .toArray()
```

## Text Search

```javascript
// Create text index first
db.articles.createIndex({ title: 'text', content: 'text' })

// Search
db.articles.find(
  { $text: { $search: 'mongodb database' } },
  { score: { $meta: 'textScore' } }
).sort({ score: { $meta: 'textScore' } }).toArray()

// Phrase search
db.articles.find({ $text: { $search: '"mongodb database"' } })

// Exclude terms
db.articles.find({ $text: { $search: 'mongodb -relational' } })
```

## Regex Queries

```javascript
// Case-sensitive regex
db.users.find({ email: { $regex: /^admin/, $options: '' } })

// Case-insensitive
db.users.find({ email: { $regex: /gmail/, $options: 'i' } })

// Multiline
db.posts.find({ content: { $regex: /^mongodb/m } })

// String pattern
db.users.find({ email: { $regex: '^[a-z]+@gmail', $options: 'i' } })
```

## Advanced Query Patterns

### Nested Document Queries
```javascript
// Query nested field
db.users.find({ 'address.city': 'New York' })

// Match entire nested document
db.users.find({ address: { street: '123 Main', city: 'NY' } })

// Nested array
db.orders.find({ 'items.productId': ObjectId(...) })
```

### Date Queries
```javascript
// Date range
db.orders.find({
  createdAt: {
    $gte: new Date('2024-01-01'),
    $lt: new Date('2024-12-31')
  }
})

// This week
const now = new Date()
const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000)
db.posts.find({ publishedAt: { $gte: weekAgo } })
```

### Null Handling
```javascript
// Find null values
db.users.find({ phone: null })

// Find missing field
db.users.find({ phone: { $exists: false } })

// Find non-null
db.users.find({ phone: { $ne: null } })

// Not missing
db.users.find({ phone: { $exists: true } })
```

## Performance Tips

✅ **Query Optimization:**
1. **Use indexes** on frequently filtered fields
2. **Filter early** - $match before other stages
3. **Project fields** - Don't fetch unnecessary data
4. **Limit results** - Use pagination
5. **Use explain()** - Analyze every query

✅ **Common Mistakes:**
1. ❌ `find({})` without limit - Returns all documents
2. ❌ No index on filtered fields - Full collection scans
3. ❌ Fetching fields you don't need - Wastes bandwidth
4. ❌ Sorting without index - Memory-intensive
5. ❌ Complex regex patterns - Slow performance

## Real-World Examples

### User Search with Pagination
```javascript
async function searchUsers(searchTerm, page = 1) {
  const pageSize = 20
  const skip = (page - 1) * pageSize

  const users = await db.users
    .find({
      $or: [
        { name: { $regex: searchTerm, $options: 'i' } },
        { email: { $regex: searchTerm, $options: 'i' } }
      ]
    })
    .project({ password: 0 })  // Don't return passwords
    .sort({ name: 1 })
    .skip(skip)
    .limit(pageSize)
    .toArray()

  const total = await db.users.countDocuments({
    $or: [
      { name: { $regex: searchTerm, $options: 'i' } },
      { email: { $regex: searchTerm, $options: 'i' } }
    ]
  })

  return {
    data: users,
    total,
    pages: Math.ceil(total / pageSize),
    currentPage: page
  }
}
```

### Advanced Filtering
```javascript
async function filterProducts(filters) {
  const query = {}

  if (filters.minPrice) query.price = { $gte: filters.minPrice }
  if (filters.maxPrice) query.price = { ...query.price, $lte: filters.maxPrice }
  if (filters.category) query.category = filters.category
  if (filters.inStock) query.stock = { $gt: 0 }
  if (filters.rating) query.rating = { $gte: filters.rating }

  return await db.products
    .find(query)
    .sort({ [filters.sortBy]: filters.sortOrder })
    .limit(filters.limit || 50)
    .toArray()
}
```

## Next Steps

1. **Create Sample Queries** - Find + filters
2. **Add Projections** - Select needed fields
3. **Implement Sorting** - Order results
4. **Add Pagination** - Handle large datasets
5. **Monitor Performance** - Use explain()

---

**You're now a MongoDB query expert!** 🎯
