---
name: trpc-docs
description: Query and manage local tRPC documentation mirror (25 docs). Search tRPC topics for end-to-end typesafe APIs, routers, procedures, React Query integration, and Next.js setup. Use when implementing tRPC features or answering tRPC-related questions. (user)
---

# tRPC Documentation Skill

Query local tRPC documentation covering routers, procedures, React Query integration, and Next.js App Router setup.

## Overview

This skill provides access to a complete local mirror of tRPC documentation (25 docs across 5 sections). The documentation is structured, indexed, and optimized for AI/LLM consumption.

## Documentation Structure

```
docs/libs/trpc/
├── _index.md              # Navigation index
├── _meta.json             # Metadata
├── README.md              # Overview
├── quickstart/            # Getting started (4 docs)
├── server/                # Server-side (6 docs)
├── client/                # Client-side (4 docs)
├── procedures/            # Procedures (3 docs)
└── adapters/              # Framework adapters (4 docs)
```

## Core Concepts

### 1. Routers
Location: `docs/libs/trpc/server/routers.md`
- Creating and organizing routers
- Merging routers for large APIs
- Router composition patterns

### 2. Procedures
Location: `docs/libs/trpc/server/procedures.md`
- Query procedures (read operations)
- Mutation procedures (write operations)
- Subscription procedures (real-time)

### 3. Client Integration
Location: `docs/libs/trpc/client/react.md`
- React Query integration
- Hooks: useQuery, useMutation
- Type inference

### 4. Next.js Setup
Location: `docs/libs/trpc/quickstart/nextjs-setup.md`
- App Router integration
- Server Components
- API routes

## Usage Protocol

### When to Activate

Use this skill when:
1. User asks about tRPC implementation
2. Questions about typesafe APIs
3. Need to integrate tRPC with Next.js/React
4. Troubleshooting tRPC issues
5. Understanding tRPC architecture

### Search Strategy

1. **Check Navigation First**
   ```bash
   Read: docs/libs/trpc/_index.md
   Purpose: See all available documentation
   ```

2. **Section-Based Search**
   - Getting Started: `docs/libs/trpc/quickstart/`
   - Server Setup: `docs/libs/trpc/server/`
   - Client Usage: `docs/libs/trpc/client/`
   - Procedures: `docs/libs/trpc/procedures/`
   - Adapters: `docs/libs/trpc/adapters/`

3. **Specific Queries**
   ```bash
   # Router creation
   Read: docs/libs/trpc/server/routers.md

   # React integration
   Read: docs/libs/trpc/client/react.md

   # Next.js setup
   Read: docs/libs/trpc/quickstart/nextjs-setup.md

   # Context & middleware
   Read: docs/libs/trpc/server/context.md
   Read: docs/libs/trpc/server/middlewares.md
   ```

## Common Queries

### "How do I set up tRPC with Next.js App Router?"
1. Read `docs/libs/trpc/quickstart/nextjs-setup.md`
2. Read `docs/libs/trpc/adapters/nextjs-adapter.md`
3. Provide setup steps with code examples

### "How do I create a tRPC router?"
1. Read `docs/libs/trpc/server/routers.md`
2. Read `docs/libs/trpc/server/procedures.md`
3. Show router creation patterns

### "How do I use tRPC with React Query?"
1. Read `docs/libs/trpc/client/react.md`
2. Read `docs/libs/trpc/client/react-query.md`
3. Explain hooks and usage patterns

### "How do I add authentication to tRPC?"
1. Read `docs/libs/trpc/server/context.md`
2. Read `docs/libs/trpc/server/middlewares.md`
3. Show auth middleware patterns

### "How do I validate input with Zod?"
1. Read `docs/libs/trpc/procedures/input-validation.md`
2. Show Zod schema examples
3. Explain type inference

## Response Format

When answering tRPC questions:

1. **Start with Context**
   - Briefly explain the concept
   - Reference the source doc

2. **Provide Code Examples**
   - Show practical implementation
   - Include TypeScript types
   - Demonstrate best practices

3. **Cite Sources**
   - Format: `docs/libs/trpc/[section]/[file].md`
   - Include line numbers if relevant

4. **Related Topics**
   - Link to related documentation
   - Suggest next steps

## Example Response

```
User: "How do I create a tRPC mutation?"