---
name: convex-docs
description: Query and manage local Convex documentation mirror (42 docs). Search Convex topics for real-time database, serverless functions, authentication, file storage, and React hooks. Use when implementing Convex backend features or answering Convex-related questions. (user)
---

# Convex Documentation Skill

Query local Convex documentation covering backend-as-a-service, real-time database, serverless functions, authentication, and TypeScript backend development.

## Overview

This skill provides access to a complete local mirror of Convex documentation (42 docs across 10 sections). The documentation is structured, indexed, and optimized for AI/LLM consumption.

## Documentation Structure

```
docs/libs/convex/
├── _index.md                    # Navigation index
├── _meta.json                   # Metadata
├── README.md                    # Overview
├── getting-started/             # Quick setup (4 docs)
├── database/                    # Database operations (8 docs)
├── functions/                   # Queries, mutations, actions (8 docs)
├── client-libraries/            # React hooks & providers (7 docs)
├── authentication/              # Auth integration (5 docs)
├── file-storage/                # File uploads (4 docs)
├── scheduling/                  # Background jobs (2 docs)
└── production/                  # Deployment (4 docs)
```

## Core Concepts

### 1. Database
Location: `docs/libs/convex/database/`
- Real-time reactive queries
- Indexes and pagination
- Full-text search
- Relationships and foreign keys

### 2. Functions
Location: `docs/libs/convex/functions/`
- **Queries**: Read operations (reactive)
- **Mutations**: Write operations (transactional)
- **Actions**: External API calls (Node.js runtime)
- **HTTP Actions**: Public HTTP endpoints

### 3. React Hooks
Location: `docs/libs/convex/client-libraries/`
- useQuery: Subscribe to data
- useMutation: Write operations
- useAction: Call actions
- Optimistic updates

### 4. Authentication
Location: `docs/libs/convex/authentication/`
- Clerk integration
- Auth0 integration
- Custom auth providers
- User identity management

## Usage Protocol

### When to Activate

Use this skill when:
1. User asks about Convex implementation
2. Questions about real-time database
3. Need serverless backend functions
4. Authentication setup
5. File storage and uploads
6. Background jobs and scheduling

### Search Strategy

1. **Check Navigation First**
   ```bash
   Read: docs/libs/convex/_index.md
   Purpose: See all available documentation
   ```

2. **Section-Based Search**
   - Getting Started: `docs/libs/convex/getting-started/`
   - Database: `docs/libs/convex/database/`
   - Functions: `docs/libs/convex/functions/`
   - Client: `docs/libs/convex/client-libraries/`
   - Auth: `docs/libs/convex/authentication/`
   - Files: `docs/libs/convex/file-storage/`
   - Scheduling: `docs/libs/convex/scheduling/`
   - Production: `docs/libs/convex/production/`

3. **Specific Queries**
   ```bash
   # Database queries
   Read: docs/libs/convex/database/reading-data.md

   # Mutations
   Read: docs/libs/convex/database/writing-data.md

   # React hooks
   Read: docs/libs/convex/client-libraries/useQuery.md

   # Authentication
   Read: docs/libs/convex/authentication/clerk.md

   # File uploads
   Read: docs/libs/convex/file-storage/uploading-files.md
   ```

## Common Queries

### "How do I set up Convex with Next.js?"
1. Read `docs/libs/convex/getting-started/installation.md`
2. Read `docs/libs/convex/client-libraries/nextjs.md`
3. Provide setup steps and provider configuration

### "How do I query the database?"
1. Read `docs/libs/convex/database/reading-data.md`
2. Read `docs/libs/convex/functions/queries.md`
3. Read `docs/libs/convex/client-libraries/useQuery.md`
4. Show query function and React hook examples

### "How do I write to the database?"
1. Read `docs/libs/convex/database/writing-data.md`
2. Read `docs/libs/convex/functions/mutations.md`
3. Read `docs/libs/convex/client-libraries/useMutation.md`
4. Show mutation patterns

### "How do I implement authentication?"
1. Read `docs/libs/convex/authentication/overview.md`
2. Read specific provider docs (Clerk, Auth0, Custom)
3. Read `docs/libs/convex/authentication/user-identity.md`
4. Show auth setup and user access

### "How do I upload files?"
1. Read `docs/libs/convex/file-storage/uploading-files.md`
2. Read `docs/libs/convex/file-storage/serving-files.md`
3. Show upload mutation and URL generation

### "What's the difference between query, mutation, and action?"
1. Read `docs/libs/convex/functions/overview.md`
2. Read individual function type docs
3. Explain use cases and limitations

## Response Format

When answering Convex questions:

1. **Start with Context**
   - Briefly explain the concept
   - Mention it's serverless/real-time
   - Reference the source doc

2. **Provide Code Examples**
   - Show both backend (convex/) and frontend code
   - Include TypeScript types
   - Demonstrate React hooks

3. **Cite Sources**
   - Format: `docs/libs/convex/[section]/[file].md`
   - Include line numbers if relevant

4. **Related Topics**
   - Link to related documentation
   - Suggest best practices

## Key Convex Features

- Real-time reactivity (automatic UI updates)
- Transactional mutations
- TypeScript-first with automatic type generation
- Built-in authentication
- File storage
- Scheduled functions
- Vector search capabilities

## Example Response

```
User: "How do I create a mutation in Convex?"