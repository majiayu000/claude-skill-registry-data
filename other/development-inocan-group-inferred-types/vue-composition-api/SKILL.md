---
name: vue-composition-api
description: Master Vue Composition API - Composables, Reactivity Utilities, Script Setup, Provide/Inject
sasmp_version: "1.3.0"
bonded_agent: 02-vue-composition
bond_type: PRIMARY_BOND
version: "2.0.0"
last_updated: "2025-01"
---

# Vue Composition API Skill

Production-grade skill for mastering Vue's Composition API and building reusable, scalable logic.

## Purpose

**Single Responsibility:** Teach composable design patterns, advanced reactivity utilities, and modern Vue 3 composition techniques.

## Parameter Schema

```typescript
interface CompositionAPIParams {
  topic: 'composables' | 'reactivity' | 'script-setup' | 'provide-inject' | 'all';
  level: 'beginner' | 'intermediate' | 'advanced';
  context?: {
    existing_knowledge?: string[];
    use_case?: string;
  };
}
```

## Learning Modules

### Module 1: Script Setup Basics
```
Prerequisites: vue-fundamentals
Duration: 1-2 hours
Outcome: Use <script setup> effectively
```

| Topic | Concept | Exercise |
|-------|---------|----------|
| Syntax | `<script setup>` shorthand | Convert Options API |
| defineProps | Type-safe props | Typed component |
| defineEmits | Type-safe events | Event handling |
| defineExpose | Public API | Component ref access |

### Module 2: Reactivity Deep Dive
```
Prerequisites: Module 1
Duration: 3-4 hours
Outcome: Master all reactivity utilities
```

| Utility | When to Use | Exercise |
|---------|-------------|----------|
| ref() | Primitives | Counter state |
| reactive() | Objects | Form state |
| readonly() | Immutable exposure | Store state |
| toRef() | Single prop reference | Props handling |
| toRefs() | Destructure reactive | Store destructure |
| shallowRef() | Large objects | Performance opt |
| customRef() | Custom behavior | Debounced input |

### Module 3: Composables Architecture
```
Prerequisites: Modules 1-2
Duration: 4-5 hours
Outcome: Design production composables
```

**Composable Anatomy:**
```typescript
// composables/useFeature.ts
export function useFeature(options?: Options) {
  // 1. State (refs)
  const state = ref(initialValue)

  // 2. Computed (derived)
  const derived = computed(() => transform(state.value))

  // 3. Methods (actions)
  function action() { /* ... */ }

  // 4. Lifecycle (setup/cleanup)
  onMounted(() => { /* setup */ })
  onUnmounted(() => { /* cleanup */ })

  // 5. Return (public API)
  return { state: readonly(state), derived, action }
}
```

| Exercise | Composable | Features |
|----------|------------|----------|
| Data Fetching | useFetch | loading, error, refetch |
| Local Storage | useStorage | sync, parse, stringify |
| Media Query | useMediaQuery | reactive breakpoints |
| Debounce | useDebounce | value, delay |
| Intersection | useIntersection | observer, cleanup |

### Module 4: Provide/Inject Patterns
```
Prerequisites: Module 3
Duration: 2 hours
Outcome: Share state across components
```

| Pattern | Use Case | Example |
|---------|----------|---------|
| Theme Provider | App-wide theming | Dark/light mode |
| Auth Context | User state | Auth provider |
| Config Injection | Feature flags | Runtime config |
| Form Context | Multi-step forms | Form validation |

### Module 5: Advanced Patterns
```
Prerequisites: Modules 1-4
Duration: 3-4 hours
Outcome: Expert-level composition
```

| Pattern | Description | Exercise |
|---------|-------------|----------|
| Composable Composition | Composables using composables | useAuth + useFetch |
| State Machines | Finite state composables | useWizard |
| Plugin Pattern | Extend with plugins | useLogger plugin |
| Async Composables | Handle async setup | useAsyncData |

## Validation Checkpoints

### Beginner Checkpoint
- [ ] Convert Options API to Composition
- [ ] Use ref and computed
- [ ] Write basic composable
- [ ] Use defineProps/Emits

### Intermediate Checkpoint
- [ ] Build reusable composable
- [ ] Implement cleanup in composable
- [ ] Use provide/inject correctly
- [ ] Handle async in composables

### Advanced Checkpoint
- [ ] Design composable library
- [ ] Compose multiple composables
- [ ] Implement SSR-safe composables
- [ ] Test composables in isolation

## Retry Logic

```typescript
const skillConfig = {
  maxAttempts: 3,
  backoffMs: [1000, 2000, 4000],
  onFailure: 'provide_simpler_example'
}
```

## Observability

```yaml
tracking:
  - event: composable_created
    data: [name, complexity_score]
  - event: pattern_learned
    data: [pattern_name, exercises_completed]
  - event: skill_mastery
    data: [modules_completed, project_quality]
```

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Lost reactivity | Destructured reactive | Use toRefs() |
| inject undefined | Missing provider | Check tree hierarchy |
| Memory leak | No cleanup | Add onUnmounted cleanup |
| Type errors | Wrong generics | Specify type params |

### Debug Steps

1. Verify composable returns refs (not raw values)
2. Check provide/inject key matches
3. Confirm lifecycle hooks are in setup
4. Use Vue Devtools to inspect state

## Unit Test Template

```typescript
import { describe, it, expect } from 'vitest'
import { useCounter } from './useCounter'

describe('useCounter', () => {
  it('initializes with default value', () => {
    const { count } = useCounter()
    expect(count.value).toBe(0)
  })

  it('increments correctly', () => {
    const { count, increment } = useCounter()
    increment()
    expect(count.value).toBe(1)
  })

  it('resets to initial value', () => {
    const { count, increment, reset } = useCounter(5)
    increment()
    increment()
    reset()
    expect(count.value).toBe(5)
  })
})
```

## Usage

```
Skill("vue-composition-api")
```

## Related Skills

- `vue-fundamentals` - Prerequisite
- `vue-pinia` - State management
- `vue-typescript` - Type-safe composables

## Resources

- [Composition API Guide](https://vuejs.org/guide/reusability/composables.html)
- [VueUse](https://vueuse.org/) - Collection of composables
- [Vue Patterns](https://www.patterns.dev/vue)
