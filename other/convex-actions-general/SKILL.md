---
name: convex-actions-general
description: This skill should be used when working with Convex actions, HTTP endpoints, validators, schemas, environment variables, scheduling, file storage, and TypeScript patterns. It provides comprehensive guidelines for function definitions, API design, database limits, and advanced Convex features.
---

# Convex Actions and General Guidelines Skill

This skill provides comprehensive guidance for Convex actions, HTTP endpoints, validators, schema design, file storage, environment variables, scheduling, and TypeScript best practices.

## When to Use This Skill

Use this skill when:
- Implementing action functions for external API calls and long-running tasks
- Creating HTTP endpoints for webhooks or public APIs
- Defining validators for function arguments and database schemas
- Designing database schemas with tables, indexes, and search capabilities
- Setting up environment variables for secrets and configuration
- Implementing cron jobs and scheduled tasks
- Working with file storage for uploads and downloads
- Using Convex-specific TypeScript patterns and types
- Understanding Convex limits and performance constraints

## Skill Resources

`references/actions-and-general.md` covers, in this order: function syntax, HTTP endpoints, validators (types, discriminated unions, ASCII field names, size limits), function registration, calling and references, API design, limits, environment variables, actions (`"use node"`, V8 vs Node, 10-minute timeout), crons and scheduler, schema and indexes, full text search, file storage (upload URL, `ctx.storage.getUrl()`, `_storage` metadata) and TypeScript (`Id<'table'>`, `Doc<'table'>`, `Record`, `as const`).

Key limits: 8 MiB arguments and return values, 8192 writes per mutation, 16384 reads per query, 1 second timeout for queries and mutations, 10 minutes for actions, 8192 array elements, 1024 object fields, 16 nesting levels, 1 MiB per record, 20 MiB HTTP streaming output.

## How to Use This Skill

1. **Read the reference documentation** at `references/actions-and-general.md` for comprehensive patterns
2. **Follow the syntax** for defining actions with proper Node.js module handling
3. **Use validators** correctly for all function arguments and schema fields
4. **Design schemas** with appropriate indexes for your access patterns
5. **Set up environment variables** for secrets and configuration
6. **Implement scheduling** for background tasks using crons or the scheduler
7. **Handle file storage** with proper URL generation and metadata lookup
8. **Understand limits** and design applications to respect them
9. **Use TypeScript strictly** with `Id` types and proper generics

## Key General Guidelines

- ALWAYS use argument validators for all functions (queries, mutations, actions)
- Do NOT store file URLs in the database; store file IDs instead
- Remapping non-ASCII characters (emoji) to ASCII codes before storing in objects
- Auth state does NOT propagate to scheduled jobs; use internal functions
- Scheduled functions should not run more than once every 10 seconds
- Never call actions from other actions unless crossing runtimes (V8 to Node)
- Objects in Convex must have ASCII-only field names
- Be strict with TypeScript types, especially for document IDs

## Examples

Two complete samples (an action with an HTTP endpoint, and a plain HTTP endpoint) are in `references/examples.md`.
