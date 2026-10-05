---
name: software-architecture
description: System design, architectural patterns, and technical decision-making for software projects. Use for system design, API design, database modeling, scalability planning, technology selection, and architectural documentation.
---

# Software Architecture

Design scalable, maintainable software systems through sound architectural principles.

## System Design Process

1. **Requirements Analysis**
   - Functional requirements (features)
   - Non-functional requirements (performance, scale, security)
   - Constraints (budget, timeline, team skills)

2. **High-Level Design**
   - Component identification
   - Data flow mapping
   - Integration points
   - Technology selection

3. **Detailed Design**
   - API contracts
   - Data models
   - Sequence diagrams
   - Error handling

4. **Validation**
   - Review against requirements
   - Identify trade-offs
   - Document decisions

## Architectural Patterns

### Monolith
```
Best for: Early-stage products, small teams
Trade-offs: Simple to develop, harder to scale independently
```

### Microservices
```
Best for: Large teams, independent scaling needs
Trade-offs: Complex operations, better team autonomy
```

### Event-Driven
```
Best for: Decoupled systems, async workflows
Trade-offs: Eventual consistency, good scalability
```

### Layered (N-Tier)
```
Best for: Clear separation of concerns
Trade-offs: Simple structure, potential performance overhead
```

## API Design

### REST Guidelines
- Use nouns for resources: `/users`, `/orders`
- HTTP verbs for actions: GET, POST, PUT, DELETE
- Version APIs: `/v1/users`
- Consistent error responses

### GraphQL Guidelines
- Single endpoint
- Client-specified queries
- Strong typing with schema
- Batch requests naturally

## Data Modeling

### Relational
- Normalize to 3NF by default
- Denormalize for read performance
- Index query patterns
- Consider partitioning for scale

### NoSQL Selection
| Type | Use Case |
|------|----------|
| Document (MongoDB) | Flexible schema, nested data |
| Key-Value (Redis) | Caching, sessions |
| Column (Cassandra) | Time-series, high write throughput |
| Graph (Neo4j) | Relationships, social networks |

## Scalability Patterns

### Horizontal Scaling
- Stateless services
- Load balancing
- Database sharding
- Caching layers

### Vertical Scaling
- Increase resources
- Optimize algorithms
- Database tuning
- Limited ceiling

### Common Bottlenecks
1. Database queries (add indexes, cache, read replicas)
2. Network latency (CDN, regional deployment)
3. CPU-bound operations (async processing, workers)
4. Memory (cache eviction, pagination)

## Technology Selection

### Decision Criteria
- Team expertise
- Community support
- Maturity and stability
- Performance characteristics
- Licensing and cost

### Documentation Template
```markdown
## Decision: [Title]
**Date**: [Date]
**Status**: [Proposed/Accepted/Deprecated]

### Context
[Why is this decision needed?]

### Options Considered
1. [Option A] - [Pros/Cons]
2. [Option B] - [Pros/Cons]

### Decision
[What was decided and why]

### Consequences
[What are the implications?]
```

## Security Considerations

### Authentication
- OAuth2/OIDC for third-party auth
- JWT for stateless tokens
- Session cookies for web apps

### Authorization
- RBAC for role-based access
- ABAC for attribute-based rules
- Principle of least privilege

### Data Protection
- Encrypt at rest and in transit
- Sanitize inputs
- Audit sensitive operations

## Documentation Outputs

### Architecture Decision Records (ADRs)
- One decision per record
- Include context and alternatives
- Track status over time

### System Diagrams
- C4 model (Context, Container, Component, Code)
- Sequence diagrams for flows
- Data flow diagrams

### API Documentation
- OpenAPI/Swagger for REST
- GraphQL schema with descriptions
- Example requests/responses
