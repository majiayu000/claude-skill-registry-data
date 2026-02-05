---
name: vue-fundamentals
description: Master Vue.js core concepts - Components, Reactivity, Templates, Directives, Lifecycle
sasmp_version: "1.3.0"
bonded_agent: 01-vue-fundamentals
bond_type: PRIMARY_BOND
version: "2.0.0"
last_updated: "2025-01"
---

# Vue Fundamentals Skill

Production-grade skill for mastering Vue.js core concepts and building robust component-based applications.

## Purpose

**Single Responsibility:** Teach and validate understanding of Vue.js fundamentals including component architecture, reactivity system, template syntax, directives, and lifecycle hooks.

## Parameter Schema

```typescript
interface VueFundamentalsParams {
  topic: 'components' | 'reactivity' | 'templates' | 'directives' | 'lifecycle' | 'all';
  level: 'beginner' | 'intermediate' | 'advanced';
  context?: {
    current_knowledge?: string[];
    learning_goal?: string;
    time_available?: string;
  };
}
```

## Learning Modules

### Module 1: Components (Foundation)
```
Prerequisites: HTML, CSS, JavaScript basics
Duration: 2-3 hours
Outcome: Build reusable Vue components
```

| Topic | Concept | Exercise |
|-------|---------|----------|
| SFC Structure | `<template>`, `<script>`, `<style>` | Create first component |
| Props | Passing data down | Build Card component |
| Events | `$emit` for child→parent | Button with click handler |
| Slots | Content distribution | Layout component |
| Registration | Local vs global | Component organization |

### Module 2: Reactivity (Core)
```
Prerequisites: Module 1
Duration: 3-4 hours
Outcome: Understand Vue's reactivity system
```

| Topic | Concept | Exercise |
|-------|---------|----------|
| ref() | Primitive reactivity | Counter app |
| reactive() | Object reactivity | Form state |
| computed() | Derived values | Shopping cart total |
| watch() | Side effects | API calls on change |
| watchEffect() | Auto-track | Logging changes |

### Module 3: Templates (Syntax)
```
Prerequisites: Module 1
Duration: 2 hours
Outcome: Master template syntax
```

| Topic | Concept | Exercise |
|-------|---------|----------|
| Interpolation | `{{ }}` binding | Display data |
| v-bind | Attribute binding | Dynamic classes |
| v-on | Event handling | Form submission |
| v-model | Two-way binding | Input forms |
| v-if/v-show | Conditional render | Toggle visibility |
| v-for | List rendering | Todo list |

### Module 4: Directives (Built-in & Custom)
```
Prerequisites: Module 3
Duration: 2 hours
Outcome: Use and create directives
```

| Topic | Concept | Exercise |
|-------|---------|----------|
| v-if/else | Conditional | Auth display |
| v-for + key | Iteration | Data tables |
| v-model modifiers | .lazy, .trim | Form validation |
| v-on modifiers | .prevent, .stop | Event control |
| Custom directives | Reusable DOM logic | v-focus directive |

### Module 5: Lifecycle (Hooks)
```
Prerequisites: Modules 1-4
Duration: 2 hours
Outcome: Manage component lifecycle
```

| Hook | Use Case | Example |
|------|----------|---------|
| onMounted | DOM ready | Fetch initial data |
| onUpdated | After reactivity | Scroll position |
| onUnmounted | Cleanup | Clear intervals |
| onErrorCaptured | Error boundary | Graceful degradation |

## Validation Checkpoints

### Beginner Checkpoint
- [ ] Create SFC with props and events
- [ ] Use ref() for counter
- [ ] Apply v-if and v-for
- [ ] Handle form with v-model

### Intermediate Checkpoint
- [ ] Build multi-slot component
- [ ] Use computed for derived state
- [ ] Implement watch with cleanup
- [ ] Create custom directive

### Advanced Checkpoint
- [ ] Design component composition patterns
- [ ] Optimize with shallowRef
- [ ] Implement error boundaries
- [ ] Build async components

## Retry Logic

```typescript
const skillConfig = {
  maxAttempts: 3,
  backoffMs: [1000, 2000, 4000],
  onFailure: 'provide_hint'
}
```

## Observability

```yaml
tracking:
  - event: module_started
    data: [module_name, user_level]
  - event: checkpoint_passed
    data: [checkpoint_name, attempts]
  - event: skill_completed
    data: [total_time, score]
```

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Component not showing | Not registered | Check import/registration |
| Props not reactive | Wrong prop type | Use correct type |
| v-for no key | Missing :key | Add unique key |
| Infinite loop | watch causing watched change | Guard the update |

### Debug Steps

1. Check Vue Devtools component tree
2. Verify props are passed correctly
3. Confirm reactive values have .value
4. Check lifecycle hook placement

## Unit Test Template

```typescript
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import MyComponent from './MyComponent.vue'

describe('MyComponent', () => {
  it('renders props correctly', () => {
    const wrapper = mount(MyComponent, {
      props: { title: 'Test' }
    })
    expect(wrapper.text()).toContain('Test')
  })

  it('emits event on action', async () => {
    const wrapper = mount(MyComponent)
    await wrapper.find('button').trigger('click')
    expect(wrapper.emitted('action')).toBeTruthy()
  })
})
```

## Usage

```
Skill("vue-fundamentals")
```

## Related Skills

- `vue-composition-api` - Next level after fundamentals
- `vue-typescript` - Adding type safety
- `vue-testing` - Testing fundamentals

## Resources

- [Vue.js Tutorial](https://vuejs.org/tutorial/)
- [Vue Mastery](https://www.vuemastery.com/)
- [Vue School](https://vueschool.io/)
