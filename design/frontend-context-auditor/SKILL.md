---
name: frontend-context-auditor
description: Audit React Context usage, detect prop drilling, verify compound component patterns. Use when reviewing frontend code for proper Context consumption, checking AgentChatContext/AgentSessionContext usage, or enforcing compound component patterns.
---

# Frontend Context Auditor

Audit React frontend code for proper Context usage and compound component patterns.

## Audit Checklist

### Context Providers

- [ ] `AgentChatContext` used for chat state (messages, input, streaming)
- [ ] `AgentSessionContext` used for session state (workflow, status, events)
- [ ] `SettingsContext` used for user preferences
- [ ] No prop drilling through intermediate components

### Compound Components

- [ ] Complex features use compound patterns: `Chat.Header`, `Chat.Messages`, `Chat.Input`
- [ ] Sub-components consume Context directly, not via props
- [ ] Parent component provides Context wrapper

### Type Safety

- [ ] No `any` types in component props or state
- [ ] Interfaces defined for all props
- [ ] Backend responses validated with type guards before use

### Styling

- [ ] Tailwind utility classes only (no arbitrary class names)
- [ ] shadcn/ui components used for accessible UI primitives
- [ ] No inline `style` objects for dynamic styling

## Audit Commands

```bash
# Find prop drilling (props passed through 2+ levels)
grep -r "props\." src/features/ | grep -v "interface\|type\|//" | head -50

# Find Context usage
grep -r "AgentChatContext\|AgentSessionContext\|SettingsContext" src/ | head -50

# Find compound component patterns
grep -r "Chat\.\|Header\|Messages\|Input" src/features/ | head -50

# Check for any types
grep -r ": any" src/ | head -20
```

## Refactoring Guidelines

When prop drilling is detected:

1. Extract shared state to a Context provider
2. Move provider to appropriate level in component tree
3. Consume Context in leaf components via `useContext`

When compound patterns are missing:

1. Split large components into `FeatureName.SubComponent` files
2. Extract shared state to `FeatureName.Context.tsx`
3. Wrap sub-components with provider in parent
