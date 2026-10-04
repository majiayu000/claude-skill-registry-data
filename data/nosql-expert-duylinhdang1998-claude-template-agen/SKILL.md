---
name: nosql-expert
description: NoSQL database expertise with MongoDB and DynamoDB from Amazon/Netflix engineers. Use when designing document schemas, optimizing MongoDB queries and indexes, configuring DynamoDB tables with GSI/LSI, implementing data modeling for flexible schemas, handling horizontal scaling, or migrating from SQL to NoSQL. Triggers on MongoDB, DynamoDB, NoSQL, document database, collection design, partition keys, or non-relational database tasks.
---

# NoSQL Expert - MongoDB & DynamoDB Mastery

**Purpose**: Design and optimize NoSQL databases for flexible schemas, horizontal scaling, and high performance

**Agent**: Amazon Cloud Architect / Netflix Backend Architect
**Use When**: Building apps with flexible data models, high write throughput, or need for horizontal scaling

---

## MongoDB

### Schema Design

```typescript
// User document
{
  _id: ObjectId("507f1f77bcf86cd799439011"),
  email: "john@example.com",
  name: "John Doe",
  profile: {
    age: 30,
    city: "NYC"
  },
  tags: ["developer", "nodejs"],
  createdAt: ISODate("2024-01-01T00:00:00Z")
}

// Embedded vs Referenced

// ✅ Embed: One-to-few, data belongs together
{
  _id: 1,
  title: "Post",
  comments: [
    { author: "Alice", text: "Great!" },
    { author: "Bob", text: "Thanks!" }
  ]
}

// ✅ Reference: One-to-many, independent entities
{
  _id: 1,
  title: "Post",
  authorId: ObjectId("...")
}
```

### CRUD Operations (Mongoose)

```typescript
import mongoose from 'mongoose'

const userSchema = new mongoose.Schema({
  email: { type: String, required: true, unique: true },
  name: { type: String, required: true },
  profile: {
    age: Number,
    city: String
  },
  tags: [String],
  createdAt: { type: Date, default: Date.now }
})

const User = mongoose.model('User', userSchema)

// Create
const user = await User.create({
  email: 'john@example.com',
  name: 'John Doe',
  profile: { age: 30, city: 'NYC' }
})

// Find
const users = await User.find({ 'profile.city': 'NYC' })
const user = await User.findOne({ email: 'john@example.com' })

// Update
await User.updateOne(
  { _id: userId },
  { $set: { 'profile.age': 31 } }
)

// Delete
await User.deleteOne({ _id: userId })

// Aggregation
const stats = await User.aggregate([
  { $match: { 'profile.city': 'NYC' } },
  { $group: { _id: '$profile.city', count: { $sum: 1 } } }
])
```

### Indexes

```typescript
// Single field
userSchema.index({ email: 1 })

// Compound index
userSchema.index({ 'profile.city': 1, createdAt: -1 })

// Text search
userSchema.index({ name: 'text', 'profile.bio': 'text' })

await User.find({ $text: { $search: 'developer nodejs' } })

// Unique index
userSchema.index({ email: 1 }, { unique: true })
```

---

## DynamoDB

### Table Design

```typescript
// Single table design
Table: app-data
Partition Key: PK (String)
Sort Key: SK (String)

// User
PK: USER#123
SK: PROFILE
Attributes: { email, name, ... }

// User's posts
PK: USER#123
SK: POST#456
Attributes: { title, content, ... }

// Post
PK: POST#456
SK: METADATA
Attributes: { title, authorId, ... }
```

### Operations (AWS SDK v3)

```typescript
import { DynamoDBClient } from '@aws-sdk/client-dynamodb'
import {
  DynamoDBDocumentClient,
  GetCommand,
  PutCommand,
  QueryCommand,
  UpdateCommand
} from '@aws-sdk/lib-dynamodb'

const client = DynamoDBDocumentClient.from(new DynamoDBClient({}))
const TABLE = 'app-data'

// Put item
await client.send(new PutCommand({
  TableName: TABLE,
  Item: {
    PK: 'USER#123',
    SK: 'PROFILE',
    email: 'john@example.com',
    name: 'John Doe'
  }
}))

// Get item
const result = await client.send(new GetCommand({
  TableName: TABLE,
  Key: { PK: 'USER#123', SK: 'PROFILE' }
}))

// Query (same partition key)
const posts = await client.send(new QueryCommand({
  TableName: TABLE,
  KeyConditionExpression: 'PK = :pk AND begins_with(SK, :sk)',
  ExpressionAttributeValues: {
    ':pk': 'USER#123',
    ':sk': 'POST#'
  }
}))

// Update
await client.send(new UpdateCommand({
  TableName: TABLE,
  Key: { PK: 'USER#123', SK: 'PROFILE' },
  UpdateExpression: 'SET #name = :name',
  ExpressionAttributeNames: { '#name': 'name' },
  ExpressionAttributeValues: { ':name': 'Jane Doe' }
}))

// Conditional update (optimistic locking)
await client.send(new UpdateCommand({
  TableName: TABLE,
  Key: { PK: 'USER#123', SK: 'PROFILE' },
  UpdateExpression: 'SET balance = balance + :amount',
  ConditionExpression: 'balance >= :min',
  ExpressionAttributeValues: {
    ':amount': 100,
    ':min': 0
  }
}))
```

### Global Secondary Index (GSI)

```typescript
// Query by email (not primary key)
GSI: EmailIndex
Partition Key: email
Sort Key: -

await client.send(new QueryCommand({
  TableName: TABLE,
  IndexName: 'EmailIndex',
  KeyConditionExpression: 'email = :email',
  ExpressionAttributeValues: {
    ':email': 'john@example.com'
  }
}))
```

---

## Best Practices

### MongoDB
- Model data for access patterns
- Use indexes wisely (check with `.explain()`)
- Limit embedded array size (<100 items)
- Use projections to reduce network transfer
- Shard for horizontal scaling

### DynamoDB
- Design for access patterns (not normalization)
- Use single-table design when possible
- Avoid hot partitions (distribute writes)
- Use batch operations for efficiency
- Set TTL for automatic deletion

---

**Remember**: NoSQL trades ACID guarantees for scalability. Choose based on access patterns, not relational habits.

**Created**: 2026-02-04
**Maintained By**: Amazon Cloud Architect
