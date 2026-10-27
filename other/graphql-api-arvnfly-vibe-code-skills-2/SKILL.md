---
name: graphql-api
description: "GraphQL schema design, DataLoader N+1 batching, query depth limiting, and relay connection pagination."
---

# GraphQL API Architecture Protocol

Build secure, scalable GraphQL services.

---

## 1. DataLoader & N+1 Prevention

Wrap all field resolvers fetching child entities in DataLoader batching to coalesce queries into single batch lookups.

---

## 2. Query Complexity & Depth Limiting

Enforce maximum query depth and complexity limits in production to prevent denial-of-service via nested query recursion.
