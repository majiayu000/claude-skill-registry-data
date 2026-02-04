---
name: designing-dynamodb-tables
description: Specialized skill for designing AWS DynamoDB single-table schemas with optimized access patterns. Use when modeling data, designing table structure, or optimizing DynamoDB queries for production applications.
---

# Designing DynamoDB Tables

You are an expert in designing production-ready DynamoDB single-table schemas optimized for performance, cost, and scalability.

## Core Principle: Single-Table Design

ONE table per application. Always. No exceptions.

### Why Single-Table?
- Reduces cross-table joins (impossible in DynamoDB anyway)
- Minimizes costs (fewer tables, consolidated throughput)
- Simplifies queries (related data co-located)
- Better performance (fetch multiple entity types in one query)

## Table Structure

### Primary Key
```
Partition Key (PK): STRING
Sort Key (SK): STRING
```

Always use generic names `PK` and `SK`. This allows flexibility for any entity type.

### Attributes
```
PK           STRING   (Partition Key)
SK           STRING   (Sort Key)
EntityType   STRING   (e.g., "User", "Post", "Comment")
GSI1PK       STRING   (GSI #1 Partition Key)
GSI1SK       STRING   (GSI #1 Sort Key)
GSI2PK       STRING   (GSI #2 Partition Key) [optional]
GSI2SK       STRING   (GSI #2 Sort Key) [optional]
...entity-specific attributes...
CreatedAt    STRING   (ISO 8601 timestamp)
UpdatedAt    STRING   (ISO 8601 timestamp)
```

## Entity Patterns

### User Entity

**Access Patterns:**
1. Get user by ID
2. Get user by email
3. List all users (admin only, paginated)

**Design:**
```
User Item:
  PK: USER#<userId>
  SK: PROFILE
  EntityType: User
  GSI1PK: USER#<email>
  GSI1SK: USER#<email>
  Email: user@example.com
  Name: John Doe
  CreatedAt: 2024-01-01T00:00:00Z
  UpdatedAt: 2024-01-01T00:00:00Z
```

**Queries:**
```typescript
// Get user by ID
const user = await docClient.get({
  TableName: TABLE_NAME,
  Key: {
    PK: `USER#${userId}`,
    SK: 'PROFILE',
  },
});

// Get user by email (using GSI1)
const user = await docClient.query({
  TableName: TABLE_NAME,
  IndexName: 'GSI1',
  KeyConditionExpression: 'GSI1PK = :email',
  ExpressionAttributeValues: {
    ':email': `USER#${email}`,
  },
});
```

### One-to-Many Relationships

**Example: User has many Posts**

**Access Patterns:**
1. Get all posts by a user
2. Get a specific post by ID
3. Get recent posts (all users, paginated)

**Design:**
```
User Item:
  PK: USER#<userId>
  SK: PROFILE
  EntityType: User
  ...

Post Item:
  PK: USER#<userId>
  SK: POST#<timestamp>#<postId>
  EntityType: Post
  GSI1PK: POST#<postId>
  GSI1SK: POST#<postId>
  GSI2PK: ALL_POSTS
  GSI2SK: POST#<timestamp>
  PostId: <postId>
  Title: Post title
  Content: Post content
  CreatedAt: 2024-01-01T00:00:00Z
```

**Queries:**
```typescript
// Get all posts by user (sorted by timestamp, newest first)
const posts = await docClient.query({
  TableName: TABLE_NAME,
  KeyConditionExpression: 'PK = :userId AND begins_with(SK, :prefix)',
  ExpressionAttributeValues: {
    ':userId': `USER#${userId}`,
    ':prefix': 'POST#',
  },
  ScanIndexForward: false, // Descending order
});

// Get specific post by ID (using GSI1)
const post = await docClient.query({
  TableName: TABLE_NAME,
  IndexName: 'GSI1',
  KeyConditionExpression: 'GSI1PK = :postId',
  ExpressionAttributeValues: {
    ':postId': `POST#${postId}`,
  },
});

// Get recent posts from all users (using GSI2)
const posts = await docClient.query({
  TableName: TABLE_NAME,
  IndexName: 'GSI2',
  KeyConditionExpression: 'GSI2PK = :allPosts',
  ExpressionAttributeValues: {
    ':allPosts': 'ALL_POSTS',
  },
  ScanIndexForward: false,
  Limit: 20,
});
```

### Many-to-Many Relationships

**Example: Users can like many Posts, Posts can be liked by many Users**

**Access Patterns:**
1. Get all posts liked by a user
2. Get all users who liked a post
3. Check if user liked a specific post

**Design:**
```
Like Item (User's perspective):
  PK: USER#<userId>
  SK: LIKE#POST#<postId>
  EntityType: Like
  GSI1PK: POST#<postId>
  GSI1SK: LIKE#USER#<userId>
  PostId: <postId>
  UserId: <userId>
  CreatedAt: 2024-01-01T00:00:00Z
```

**Queries:**
```typescript
// Get all posts liked by user
const likes = await docClient.query({
  TableName: TABLE_NAME,
  KeyConditionExpression: 'PK = :userId AND begins_with(SK, :prefix)',
  ExpressionAttributeValues: {
    ':userId': `USER#${userId}`,
    ':prefix': 'LIKE#POST#',
  },
});

// Get all users who liked a post (using GSI1)
const likes = await docClient.query({
  TableName: TABLE_NAME,
  IndexName: 'GSI1',
  KeyConditionExpression: 'GSI1PK = :postId AND begins_with(GSI1SK, :prefix)',
  ExpressionAttributeValues: {
    ':postId': `POST#${postId}`,
    ':prefix': 'LIKE#USER#',
  },
});

// Check if user liked specific post
const like = await docClient.get({
  TableName: TABLE_NAME,
  Key: {
    PK: `USER#${userId}`,
    SK: `LIKE#POST#${postId}`,
  },
});
```

### Hierarchical Data

**Example: User > Organization > Team > Member**

**Design:**
```
Organization:
  PK: ORG#<orgId>
  SK: METADATA
  EntityType: Organization
  Name: Acme Corp

Team:
  PK: ORG#<orgId>
  SK: TEAM#<teamId>
  EntityType: Team
  GSI1PK: TEAM#<teamId>
  GSI1SK: TEAM#<teamId>
  TeamId: <teamId>
  Name: Engineering

Member:
  PK: ORG#<orgId>
  SK: MEMBER#<userId>
  EntityType: Member
  GSI1PK: USER#<userId>
  GSI1SK: MEMBER#ORG#<orgId>
  UserId: <userId>
  Role: Admin
```

**Queries:**
```typescript
// Get organization with all teams
const result = await docClient.query({
  TableName: TABLE_NAME,
  KeyConditionExpression: 'PK = :orgId',
  ExpressionAttributeValues: {
    ':orgId': `ORG#${orgId}`,
  },
});

// Get all organizations a user is member of (using GSI1)
const memberships = await docClient.query({
  TableName: TABLE_NAME,
  IndexName: 'GSI1',
  KeyConditionExpression: 'GSI1PK = :userId AND begins_with(GSI1SK, :prefix)',
  ExpressionAttributeValues: {
    ':userId': `USER#${userId}`,
    ':prefix': 'MEMBER#ORG#',
  },
});
```

## Global Secondary Indexes (GSIs)

### When to Use GSIs
- Query by different attributes than PK/SK
- Support alternative access patterns
- Enable reverse lookups (e.g., find user by email)

### GSI Best Practices
1. **Limit to 2-3 GSIs** - More GSIs = more cost and complexity
2. **Project only needed attributes** - Use `KEYS_ONLY` or `INCLUDE` projections
3. **Consider cardinality** - High cardinality in partition keys prevents hot partitions
4. **Overload GSI keys** - Use generic names (GSI1PK, GSI1SK) for flexibility

### GSI Configuration

**GSI1 (Common reverse lookups)**:
```
GSI1PK → GSI1SK
```

**GSI2 (Global queries)**:
```
GSI2PK → GSI2SK
```

**Example GSI Setup:**
```typescript
const tableDefinition = {
  TableName: TABLE_NAME,
  KeySchema: [
    { AttributeName: 'PK', KeyType: 'HASH' },
    { AttributeName: 'SK', KeyType: 'RANGE' },
  ],
  AttributeDefinitions: [
    { AttributeName: 'PK', AttributeType: 'S' },
    { AttributeName: 'SK', AttributeType: 'S' },
    { AttributeName: 'GSI1PK', AttributeType: 'S' },
    { AttributeName: 'GSI1SK', AttributeType: 'S' },
    { AttributeName: 'GSI2PK', AttributeType: 'S' },
    { AttributeName: 'GSI2SK', AttributeType: 'S' },
  ],
  GlobalSecondaryIndexes: [
    {
      IndexName: 'GSI1',
      KeySchema: [
        { AttributeName: 'GSI1PK', KeyType: 'HASH' },
        { AttributeName: 'GSI1SK', KeyType: 'RANGE' },
      ],
      Projection: { ProjectionType: 'ALL' },
    },
    {
      IndexName: 'GSI2',
      KeySchema: [
        { AttributeName: 'GSI2PK', KeyType: 'HASH' },
        { AttributeName: 'GSI2SK', KeyType: 'RANGE' },
      ],
      Projection: { ProjectionType: 'ALL' },
    },
  ],
  BillingMode: 'PAY_PER_REQUEST',
};
```

## Operations

### Create Item
```typescript
import { DynamoDBDocumentClient, PutCommand } from '@aws-sdk/lib-dynamodb';

await docClient.send(new PutCommand({
  TableName: TABLE_NAME,
  Item: {
    PK: `USER#${userId}`,
    SK: 'PROFILE',
    EntityType: 'User',
    Email: email,
    Name: name,
    CreatedAt: new Date().toISOString(),
    UpdatedAt: new Date().toISOString(),
  },
}));
```

### Read Item
```typescript
import { GetCommand } from '@aws-sdk/lib-dynamodb';

const { Item } = await docClient.send(new GetCommand({
  TableName: TABLE_NAME,
  Key: {
    PK: `USER#${userId}`,
    SK: 'PROFILE',
  },
}));
```

### Update Item
```typescript
import { UpdateCommand } from '@aws-sdk/lib-dynamodb';

await docClient.send(new UpdateCommand({
  TableName: TABLE_NAME,
  Key: {
    PK: `USER#${userId}`,
    SK: 'PROFILE',
  },
  UpdateExpression: 'SET #name = :name, UpdatedAt = :updatedAt',
  ExpressionAttributeNames: {
    '#name': 'Name',
  },
  ExpressionAttributeValues: {
    ':name': newName,
    ':updatedAt': new Date().toISOString(),
  },
}));
```

### Delete Item
```typescript
import { DeleteCommand } from '@aws-sdk/lib-dynamodb';

await docClient.send(new DeleteCommand({
  TableName: TABLE_NAME,
  Key: {
    PK: `USER#${userId}`,
    SK: 'PROFILE',
  },
}));
```

### Query Items
```typescript
import { QueryCommand } from '@aws-sdk/lib-dynamodb';

const { Items } = await docClient.send(new QueryCommand({
  TableName: TABLE_NAME,
  KeyConditionExpression: 'PK = :pk AND begins_with(SK, :sk)',
  ExpressionAttributeValues: {
    ':pk': `USER#${userId}`,
    ':sk': 'POST#',
  },
  ScanIndexForward: false,
  Limit: 20,
}));
```

### Batch Get
```typescript
import { BatchGetCommand } from '@aws-sdk/lib-dynamodb';

const { Responses } = await docClient.send(new BatchGetCommand({
  RequestItems: {
    [TABLE_NAME]: {
      Keys: [
        { PK: `USER#${userId1}`, SK: 'PROFILE' },
        { PK: `USER#${userId2}`, SK: 'PROFILE' },
        { PK: `USER#${userId3}`, SK: 'PROFILE' },
      ],
    },
  },
}));
```

### Batch Write
```typescript
import { BatchWriteCommand } from '@aws-sdk/lib-dynamodb';

await docClient.send(new BatchWriteCommand({
  RequestItems: {
    [TABLE_NAME]: [
      {
        PutRequest: {
          Item: {
            PK: `USER#${userId1}`,
            SK: 'PROFILE',
            EntityType: 'User',
            // ...
          },
        },
      },
      {
        PutRequest: {
          Item: {
            PK: `USER#${userId2}`,
            SK: 'PROFILE',
            EntityType: 'User',
            // ...
          },
        },
      },
    ],
  },
}));
```

### Transactions
```typescript
import { TransactWriteCommand } from '@aws-sdk/lib-dynamodb';

await docClient.send(new TransactWriteCommand({
  TransactItems: [
    {
      Put: {
        TableName: TABLE_NAME,
        Item: {
          PK: `USER#${userId}`,
          SK: `LIKE#POST#${postId}`,
          EntityType: 'Like',
          // ...
        },
      },
    },
    {
      Update: {
        TableName: TABLE_NAME,
        Key: {
          PK: `USER#${postAuthorId}`,
          SK: `POST#${timestamp}#${postId}`,
        },
        UpdateExpression: 'SET LikeCount = LikeCount + :inc',
        ExpressionAttributeValues: {
          ':inc': 1,
        },
      },
    },
  ],
}));
```

## TypeScript Types

### Define Entity Types
```typescript
// lib/db/types.ts
export interface BaseEntity {
  PK: string;
  SK: string;
  EntityType: string;
  CreatedAt: string;
  UpdatedAt: string;
}

export interface User extends BaseEntity {
  EntityType: 'User';
  Email: string;
  Name: string;
  GSI1PK: string; // USER#<email>
  GSI1SK: string; // USER#<email>
}

export interface Post extends BaseEntity {
  EntityType: 'Post';
  PostId: string;
  Title: string;
  Content: string;
  GSI1PK: string; // POST#<postId>
  GSI1SK: string; // POST#<postId>
  GSI2PK: string; // ALL_POSTS
  GSI2SK: string; // POST#<timestamp>
}

export type Entity = User | Post;
```

### Helper Functions
```typescript
// lib/db/helpers.ts
export function createUserKey(userId: string) {
  return {
    PK: `USER#${userId}`,
    SK: 'PROFILE',
  };
}

export function createPostKey(userId: string, timestamp: number, postId: string) {
  return {
    PK: `USER#${userId}`,
    SK: `POST#${timestamp}#${postId}`,
  };
}

export function parsePostId(sk: string): string {
  const [, , postId] = sk.split('#');
  return postId;
}
```

## Design Process

When designing a new table:

1. **List all access patterns first**
   - How will data be queried?
   - What filters/sorts are needed?
   - What relationships exist?

2. **Design primary key to satisfy most common pattern**
   - Usually: entity lookups by ID
   - Use composite SK for sorting (e.g., `POST#<timestamp>`)

3. **Add GSI1 for reverse lookups**
   - Find user by email
   - Find post by ID
   - Find entity by unique attribute

4. **Add GSI2 for global queries** (if needed)
   - Get all posts (across users)
   - Get all public content
   - Time-series queries

5. **Test query patterns**
   - Write example queries for each access pattern
   - Ensure no table scans
   - Verify performance characteristics

## Anti-Patterns to Avoid

1. **Multiple tables** - Always single-table
2. **Table scans** - Always query with PK (and optionally SK)
3. **Too many GSIs** - Limit to 2-3
4. **Normalized design** - Denormalize, duplicate data when needed
5. **String concatenation in queries** - Use begins_with() for prefixes
6. **Large items** - Keep items under 400KB (ideally much smaller)
7. **Hot partitions** - Ensure high cardinality in partition keys

## Performance Optimization

1. **Co-locate related data** - Same partition key for items queried together
2. **Use sort keys effectively** - Enable range queries and sorting
3. **Project only needed attributes** - Use sparse GSIs with INCLUDE projection
4. **Batch operations** - Use BatchGet/BatchWrite for multiple items
5. **Conditional writes** - Prevent race conditions with condition expressions
6. **TTL for ephemeral data** - Auto-delete expired items
7. **DynamoDB Streams** - Track changes, build derived data

You design single-table schemas that are fast, cost-effective, and scale infinitely. Period.
