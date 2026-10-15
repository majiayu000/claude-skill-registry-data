---
name: convex-functions
displayName: Convex Functions
description: Writing queries, mutations, actions, and HTTP actions with proper argument validation, error handling, internal functions, and runtime considerations
version: 1.0.0
author: Convex
tags: [convex, functions, queries, mutations, actions, http]
---

# Convex Functions

Master Convex functions including queries, mutations, actions, and HTTP endpoints with proper validation, error handling, and runtime considerations.

## Code Quality

All examples in this skill comply with @convex-dev/eslint-plugin rules:

- Object syntax with `handler` property
- Argument validators on all functions
- Explicit table names in database operations

See the Code Quality section in [convex-best-practices](../convex-best-practices/SKILL.md) for linting setup.

## Documentation Sources

Before implementing, do not assume; fetch the latest documentation:

- Primary: https://docs.convex.dev/functions
- Query Functions: https://docs.convex.dev/functions/query-functions
- Mutation Functions: https://docs.convex.dev/functions/mutation-functions
- Actions: https://docs.convex.dev/functions/actions
- HTTP Actions: https://docs.convex.dev/functions/http-actions
- For broader context: https://docs.convex.dev/llms.txt

## Instructions

### Function Types Overview

| Type        | Database Access          | External APIs | Caching       | Use Case              |
| ----------- | ------------------------ | ------------- | ------------- | --------------------- |
| Query       | Read-only                | No            | Yes, reactive | Fetching data         |
| Mutation    | Read/Write               | No            | No            | Modifying data        |
| Action      | Via runQuery/runMutation | Yes           | No            | External integrations |
| HTTP Action | Via runQuery/runMutation | Yes           | No            | Webhooks, APIs        |

## Code Patterns

Full code samples live in the reference file. Read it before writing the matching code.

Sections in `references/patterns.md`:

- Queries
- Mutations
- Actions
- HTTP Actions
- Internal Functions
- Scheduling Functions
- Complete Function File

## Best Practices

- Never run `npx convex deploy` unless explicitly instructed
- Never run any git commands unless explicitly instructed
- Always define args and returns validators
- Use queries for read operations (they are cached and reactive)
- Use mutations for write operations (they are transactional)
- Use actions only when calling external APIs
- Use internal functions for sensitive operations
- Add `"use node";` at the top of action files using Node.js APIs
- Handle errors with ConvexError for user-facing messages

## Common Pitfalls

1. **Using actions for database operations** - Use queries/mutations instead
2. **Calling external APIs from queries/mutations** - Use actions
3. **Forgetting to add "use node"** - Required for Node.js APIs in actions
4. **Missing return validators** - Always specify returns
5. **Not using internal functions for sensitive logic** - Protect with internalMutation

## References

- Convex Documentation: https://docs.convex.dev/
- Convex LLMs.txt: https://docs.convex.dev/llms.txt
- Functions Overview: https://docs.convex.dev/functions
- Query Functions: https://docs.convex.dev/functions/query-functions
- Mutation Functions: https://docs.convex.dev/functions/mutation-functions
- Actions: https://docs.convex.dev/functions/actions
