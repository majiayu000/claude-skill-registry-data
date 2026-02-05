---
name: reviewing-component-architecture
description: Review component architecture for React 19 best practices including size, composition, Server/Client boundaries, and anti-patterns. Use when reviewing component design.
review: true
allowed-tools: Read, Grep, Glob
version: 1.0.0
---

# Review: Component Architecture

## Review Checklist

### Component Size
- [ ] Components under 300 lines (break into smaller pieces)
- [ ] Single responsibility per component
- [ ] No "god components" handling multiple concerns

### Server vs Client Boundaries
- [ ] `'use client'` only where needed (hooks, events, browser APIs)
- [ ] Most components are Server Components (smaller bundle)
- [ ] Data fetching in Server Components
- [ ] No Server Components imported in Client Components

### Composition Patterns
- [ ] Using children prop appropriately
- [ ] Compound components for coordinated behavior
- [ ] No excessive prop drilling (use Context)
- [ ] Composition preferred over complex prop APIs

### Custom Elements
- [ ] Web Components used correctly (no ref workarounds in React 19)
- [ ] Custom events use `on + EventName` convention
- [ ] Properties vs attributes handled by React

### Anti-Patterns to Flag
- [ ] ❌ God components (> 300 lines, multiple responsibilities)
- [ ] ❌ Unnecessary `'use client'` (no hooks/events/browser APIs)
- [ ] ❌ Deep prop drilling (3+ levels without Context)
- [ ] ❌ Server Components in Client Components
- [ ] ❌ Complex component hierarchies (hard to follow)

For comprehensive component patterns, see: `research/react-19-comprehensive.md`.
