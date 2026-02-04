---
name: graphql-reviewer
description: |
  WHEN: GraphQL schema review, resolver patterns, N+1 detection, query complexity, API security
  WHAT: Schema design + N+1 detection + Query complexity + Input validation + Error handling + DataLoader patterns
  WHEN NOT: REST API → api-documenter, Database schema → schema-reviewer, ORM → orm-reviewer
---

# GraphQL Reviewer Skill

## Purpose
Reviews GraphQL schemas, resolvers, and operations for N+1 problems, query complexity limits, input validation, security best practices, and proper error handling.

## When to Use
- GraphQL schema or resolver review requests
- "GraphQL", "N+1", "DataLoader", "query complexity" mentions
- Schema design review
- Projects with `.graphql`, `.gql` files
- GraphQL library dependencies (Apollo, Relay, graphql-js)

## Project Detection
- `.graphql` or `.gql` schema files
- `schema.graphql` or `type-defs.ts`
- `graphql` package in dependencies
- `@apollo/server`, `graphql-yoga`, `mercurius` dependencies
- `@Query`, `@Mutation`, `@Resolver` decorators (NestJS/TypeGraphQL)

## Workflow

### Step 1: Analyze Project
```
**GraphQL Server**: Apollo Server 4.x / GraphQL Yoga
**Schema**: Code-first / SDL-first
**Language**: TypeScript / JavaScript
**ORM**: Prisma / TypeORM / Drizzle
**Key Features**:
  - DataLoader for batching
  - Query complexity plugin
  - Persisted queries
```

### Step 2: Select Review Areas
**AskUserQuestion:**
```
"Which GraphQL areas to review?"
Options:
- Full GraphQL audit (recommended)
- N+1 / DataLoader patterns
- Schema design
- Query complexity / Security
- Error handling
- Input validation
multiSelect: true
```

## Detection Rules

### Critical: N+1 Query Problem
| Pattern | Issue | Severity |
|---------|-------|----------|
| Resolver per item | N+1 queries | CRITICAL |
| No DataLoader | Unbatched fetches | CRITICAL |
| ORM lazy load in resolver | Hidden N+1 | CRITICAL |

```typescript
// BAD: N+1 problem
// Schema
type Query {
  posts: [Post!]!
}

type Post {
  id: ID!
  author: User!  // N+1 here!
}

// Resolver - fetches author per post
const resolvers = {
  Query: {
    posts: () => db.post.findMany()
  },
  Post: {
    author: (post) => db.user.findUnique({ where: { id: post.authorId } })
    // If 100 posts → 1 + 100 queries!
  }
};

// GOOD: DataLoader for batching
import DataLoader from 'dataloader';

const createLoaders = () => ({
  userLoader: new DataLoader(async (ids: string[]) => {
    const users = await db.user.findMany({
      where: { id: { in: ids } }
    });
    const userMap = new Map(users.map(u => [u.id, u]));
    return ids.map(id => userMap.get(id) ?? null);
  })
});

// Resolver with DataLoader
const resolvers = {
  Post: {
    author: (post, _, { loaders }) => loaders.userLoader.load(post.authorId)
    // Now: 1 + 1 queries (batched)
  }
};

// BEST: Prisma with includes (no N+1)
const resolvers = {
  Query: {
    posts: () => db.post.findMany({
      include: { author: true }  // Single query with JOIN
    })
  }
};
```

### Critical: Excessive Fetching in Resolvers
| Pattern | Issue | Severity |
|---------|-------|----------|
| SELECT * in resolver | Over-fetching | HIGH |
| No field selection | Wasted resources | MEDIUM |
| Ignoring selection set | Missing optimization | HIGH |

```typescript
// BAD: Fetches all fields regardless of query
const resolvers = {
  Query: {
    user: (_, { id }) => db.user.findUnique({
      where: { id },
      include: {
        posts: true,      // Maybe not requested
        comments: true,   // Maybe not requested
        followers: true   // Maybe not requested
      }
    })
  }
};

// GOOD: Use info to select only requested fields
import { GraphQLResolveInfo } from 'graphql';
import graphqlFields from 'graphql-fields';

const resolvers = {
  Query: {
    user: (_, { id }, __, info: GraphQLResolveInfo) => {
      const requestedFields = graphqlFields(info);
      return db.user.findUnique({
        where: { id },
        include: {
          posts: 'posts' in requestedFields,
          comments: 'comments' in requestedFields
        }
      });
    }
  }
};

// BETTER: Use Prisma's select based on GraphQL query
import { PrismaSelect } from '@paljs/plugins';

const resolvers = {
  Query: {
    user: (_, { id }, __, info) => {
      const select = new PrismaSelect(info).value;
      return db.user.findUnique({ where: { id }, ...select });
    }
  }
};
```

### Critical: Mutation in Query
| Pattern | Issue | Severity |
|---------|-------|----------|
| Side effects in Query | Violates spec | CRITICAL |
| Write operation in Query | Unexpected behavior | CRITICAL |

```graphql
# BAD: Mutation disguised as Query
type Query {
  incrementViewCount(postId: ID!): Int!  # WRONG! This mutates data
  markAsRead(notificationId: ID!): Boolean!  # WRONG!
}

# GOOD: Mutations for side effects
type Mutation {
  incrementViewCount(postId: ID!): Post!
  markAsRead(notificationId: ID!): Notification!
}

# Query should be idempotent (read-only)
type Query {
  post(id: ID!): Post
  viewCount(postId: ID!): Int!
}
```

### High: Missing Input Validation
| Pattern | Issue | Severity |
|---------|-------|----------|
| No validation in resolver | Bad data accepted | HIGH |
| Trusting client input | Security risk | HIGH |
| No sanitization | Injection risk | CRITICAL |

```typescript
// BAD: No validation
const resolvers = {
  Mutation: {
    createUser: (_, { input }) => {
      // input.email could be anything
      return db.user.create({ data: input });
    }
  }
};

// GOOD: Validate inputs
import { z } from 'zod';

const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
  age: z.number().int().min(0).max(150).optional()
});

const resolvers = {
  Mutation: {
    createUser: (_, { input }) => {
      const validated = CreateUserSchema.parse(input);
      return db.user.create({ data: validated });
    }
  }
};

// Schema-level validation (GraphQL)
"""
User creation input
"""
input CreateUserInput {
  email: String! @constraint(format: "email")
  name: String! @constraint(minLength: 1, maxLength: 100)
  age: Int @constraint(min: 0, max: 150)
}
```

### High: No Query Complexity Limit
| Pattern | Issue | Severity |
|---------|-------|----------|
| Unlimited depth | DoS vector | HIGH |
| No complexity limit | Resource exhaustion | HIGH |
| No rate limiting | Abuse possible | MEDIUM |

```typescript
// BAD: Allows dangerous queries
// Can request: user.friends.friends.friends.friends...

// GOOD: Limit query depth
import depthLimit from 'graphql-depth-limit';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [depthLimit(5)]  // Max 5 levels deep
});

// GOOD: Query complexity plugin
import { createComplexityPlugin } from 'graphql-query-complexity';

const complexityPlugin = createComplexityPlugin({
  estimators: [
    fieldExtensionsEstimator(),
    simpleEstimator({ defaultComplexity: 1 })
  ],
  maximumComplexity: 1000,
  onComplete: (complexity) => {
    console.log('Query Complexity:', complexity);
  }
});

// Schema with complexity hints
type Query {
  users(first: Int!): [User!]! @complexity(multipliers: ["first"], value: 5)
  posts(first: Int!): [Post!]! @complexity(multipliers: ["first"], value: 3)
}

// GOOD: Rate limiting
import { rateLimitDirective } from 'graphql-rate-limit-directive';

const { rateLimitDirectiveTypeDefs, rateLimitDirectiveTransformer } =
  rateLimitDirective();

type Query {
  expensiveQuery: Data! @rateLimit(limit: 10, duration: 60)
}
```

### High: No List Pagination
| Pattern | Issue | Severity |
|---------|-------|----------|
| Unbounded lists | Memory exhaustion | HIGH |
| No cursor pagination | Poor performance | MEDIUM |
| Missing total count | Bad UX | LOW |

```graphql
# BAD: Unbounded list
type Query {
  posts: [Post!]!  # Could return millions!
}

# GOOD: Relay-style pagination
type Query {
  posts(
    first: Int
    after: String
    last: Int
    before: String
  ): PostConnection!
}

type PostConnection {
  edges: [PostEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type PostEdge {
  node: Post!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

# SIMPLER: Offset pagination (for small datasets)
type Query {
  posts(offset: Int = 0, limit: Int = 20): PostPage!
}

type PostPage {
  items: [Post!]!
  totalCount: Int!
  hasMore: Boolean!
}
```

### High: Missing Error Handling
| Pattern | Issue | Severity |
|---------|-------|----------|
| Throwing raw errors | Leaks info | HIGH |
| No error codes | Hard to handle | MEDIUM |
| Stack traces in response | Security risk | HIGH |

```typescript
// BAD: Raw error exposure
const resolvers = {
  Query: {
    user: async (_, { id }) => {
      const user = await db.user.findUnique({ where: { id } });
      if (!user) {
        throw new Error('User not found');  // Generic error
      }
      return user;
    }
  }
};

// GOOD: Structured GraphQL errors
import { GraphQLError } from 'graphql';

class NotFoundError extends GraphQLError {
  constructor(resource: string, id: string) {
    super(`${resource} not found`, {
      extensions: {
        code: 'NOT_FOUND',
        resource,
        id
      }
    });
  }
}

const resolvers = {
  Query: {
    user: async (_, { id }) => {
      const user = await db.user.findUnique({ where: { id } });
      if (!user) {
        throw new NotFoundError('User', id);
      }
      return user;
    }
  }
};

// Error formatting plugin
const formatError = (error: GraphQLError) => {
  // Don't expose internal errors
  if (error.extensions?.code === 'INTERNAL_SERVER_ERROR') {
    return new GraphQLError('Internal server error', {
      extensions: { code: 'INTERNAL_SERVER_ERROR' }
    });
  }
  return error;
};
```

### Medium: Internal ID Exposure
| Pattern | Issue | Severity |
|---------|-------|----------|
| Database ID in schema | Information leak | MEDIUM |
| Sequential IDs | Enumeration risk | MEDIUM |
| No ID obfuscation | Privacy concern | LOW |

```graphql
# BAD: Exposes database IDs
type User {
  id: Int!  # Sequential, guessable
}

# GOOD: Use opaque IDs
type User {
  id: ID!  # Could be UUID, hashid, etc.
}
```

```typescript
// ID encoding/decoding
import Hashids from 'hashids';
const hashids = new Hashids('secret-salt', 10);

const resolvers = {
  User: {
    id: (user) => hashids.encode(user.dbId)
  },
  Query: {
    user: (_, { id }) => {
      const [dbId] = hashids.decode(id);
      return db.user.findUnique({ where: { id: dbId } });
    }
  }
};
```

### Medium: Missing Non-null Defaults
| Pattern | Issue | Severity |
|---------|-------|----------|
| Nullable without reason | Confusing API | MEDIUM |
| Everything nullable | Too permissive | LOW |

```graphql
# BAD: Unnecessarily nullable
type User {
  id: ID          # Should always exist
  email: String   # Required for user
  name: String    # Should be required
  bio: String     # OK to be nullable
}

# GOOD: Clear nullability
type User {
  id: ID!          # Always present
  email: String!   # Required
  name: String!    # Required
  bio: String      # Optional (nullable)
  deletedAt: DateTime  # Optional
}

# For fields that may fail to resolve
type Post {
  id: ID!
  author: User  # Nullable if author deleted
  authorId: ID! # Always has the reference
}
```

## Response Template
```
## GraphQL Code Review Results

**Project**: [name]
**Server**: Apollo Server 4.x
**Schema**: SDL-first / Code-first

### N+1 / DataLoader

#### CRITICAL
| File | Line | Issue |
|------|------|-------|
| resolvers/post.ts | 23 | N+1 in author resolver - use DataLoader |
| resolvers/user.ts | 45 | posts fetched per user without batching |

### Query Complexity / Security
| File | Line | Issue |
|------|------|-------|
| server.ts | 12 | No depth limit configured |
| schema.graphql | 34 | posts query unbounded - add pagination |

### Input Validation
| File | Line | Issue |
|------|------|-------|
| mutations/user.ts | 56 | No email validation |
| mutations/post.ts | 23 | Missing input sanitization |

### Error Handling
| File | Line | Issue |
|------|------|-------|
| resolvers/query.ts | 78 | Raw error thrown - use GraphQLError |

### Schema Design
| File | Line | Issue |
|------|------|-------|
| schema.graphql | 12 | Query with side effect - move to Mutation |
| types/user.graphql | 8 | Exposes sequential database ID |

### Recommendations
1. [ ] Implement DataLoader for all relationship resolvers
2. [ ] Add depth limit (max 5-7 levels)
3. [ ] Add query complexity plugin (max 1000)
4. [ ] Add pagination to all list fields
5. [ ] Validate all mutation inputs with Zod/Yup

### Positive Patterns
- Good use of Relay connections for pagination
- Proper error codes in GraphQL errors
```

## Best Practices
1. **DataLoader**: Always batch relationship resolvers
2. **Complexity**: Limit depth and complexity
3. **Pagination**: Cursor-based for large lists
4. **Validation**: Validate all inputs server-side
5. **Errors**: Use structured GraphQL errors
6. **Security**: Rate limit, no introspection in prod

## Integration
- `schema-reviewer` skill: Database schema
- `orm-reviewer` skill: ORM patterns
- `typescript-reviewer` skill: TS type safety
- `security-scanner` skill: API security

## Notes
- Based on GraphQL best practices 2024
- Works with Apollo, Yoga, Mercurius
- Supports both SDL and code-first
- Compatible with Prisma, TypeORM, Drizzle
