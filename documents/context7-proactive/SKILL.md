---
name: context7-proactive
version: 1.0.0
description: Proactive documentation lookup via Context7 MCP. Query docs before using unfamiliar libraries.
---

# Context7 Proactive（文档智能查询）

## Trigger

Any of → `mcp__context7__resolve-library-id` → `mcp__context7__query-docs`:

1. Unfamiliar library (released or major-version-changed in last 6 months)
2. Uncertain API (function signature, parameter type, return value unclear)
3. Version migration ("how to upgrade to vX", "vX vs vY differences")
4. Fast-moving toolchain (Webpack, Vite, Next.js, Prisma, etc.)

## Flow

```
Unfamiliar library → resolve-library-id(name) → query-docs(specific question) → write code from docs
```

## Skip

- Standard language features (list comprehension, Promise)
- Well-known library with confirmed stable version
- User provided specific documentation URL
