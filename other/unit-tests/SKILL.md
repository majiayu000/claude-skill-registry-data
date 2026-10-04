---
name: testing:unit-tests
description: |
  Create comprehensive unit tests for components, modules, stores, and utilities.
  Use when asked to write tests, add test coverage, or test a specific file.
disable-model-invocation: false
allowed-tools: Read Write Edit Bash Grep Glob
---

# Unit Test Creation

Create unit tests following project conventions.

## Usage

- `/testing:unit-tests [target]` - Create tests for specific file
- `/testing:unit-tests scan` - Find files needing tests

## Test Patterns

<!-- Customize these patterns for your framework -->

### Component Testing
```typescript
import { describe, expect, it } from 'vitest';

describe('MyComponent', () => {
  it('renders correctly', async () => {
    // Mount component with test utilities
    // Assert expected behavior
  });
});
```

### Module/Composable Testing
```typescript
import { describe, expect, it } from 'vitest';

describe('useMyModule', () => {
  it('returns expected structure', () => {
    const result = useMyModule();
    expect(result).toBeDefined();
  });
});
```

### Store Testing
```typescript
import { describe, expect, it } from 'vitest';

describe('MyStore', () => {
  it('initializes correctly', () => {
    const store = useMyStore();
    expect(store.items).toEqual([]);
  });
});
```

## File Locations

| Source | Test Location |
|--------|---------------|
| `src/components/Card.vue` | `tests/components/Card.test.ts` |
| `src/composables/useData.ts` | `tests/composables/useData.test.ts` |
| `src/stores/data.ts` | `tests/stores/data.test.ts` |

## Workflow

1. Analyze target file structure and exports
2. Create test file in appropriate directory
3. Cover: happy path, edge cases, error conditions
4. Run tests to verify
5. Check coverage improvement
