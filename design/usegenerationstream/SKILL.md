---
name: usegenerationstream-hook
description: >
  This skill covers patterns for managing generation streams in a React application.
  Trigger: Load when using `useGenerationStream` for state management.
license: Apache-2.0
metadata:
  author: repoforge
  version: "1.0"
  complexity: medium
  token_estimate: 350
  dependencies: []
  related_skills: []
  load_priority: high
---

<!-- L1:START -->
# usegenerationstream-hook

This skill covers patterns for managing generation streams in a React application.

**Trigger**: Load when using `useGenerationStream` for state management.
<!-- L1:END -->

<!-- L2:START -->
## Quick Reference

| Task | Pattern |
|------|---------|
| Manage stream status | `StreamStatus` |
| Handle step items | `StepItem` |

## Critical Patterns (Summary)
- **StreamStatus Management**: Utilize `StreamStatus` to track the state of the generation stream.
- **StepItem Handling**: Use `StepItem` to represent individual steps in the generation process.
<!-- L2:END -->

<!-- L3:START -->
## Critical Patterns (Detailed)

### StreamStatus Management

Utilize `StreamStatus` to track the state of the generation stream, allowing for responsive UI updates.

```typescript
import { StreamStatus } from '@/hooks/useGenerationStream';

const status: StreamStatus = StreamStatus.RUNNING; // Example usage
```

### StepItem Handling

Use `StepItem` to represent individual steps in the generation process, enabling detailed tracking of progress.

```typescript
import { StepItem } from '@/hooks/useGenerationStream';

const step: StepItem = { id: 1, description: 'Initializing...' }; // Example usage
```

## When to Use

- When managing the state of a generation process in a React component.
- When displaying progress through individual steps of a generation task.

## Commands

```bash
docker-compose up
python repoforge/cli.py
```

## Anti-Patterns

### Don't: Ignore StreamState

Ignoring `StreamState` can lead to unresponsive UI and poor user experience.

```typescript
// BAD
const state = {}; // Missing StreamState management
```
<!-- L3:END -->