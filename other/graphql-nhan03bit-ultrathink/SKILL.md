---
name: graphql
description: GraphQL schema design, resolver patterns, subscriptions, DataLoader batching, federation, and security best practices
layer: domain
category: backend
triggers:
  - "graphql"
  - "gql"
  - "schema design"
  - "resolvers"
  - "graphql subscriptions"
  - "apollo"
  - "graphql federation"
inputs:
  - "API design requirements"
  - "Schema definitions"
  - "Real-time data needs"
outputs:
  - "GraphQL schema designs"
  - "Resolver implementations"
  - "Federation configurations"
linksTo:
  - nodejs
  - python
  - websockets
  - redis
  - postgresql
  - microservices
linkedFrom:
  - error-handling
  - authentication
  - caching
preferredNextSkills:
  - postgresql
  - redis
  - websockets
fallbackSkills:
  - nodejs
  - fastapi
riskLevel: low
memoryReadPolicy: selective
memoryWritePolicy: none
sideEffects: []
---

# GraphQL Domain Skill

## Purpose

Provide expert-level guidance on GraphQL schema design, resolver implementation, subscriptions, DataLoader for N+1 prevention, schema federation, security hardening, and production optimization patterns.

## Key Patterns

### 1. Schema Design Principles

```graphql
# Use Relay-style connections for pagination
type Query {
  """List users with cursor-based pagination."""
  users(
    first: Int
    after: String
    last: Int
    before: String
    filter: UserFilter
    orderBy: UserOrderBy
  ): UserConnection!

  """Get a single user by ID."""
  user(id: ID!): User

  """Get the currently authenticated user."""
  me: User
}

type Mutation {
  """Create a new user account."""
  createUser(input: CreateUserInput!): CreateUserPayload!

  """Update user profile fields."""
  updateUser(input: UpdateUserInput!): UpdateUserPayload!

  """Delete a user account (soft delete)."""
  deleteUser(id: ID!): DeleteUserPayload!
}

type Subscription {
  """Subscribe to new messages in a channel."""
  messageReceived(channelId: ID!): Message!
}

# Input types for mutations
input CreateUserInput {
  email: String!
  name: String!
  role: UserRole = MEMBER
}

# Payload types with userErrors for client-safe errors
type CreateUserPayload {
  user: User
  userErrors: [UserError!]!
}

type UserError {
  field: [String!]
  message: String!
  code: ErrorCode!
}

enum ErrorCode {
  INVALID_INPUT
  NOT_FOUND
  ALREADY_EXISTS
  UNAUTHORIZED
}

# Relay connection types
type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type UserEdge {
  node: User!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

# Interfaces for shared types
interface Node {
  id: ID!
}

interface Timestamped {
  createdAt: DateTime!
  updatedAt: DateTime!
}

type User implements Node & Timestamped {
  id: ID!
  email: String!
  name: String!
  role: UserRole!
  posts(first: Int, after: String): PostConnection!
  createdAt: DateTime!
  updatedAt: DateTime!
}

enum UserRole {
  ADMIN
  MEMBER
  VIEWER
}

# Custom scalars
scalar DateTime
scalar JSON
scalar EmailAddress
```

### 2. Resolver Patterns (Node.js / TypeScript)

```typescript
import { GraphQLResolveInfo } from 'graphql';
import DataLoader from 'dataloader';

// Context type
interface Context {
  currentUser: User | null;
  loaders: ReturnType<typeof createLoaders>;
  db: Database;
}

// DataLoader factory -- create per-request to prevent caching across users
function createLoaders(db: Database) {
  return {
    user: new DataLoader<string, User | null>(async (ids) => {
      const users = await db.user.findMany({ where: { id: { in: [...ids] } } });
      const userMap = new Map(users.map(u => [u.id, u]));
      return ids.map(id => userMap.get(id) ?? null);
    }),

    userPosts: new DataLoader<string, Post[]>(async (userIds) => {
      const posts = await db.post.findMany({
        where: { authorId: { in: [...userIds] } },
      });
      const grouped = groupBy(posts, 'authorId');
      return userIds.map(id => grouped[id] ?? []);
    }),
  };
}

// Resolvers
const resolvers = {
  Query: {
    me: (_parent: unknown, _args: unknown, ctx: Context) => {
      return ctx.currentUser;
    },

    users: async (_parent: unknown, args: ConnectionArgs, ctx: Context) => {
      requireAuth(ctx);
      return paginateConnection(ctx.db.user, args);
    },

    user: async (_parent: unknown, args: { id: string }, ctx: Context) => {
      return ctx.loaders.user.load(args.id);
    },
  },

  Mutation: {
    createUser: async (_parent: unknown, args: { input: CreateUserInput }, ctx: Context) => {
      requireRole(ctx, 'ADMIN');

      const existing = await ctx.db.user.findUnique({ where: { email: args.input.email } });
      if (existing) {
        return {
          user: null,
          userErrors: [{ field: ['email'], message: 'Email already registered', code: 'ALREADY_EXISTS' }],
        };
      }

      const user = await ctx.db.user.create({ data: args.input });
      return { user, userErrors: [] };
    },
  },

  User: {
    // Field-level resolver with DataLoader
    posts: (parent: User, args: ConnectionArgs, ctx: Context) => {
      return ctx.loaders.userPosts.load(parent.id);
    },
  },

  Subscription: {
    messageReceived: {
      subscribe: (_parent: unknown, args: { channelId: string }, ctx: Context) => {
        requireAuth(ctx);
        return ctx.pubsub.asyncIterator(`CHANNEL_${args.channelId}`);
      },
    },
  },
};
```

### 3. Connection/Pagination Helper

```typescript
interface ConnectionArgs {
  first?: number | null;
  after?: string | null;
  last?: number | null;
  before?: string | null;
}

async function paginateConnection<T extends { id: string }>(
  model: PrismaModel<T>,
  args: ConnectionArgs,
  where?: Record<string, unknown>,
) {
  const limit = args.first ?? args.last ?? 20;
  const clampedLimit = Math.min(limit, 100);

  let cursor: string | undefined;
  let direction: 'forward' | 'backward' = 'forward';

  if (args.after) {
    cursor = decodeCursor(args.after);
    direction = 'forward';
  } else if (args.before) {
    cursor = decodeCursor(args.before);
    direction = 'backward';
  }

  // Fetch one extra to determine hasNextPage/hasPreviousPage
  const items = await model.findMany({
    where: {
      ...where,
      ...(cursor ? { id: { [direction === 'forward' ? 'gt' : 'lt']: cursor } } : {}),
    },
    take: clampedLimit + 1,
    orderBy: { id: direction === 'forward' ? 'asc' : 'desc' },
  });

  const hasMore = items.length > clampedLimit;
  const nodes = hasMore ? items.slice(0, clampedLimit) : items;
  if (direction === 'backward') nodes.reverse();

  const totalCount = await model.count({ where });

  return {
    edges: nodes.map(node => ({
      node,
      cursor: encodeCursor(node.id),
    })),
    pageInfo: {
      hasNextPage: direction === 'forward' ? hasMore : !!cursor,
      hasPreviousPage: direction === 'backward' ? hasMore : !!cursor,
      startCursor: nodes.length ? encodeCursor(nodes[0].id) : null,
      endCursor: nodes.length ? encodeCursor(nodes[nodes.length - 1].id) : null,
    },
    totalCount,
  };
}
```

### 4. Security

```typescript
// Query depth limiting
import depthLimit from 'graphql-depth-limit';

const server = new ApolloServer({
  schema,
  validationRules: [depthLimit(10)],
  plugins: [
    // Query complexity analysis
    createComplexityPlugin({
      maximumComplexity: 1000,
      defaultComplexity: 1,
      estimators: [
        fieldExtensionsEstimator(),
        simpleEstimator({ defaultComplexity: 1 }),
      ],
      onComplete: (complexity) => {
        if (complexity > 500) {
          logger.warn({ complexity }, 'High query complexity');
        }
      },
    }),
  ],
});

// Disable introspection in production
const server = new ApolloServer({
  introspection: process.env.NODE_ENV !== 'production',
});

// Rate limiting per operation
const rateLimitDirective = (limit: number, window: string) => {
  return (next: Function) => async (root: any, args: any, ctx: Context, info: any) => {
    const key = `ratelimit:${ctx.currentUser?.id}:${info.fieldName}`;
    const current = await ctx.redis.incr(key);
    if (current === 1) await ctx.redis.expire(key, parseWindow(window));
    if (current > limit) throw new Error('Rate limit exceeded');
    return next(root, args, ctx, info);
  };
};
```

## Best Practices

1. **Use Relay cursor-based pagination** for all list fields
2. **Return payload types from mutations** with `userErrors` array, never throw for user errors
3. **Use DataLoader for every relationship** -- N+1 queries are the #1 GraphQL perf issue
4. **Create DataLoader instances per-request** -- never share across requests
5. **Limit query depth** (10 max) and complexity (1000 max)
6. **Use input types** for mutation arguments -- never inline scalars
7. **Design nullable by default** -- only mark `!` when you can guarantee the field
8. **Version via schema evolution** -- add fields, deprecate old ones, never remove
9. **Use persisted queries** in production to prevent arbitrary query injection
10. **Log and monitor resolver execution times** per field

## Common Pitfalls

| Pitfall | Impact | Fix |
|---------|--------|-----|
| N+1 queries without DataLoader | Exponential DB load | DataLoader for every relationship resolver |
| Deeply nested queries | DoS via resource exhaustion | Depth limiting + complexity analysis |
| Over-fetching in resolvers | Slow responses | Check `info.fieldNodes` to resolve only requested fields |
| Throwing errors in mutations | Bad client experience | Return structured `userErrors` in payload types |
| Shared DataLoader across requests | Data leaks between users | Create new DataLoader per request in context |
| No introspection control | Schema exposure | Disable introspection in production |
