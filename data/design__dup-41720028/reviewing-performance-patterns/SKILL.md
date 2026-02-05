---
name: reviewing-performance-patterns
description: Review React 19 performance patterns including memoization, re-renders, and bundle size. Use when reviewing performance or optimization.
review: true
allowed-tools: Read, Grep
version: 1.0.0
---

# Review: Performance Patterns

## Checklist

### Re-Rendering
- [ ] No unnecessary re-renders from prop changes
- [ ] Using React Compiler when possible (reduces manual memoization)
- [ ] Context split for different concerns (avoid re-render cascades)
- [ ] Children prop pattern to prevent wrapper re-renders

### Memoization
- [ ] Manual `useMemo`/`useCallback` only when needed (React Compiler handles most cases)
- [ ] `React.memo` used selectively for expensive components
- [ ] Dependencies correct in memoization hooks
- [ ] Not over-optimizing (premature optimization)

### Bundle Size
- [ ] Code splitting used for heavy components/routes
- [ ] Server Components used where appropriate (zero client JS)
- [ ] `'use client'` only where needed
- [ ] Lazy loading for non-critical components

### Resource Loading
- [ ] Using preload/preinit for critical resources
- [ ] DNS prefetch for external domains
- [ ] Images optimized and lazy loaded
- [ ] Fonts preloaded

### Anti-Patterns
- [ ] ❌ Array index as key (causes unnecessary re-renders)
- [ ] ❌ Creating new objects/arrays in render (breaks memoization)
- [ ] ❌ Excessive memoization without measurement
- [ ] ❌ Unnecessary `'use client'` (increases bundle)

For comprehensive performance patterns, see: `research/react-19-comprehensive.md`.
