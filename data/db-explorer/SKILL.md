---
name: db-explorer
description: MongoDB database exploration and querying. Use when you need to understand database structure, view existing data, check collection schemas, count documents, or run queries to investigate the database state. (project)
---

# MongoDB Database Explorer

Use this skill when you need to explore the MongoDB database to understand data structure, verify existing records, or investigate database state.

## When to Use

- Understanding what data exists in collections
- Checking collection schemas and indexes
- Counting documents matching certain criteria
- Viewing sample documents
- Debugging data-related issues
- Verifying database state after operations

## Quick Exploration Commands

Use mongosh or a MongoDB client to explore the database:

```bash
# Connect to MongoDB
mongosh mongodb://localhost:27017/freelancelyst

# Show all collections
show collections

# Count documents in a collection
db.users.countDocuments()
db.blogposts.countDocuments()

# View sample documents
db.users.find().limit(5).pretty()
db.blogposts.find().limit(5).pretty()

# Query with filters
db.blogposts.find({ status: "published" }).limit(10).pretty()
db.users.find({ roles: "admin" }).pretty()

# Aggregate examples
db.blogposts.aggregate([
  { $group: { _id: "$status", count: { $sum: 1 } } }
])
```

## Database Schema Overview

The database has the following collections:

### Users
Collection: `users`
```typescript
{
  _id: ObjectId,
  name: string,
  email: string,
  password: string,  // bcrypt hashed
  roles: string[],   // ['user'] or ['admin']
  createdAt: Date,
  updatedAt: Date
}
```

### Blog Posts
Collection: `blogposts`
```typescript
{
  _id: ObjectId,
  slug: string,      // unique
  status: 'draft' | 'published' | 'archived',
  publishedAt: Date | null,
  coverImage: string | null,
  owner: ObjectId,   // ref: users
  category: ObjectId | null,  // ref: blogcategories
  tags: ObjectId[],  // refs: blogtags
  translations: [
    { langCode: 'en' | 'fa', title: string, content: string, excerpt: string }
  ],
  createdAt: Date,
  updatedAt: Date
}
```

### Blog Categories
Collection: `blogcategories`
```typescript
{
  _id: ObjectId,
  slug: string,      // unique
  translations: [
    { langCode: 'en' | 'fa', name: string }
  ],
  createdAt: Date,
  updatedAt: Date
}
```

### Blog Tags
Collection: `blogtags`
```typescript
{
  _id: ObjectId,
  slug: string,      // unique
  translations: [
    { langCode: 'en' | 'fa', name: string }
  ],
  createdAt: Date,
  updatedAt: Date
}
```

### Project Applications
Collection: `projectapplications`
```typescript
{
  _id: ObjectId,
  title: string,
  description: string,
  budgetEstimate: string,
  deadline: string,
  clientEmail: string | null,
  utm: object | null,  // UTM tracking params
  createdAt: Date,
  updatedAt: Date
}
```

### Freelancer Applications
Collection: `freelancerapplications`
```typescript
{
  _id: ObjectId,
  fullName: string,
  email: string,
  skillTags: string,
  description: string,
  utm: object | null,  // UTM tracking params
  createdAt: Date,
  updatedAt: Date
}
```

## Common Queries

### Find posts with translations in specific language
```javascript
db.blogposts.find({
  "translations.langCode": "en"
}).pretty()
```

### Get published posts with category populated
```javascript
db.blogposts.aggregate([
  { $match: { status: "published" } },
  { $lookup: {
    from: "blogcategories",
    localField: "category",
    foreignField: "_id",
    as: "categoryData"
  }},
  { $limit: 5 }
])
```

### Count applications by month
```javascript
db.projectapplications.aggregate([
  { $group: {
    _id: { $month: "$createdAt" },
    count: { $sum: 1 }
  }}
])
```

## Important Notes

1. **Environment**: Ensure `MONGODB_URI` is set in your `.env.local` file
2. **Read-Only**: This skill is for exploration only. Never modify data through raw queries.
3. **Sensitive Data**: Be careful with password hashes - don't log them in plain text
4. **Performance**: Use limits on large collections to avoid slow queries
5. **Translations**: Remember blog entities use embedded translation arrays
