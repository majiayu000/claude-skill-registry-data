---
name: graphql-api-design
category: api
difficulty: intermediate
estimated_time: 45 minutes
description: Comprehensive GraphQL API design with Apollo Server, GraphQL Yoga, and Federation v2
version: 1.0.0
---

# GraphQL API Design Skill

## Level 1: Quick Reference (~800 tokens)

### GraphQL vs REST: When to Use GraphQL

**Use GraphQL When:**

- Clients need flexible data fetching (avoid over/under-fetching)
- Multiple client types with different data requirements (mobile, web, IoT)
- Real-time data updates via subscriptions
- Complex data relationships and nested queries
- Rapid frontend iteration without backend changes

**Use REST When:**

- Simple CRUD operations with predictable access patterns
- File uploads/downloads (though GraphQL can handle with multipart)
- HTTP caching is critical (GET requests)
- Team unfamiliarity with GraphQL tooling

### Schema Design Principles

**Core Concepts:**

1. **Type System**: Strongly typed schema defines API contract
2. **Query**: Read operations (like GET)
3. **Mutation**: Write operations (like POST/PUT/DELETE)
4. **Subscription**: Real-time data streams over WebSocket
5. **Resolver**: Function that returns data for a field

**Design Rules:**

- Use nouns for types, verbs for mutations
- Prefer pagination over large lists
- Design for client use cases, not database structure
- Use interfaces for polymorphic types
- Leverage custom scalars (DateTime, Email, URL)

### Essential Checklist

#### Schema Design

- [ ] Define clear type hierarchy (Query, Mutation, Subscription roots)
- [ ] Use descriptive field names and types
- [ ] Add field-level descriptions for documentation
- [ ] Implement input validation with custom scalars
- [ ] Design pagination with cursor-based approach

#### Resolvers & Performance

- [ ] Implement DataLoader for N+1 query prevention
- [ ] Batch database queries within request context
- [ ] Add resolver-level caching strategy
- [ ] Use field-level resolvers only when needed
- [ ] Implement query complexity analysis

#### Authorization & Security

- [ ] Context-based authentication (verify tokens)
- [ ] Field-level authorization with directives
- [ ] Query depth limiting (prevent deeply nested attacks)
- [ ] Query complexity cost analysis
- [ ] Rate limiting per client/operation

#### Federation (Microservices)

- [ ] Define subgraph schemas with `@key` directives
- [ ] Implement reference resolvers for entity resolution
- [ ] Configure Apollo Gateway for schema composition
- [ ] Set up schema registry for version control
- [ ] Monitor federated trace data

#### Error Handling

- [ ] Return structured errors with codes and extensions
- [ ] Distinguish user errors from system errors
- [ ] Implement partial error responses
- [ ] Log errors with correlation IDs
- [ ] Mask sensitive data in error messages

#### Testing

- [ ] Unit test resolvers with mocked data sources
- [ ] Integration test with test database
- [ ] Schema validation with apollo CLI
- [ ] Performance test with realistic queries
- [ ] Security test for common vulnerabilities

### Quick Wins

**Immediate Optimizations:**

1. **DataLoader**: Reduce N+1 queries by 90%+

   ```typescript
   const userLoader = new DataLoader(async (userIds) => {
     const users = await db.users.findMany({ where: { id: { in: userIds } } });
     return userIds.map(id => users.find(u => u.id === id));
   });
   ```

2. **Query Complexity**: Prevent expensive queries

   ```typescript
   const server = new ApolloServer({
     schema,
     plugins: [createComplexityPlugin({ maximumComplexity: 1000 })]
   });
   ```

3. **Response Caching**: Cache at resolver or HTTP level

   ```typescript
   @cacheControl(maxAge: 3600)
   type User { id: ID! name: String! }
   ```

4. **Subscription Filtering**: Reduce unnecessary events

   ```typescript
   subscribe: {
     messageAdded: {
       subscribe: withFilter(
         () => pubsub.asyncIterator('MESSAGE_ADDED'),
         (payload, variables) => payload.channelId === variables.channelId
       )
     }
   }
   ```

---

## Level 2:
>
> **📚 Full Examples**: See [REFERENCE.md](./REFERENCE.md) for complete code samples, detailed configurations, and production-ready implementations.

 Implementation Guide (~4500 tokens)

### 1. GraphQL Schema Design Best Practices

#### Type System Fundamentals

**Object Types**: Primary building blocks


*See [REFERENCE.md](./REFERENCE.md#example-0) for complete implementation.*


**Input Types**: For mutations and complex arguments


*See [REFERENCE.md](./REFERENCE.md#example-1) for complete implementation.*


**Enums**: For fixed sets of values


*See [REFERENCE.md](./REFERENCE.md#example-2) for complete implementation.*


**Interfaces**: For polymorphic types


*See [REFERENCE.md](./REFERENCE.md#example-3) for complete implementation.*


**Unions**: For heterogeneous result types

```graphql
union SearchResult = User | Post | Comment

type Query {
  search(query: String!): [SearchResult!]!
}
```

**Custom Scalars**: For domain-specific types

```graphql
scalar DateTime
scalar Email
scalar URL
scalar JSON
scalar PositiveInt
```

#### Query Design Patterns

**Root Query Type**


*See [REFERENCE.md](./REFERENCE.md#example-6) for complete implementation.*


**Cursor-Based Pagination** (Relay spec)


*See [REFERENCE.md](./REFERENCE.md#example-7) for complete implementation.*


#### Mutation Design Patterns

**Input/Payload Pattern**: Consistent structure


*See [REFERENCE.md](./REFERENCE.md#example-8) for complete implementation.*


**Optimistic Response Support**

```graphql
type UpdatePostPayload {
  post: Post
  clientMutationId: String  # Client-provided ID for tracking
  errors: [ValidationError!]
}
```

#### Subscription Design

**Real-Time Events**


*See [REFERENCE.md](./REFERENCE.md#example-10) for complete implementation.*


### 2. Resolvers and DataLoaders

#### Resolver Structure

**Basic Resolvers**


*See [REFERENCE.md](./REFERENCE.md#example-11) for complete implementation.*


**Resolver Best Practices**

1. Keep resolvers thin - delegate to data sources
2. Use TypeScript for type safety
3. Handle errors gracefully
4. Return consistent payload structures
5. Log resolver execution for debugging

#### DataLoader Implementation

**Solving the N+1 Problem**

Without DataLoader (N+1 queries):

```typescript
// For 10 posts, this executes 11 queries!
query {
  posts {           # 1 query
    id
    title
    author {        # 10 queries (one per post)
      name
    }
  }
}
```

With DataLoader (2 queries):


*See [REFERENCE.md](./REFERENCE.md#example-13) for complete implementation.*


**DataLoader in Context**


*See [REFERENCE.md](./REFERENCE.md#example-14) for complete implementation.*


**Using DataLoader in Resolvers**


*See [REFERENCE.md](./REFERENCE.md#example-15) for complete implementation.*


**Advanced DataLoader Patterns**


*See [REFERENCE.md](./REFERENCE.md#example-16) for complete implementation.*


### 3. Apollo Federation v2

#### Subgraph Design

**Users Subgraph**


*See [REFERENCE.md](./REFERENCE.md#example-17) for complete implementation.*


**Posts Subgraph**


*See [REFERENCE.md](./REFERENCE.md#example-18) for complete implementation.*


**Reference Resolvers**


*See [REFERENCE.md](./REFERENCE.md#example-19) for complete implementation.*


#### Gateway Configuration

**Apollo Gateway Setup**


*See [REFERENCE.md](./REFERENCE.md#example-20) for complete implementation.*


**Managed Federation** (Apollo Studio)


*See [REFERENCE.md](./REFERENCE.md#example-21) for complete implementation.*


### 4. Authentication and Authorization

#### Context-Based Authentication

**JWT Token Verification**


*See [REFERENCE.md](./REFERENCE.md#example-22) for complete implementation.*


**Resolver-Level Authorization**


*See [REFERENCE.md](./REFERENCE.md#example-23) for complete implementation.*


#### Directive-Based Authorization

**Schema Directives**


*See [REFERENCE.md](./REFERENCE.md#example-24) for complete implementation.*


**Directive Implementation**


*See [REFERENCE.md](./REFERENCE.md#example-25) for complete implementation.*


### 5. Subscriptions for Real-Time Data

#### WebSocket Transport

**Apollo Server Subscriptions**


*See [REFERENCE.md](./REFERENCE.md#example-26) for complete implementation.*


**PubSub Implementation**


*See [REFERENCE.md](./REFERENCE.md#example-27) for complete implementation.*


**Subscription Resolvers**


*See [REFERENCE.md](./REFERENCE.md#example-28) for complete implementation.*


### 6. Performance Optimization

#### Caching Strategies

**Apollo Cache Control**

```graphql
type Query {
  user(id: ID!): User @cacheControl(maxAge: 3600)
  posts: [Post!]! @cacheControl(maxAge: 300)
}
```


*See [REFERENCE.md](./REFERENCE.md#example-30) for complete implementation.*


**Redis Response Caching**


*See [REFERENCE.md](./REFERENCE.md#example-31) for complete implementation.*


#### Query Complexity Analysis

**Cost-Based Limiting**


*See [REFERENCE.md](./REFERENCE.md#example-32) for complete implementation.*


#### Pagination Best Practices

**Cursor-Based Pagination**


*See [REFERENCE.md](./REFERENCE.md#example-33) for complete implementation.*


### 7. Error Handling and Validation

#### Structured Error Responses

**Custom Error Classes**


*See [REFERENCE.md](./REFERENCE.md#example-34) for complete implementation.*


**Error Formatting**


*See [REFERENCE.md](./REFERENCE.md#example-35) for complete implementation.*


### 8. Testing GraphQL APIs

#### Unit Testing Resolvers

**Resolver Tests**


*See [REFERENCE.md](./REFERENCE.md#example-36) for complete implementation.*


#### Integration Testing

**GraphQL Server Tests**


*See [REFERENCE.md](./REFERENCE.md#example-37) for complete implementation.*


### 9. Production Deployment

#### Health Checks

**Readiness and Liveness**


*See [REFERENCE.md](./REFERENCE.md#example-38) for complete implementation.*


#### Monitoring and Observability

**Apollo Studio Integration**


*See [REFERENCE.md](./REFERENCE.md#example-39) for complete implementation.*


**Custom Metrics**


*See [REFERENCE.md](./REFERENCE.md#example-40) for complete implementation.*


## Examples

### Basic Usage


*See [REFERENCE.md](./REFERENCE.md#example-41) for complete implementation.*


### Advanced Usage

```python
// TODO: Add advanced example for graphql
// This example shows production-ready patterns
```

### Integration Example

```python
// TODO: Add integration example showing how graphql
// works with other systems and services
```

See `examples/graphql/` for complete working examples.

## Integration Points

This skill integrates with:

### Upstream Dependencies

- **Tools**: Apollo Server, GraphQL Yoga, Hasura
- **Prerequisites**: Basic understanding of api concepts

### Downstream Consumers

- **Applications**: Production systems requiring graphql functionality
- **CI/CD Pipelines**: Automated testing and deployment workflows
- **Monitoring Systems**: Observability and logging platforms

### Related Skills

- [Authentication](../../authentication/SKILL.md)
- [Authorization](../../authorization/SKILL.md)
- [Api Security](../../api-security/SKILL.md)

### Common Integration Patterns

1. **Development Workflow**: How this skill fits into daily development
2. **Production Deployment**: Integration with production systems
3. **Monitoring & Alerting**: Observability integration points

## Common Pitfalls

### Pitfall 1: Insufficient Testing

**Problem:** Not testing edge cases and error conditions leads to production bugs

**Solution:** Implement comprehensive test coverage including:

- Happy path scenarios
- Error handling and edge cases
- Integration points with external systems

**Prevention:** Enforce minimum code coverage (80%+) in CI/CD pipeline

### Pitfall 2: Hardcoded Configuration

**Problem:** Hardcoding values makes applications inflexible and environment-dependent

**Solution:** Use environment variables and configuration management:

- Separate config from code
- Use environment-specific configuration files
- Never commit secrets to version control

**Prevention:** Use tools like dotenv, config validators, and secret scanners

### Pitfall 3: Ignoring Security Best Practices

**Problem:** Security vulnerabilities from not following established security patterns

**Solution:** Follow security guidelines:

- Input validation and sanitization
- Proper authentication and authorization
- Encrypted data transmission (TLS/SSL)
- Regular security audits and updates

**Prevention:** Use security linters, SAST tools, and regular dependency updates

**Best Practices:**

- Follow established patterns and conventions for graphql
- Keep dependencies up to date and scan for vulnerabilities
- Write comprehensive documentation and inline comments
- Use linting and formatting tools consistently
- Implement proper error handling and logging
- Regular code reviews and pair programming
- Monitor production metrics and set up alerts

---

## Level 3: Deep Dive Resources

### Official Documentation

- **Apollo Server**: https://www.apollographql.com/docs/apollo-server/
- **GraphQL.org**: https://graphql.org/learn/
- **GraphQL Yoga**: https://the-guild.dev/graphql/yoga-server
- **Apollo Federation**: https://www.apollographql.com/docs/federation/

### Tools & Libraries

- **DataLoader**: https://github.com/graphql/dataloader
- **GraphQL Code Generator**: https://the-guild.dev/graphql/codegen
- **GraphQL ESLint**: https://the-guild.dev/graphql/eslint
- **Apollo Studio**: https://studio.apollographql.com/

### Books & Courses

- "Production Ready GraphQL" by Marc-André Giroux
- "Learning GraphQL" by Eve Porcello & Alex Banks
- Apollo Odyssey (free courses): https://www.apollographql.com/tutorials/

### Bundled Resources

See `templates/` and `config/` directories for production-ready implementations:

- `graphql-schema.graphql` - Complete schema example
- `resolver-patterns.ts` - Resolver implementation patterns
- `federation-config.yaml` - Apollo Federation setup
- `dataloader-implementation.ts` - DataLoader patterns
- `subscription-server.ts` - Real-time subscriptions
- `apollo-studio.yaml` - Monitoring configuration
