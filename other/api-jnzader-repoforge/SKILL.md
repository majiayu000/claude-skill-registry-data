---
name: add-api-endpoint
description: >
  Centralized API client for the web frontend with React Query integration.
  Trigger: when fetching or mutating data from the backend API.
license: Apache-2.0
metadata:
  author: repoforge
  version: "1.0"
complexity: medium
token_estimate: 450
dependencies: []
related_skills: []
load_priority: high
---

<!-- L1:START -->
# add-api-endpoint

One sentence: Centralized API client for the web frontend with React Query integration.

Trigger: when fetching or mutating data from the backend API.
<!-- L1:END -->

<!-- L2:START -->
## Quick Reference

| Task | Pattern |
|------|---------|
| Fetch generations | `useGenerations()` |
| Start generation | `useStartGeneration()` |
<!-- L2:END -->

<!-- L3:START -->
## Critical Patterns (Summary)

### Error Handling with ApiError

Handle structured API errors using the `ApiError` class which provides `status` and `code` fields for precise error categorization.

```typescript
import { ApiError } from '@/lib/api';

try {
  const data = await fetchApi<User>('/api/user');
} catch (error) {
  if (error instanceof ApiError) {
    // Handle specific status codes
    if (error.status === 401) {
      // Redirect to login
    }
  }
}
```

### useStartGeneration Mutation

Use the `useStartGeneration` mutation to trigger generation workflows with automatic query invalidation.

```typescript
import { useStartGeneration } from '@/lib/api';

const { mutate, isLoading } = useStartGeneration();
mutate({ mode: 'docs' });
```
## When to Use

- Fetching generation data or provider lists from the backend
- Starting new generation workflows with proper mutation handling
- Canceling in-progress generation tasks
- Querying analytics and provider information

## Commands

```bash
docker compose -f docker-compose.dev.yml up -d
python repoforge/cli.py dev
```

## Anti-Patterns

### Don't: Ignore ApiError status codes

Accessing `error.message` without checking `error.status` or `error.code` leads to brittle error handling that breaks on different error types.

```typescript
// BAD - assumes all errors are generic
catch (error) {
  console.error(error.message); // Misses status/code context
}
```
<!-- L3:END -->