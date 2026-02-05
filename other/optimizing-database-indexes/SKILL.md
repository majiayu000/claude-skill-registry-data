---
name: optimizing-database-indexes
description: Guidelines for creating efficient database indexes in Appwrite. Use to ensure search and filter operations stay fast.
---

# Database Indexing Strategy

## When to use this skill
- When queries are becoming slow.
- Before launching categories, search, or price sorting filters.

## Index Types
- **Key**: For simple equality checks (e.g., `userId`).
- **Fulltext**: For searching titles and descriptions.
- **Unique**: For fields like `email` or `slug` that must not repeat.

## Rules
- **Query Alignment**: Every field used in a `Query.equal` or `Query.orderAsc` should be indexed.
- **Index Order**: For compound queries, the order of attributes in the index matters (e.g., `Price` + `Status`).

## Instructions
- **Monitor**: Watch the Appwrite "Usage" tab to identify slow queries.
- **Limit**: Don't index every single field; it slows down writes (Creation/Updates).
