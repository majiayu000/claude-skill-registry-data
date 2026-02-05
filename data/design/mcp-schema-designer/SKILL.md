---
name: mcp-schema-designer
version: 1.0.0
category: validation
complexity: simple
status: active
created: 2025-12-18
author: braiins-pool-mcp-server

description: |
  Designs comprehensive Zod schemas for MCP tool inputs and API responses,
  ensuring type safety, clear validation error messages, and security
  through input sanitization patterns.

triggers:
  - "design tool schema"
  - "create input validation"
  - "Zod schema for"
  - "validate tool parameters"
  - "create response schema"
  - "input schema"

dependencies: []
---

# MCP Schema Designer Skill

## Description

Design and implement Zod validation schemas for MCP tool inputs and Braiins API responses. This skill ensures type safety, prevents injection attacks through input validation, and provides clear error messages for invalid parameters.

## When to Use This Skill

- When defining input parameters for a new MCP tool
- When creating response validation for API endpoints
- When adding new parameters to existing tools
- When reviewing schemas for security vulnerabilities
- When standardizing validation patterns across tools

## When NOT to Use This Skill

- When implementing the full tool handler (use mcp-tool-builder)
- When designing caching strategy (use braiins-cache-strategist)
- When working on API client code (use braiins-api-mapper)

## Prerequisites

- Zod is installed: `npm install zod`
- Understanding of the parameter requirements from API.md
- Knowledge of TypeScript types

---

## Schema Design Patterns

### Pattern 1: Required String ID

Use for identifiers like worker IDs, pool IDs:

```typescript
import { z } from 'zod';

const WorkerIdSchema = z.object({
  workerId: z.string()
    .min(1, 'Worker ID is required')
    .max(100, 'Worker ID must be 100 characters or less')
    .regex(
      /^[a-zA-Z0-9\-_]+$/,
      'Worker ID can only contain letters, numbers, hyphens, and underscores'
    ),
});

// Usage in tool:
// workerId: "farm1-s19-01" -> Valid
// workerId: "" -> Error: "Worker ID is required"
// workerId: "abc@123" -> Error: "Worker ID can only contain..."
```

**Security Notes**:
- Regex prevents injection attacks
- Max length prevents memory exhaustion
- Min length ensures meaningful input

---

### Pattern 2: Pagination Parameters

Use for paginated list endpoints:

```typescript
const PaginationSchema = z.object({
  page: z.number()
    .int('Page must be a whole number')
    .min(1, 'Page must be at least 1')
    .default(1),

  pageSize: z.number()
    .int('Page size must be a whole number')
    .min(1, 'Page size must be at least 1')
    .max(200, 'Page size cannot exceed 200')
    .default(50),
});

// Extend for tool-specific pagination:
const ListWorkersInputSchema = PaginationSchema.extend({
  status: z.enum(['active', 'inactive', 'all']).default('all'),
});
```

**Default Values**:
- `page: 1` - Start at first page
- `pageSize: 50` - Reasonable default batch size
- `status: 'all'` - Include everything by default

---

### Pattern 3: Time Range Parameters

Use for historical data queries:

```typescript
const TimeRangeSchema = z.object({
  from: z.string()
    .datetime({ message: 'From must be a valid ISO 8601 datetime' })
    .optional(),

  to: z.string()
    .datetime({ message: 'To must be a valid ISO 8601 datetime' })
    .optional(),

  granularity: z.enum(['minute', 'hour', 'day'], {
    errorMap: () => ({ message: 'Granularity must be: minute, hour, or day' }),
  }).default('hour'),
}).refine(
  (data) => {
    if (data.from && data.to) {
      return new Date(data.from) <= new Date(data.to);
    }
    return true;
  },
  { message: 'From date must be before or equal to To date' }
);

// Usage:
// { from: "2025-01-01T00:00:00Z", to: "2025-01-10T00:00:00Z" } -> Valid
// { from: "2025-01-10T00:00:00Z", to: "2025-01-01T00:00:00Z" } -> Error: "From date must be..."
```

**Refinement**:
- Custom validation ensures logical date ranges
- `.refine()` enables cross-field validation

---

### Pattern 4: Filter Parameters with Allow-List

Use for search and filter endpoints:

```typescript
const WorkerFilterSchema = z.object({
  status: z.enum(['active', 'inactive', 'disabled', 'all'])
    .default('all')
    .describe('Filter workers by operational status'),

  search: z.string()
    .max(100, 'Search query too long')
    .regex(/^[a-zA-Z0-9\-_ ]*$/, 'Search contains invalid characters')
    .optional()
    .describe('Partial match on worker name'),

  sortBy: z.enum([
    'hashrate_desc',
    'hashrate_asc',
    'name_asc',
    'name_desc',
    'last_share_desc',
    'last_share_asc',
  ])
    .optional()
    .describe('Sort order for results'),

  tags: z.array(z.string().max(50))
    .max(10, 'Too many tags')
    .optional()
    .describe('Filter by worker tags'),
});
```

**Allow-List Pattern**:
- Enums prevent arbitrary sort/filter injection
- Only predefined values are accepted
- Clear error messages for invalid choices

---

### Pattern 5: API Response Validation

Use for validating Braiins API responses:

```typescript
// Base response fields
const TimestampedResponseSchema = z.object({
  updated_at: z.string().datetime(),
});

// Hashrate object (reusable)
const HashrateSchema = z.object({
  current: z.number().nonnegative(),
  avg_1h: z.number().nonnegative(),
  avg_24h: z.number().nonnegative(),
});

// Full response schema
const UserOverviewResponseSchema = TimestampedResponseSchema.extend({
  username: z.string(),
  currency: z.literal('BTC'),

  hashrate: HashrateSchema,

  rewards: z.object({
    confirmed: z.string().regex(/^\d+\.\d{8}$/, 'Invalid BTC amount format'),
    unconfirmed: z.string().regex(/^\d+\.\d{8}$/, 'Invalid BTC amount format'),
    last_payout: z.string(),
    last_payout_at: z.string().datetime(),
  }),

  workers: z.object({
    active: z.number().int().nonnegative(),
    inactive: z.number().int().nonnegative(),
    total: z.number().int().nonnegative(),
  }),
});

// Type inference
type UserOverviewResponse = z.infer<typeof UserOverviewResponseSchema>;
```

**Response Validation Benefits**:
- Catches API changes early (schema mismatch)
- Ensures type safety in handler code
- Documents expected API structure

---

### Pattern 6: Union Types for Polymorphic Data

Use when response varies by type:

```typescript
const WorkerStatusSchema = z.discriminatedUnion('status', [
  z.object({
    status: z.literal('active'),
    hashrate: HashrateSchema,
    last_share_at: z.string().datetime(),
    uptime_hours: z.number(),
  }),
  z.object({
    status: z.literal('inactive'),
    last_seen_at: z.string().datetime(),
    inactive_reason: z.enum(['no_shares', 'disconnected', 'maintenance']),
  }),
  z.object({
    status: z.literal('disabled'),
    disabled_at: z.string().datetime(),
    disabled_by: z.string(),
  }),
]);

// Type-safe access:
// if (worker.status === 'active') {
//   console.log(worker.hashrate); // TypeScript knows hashrate exists
// }
```

---

## Workflow

### Step 1: Gather Requirements

From API.md, extract:
- All parameters (name, type, required/optional)
- Valid value ranges and formats
- Default values
- Relationships between parameters

### Step 2: Choose Base Patterns

Select from patterns above based on parameter type:
- ID fields -> Pattern 1
- Pagination -> Pattern 2
- Date ranges -> Pattern 3
- Filters -> Pattern 4
- API responses -> Pattern 5

### Step 3: Implement Schema

```typescript
// src/schemas/{toolName}Input.ts
import { z } from 'zod';

/**
 * Input schema for {toolName} MCP tool
 *
 * Parameters:
 * - param1: Description (required)
 * - param2: Description (optional, default: X)
 *
 * @example
 * {
 *   param1: "value1",
 *   param2: 10
 * }
 */
export const {ToolName}InputSchema = z.object({
  // Define all parameters with validation
});

export type {ToolName}Input = z.infer<typeof {ToolName}InputSchema>;
```

### Step 4: Write Tests

```typescript
// tests/unit/schemas/{toolName}Input.test.ts
import { describe, it, expect } from 'vitest';
import { {ToolName}InputSchema } from '../../../src/schemas/{toolName}Input';

describe('{ToolName}InputSchema', () => {
  it('should accept valid input', () => {
    const result = {ToolName}InputSchema.safeParse({
      param1: 'valid-value',
    });
    expect(result.success).toBe(true);
  });

  it('should reject missing required field', () => {
    const result = {ToolName}InputSchema.safeParse({});
    expect(result.success).toBe(false);
    expect(result.error?.issues[0].message).toContain('required');
  });

  it('should apply default values', () => {
    const result = {ToolName}InputSchema.parse({
      param1: 'value',
    });
    expect(result.param2).toBe(50); // Default value
  });

  it('should reject invalid format', () => {
    const result = {ToolName}InputSchema.safeParse({
      param1: 'invalid@format!',
    });
    expect(result.success).toBe(false);
  });
});
```

---

## Quality Checklist

Every schema must pass these checks:

- [ ] All required fields have validation messages
- [ ] All strings have `.max()` to prevent abuse
- [ ] ID fields have regex patterns preventing injection
- [ ] Enums used for fixed-choice parameters
- [ ] Defaults provided where sensible
- [ ] JSDoc comment with example
- [ ] Type exported for use in handler
- [ ] Unit tests for valid/invalid cases
- [ ] Error messages are user-friendly (not technical)

---

## Examples

### Example 1: getWorkerDetails Input Schema

**Requirements** from API.md Section 6.2:
- workerId: Required, string identifier

```typescript
// src/schemas/getWorkerDetailsInput.ts
import { z } from 'zod';

/**
 * Input schema for getWorkerDetails MCP tool
 *
 * @param workerId - Unique identifier for the worker device
 *
 * @example
 * { workerId: "farm1-s19-01" }
 */
export const GetWorkerDetailsInputSchema = z.object({
  workerId: z.string()
    .min(1, 'Worker ID is required')
    .max(100, 'Worker ID must be 100 characters or less')
    .regex(
      /^[a-zA-Z0-9\-_]+$/,
      'Worker ID can only contain letters, numbers, hyphens, and underscores'
    ),
});

export type GetWorkerDetailsInput = z.infer<typeof GetWorkerDetailsInputSchema>;
```

---

### Example 2: listWorkers Input Schema

**Requirements** from API.md Section 6.1:
- page, pageSize: Pagination
- status, search, sortBy: Filters

```typescript
// src/schemas/listWorkersInput.ts
import { z } from 'zod';

/**
 * Input schema for listWorkers MCP tool
 *
 * @param page - Page number (default: 1)
 * @param pageSize - Items per page (default: 50, max: 200)
 * @param status - Filter by worker status
 * @param search - Partial name match
 * @param sortBy - Sort order
 *
 * @example
 * {
 *   page: 1,
 *   pageSize: 25,
 *   status: "active",
 *   sortBy: "hashrate_desc"
 * }
 */
export const ListWorkersInputSchema = z.object({
  // Pagination
  page: z.number()
    .int('Page must be a whole number')
    .min(1, 'Page must be at least 1')
    .default(1),

  pageSize: z.number()
    .int('Page size must be a whole number')
    .min(1, 'Page size must be at least 1')
    .max(200, 'Page size cannot exceed 200')
    .default(50),

  // Filters
  status: z.enum(['active', 'inactive', 'all'], {
    errorMap: () => ({ message: 'Status must be: active, inactive, or all' }),
  }).default('all'),

  search: z.string()
    .max(100, 'Search query too long')
    .regex(/^[a-zA-Z0-9\-_ ]*$/, 'Search contains invalid characters')
    .optional(),

  sortBy: z.enum([
    'hashrate_desc',
    'hashrate_asc',
    'name_asc',
    'name_desc',
    'last_share',
  ], {
    errorMap: () => ({
      message: 'Invalid sort option. Valid options: hashrate_desc, hashrate_asc, name_asc, name_desc, last_share',
    }),
  }).optional(),
});

export type ListWorkersInput = z.infer<typeof ListWorkersInputSchema>;
```

---

### Example 3: getWorkerHashrateTimeseries Input Schema

**Requirements** from API.md Section 6.3:
- workerId: Required identifier
- from, to: Optional time range
- granularity: Aggregation level

```typescript
// src/schemas/getWorkerHashrateTimeseriesInput.ts
import { z } from 'zod';

/**
 * Input schema for getWorkerHashrateTimeseries MCP tool
 *
 * @param workerId - Worker identifier
 * @param from - Start timestamp (ISO 8601)
 * @param to - End timestamp (ISO 8601)
 * @param granularity - Data point aggregation level
 *
 * @example
 * {
 *   workerId: "farm1-s19-01",
 *   from: "2025-01-01T00:00:00Z",
 *   to: "2025-01-07T00:00:00Z",
 *   granularity: "hour"
 * }
 */
export const GetWorkerHashrateTimeseriesInputSchema = z.object({
  workerId: z.string()
    .min(1, 'Worker ID is required')
    .max(100, 'Worker ID too long')
    .regex(/^[a-zA-Z0-9\-_]+$/, 'Invalid worker ID format'),

  from: z.string()
    .datetime({ message: 'From must be a valid ISO 8601 datetime' })
    .optional(),

  to: z.string()
    .datetime({ message: 'To must be a valid ISO 8601 datetime' })
    .optional(),

  granularity: z.enum(['minute', 'hour', 'day'], {
    errorMap: () => ({ message: 'Granularity must be: minute, hour, or day' }),
  }).default('hour'),
}).refine(
  (data) => {
    if (data.from && data.to) {
      return new Date(data.from) <= new Date(data.to);
    }
    return true;
  },
  { message: 'From date must be before or equal to To date' }
);

export type GetWorkerHashrateTimeseriesInput = z.infer<
  typeof GetWorkerHashrateTimeseriesInputSchema
>;
```

---

## Common Pitfalls

**Pitfall 1: Missing max length on strings**
```typescript
// BAD: No length limit
workerId: z.string()

// GOOD: Prevent memory exhaustion
workerId: z.string().max(100)
```

**Pitfall 2: Technical error messages**
```typescript
// BAD: Zod default message
.min(1) // Error: "String must contain at least 1 character(s)"

// GOOD: User-friendly message
.min(1, 'Worker ID is required')
```

**Pitfall 3: No regex on IDs**
```typescript
// BAD: Accepts any string (injection risk)
workerId: z.string().min(1).max(100)

// GOOD: Only safe characters
workerId: z.string().min(1).max(100).regex(/^[a-zA-Z0-9\-_]+$/)
```

**Pitfall 4: Hardcoded strings instead of enums**
```typescript
// BAD: Any string accepted
status: z.string()

// GOOD: Only valid options
status: z.enum(['active', 'inactive', 'all'])
```

---

## Version History

- **1.0.0** (2025-12-18): Initial skill definition

---

## References

- [Zod Documentation](https://zod.dev/)
- [API.md](../../../API.md) - Braiins API specification
- [ARCHITECTURE.md](../../../ARCHITECTURE.md) - Validation layer design
