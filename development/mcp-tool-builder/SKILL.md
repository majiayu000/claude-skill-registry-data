---
name: mcp-tool-builder
version: 1.0.0
category: mcp-development
complexity: moderate
status: active
created: 2025-12-18
author: braiins-pool-mcp-server

description: |
  Guides implementation of new MCP tools from specification to production-ready
  code, following the braiins-pool-mcp-server architecture patterns and best
  practices defined in ARCHITECTURE.md.

triggers:
  - "create MCP tool"
  - "implement tool"
  - "build tool for"
  - "new MCP handler"
  - "add tool to MCP server"

dependencies:
  - mcp-schema-designer
  - braiins-api-mapper
  - braiins-cache-strategist
---

# MCP Tool Builder Skill

## Description

Implement new MCP tools for the braiins-pool-mcp-server from specification to production-ready code. This skill enforces the project's architectural patterns: cache-first data access, Zod validation, comprehensive error handling, and >80% test coverage.

## When to Use This Skill

- When implementing a new MCP tool from API.md specification
- When adding functionality to query Braiins Pool API
- When the user asks to "create", "build", or "implement" a tool
- After completing the design phase for a new tool
- When converting API endpoints to MCP tools

## When NOT to Use This Skill

- When refactoring existing tools (use refactoring workflow)
- When only updating schemas (use mcp-schema-designer)
- When debugging issues (use root-cause-tracing)
- When writing documentation only (use scribe-role-skill)

## Prerequisites

- [ ] API.md contains the endpoint specification
- [ ] ARCHITECTURE.md is available for patterns
- [ ] TypeScript project is initialized (package.json exists)
- [ ] Redis is configured (for caching)
- [ ] Test framework is set up (vitest/jest)

---

## Workflow

### Phase 1: Specification Review

**Step 1.1: Read API Documentation**

```bash
# Review the API specification
cat API.md | grep -A 50 "{endpoint_path}"
```

Extract and document:
- HTTP method (GET/POST)
- Endpoint path with parameters
- Query parameters and their types
- Response schema
- Authentication requirements
- Rate limiting constraints

**Step 1.2: Determine Tool Requirements**

Fill out this specification template:

```markdown
## Tool Specification: {toolName}

**MCP Tool Name**: {camelCase name, e.g., getMinerStats}
**API Endpoint**: {method} {path}
**Cache TTL**: {seconds}
**Priority**: {P0/P1/P2}

### Input Parameters
| Name | Type | Required | Validation |
|------|------|----------|------------|
| {param} | {type} | {yes/no} | {constraints} |

### Output Format
- Content Type: text (JSON stringified)
- Error Handling: {specific error cases}

### Caching Strategy
- Cache Key: braiins:{resource}:{identifiers}
- TTL: {seconds}
- Invalidation: {conditions}
```

---

### Phase 2: Schema Definition

**Step 2.1: Create Input Schema**

Create file: `src/schemas/{toolName}Input.ts`

```typescript
import { z } from 'zod';

/**
 * Input schema for {toolName} MCP tool
 *
 * @example
 * {
 *   paramName: "example_value"
 * }
 */
export const {ToolName}InputSchema = z.object({
  // Required parameters
  requiredParam: z.string()
    .min(1, '{Param} is required')
    .max(100, '{Param} too long')
    .regex(/^[a-zA-Z0-9\-_]+$/, 'Invalid {param} format'),

  // Optional parameters with defaults
  optionalParam: z.number()
    .int()
    .min(1)
    .max(1000)
    .default(50),
});

export type {ToolName}Input = z.infer<typeof {ToolName}InputSchema>;
```

**Step 2.2: Create Response Schema**

Create file: `src/schemas/{toolName}Response.ts`

```typescript
import { z } from 'zod';

/**
 * API response schema for {endpoint}
 * Based on API.md Section {X.Y}
 */
export const {ToolName}ResponseSchema = z.object({
  // Define all response fields with types
  field1: z.string(),
  field2: z.number(),
  nested: z.object({
    subField: z.string(),
  }),
  timestamp: z.string().datetime(),
});

export type {ToolName}Response = z.infer<typeof {ToolName}ResponseSchema>;
```

---

### Phase 3: Handler Implementation

**Step 3.1: Create Tool File**

Create file: `src/tools/{toolName}.ts`

```typescript
import { z } from 'zod';
import { {ToolName}InputSchema, type {ToolName}Input } from '../schemas/{toolName}Input';
import { {ToolName}ResponseSchema } from '../schemas/{toolName}Response';
import { braiinsClient } from '../api/braiinsClient';
import { redisManager } from '../cache/redisManager';
import { BraiinsApiError, CacheError } from '../utils/errors';
import { logger } from '../utils/logger';

/**
 * MCP Tool: {toolName}
 *
 * {Description of what the tool does}
 *
 * @see API.md Section {X.Y}
 */
export const {toolName}Tool = {
  name: '{toolName}',
  description: '{User-friendly description for AI model}',
  inputSchema: {ToolName}InputSchema,

  handler: async (rawInput: unknown) => {
    // Step 1: Validate input
    const parseResult = {ToolName}InputSchema.safeParse(rawInput);
    if (!parseResult.success) {
      return {
        content: [{
          type: 'text' as const,
          text: JSON.stringify({
            error: 'VALIDATION_ERROR',
            message: 'Invalid input parameters',
            details: parseResult.error.flatten(),
          }),
        }],
        isError: true,
      };
    }
    const input = parseResult.data;

    // Step 2: Generate cache key
    const cacheKey = `braiins:{resource}:${input.requiredParam}`;

    // Step 3: Check cache
    try {
      const cached = await redisManager.get<{ToolName}Response>(cacheKey);
      if (cached) {
        logger.debug('Cache hit', { tool: '{toolName}', key: cacheKey });
        return {
          content: [{
            type: 'text' as const,
            text: JSON.stringify(cached),
          }],
        };
      }
    } catch (error) {
      // Log but don't fail on cache errors
      logger.warn('Cache error, falling through to API', { error });
    }

    // Step 4: Call API
    try {
      const response = await braiinsClient.{apiMethod}(input);

      // Step 5: Validate response
      const validated = {ToolName}ResponseSchema.parse(response);

      // Step 6: Cache result
      try {
        await redisManager.set(cacheKey, validated, {TTL_SECONDS});
      } catch (cacheError) {
        logger.warn('Failed to cache result', { error: cacheError });
      }

      // Step 7: Return formatted response
      return {
        content: [{
          type: 'text' as const,
          text: JSON.stringify(validated),
        }],
      };
    } catch (error) {
      // Handle specific error types
      if (error instanceof BraiinsApiError) {
        return {
          content: [{
            type: 'text' as const,
            text: JSON.stringify({
              error: error.code,
              message: error.message,
              statusCode: error.statusCode,
            }),
          }],
          isError: true,
        };
      }

      // Unknown error
      logger.error('Unexpected error in {toolName}', { error });
      return {
        content: [{
          type: 'text' as const,
          text: JSON.stringify({
            error: 'INTERNAL_ERROR',
            message: 'An unexpected error occurred',
          }),
        }],
        isError: true,
      };
    }
  },
};
```

---

### Phase 4: Testing

**Step 4.1: Create Unit Tests**

Create file: `tests/unit/tools/{toolName}.test.ts`

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { {toolName}Tool } from '../../../src/tools/{toolName}';
import { braiinsClient } from '../../../src/api/braiinsClient';
import { redisManager } from '../../../src/cache/redisManager';

// Mock dependencies
vi.mock('../../../src/api/braiinsClient');
vi.mock('../../../src/cache/redisManager');

describe('{toolName} Tool', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('Input Validation', () => {
    it('should reject missing required parameter', async () => {
      const result = await {toolName}Tool.handler({});
      expect(result.isError).toBe(true);
      expect(JSON.parse(result.content[0].text)).toMatchObject({
        error: 'VALIDATION_ERROR',
      });
    });

    it('should reject invalid parameter format', async () => {
      const result = await {toolName}Tool.handler({
        requiredParam: 'invalid@format!',
      });
      expect(result.isError).toBe(true);
    });

    it('should accept valid parameters', async () => {
      vi.mocked(redisManager.get).mockResolvedValue(null);
      vi.mocked(braiinsClient.{apiMethod}).mockResolvedValue({
        // Valid response
      });

      const result = await {toolName}Tool.handler({
        requiredParam: 'valid-id',
      });
      expect(result.isError).toBeFalsy();
    });
  });

  describe('Caching', () => {
    it('should return cached data on cache hit', async () => {
      const cachedData = { /* mock cached response */ };
      vi.mocked(redisManager.get).mockResolvedValue(cachedData);

      const result = await {toolName}Tool.handler({
        requiredParam: 'test-id',
      });

      expect(braiinsClient.{apiMethod}).not.toHaveBeenCalled();
      expect(JSON.parse(result.content[0].text)).toEqual(cachedData);
    });

    it('should call API on cache miss', async () => {
      vi.mocked(redisManager.get).mockResolvedValue(null);
      vi.mocked(braiinsClient.{apiMethod}).mockResolvedValue({
        // API response
      });

      await {toolName}Tool.handler({ requiredParam: 'test-id' });

      expect(braiinsClient.{apiMethod}).toHaveBeenCalled();
    });

    it('should cache API response', async () => {
      vi.mocked(redisManager.get).mockResolvedValue(null);
      const apiResponse = { /* mock response */ };
      vi.mocked(braiinsClient.{apiMethod}).mockResolvedValue(apiResponse);

      await {toolName}Tool.handler({ requiredParam: 'test-id' });

      expect(redisManager.set).toHaveBeenCalledWith(
        expect.stringContaining('braiins:'),
        expect.anything(),
        {TTL_SECONDS}
      );
    });
  });

  describe('Error Handling', () => {
    it('should handle API errors gracefully', async () => {
      vi.mocked(redisManager.get).mockResolvedValue(null);
      vi.mocked(braiinsClient.{apiMethod}).mockRejectedValue(
        new BraiinsApiError('Not found', 404)
      );

      const result = await {toolName}Tool.handler({
        requiredParam: 'nonexistent',
      });

      expect(result.isError).toBe(true);
      expect(JSON.parse(result.content[0].text)).toMatchObject({
        statusCode: 404,
      });
    });

    it('should fall through on cache errors', async () => {
      vi.mocked(redisManager.get).mockRejectedValue(new Error('Redis down'));
      vi.mocked(braiinsClient.{apiMethod}).mockResolvedValue({
        // API response
      });

      const result = await {toolName}Tool.handler({
        requiredParam: 'test-id',
      });

      expect(result.isError).toBeFalsy();
    });
  });
});
```

**Step 4.2: Run Tests**

```bash
npm test -- --coverage tests/unit/tools/{toolName}.test.ts
```

Target: >80% coverage for the tool file.

---

### Phase 5: Integration

**Step 5.1: Export Tool**

Update `src/tools/index.ts`:

```typescript
export { {toolName}Tool } from './{toolName}';
```

**Step 5.2: Register with MCP Server**

Update `src/index.ts`:

```typescript
import { {toolName}Tool } from './tools';

// In server initialization
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    // ... existing tools
    {
      name: {toolName}Tool.name,
      description: {toolName}Tool.description,
      inputSchema: zodToJsonSchema({toolName}Tool.inputSchema),
    },
  ],
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  switch (request.params.name) {
    // ... existing cases
    case '{toolName}':
      return {toolName}Tool.handler(request.params.arguments);
  }
});
```

**Step 5.3: Final Verification**

```bash
# Run full test suite
npm test

# Run type check
npm run type-check

# Run linter
npm run lint
```

---

## Examples

### Example 1: Implementing getUserOverview Tool

**Input**: "Create the getUserOverview MCP tool based on API.md Section 5.1"

**Process**:

1. **Specification Review**:
   - Endpoint: GET /user/overview
   - No input parameters (uses auth token)
   - Returns: hashrate, rewards, worker counts
   - Cache TTL: 30s

2. **Schema Creation**:
```typescript
// src/schemas/getUserOverviewInput.ts
export const GetUserOverviewInputSchema = z.object({
  // No parameters needed - uses bearer token auth
});

// src/schemas/getUserOverviewResponse.ts
export const GetUserOverviewResponseSchema = z.object({
  username: z.string(),
  currency: z.string(),
  hashrate: z.object({
    current: z.number(),
    avg_1h: z.number(),
    avg_24h: z.number(),
  }),
  rewards: z.object({
    confirmed: z.string(),
    unconfirmed: z.string(),
    last_payout: z.string(),
    last_payout_at: z.string().datetime(),
  }),
  workers: z.object({
    active: z.number(),
    inactive: z.number(),
    total: z.number(),
  }),
  updated_at: z.string().datetime(),
});
```

3. **Handler Implementation**: Following template with TTL=30

4. **Tests**: 12 tests covering validation, caching, errors

5. **Integration**: Registered in index.ts

---

### Example 2: Implementing listWorkers Tool with Pagination

**Input**: "Create the listWorkers tool with pagination support"

**Specification**:
- Endpoint: GET /workers
- Parameters: page, pageSize, status, search, sortBy
- Cache TTL: 30s (varies by filters)

**Key Implementation Differences**:

1. **Cache Key includes filter hash**:
```typescript
const filtersHash = hashObject({ status, search, sortBy });
const cacheKey = `braiins:workers:list:${page}:${filtersHash}`;
```

2. **Pagination in response**:
```typescript
return {
  content: [{
    type: 'text',
    text: JSON.stringify({
      data: validated.workers,
      pagination: {
        page: validated.page,
        pageSize: validated.page_size,
        total: validated.total,
        hasMore: validated.page * validated.page_size < validated.total,
      },
    }),
  }],
};
```

---

## Quality Standards

Every tool implemented with this skill must meet:

- [ ] Input schema validates all parameters
- [ ] Response schema matches API.md specification
- [ ] Cache-first pattern implemented correctly
- [ ] All error cases handled (401, 403, 404, 429, 500)
- [ ] Logging at appropriate levels
- [ ] Unit tests >80% coverage
- [ ] Integration tests for happy path
- [ ] No sensitive data in logs or errors
- [ ] Type-safe throughout (no `any` types)

---

## Common Pitfalls

**Pitfall 1: Forgetting to sanitize cache keys**
```typescript
// BAD: User input directly in cache key
const cacheKey = `braiins:worker:${input.workerId}`;

// GOOD: Sanitize or hash user input
const sanitized = input.workerId.replace(/[^a-zA-Z0-9\-_]/g, '');
const cacheKey = `braiins:worker:${sanitized}`;
```

**Pitfall 2: Not handling cache errors**
```typescript
// BAD: Cache error breaks the request
const cached = await redisManager.get(cacheKey);

// GOOD: Fall through on cache errors
try {
  const cached = await redisManager.get(cacheKey);
  if (cached) return formatResponse(cached);
} catch {
  logger.warn('Cache unavailable, calling API directly');
}
```

**Pitfall 3: Exposing internal errors**
```typescript
// BAD: Leaking stack traces
return { error: error.stack };

// GOOD: User-friendly error message
return { error: 'INTERNAL_ERROR', message: 'An unexpected error occurred' };
```

---

## Troubleshooting

**Issue**: Tool not appearing in Claude's available tools
**Solution**:
1. Check tool is exported from `src/tools/index.ts`
2. Verify tool is registered in `src/index.ts`
3. Restart MCP server after changes

**Issue**: Tests failing with "Cannot find module"
**Solution**:
1. Check import paths are correct
2. Run `npm run build` to compile TypeScript
3. Verify file exists at expected path

**Issue**: Cache always misses
**Solution**:
1. Verify Redis connection in logs
2. Check cache key generation is consistent
3. Confirm TTL is set correctly

---

## Version History

- **1.0.0** (2025-12-18): Initial skill definition for braiins-pool-mcp-server

---

## References

- [ARCHITECTURE.md](../../../ARCHITECTURE.md) - System architecture patterns
- [API.md](../../../API.md) - Braiins API specification
- [MCP Protocol Spec](https://modelcontextprotocol.io/) - MCP standard
