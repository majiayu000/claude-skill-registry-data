---
name: add-types-endpoint
description: >
  Type-safe frontend types for generation workflows and SSE events.
  Trigger: when adding new generation types or SSE events to the frontend.
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
# add-types-endpoint

Type-safe frontend types for generation workflows and SSE events.

**Trigger**: when adding new generation types or events to the frontend.
<!-- L1:END -->

<!-- L2:START -->
## Quick Reference

| Task | Pattern |
|------|---------|
| Validate user login | `User` |
| Create generation request | `GenerateRequest` |

## Critical Patterns (Summary)
- **User Pattern**: Validates `github_user_id` and `login` from `User` interface
- **GenerationRequest Pattern**: Constructs `GenerateRequest` with required `repo_url`, `mode`, and `provider`
<!-- L2:END -->

<!-- L3:START -->
## Critical Patterns (Detailed)

### User Pattern

Validates `github_user_id` and `login` from `User` interface to ensure authenticated session state before initiating generation workflows.

```typescript
import { User } from '@/lib/types';

if (!User || !User.github_user_id) {
  throw new Error('User not authenticated');
}
```
### GenerationRequest Pattern

Constructs `GenerateRequest` with required `repo_url`, `mode`, and `provider` fields to start a new generation pipeline.

```typescript
import { GenerateRequest } from '@/lib/types';

const request: GenerateRequest = {
  repo_url: 'https://github.com/example/repo',
  mode: 'skills',
  provider: 'openai',
};
```
## When to Use

- Validating authenticated user session before generation
- Constructing generation requests with proper mode and provider selection
- Handling user authentication state in generation workflows

## Commands

```bash
docker build -t repoforge/app:latest .
python repoforge/cli.py --help
```

## Anti-Patterns

### Don't: Missing required fields in GenerateRequest

<Why it's wrong: Omitting `repo_url`, `mode`, or `provider` causes runtime errors during generation pipeline initialization. All three fields are required per the `GenerateRequest` interface definition.>

```typescript
import { GenerateRequest } from '@/lib/types';

const badRequest: GenerateRequest = {
  // Missing repo_url, mode, provider — will fail validation
  mode: 'skills',
};
```
<!-- L3:END -->