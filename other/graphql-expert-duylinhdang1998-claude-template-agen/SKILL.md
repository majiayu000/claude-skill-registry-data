---
name: graphql-expert
description: GraphQL API expertise from Meta - the company that created GraphQL. Build efficient, type-safe APIs with powerful querying capabilities. Use when building GraphQL APIs, implementing GraphQL clients, or migrating from REST to GraphQL. Learn GraphQL from Facebook/Instagram's production experience.
expert_level: 9/10
source_company: Meta (Facebook/Instagram)
specialist: meta-react-architect
requires:
  - react-expert
related:
  - typescript-master
  - node-backend
---

# GraphQL Expert - Meta Created GraphQL

**Expert**: Sarah Chen (Meta React Core Team, 12 years)
**Level**: 9/10 - Meta created GraphQL in 2012

## Overview

GraphQL from Meta (Facebook) - created to solve API inefficiencies at scale. Used by Instagram, Facebook, GitHub, Shopify, and thousands of companies.

## Why Meta Created GraphQL (2012)

**The Problem:**
- Facebook mobile app made 100+ REST API calls per screen
- Over-fetching: Getting data you don't need
- Under-fetching: Making multiple requests for related data
- API versioning nightmare (v1, v2, v3...)

**The Solution: GraphQL**
- Client specifies exactly what data it needs
- One request, all data
- Strongly typed schema
- No versioning needed

## Core Workflow

1. **Define schema** - GraphQL types and relationships (see references/schema.md)
2. **Implement resolvers** - Business logic to fetch data (see references/resolvers.md)
3. **Client queries** - Fetch exactly what you need (see references/client.md)
4. **Optimize** - DataLoader for N+1 prevention (see references/optimization.md)

## Key Concepts

### Schema-First Development
Define your API contract in GraphQL schema language, then implement resolvers.

### DataLoader Pattern
Meta created DataLoader to solve N+1 query problems. See references/optimization.md for details.

### Relay Cursor Connections
Meta's pattern for pagination in GraphQL. See references/schema.md for implementation.

## Meta's GraphQL at Scale

### Instagram
- 3 billion users
- GraphQL replaced 100+ REST endpoints
- Single GraphQL endpoint handles all data
- Relay for efficient data fetching

### Facebook
- Largest GraphQL deployment
- Thousands of types in schema
- Billions of queries per day
- Relay Compiler for optimization

## Best Practices

1. Use Relay Cursor Connections for pagination
2. DataLoader for N+1 prevention
3. Strongly typed schema with TypeScript
4. Persisted queries for security
5. Query complexity limits to prevent abuse

## Related Skills

- **[react-expert](../react-expert/SKILL.md)** - React + GraphQL
- **[typescript-master](../typescript-master/SKILL.md)** - Type-safe GraphQL
- **[node-backend](../node-backend/SKILL.md)** - GraphQL server

---

**Last Updated**: 2026-02-03
**Expert**: Sarah Chen (Meta, 12 years) - Meta created GraphQL
