---
name: noop-architecture
description: Guide for implementing code following the noop function-first, layered architecture. Use when writing handlers, services, database operations, or middleware. Automatically invoked when working on noop-based projects.
---

# Noop Architecture Guide

This skill provides guidance on implementing code that follows the noop architectural patterns.

## When Claude Should Use This

Automatically use this skill when:
- Writing new handlers or services in a noop project
- Implementing database operations
- Adding middleware
- Reviewing code for architectural compliance
- The user asks about noop patterns or conventions

## Framework Context

### Core Philosophy (MUST FOLLOW)
@docs/universal-framework/PHILOSOPHY.md

### Architecture Specification (LAYER RULES)
@docs/universal-framework/ARCHITECTURE_SPEC.md

### Coding Conventions (NAMING & STYLE)
@docs/universal-framework/CONVENTIONS.md

---

## Layer Summary

### Handlers - Orchestration Only
```typescript
export const create = asyncHandler(async (req, res) => {
  const { name } = req.body
  if (!name) throw createError.requiredField('name')

  const dbStore = getDbStore()
  const item = await service.create(data, req.user.organizationId, dbStore)

  return sendSuccess(res, item, 'Created', 201)
})
```

### Services - Business Logic
```typescript
export async function create(
  data: CreateInput,
  organizationId: string,
  dbStore: DbStore
): Promise<ItemInfo> {
  if (!organizationId) throw new Error('organizationId required')
  return dbStore.items.create(data, organizationId)
}
```

### Ops - Database Operations
```typescript
async create(data: CreateInput, organizationId: string): Promise<ItemInfo> {
  if (!organizationId) throw new Error('organization_id required')

  const result = await this.pgClient.executeQuery(
    'INSERT INTO items (...) VALUES ($1, $2, $3) RETURNING *',
    [id, data.name, organizationId]
  )

  return this.mapRowToItem(result.rows[0])
}
```

## Critical Anti-Patterns (NEVER DO)

```typescript
// 1. Silent fallbacks
catch { return defaultValue }  // ❌ NEVER

// 2. Any types
function process(data: any) { }  // ❌ NEVER

// 3. Missing org scoping
async getById(id: string) { }  // ❌ NEVER

// 4. Field fallbacks
id = a.id || a.data.id  // ❌ NEVER

// 5. Logic in handlers
const x = items.map(transform)  // ❌ NEVER (in handler)
```

## Import Rules

```typescript
// Always .js extension
import { config } from './config.js'

// Type imports
import type { UserInfo } from '../types/user.types.js'
```

## Response Utilities

```typescript
import { createError } from '../utils/errors.js'
import { sendSuccess, sendPaginatedResponse } from '../utils/standardResponse.js'

// Validation
if (!name) throw createError.requiredField('name')
if (!item) throw createError.notFound('Item', id)

// Success responses
return sendSuccess(res, item, 'Created', 201)
return sendPaginatedResponse(res, items, pagination)
```
