---
name: reviewing-state-management
description: Review state management patterns for React 19 best practices. Use when reviewing component state, Context usage, or state architecture.
review: true
allowed-tools: Read, Grep
version: 1.0.0
---

# Review: State Management

## Checklist

### State Immutability
- [ ] No direct state mutation
- [ ] Using spread operators or immutable update patterns
- [ ] Arrays updated with map/filter/concat (not push/splice)
- [ ] Objects updated with spread or Object.assign

### State Location
- [ ] Local state used when appropriate
- [ ] Context only for cross-cutting concerns
- [ ] No prop drilling through 3+ levels
- [ ] Frequently changing state not in Context

### useReducer Usage
- [ ] Used for complex state logic
- [ ] Reducer functions are pure
- [ ] Action types are consistent
- [ ] State updates follow patterns

### Context Patterns
- [ ] Split contexts for different concerns
- [ ] Using `use()` API in React 19 (not `useContext`)
- [ ] Context providers at appropriate level
- [ ] No unnecessary re-renders

### Anti-Patterns
- [ ] ❌ Direct state mutation (`state.push()`, `state.x = y`)
- [ ] ❌ Context for frequently changing values
- [ ] ❌ Excessive prop drilling
- [ ] ❌ God components managing too much state

For comprehensive state patterns, see: `research/react-19-comprehensive.md`.
