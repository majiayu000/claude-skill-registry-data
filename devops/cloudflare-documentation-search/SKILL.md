---
name: Cloudflare Documentation Search
description: This skill should be used when the user asks about "Cloudflare", "Workers", "Pages", "R2", "D1", "KV", "Durable Objects", "Queues", "Vectorize", "AI Gateway", "Hyperdrive", "Cloudflare API", "Wrangler", "Cloudflare documentation", "how to deploy to Cloudflare", "Cloudflare best practices", "Cloudflare pricing", "Cloudflare limits".
version: 1.0.0
---

# Cloudflare Documentation Search

Use the `search_cloudflare_documentation` MCP tool for semantic search across Cloudflare's official documentation.

## Tool Reference

**Tool:** `search_cloudflare_documentation`
**Server:** cloudflare-docs
**Input:** Natural language query
**Output:** Relevant documentation snippets

## When to Use

- Answering questions about Cloudflare services
- Looking up API references and configuration options
- Finding deployment guides and tutorials
- Checking pricing, limits, or specifications

## Query Patterns

| Use Case | Pattern | Example |
|----------|---------|---------|
| API reference | "[service] [operation] API" | "Workers fetch API headers" |
| Configuration | "how to configure [feature] in [service]" | "how to configure caching in Workers" |
| Limits/pricing | "[service] limits" or "[service] pricing" | "R2 storage limits" |
| Troubleshooting | "[service] [specific issue]" | "Workers timeout exceeded error" |
| Integration | "[service A] with [service B]" | "Workers with D1 database" |
| Migration | "migrate from [source] to [Cloudflare service]" | "migrate from S3 to R2" |

## Product Reference

| Product | Purpose | Common Topics |
|---------|---------|---------------|
| **Workers** | Serverless compute | Runtime APIs, bindings, limits, deployment |
| **Pages** | Static site hosting | Build config, functions, custom domains |
| **R2** | Object storage | API, pricing, lifecycle, S3 compatibility |
| **D1** | SQL database | SQL syntax, bindings, backups, limits |
| **KV** | Key-value store | API, consistency, limits, pricing |
| **Durable Objects** | Stateful coordination | Alarms, websockets, storage |
| **Queues** | Message queues | Producers, consumers, batching |
| **Vectorize** | Vector database | Indexes, queries, embeddings |
| **AI Gateway** | AI proxy | Caching, rate limiting, logging |
| **Hyperdrive** | Database connector | Connection pooling, supported DBs |
| **Wrangler** | CLI tool | Commands, config, deployment |

## Tips

1. Be specific - include the product name and feature
2. For complex questions, search multiple times with focused queries
3. Include exact error messages when troubleshooting
