---
name: mongodb
description: MongoDB schema design, aggregation pipelines, indexing strategies, change streams, transactions, and production optimization
layer: domain
category: database
triggers:
  - "mongodb"
  - "mongo"
  - "mongoose"
  - "nosql"
  - "document database"
  - "aggregation pipeline"
inputs:
  - "Data modeling requirements"
  - "Query patterns"
  - "Scaling requirements"
outputs:
  - "Schema designs with embedding/referencing strategies"
  - "Aggregation pipeline implementations"
  - "Indexing and performance recommendations"
linksTo:
  - nodejs
  - python
  - fastapi
  - redis
  - microservices
linkedFrom:
  - error-handling
  - monitoring
preferredNextSkills:
  - redis
  - nodejs
  - microservices
fallbackSkills:
  - postgresql
riskLevel: low
memoryReadPolicy: selective
memoryWritePolicy: none
sideEffects: []
---

# MongoDB Domain Skill

## Purpose

Provide expert-level guidance on MongoDB schema design, the embedding vs. referencing trade-off, aggregation pipelines, indexing strategies, change streams, transactions, sharding, and production optimization.

## Key Design Principle

**Design for your query patterns, not for data normalization.** MongoDB schema design is driven by how you read data, not how you write it.

## Key Patterns

### 1. Schema Design: Embed vs. Reference

```javascript
// EMBED when:
// - Data is read together (1:1 or 1:few)
// - Child data doesn't change independently
// - Document size stays under 16MB

// Embedded: Blog post with comments
{
  _id: ObjectId("..."),
  title: "Understanding MongoDB",
  author: {                    // Embedded 1:1
    name: "Jane Doe",
    email: "jane@example.com"
  },
  tags: ["mongodb", "nosql"], // Embedded array
  comments: [                  // Embedded 1:few
    {
      _id: ObjectId("..."),
      user: "Bob",
      text: "Great article!",
      createdAt: ISODate("2024-01-15")
    }
  ],
  createdAt: ISODate("2024-01-10"),
  updatedAt: ISODate("2024-01-15")
}

// REFERENCE when:
// - Data is accessed independently
// - Many-to-many relationships
// - Unbounded arrays (comments on viral posts)
// - Data changes frequently and independently

// Referenced: Order with products
// orders collection
{
  _id: ObjectId("..."),
  userId: ObjectId("..."),      // Reference to users
  items: [
    {
      productId: ObjectId("..."), // Reference to products
      quantity: 2,
      priceAtPurchase: 2999       // Snapshot! Don't reference current price
    }
  ],
  total: 5998,
  status: "shipped",
  createdAt: ISODate("2024-01-10")
}

// HYBRID: Subset pattern -- embed frequently accessed fields
// products collection
{
  _id: ObjectId("..."),
  name: "Wireless Headphones",
  price: 2999,
  // Embed top 5 reviews for display
  topReviews: [
    { user: "Alice", rating: 5, text: "Amazing sound!" },
    { user: "Bob", rating: 4, text: "Good value" }
  ],
  reviewCount: 347,
  avgRating: 4.2
}
// Full reviews in separate collection
// reviews collection
{
  _id: ObjectId("..."),
  productId: ObjectId("..."),
  userId: ObjectId("..."),
  rating: 5,
  text: "Amazing sound quality...",
  createdAt: ISODate("2024-01-12")
}
```

### 2. Indexing Strategies

```javascript
// Compound index (most important pattern)
// The ESR Rule: Equality, Sort, Range
db.orders.createIndex({
  status: 1,        // Equality first
  createdAt: -1,    // Sort second
  total: 1          // Range last
});

// Supports:
// db.orders.find({ status: "pending" }).sort({ createdAt: -1 })
// db.orders.find({ status: "pending", total: { $gt: 100 } }).sort({ createdAt: -1 })

// Partial index: only index relevant documents
db.orders.createIndex(
  { createdAt: -1 },
  { partialFilterExpression: { status: "pending" } }
);

// TTL index: auto-delete expired documents
db.sessions.createIndex(
  { expiresAt: 1 },
  { expireAfterSeconds: 0 }
);

// Text index for search
db.products.createIndex(
  { name: "text", description: "text" },
  { weights: { name: 10, description: 1 } }
);

// Wildcard index for dynamic JSONB-like fields
db.events.createIndex({ "metadata.$**": 1 });

// Unique sparse index (allows multiple nulls)
db.users.createIndex(
  { phoneNumber: 1 },
  { unique: true, sparse: true }
);

// Covered query: all fields in the index
db.users.createIndex({ email: 1, name: 1, role: 1 });
db.users.find(
  { email: "jane@example.com" },
  { name: 1, role: 1, _id: 0 }  // Only returns indexed fields = covered query
);
```

### 3. Aggregation Pipelines

```javascript
// Sales analytics pipeline
db.orders.aggregate([
  // Stage 1: Filter
  { $match: {
    status: "completed",
    createdAt: {
      $gte: ISODate("2024-01-01"),
      $lt: ISODate("2025-01-01")
    }
  }},

  // Stage 2: Unwind array
  { $unwind: "$items" },

  // Stage 3: Lookup (LEFT JOIN)
  { $lookup: {
    from: "products",
    localField: "items.productId",
    foreignField: "_id",
    as: "product"
  }},
  { $unwind: "$product" },

  // Stage 4: Group by category and month
  { $group: {
    _id: {
      category: "$product.category",
      month: { $dateToString: { format: "%Y-%m", date: "$createdAt" } }
    },
    totalRevenue: { $sum: { $multiply: ["$items.quantity", "$items.priceAtPurchase"] } },
    orderCount: { $sum: 1 },
    avgOrderValue: { $avg: { $multiply: ["$items.quantity", "$items.priceAtPurchase"] } },
    uniqueCustomers: { $addToSet: "$userId" }
  }},

  // Stage 5: Reshape
  { $project: {
    _id: 0,
    category: "$_id.category",
    month: "$_id.month",
    totalRevenue: 1,
    orderCount: 1,
    avgOrderValue: { $round: ["$avgOrderValue", 2] },
    uniqueCustomerCount: { $size: "$uniqueCustomers" }
  }},

  // Stage 6: Sort
  { $sort: { month: 1, totalRevenue: -1 } }
]);

// Bucket pattern for histograms
db.products.aggregate([
  { $bucket: {
    groupBy: "$price",
    boundaries: [0, 1000, 5000, 10000, 50000],
    default: "50000+",
    output: {
      count: { $sum: 1 },
      avgRating: { $avg: "$avgRating" },
      products: { $push: { name: "$name", price: "$price" } }
    }
  }}
]);

// Graph lookup: Find all connected users (social network)
db.users.aggregate([
  { $match: { _id: ObjectId("...") } },
  { $graphLookup: {
    from: "friendships",
    startWith: "$_id",
    connectFromField: "friendId",
    connectToField: "userId",
    maxDepth: 2,
    depthField: "degrees",
    as: "network"
  }}
]);
```

### 4. Change Streams

```javascript
// Watch for real-time changes
const pipeline = [
  { $match: {
    operationType: { $in: ["insert", "update"] },
    "fullDocument.status": "pending"
  }}
];

const changeStream = db.orders.watch(pipeline, {
  fullDocument: "updateLookup", // Include full document on updates
  resumeAfter: lastResumeToken, // Resume from last position
});

changeStream.on("change", async (change) => {
  console.log("Change detected:", change.operationType);
  const order = change.fullDocument;
  await processNewOrder(order);
  // Save resume token for crash recovery
  await saveResumeToken(change._id);
});

changeStream.on("error", (err) => {
  console.error("Change stream error:", err);
  // Reconnect with last resume token
});
```

### 5. Transactions (Multi-Document)

```javascript
const session = client.startSession();

try {
  await session.withTransaction(async () => {
    // All operations within the transaction
    const order = await db.orders.insertOne(
      { userId, items, total, status: "pending" },
      { session }
    );

    await db.inventory.updateMany(
      { _id: { $in: items.map(i => i.productId) } },
      { $inc: { stock: -1 } }, // This should be item-specific in real code
      { session }
    );

    await db.users.updateOne(
      { _id: userId },
      { $inc: { orderCount: 1, totalSpent: total } },
      { session }
    );
  }, {
    readConcern: { level: "snapshot" },
    writeConcern: { w: "majority" },
    maxCommitTimeMS: 5000,
  });
} finally {
  await session.endSession();
}
```

## Best Practices

1. **Design schemas around query patterns** -- embed what you read together
2. **Follow the ESR Rule** for compound indexes: Equality, Sort, Range
3. **Avoid unbounded arrays** -- use the subset pattern or separate collection
4. **Use `$match` early** in aggregation pipelines to leverage indexes
5. **Set `maxTimeMS`** on all queries to prevent runaway operations
6. **Use `readPreference: secondaryPreferred`** for read-heavy analytics queries
7. **Monitor with `db.currentOp()`** and `profiler` for slow queries
8. **Use change streams** instead of polling for real-time features
9. **Snapshot prices/names** in orders -- don't reference current values
10. **Use `writeConcern: { w: "majority" }`** for critical data

## Common Pitfalls

| Pitfall | Impact | Fix |
|---------|--------|-----|
| Unbounded arrays (e.g., all comments embedded) | Document exceeds 16MB limit | Bucket pattern or separate collection |
| Missing compound indexes | Full collection scans | Follow ESR rule, use `explain()` |
| Over-normalizing (too many references) | Excessive `$lookup` operations | Embed data that is read together |
| Not using projection | Transferring unnecessary data | Always specify `{ field: 1 }` projection |
| Using `$where` or `$regex` without index | Cannot use indexes | Use text indexes or Atlas Search |
| Ignoring write concern | Data loss on failures | Use `w: "majority"` for important writes |
| Not handling duplicate key errors | Silent data corruption | Use `upsert` or handle E11000 explicitly |
