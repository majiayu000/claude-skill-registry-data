---
name: apollo-server
description: Builds GraphQL APIs with Apollo Server 4, schema design, resolvers, and data sources. Use when implementing GraphQL servers, building federated graphs, or integrating GraphQL with Node.js frameworks.
---

# Apollo Server

Apollo Server is a spec-compliant GraphQL server for Node.js. Version 4+ is framework-agnostic and supports Express, Fastify, Lambda, and more.

## Quick Start

```bash
npm install @apollo/server graphql
```

### Standalone Server

```typescript
import { ApolloServer } from '@apollo/server'
import { startStandaloneServer } from '@apollo/server/standalone'

// Type definitions
const typeDefs = `#graphql
  type User {
    id: ID!
    email: String!
    name: String
    posts: [Post!]!
  }

  type Post {
    id: ID!
    title: String!
    content: String
    author: User!
  }

  type Query {
    users: [User!]!
    user(id: ID!): User
    posts: [Post!]!
  }

  type Mutation {
    createUser(email: String!, name: String): User!
    createPost(title: String!, content: String, authorId: ID!): Post!
  }
`

// Resolvers
const resolvers = {
  Query: {
    users: () => db.users.findMany(),
    user: (_, { id }) => db.users.findById(id),
    posts: () => db.posts.findMany()
  },
  Mutation: {
    createUser: (_, { email, name }) => db.users.create({ email, name }),
    createPost: (_, { title, content, authorId }) =>
      db.posts.create({ title, content, authorId })
  },
  User: {
    posts: (user) => db.posts.findByAuthor(user.id)
  },
  Post: {
    author: (post) => db.users.findById(post.authorId)
  }
}

// Create server
const server = new ApolloServer({
  typeDefs,
  resolvers
})

// Start server
const { url } = await startStandaloneServer(server, {
  listen: { port: 4000 }
})

console.log(`Server ready at ${url}`)
```

## Express Integration

```bash
npm install @apollo/server express cors
```

```typescript
import { ApolloServer } from '@apollo/server'
import { expressMiddleware } from '@apollo/server/express4'
import express from 'express'
import cors from 'cors'

const app = express()

const server = new ApolloServer({
  typeDefs,
  resolvers
})

await server.start()

app.use(
  '/graphql',
  cors(),
  express.json(),
  expressMiddleware(server, {
    context: async ({ req }) => ({
      token: req.headers.authorization,
      user: await getUserFromToken(req.headers.authorization)
    })
  })
)

app.listen(4000)
```

## Context

### Context Setup

```typescript
interface Context {
  user: User | null
  dataSources: {
    users: UserDataSource
    posts: PostDataSource
  }
}

const server = new ApolloServer<Context>({
  typeDefs,
  resolvers
})

await server.start()

app.use(
  '/graphql',
  expressMiddleware(server, {
    context: async ({ req }): Promise<Context> => {
      const token = req.headers.authorization?.replace('Bearer ', '')
      const user = token ? await verifyToken(token) : null

      return {
        user,
        dataSources: {
          users: new UserDataSource(),
          posts: new PostDataSource()
        }
      }
    }
  })
)
```

### Using Context in Resolvers

```typescript
const resolvers = {
  Query: {
    me: (_, __, context) => context.user,
    users: (_, __, { dataSources }) => dataSources.users.findAll()
  },
  Mutation: {
    createPost: (_, args, { user, dataSources }) => {
      if (!user) throw new GraphQLError('Not authenticated')
      return dataSources.posts.create({ ...args, authorId: user.id })
    }
  }
}
```

## Schema Design

### Input Types

```graphql
input CreateUserInput {
  email: String!
  name: String
  role: Role = USER
}

input UpdateUserInput {
  email: String
  name: String
  role: Role
}

type Mutation {
  createUser(input: CreateUserInput!): User!
  updateUser(id: ID!, input: UpdateUserInput!): User!
}
```

### Enums

```graphql
enum Role {
  USER
  ADMIN
  MODERATOR
}

enum PostStatus {
  DRAFT
  PUBLISHED
  ARCHIVED
}
```

### Interfaces

```graphql
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
  createdAt: DateTime!
  updatedAt: DateTime!
}
```

### Unions

```graphql
union SearchResult = User | Post | Comment

type Query {
  search(query: String!): [SearchResult!]!
}
```

```typescript
const resolvers = {
  SearchResult: {
    __resolveType(obj) {
      if (obj.email) return 'User'
      if (obj.title) return 'Post'
      if (obj.body) return 'Comment'
      return null
    }
  }
}
```

### Custom Scalars

```bash
npm install graphql-scalars
```

```typescript
import { DateTimeResolver, EmailAddressResolver } from 'graphql-scalars'

const typeDefs = `#graphql
  scalar DateTime
  scalar EmailAddress

  type User {
    email: EmailAddress!
    createdAt: DateTime!
  }
`

const resolvers = {
  DateTime: DateTimeResolver,
  EmailAddress: EmailAddressResolver
}
```

## Error Handling

### GraphQL Errors

```typescript
import { GraphQLError } from 'graphql'

const resolvers = {
  Query: {
    user: async (_, { id }, { dataSources }) => {
      const user = await dataSources.users.findById(id)

      if (!user) {
        throw new GraphQLError('User not found', {
          extensions: {
            code: 'NOT_FOUND',
            argumentName: 'id'
          }
        })
      }

      return user
    }
  }
}
```

### Authentication Error

```typescript
function requireAuth(context: Context) {
  if (!context.user) {
    throw new GraphQLError('You must be logged in', {
      extensions: { code: 'UNAUTHENTICATED' }
    })
  }
  return context.user
}

const resolvers = {
  Mutation: {
    createPost: (_, args, context) => {
      const user = requireAuth(context)
      return createPost({ ...args, authorId: user.id })
    }
  }
}
```

### Error Formatting

```typescript
const server = new ApolloServer({
  typeDefs,
  resolvers,
  formatError: (formattedError, error) => {
    // Log error
    console.error(error)

    // Hide internal errors in production
    if (process.env.NODE_ENV === 'production') {
      if (formattedError.extensions?.code === 'INTERNAL_SERVER_ERROR') {
        return {
          message: 'Internal server error',
          extensions: { code: 'INTERNAL_SERVER_ERROR' }
        }
      }
    }

    return formattedError
  }
})
```

## Data Sources

### REST Data Source

```bash
npm install @apollo/datasource-rest
```

```typescript
import { RESTDataSource } from '@apollo/datasource-rest'

class UsersAPI extends RESTDataSource {
  override baseURL = 'https://api.example.com/'

  async getUser(id: string) {
    return this.get(`users/${id}`)
  }

  async getUsers() {
    return this.get('users')
  }

  async createUser(user: CreateUserInput) {
    return this.post('users', { body: user })
  }

  // Caching
  override willSendRequest(path, request) {
    request.headers['Authorization'] = this.context.token
  }
}
```

### Database Data Source

```typescript
import { PrismaClient } from '@prisma/client'

class UserDataSource {
  private prisma: PrismaClient

  constructor() {
    this.prisma = new PrismaClient()
  }

  async findById(id: string) {
    return this.prisma.user.findUnique({ where: { id } })
  }

  async findAll() {
    return this.prisma.user.findMany()
  }

  async create(data: CreateUserInput) {
    return this.prisma.user.create({ data })
  }
}
```

## Pagination

### Cursor-Based (Relay Style)

```graphql
type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

type UserEdge {
  node: User!
  cursor: String!
}

type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type Query {
  users(first: Int, after: String): UserConnection!
}
```

```typescript
const resolvers = {
  Query: {
    users: async (_, { first = 10, after }, { dataSources }) => {
      const decodedCursor = after ? Buffer.from(after, 'base64').toString() : null
      const users = await dataSources.users.findMany({
        take: first + 1,
        cursor: decodedCursor ? { id: decodedCursor } : undefined,
        skip: decodedCursor ? 1 : 0
      })

      const hasNextPage = users.length > first
      const edges = users.slice(0, first).map(user => ({
        node: user,
        cursor: Buffer.from(user.id).toString('base64')
      }))

      return {
        edges,
        pageInfo: {
          hasNextPage,
          hasPreviousPage: !!after,
          startCursor: edges[0]?.cursor,
          endCursor: edges[edges.length - 1]?.cursor
        },
        totalCount: await dataSources.users.count()
      }
    }
  }
}
```

## Subscriptions

```bash
npm install graphql-ws ws
```

```typescript
import { createServer } from 'http'
import { WebSocketServer } from 'ws'
import { useServer } from 'graphql-ws/lib/use/ws'
import { makeExecutableSchema } from '@graphql-tools/schema'

const typeDefs = `#graphql
  type Subscription {
    messageCreated: Message!
    userTyping(channelId: ID!): User!
  }
`

const resolvers = {
  Subscription: {
    messageCreated: {
      subscribe: () => pubsub.asyncIterator(['MESSAGE_CREATED'])
    },
    userTyping: {
      subscribe: (_, { channelId }) =>
        pubsub.asyncIterator([`USER_TYPING_${channelId}`])
    }
  }
}

const schema = makeExecutableSchema({ typeDefs, resolvers })

const httpServer = createServer(app)

const wsServer = new WebSocketServer({
  server: httpServer,
  path: '/graphql'
})

useServer({ schema }, wsServer)

httpServer.listen(4000)
```

### PubSub

```typescript
import { PubSub } from 'graphql-subscriptions'

const pubsub = new PubSub()

const resolvers = {
  Mutation: {
    createMessage: async (_, { input }, { user }) => {
      const message = await db.messages.create({
        ...input,
        authorId: user.id
      })

      pubsub.publish('MESSAGE_CREATED', { messageCreated: message })

      return message
    }
  }
}
```

## Plugins

### Logging Plugin

```typescript
const loggingPlugin = {
  async requestDidStart(requestContext) {
    console.log('Request started:', requestContext.request.query)

    return {
      async willSendResponse(requestContext) {
        console.log('Response:', requestContext.response)
      },
      async didEncounterErrors(requestContext) {
        console.error('Errors:', requestContext.errors)
      }
    }
  }
}

const server = new ApolloServer({
  typeDefs,
  resolvers,
  plugins: [loggingPlugin]
})
```

### Performance Plugin

```typescript
import { ApolloServerPluginUsageReporting } from '@apollo/server/plugin/usageReporting'

const server = new ApolloServer({
  typeDefs,
  resolvers,
  plugins: [
    ApolloServerPluginUsageReporting({
      sendVariableValues: { all: true },
      sendHeaders: { all: true }
    })
  ]
})
```

## Type Safety with Codegen

```bash
npm install -D @graphql-codegen/cli @graphql-codegen/typescript @graphql-codegen/typescript-resolvers
```

```yaml
# codegen.yml
generates:
  ./src/generated/graphql.ts:
    plugins:
      - typescript
      - typescript-resolvers
    config:
      contextType: ../context#Context
      mappers:
        User: ../models#UserModel
```

```typescript
import type { Resolvers } from './generated/graphql'

const resolvers: Resolvers = {
  Query: {
    // Fully typed resolvers
    user: (_, { id }) => db.users.findById(id)
  }
}
```

## Best Practices

1. **Use input types** for mutations
2. **Implement DataLoader** for N+1 prevention
3. **Add query depth limiting** to prevent abuse
4. **Use persisted queries** in production
5. **Implement proper error codes**
6. **Generate types with GraphQL Codegen**

## References

- [DataLoader & N+1](references/dataloader.md)
- [Federation](references/federation.md)
