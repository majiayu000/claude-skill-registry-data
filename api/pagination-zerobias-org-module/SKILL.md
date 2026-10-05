---
name: pagination
description: Pagination implementation patterns for list operations. Use when implementing paginated list operations or handling page tokens/numbers.
---

# Pagination Patterns

Complete patterns for implementing pagination in LIST operations across all producer implementations.

## 🚨 CRITICAL: Three Mutually Exclusive Pagination Approaches

There are THREE different pagination approaches. **YOU CANNOT MIX THEM**:

1. **Offset/Limit Pagination** (pageNumber + pageSize) → API supports pagination parameters
2. **No Pagination Support** (client-side) → Use `PagedResults.ingest()` to apply pagination
3. **Token-Based Pagination** (pageToken) → API uses cursor-based pagination

**NEVER mix approaches in the same implementation!**

## Approach 1: Offset/Limit Pagination (STANDARD)

**Use this for APIs that support offset/limit query parameters.**

This is the STANDARD pattern for most LIST operations:

```typescript
async list(results: PagedResults<ResourceType>, organizationId: string): Promise<void> {
  const params: Record<string, number> = {};

  // ✅ REQUIRED: Convert pageNumber/pageSize to offset/limit
  if (results.pageNumber && results.pageSize) {
    params.offset = (results.pageNumber - 1) * results.pageSize;
    params.limit = Math.min(Math.max(results.pageSize, 1), 1000);
  } else {
    // 🚨 MANDATORY: Always initialize offset when pagination not provided
    params.offset = 0;
  }

  const response = await this.httpClient.get(
    `/orgs/${organizationId}/resources`,
    { params }
  );

  // ✅ REQUIRED: Validate response structure before mapping
  if (!response.data || !Array.isArray(response.data.data)) {
    throw new UnexpectedError('Invalid response format: expected data array');
  }

  // ✅ Map without ternary (validation ensures array exists)
  results.items = response.data.data.map(toResource);
  results.count = response.data.totalCount || 0;

  // ❌ DO NOT assign pageToken when using offset/limit pagination
  // results.pageToken = ... // WRONG!
}
```

## Approach 2: No Pagination Support (Client-Side Pagination)

**Use this ONLY when the API does NOT support any pagination parameters.**

When an API endpoint returns ALL results without pagination support, use `PagedResults.ingest()` to apply client-side pagination:

```typescript
async list(results: PagedResults<AuthenticationStrengthPolicy>): Promise<void> {
  // This endpoint doesn't support pagination parameters - make direct request
  const { data } = await this.msGraph.executeRequest(
    { url: 'policies/authenticationStrengthPolicies' },
    defaultErrorHandler,
    'beta'
  );

  // ✅ REQUIRED: Validate response structure before mapping
  if (!data?.value || !Array.isArray(data.value)) {
    throw new UnexpectedError('Invalid response format: expected value array');
  }

  // Map all results to domain objects
  const allItems = data.value.map(toAuthenticationStrengthPolicy);

  // ✅ Use PagedResults.ingest() to apply client-side pagination
  // This method will:
  // - Set results.count to total array length
  // - Slice the array based on pageNumber and pageSize
  // - Set results.items to the paginated slice
  // - Validate page bounds and throw errors if invalid
  results.ingest(
    allItems,
    results.pageNumber,
    results.pageSize
  );

  // ❌ DO NOT manually set items/count when using ingest()
  // results.items = allItems;  // WRONG!
  // results.count = allItems.length;  // WRONG!
}
```

**What `PagedResults.ingest()` does**:
1. Validates `pageNumber` is >= 1
2. Calculates total `pageCount` from array length
3. Validates requested page exists
4. Calculates slice bounds: `start = (pageNumber - 1) * pageSize`, `end = start + pageSize`
5. Sets `results.items = array.slice(start, end)`
6. Sets `results.count = array.length` (total count)
7. Sets `results.pageNumber` and `results.pageSize`

**Parameters**:
- `array`: Full array of mapped domain objects
- `pageNumber`: Optional page number (defaults to 1)
- `pageSize`: Optional page size (defaults to 50)
- `pageToken`: Optional page token (for compatibility)

**When to use**:
- API returns all results in a single response
- No pagination query parameters supported
- API documentation states "pagination not supported"
- Response doesn't include `nextPageToken` or `totalCount`

**Benefits**:
- Consistent pagination behavior for clients
- Automatic validation of page bounds
- Error handling for invalid pages
- Single source of truth for pagination logic

## Approach 3: Token-Based Pagination (CURSOR)

**Use this ONLY for APIs that use cursor-based pagination with tokens.**

```typescript
async list(results: PagedResults<ResourceType>, organizationId: string): Promise<void> {
  const params: Record<string, string> = {};

  // ✅ Use pageToken from previous request if available
  if (results.pageToken) {
    params.pageToken = results.pageToken;
  }

  // ❌ DO NOT use offset/limit when using token-based pagination
  // if (results.pageNumber && results.pageSize) { ... } // WRONG!

  const response = await this.httpClient.get(
    `/orgs/${organizationId}/resources`,
    { params }
  );

  // ✅ REQUIRED: Validate response structure before mapping
  if (!response.data || !Array.isArray(response.data.data)) {
    throw new UnexpectedError('Invalid response format: expected data array');
  }

  // ✅ Map without ternary (validation ensures array exists)
  results.items = response.data.data.map(toResource);
  results.count = response.data.totalCount || 0;

  // ✅ REQUIRED: Assign next pageToken for cursor-based pagination
  results.pageToken = response.headers['x-next-page-token'];
}
```

## Mandatory Requirements

### 1. Offset Initialization

**CRITICAL**: The `else` clause with `params.offset = 0` is MANDATORY:

```typescript
// ✅ CORRECT - Always initialize offset
if (results.pageNumber && results.pageSize) {
  params.offset = (results.pageNumber - 1) * results.pageSize;
  params.limit = Math.min(Math.max(results.pageSize, 1), 1000);
} else {
  params.offset = 0;  // MANDATORY
}

// ❌ WRONG - Missing offset initialization
if (results.pageNumber && results.pageSize) {
  params.offset = (results.pageNumber - 1) * results.pageSize;
  params.limit = Math.min(Math.max(results.pageSize, 1), 1000);
}
// Missing else clause causes undefined offset when pagination not provided
```

**WHY**: APIs may require offset parameter even for first page. Missing offset can cause request failures or incorrect results.

### 2. Response Validation

**REQUIRED**: Always validate response structure before mapping:

```typescript
// ✅ CORRECT - Validate before mapping
if (!response.data || !Array.isArray(response.data.data)) {
  throw new UnexpectedError('Invalid response format: expected data array');
}
results.items = response.data.data.map(toResource);

// ❌ WRONG - Ternary without validation
results.items = response.data?.data?.map(toResource) || [];
```

**WHY**:
- Fails fast with clear error message
- Prevents silent failures with empty arrays
- Consistent error handling across all producers
- TypeScript type narrowing ensures array exists

### 3. Limit Enforcement

Enforce minimum and maximum limits:

```typescript
// ✅ CORRECT - Enforce bounds
params.limit = Math.min(Math.max(results.pageSize, 1), 1000);

// Breakdown:
// Math.max(results.pageSize, 1)  → Minimum 1 item
// Math.min(..., 1000)             → Maximum 1000 items
```

**WHY**:
- Prevents requesting 0 items (invalid)
- Prevents overwhelming API with huge page sizes
- Respects API rate limits and best practices

## Parameter Conversion

### PagedResults to API Parameters

Standard conversion pattern:

```typescript
// Input: PagedResults object with pageNumber and pageSize
// Output: API params with offset and limit

const params: Record<string, number> = {};

if (results.pageNumber && results.pageSize) {
  // Page 1, Size 10 → offset: 0, limit: 10
  // Page 2, Size 10 → offset: 10, limit: 10
  // Page 3, Size 10 → offset: 20, limit: 10
  params.offset = (results.pageNumber - 1) * results.pageSize;
  params.limit = Math.min(Math.max(results.pageSize, 1), 1000);
} else {
  // No pagination provided → start from beginning
  params.offset = 0;
}
```

**Examples**:
- pageNumber=1, pageSize=25 → offset=0, limit=25
- pageNumber=3, pageSize=50 → offset=100, limit=50
- pageNumber=5, pageSize=100 → offset=400, limit=100
- No pagination → offset=0, no limit

## Response Mapping

### Standard Response Structure

Most APIs return paginated responses in this format:

```json
{
  "data": [
    { "id": "1", "name": "Resource 1" },
    { "id": "2", "name": "Resource 2" }
  ],
  "totalCount": 42,
  "metadata": { ... }
}
```

### Mapping to PagedResults (Offset/Limit)

```typescript
// ✅ CORRECT - Offset/Limit pagination mapping
results.items = response.data.data.map(toResource);  // Array of mapped items
results.count = response.data.totalCount || 0;       // Total count for pagination UI
// ❌ DO NOT assign pageToken for offset/limit pagination
```

**Fields for Offset/Limit Pagination**:
- `items`: Mapped domain objects (not raw API data)
- `count`: Total number of items across all pages
- `pageToken`: **NOT USED** - left undefined

### Mapping to PagedResults (Token-Based)

```typescript
// ✅ CORRECT - Token-based pagination mapping
results.items = response.data.data.map(toResource);  // Array of mapped items
results.count = response.data.totalCount || 0;       // Total count (if available)
results.pageToken = response.headers['x-next-page-token'];  // ✅ Token for next page
```

**Fields for Token-Based Pagination**:
- `items`: Mapped domain objects (not raw API data)
- `count`: Total count (may not be available in cursor-based pagination)
- `pageToken`: Next page token from response headers

## Choosing the Right Approach

**Use Offset/Limit (Approach 1)** when:
- API supports `offset` and `limit` query parameters
- API returns `totalCount` in response
- Need to jump to specific pages (e.g., page 5)
- Most common for REST APIs

**Use Client-Side Pagination (Approach 2)** when:
- API returns ALL results in a single response
- No pagination parameters supported by the API
- API documentation states "pagination not supported"
- Endpoint returns complete dataset (typically small, < 1000 items)
- Need to provide paginated interface to clients despite API limitations

**Use Token-Based (Approach 3)** when:
- API requires `pageToken` parameter
- API returns next page token in headers or response body
- Data changes frequently (cursor prevents skipped/duplicate items)
- API documentation explicitly uses cursor-based pagination

**NEVER**:
- Mix approaches in the same implementation
- Assign `pageToken` when using offset/limit or client-side pagination
- Use offset/limit when API requires tokens
- Manually set items/count when using `PagedResults.ingest()`
- Use `PagedResults.ingest()` when API supports native pagination

## Complete Examples

### Example 1: Simple LIST

```typescript
async listUsers(results: PagedResults<User>, organizationId: string): Promise<void> {
  const params: Record<string, number> = {};

  if (results.pageNumber && results.pageSize) {
    params.offset = (results.pageNumber - 1) * results.pageSize;
    params.limit = Math.min(Math.max(results.pageSize, 1), 1000);
  } else {
    params.offset = 0;
  }

  const response = await this.httpClient.get(`/orgs/${organizationId}/users`, { params });

  if (!response.data || !Array.isArray(response.data.data)) {
    throw new UnexpectedError('Invalid response format: expected data array');
  }

  results.items = response.data.data.map(toUser);
  results.count = response.data.totalCount || 0;
}
```

### Example 2: LIST with Nested Path

```typescript
async listGroupUsers(
  results: PagedResults<UserInfo>,
  organizationId: string,
  groupId: string
): Promise<void> {
  const params: Record<string, number> = {};

  if (results.pageNumber && results.pageSize) {
    params.offset = (results.pageNumber - 1) * results.pageSize;
    params.limit = Math.min(Math.max(results.pageSize, 1), 1000);
  } else {
    params.offset = 0;
  }

  const response = await this.httpClient.get(
    `/orgs/${organizationId}/groups/${groupId}/users`,
    { params }
  );

  if (!response.data || !Array.isArray(response.data.data)) {
    throw new UnexpectedError('Invalid response format: expected data array');
  }

  results.items = response.data.data.map(toUserInfo);
  results.count = response.data.totalCount || 0;
}
```

### Example 3: LIST with Additional Filters

```typescript
async searchResources(
  results: PagedResults<Resource>,
  organizationId: string,
  filter?: string
): Promise<void> {
  const params: Record<string, string | number> = {};

  // Pagination
  if (results.pageNumber && results.pageSize) {
    params.offset = (results.pageNumber - 1) * results.pageSize;
    params.limit = Math.min(Math.max(results.pageSize, 1), 1000);
  } else {
    params.offset = 0;
  }

  // Additional filters
  if (filter) {
    params.q = filter;
  }

  const response = await this.httpClient.get(
    `/orgs/${organizationId}/resources`,
    { params }
  );

  if (!response.data || !Array.isArray(response.data.data)) {
    throw new UnexpectedError('Invalid response format: expected data array');
  }

  results.items = response.data.data.map(toResource);
  results.count = response.data.totalCount || 0;
}
```

## Common Mistakes

### Mistake 1: Missing Offset Initialization

```typescript
// ❌ WRONG - No else clause
if (results.pageNumber && results.pageSize) {
  params.offset = (results.pageNumber - 1) * results.pageSize;
  params.limit = Math.min(Math.max(results.pageSize, 1), 1000);
}
// params.offset is undefined when pagination not provided
```

**Impact**: API requests may fail or return unexpected results.

### Mistake 2: Ternary Instead of Validation

```typescript
// ❌ WRONG - Silent failure with empty array
results.items = response.data?.data?.map(toResource) || [];
```

**Impact**:
- Masks API errors
- Returns empty array for malformed responses
- Difficult to debug issues
- Inconsistent error handling

### Mistake 3: No Limit Bounds

```typescript
// ❌ WRONG - No bounds checking
params.limit = results.pageSize;
```

**Impact**:
- Can request 0 items (invalid)
- Can overwhelm API with huge requests
- May hit API rate limits

### Mistake 4: Mixing Pagination Approaches

```typescript
// ❌ WRONG - Using pageToken with offset/limit pagination
async list(results: PagedResults<Resource>, orgId: string): Promise<void> {
  const params: Record<string, number> = {};

  if (results.pageNumber && results.pageSize) {
    params.offset = (results.pageNumber - 1) * results.pageSize;
    params.limit = Math.min(Math.max(results.pageSize, 1), 1000);
  }

  // ... fetch and map ...

  results.pageToken = response.headers['x-next-page-token'];  // ❌ WRONG!
}
```

**Impact**:
- Confuses pagination approach
- PageToken is meaningless in offset/limit pagination
- Can cause unexpected behavior in calling code

**Correct**:
```typescript
// ✅ CORRECT - Offset/limit WITHOUT pageToken
results.items = response.data.data.map(toResource);
results.count = response.data.totalCount || 0;
// No pageToken assignment for offset/limit pagination
```

### Mistake 5: Wrong totalCount Fallback

```typescript
// ❌ WRONG - Using items length as fallback
results.count = response.data.totalCount || response.data.data.length;
```

**Impact**:
- Shows wrong total on pagination UI
- First page of 10 items shows "10 total" when actually 1000+
- Breaks pagination controls

**Correct**:
```typescript
// ✅ CORRECT - Fallback to 0 if missing
results.count = response.data.totalCount || 0;
```

## Validation Checklists

### Offset/Limit Pagination Checklist

Before completing a LIST operation with offset/limit pagination:

- [ ] `params` object declared as `Record<string, number>`
- [ ] `if (results.pageNumber && results.pageSize)` condition present
- [ ] `params.offset = (results.pageNumber - 1) * results.pageSize` calculation
- [ ] `params.limit = Math.min(Math.max(results.pageSize, 1), 1000)` bounds
- [ ] `else { params.offset = 0; }` clause present (MANDATORY)
- [ ] Response validation with `UnexpectedError` before mapping
- [ ] `results.items = response.data.data.map(toMapper)` (no ternary)
- [ ] `results.count = response.data.totalCount || 0` assignment
- [ ] **NO** `results.pageToken` assignment
- [ ] Consistent `/orgs/` URL prefix used

### Token-Based Pagination Checklist

Before completing a LIST operation with token-based pagination:

- [ ] `params` object declared as `Record<string, string>`
- [ ] `if (results.pageToken)` condition to use token from previous request
- [ ] `params.pageToken = results.pageToken` assignment when token exists
- [ ] **NO** offset/limit parameters used
- [ ] Response validation with `UnexpectedError` before mapping
- [ ] `results.items = response.data.data.map(toMapper)` (no ternary)
- [ ] `results.count = response.data.totalCount || 0` assignment (if available)
- [ ] `results.pageToken = response.headers['x-next-page-token']` assignment
- [ ] Consistent `/orgs/` URL prefix used

## Integration with PagedResults

The `PagedResults<T>` type is provided by `@zerobias-org/types-core-js`:

```typescript
import { PagedResults } from '@zerobias-org/types-core-js';

interface PagedResults<T> {
  items: T[];           // Array of domain objects (output)
  count: number;        // Total count across all pages (output)
  pageNumber?: number;  // Current page number (input, optional)
  pageSize?: number;    // Items per page (input, optional)
  pageToken?: string;   // Token for next page (output, optional)
}
```

**Input Parameters** (provided by caller):
- `pageNumber`: Which page to retrieve (1-based) - **Offset/Limit only**
- `pageSize`: How many items per page - **Offset/Limit only**
- `pageToken`: Token from previous response - **Token-Based only**

**Output Fields** (set by LIST method):
- `items`: Mapped domain objects for current page - **Always set**
- `count`: Total number of items across all pages - **Always set**
- `pageToken`: Token for next page - **Token-Based only, NOT set for Offset/Limit**

## References

- Producer Implementation: @.claude/skills/implementation-core/SKILL.md
- Error Handling: @.claude/skills/error-handling/SKILL.md
- Operation Patterns: @.claude/skills/api-operations/SKILL.md
- Operation Engineer: @.claude/agents/operation-engineer.md
