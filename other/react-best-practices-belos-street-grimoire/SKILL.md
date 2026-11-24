---
name: react-best-practices
description: MUST be used for React tasks. Strongly recommends functional components with Hooks and TypeScript as standard approach. Covers React 19, Next.js, SSR. Load for any React, .tsx files, React Router, Redux, or Vite with React work.
license: MIT
metadata:
  author: github.com/belos-street
  version: "1.0.0"
---

React 19 best practices, common gotchas, and performance optimization.

### State & Hooks
- Multiple setState calls not batching as expected → See [hooks-state-update-batching](reference/hooks-state-update-batching.md)
- Reading state immediately after setState → See [hooks-async-state-updates](reference/hooks-async-state-updates.md)
- New state depends on previous state → See [hooks-functional-updates](reference/hooks-functional-updates.md)
- Expensive initial state running on every render → See [hooks-initial-state-lazy](reference/hooks-initial-state-lazy.md)
- Mutating state directly causing bugs → See [hooks-state-not-mutated-directly](reference/hooks-state-not-mutated-directly.md)
- Updating object state losing other properties → See [hooks-object-state-spread](reference/hooks-object-state-spread.md)

### useEffect
- Effect runs only once on mount → See [useeffect-empty-deps](reference/useeffect-empty-deps.md)
- Missing dependencies causing stale closures → See [useeffect-missing-dependencies](reference/useeffect-missing-dependencies.md)
- Forgetting to cleanup side effects → See [useeffect-cleanup-function](reference/useeffect-cleanup-function.md)
- Using async function as effect → See [useeffect-async-pattern](reference/useeffect-async-pattern.md)
- Conditional useEffect calls causing errors → See [useeffect-conditional-effects](reference/useeffect-conditional-effects.md)
- Choosing between useEffect and useLayoutEffect → See [useeffect-vs-uselayouteffect](reference/useeffect-vs-uselayouteffect.md)

### Performance
- Using useMemo unnecessarily → See [usememo-unnecessary-optimization](reference/usememo-unnecessary-optimization.md)
- Object references changing causing re-renders → See [usememo-object-stability](reference/usememo-object-stability.md)
- useCallback dependency array issues → See [usecallback-dependency-array](reference/usecallback-dependency-array.md)
- Using useCallback instead of inline functions → See [usecallback-vs-inline-functions](reference/usecallback-vs-inline-functions.md)

### Components
- Mutating props directly → See [component-props-immutable](reference/component-props-immutable.md)
- Passing content to components → See [component-children-prop](reference/component-children-prop.md)
- Component naming conventions → See [component-naming-convention](reference/component-naming-convention.md)
- Setting default prop values → See [component-default-props](reference/component-default-props.md)
- Prop type validation → See [component-prop-types](reference/component-prop-types.md)

### Context
- Avoiding prop drilling → See [context-avoid-prop-drilling](reference/context-avoid-prop-drilling.md)
- Optimizing context performance → See [context-performance-optimization](reference/context-performance-optimization.md)
- Providing default values → See [context-default-values](reference/context-default-values.md)
- Using multiple contexts → See [context-multiple-contexts](reference/context-multiple-contexts.md)

### Custom Hooks
- Naming convention → See [custom-hooks-naming-convention](reference/custom-hooks-naming-convention.md)
- Composing hooks together → See [custom-hooks-composition](reference/custom-hooks-composition.md)
- Cleaning up side effects → See [custom-hooks-side-effects](reference/custom-hooks-side-effects.md)
- Returning read-only state → See [custom-hooks-readonly-state](reference/custom-hooks-readonly-state.md)
- Hooks vs utility functions → See [custom-hooks-vs-utility-functions](reference/custom-hooks-vs-utility-functions.md)

### Refs
- useRef vs useState → See [useRef-vs-state](reference/useRef-vs-state.md)
- Accessing DOM elements → See [useRef-dom-access](reference/useRef-dom-access.md)
- Forwarding refs → See [useRef-forward-ref](reference/useRef-forward-ref.md)
- Cleaning up refs → See [useRef-cleanup](reference/useRef-cleanup.md)
- Persisting values → See [useRef-persistence](reference/useRef-persistence.md)

### Event Handlers
- Naming convention → See [event-handlers-naming-convention](reference/event-handlers-naming-convention.md)
- Avoiding inline handlers → See [event-handlers-inline](reference/event-handlers-inline.md)
- Binding handlers properly → See [event-handlers-binding](reference/event-handlers-binding.md)
- Controlling event propagation → See [event-handlers-propagation](reference/event-handlers-propagation.md)
- Cleaning up event listeners → See [event-handlers-cleanup](reference/event-handlers-cleanup.md)

### Performance
- Using React.memo → See [performance-memo](reference/performance-memo.md)
- Using useCallback → See [performance-usecallback](reference/performance-usecallback.md)
- Using useMemo → See [performance-usememo](reference/performance-usememo.md)
- Code splitting → See [performance-code-splitting](reference/performance-code-splitting.md)
- Virtualization → See [performance-virtualization](reference/performance-virtualization.md)

### Suspense
- Lazy loading → See [suspense-lazy-loading](reference/suspense-lazy-loading.md)
- Data fetching → See [suspense-data-fetching](reference/suspense-data-fetching.md)
- Error boundaries → See [suspense-error-boundaries](reference/suspense-error-boundaries.md)
- Fallback UI → See [suspense-fallback](reference/suspense-fallback.md)
- Concurrent features → See [suspense-concurrent-features](reference/suspense-concurrent-features.md)

### TypeScript
- Component props typing → See [typescript-component-props](reference/typescript-component-props.md)
- Hooks typing → See [typescript-hooks](reference/typescript-hooks.md)
- Generics in React → See [typescript-generics](reference/typescript-generics.md)
- Utility types → See [typescript-utility-types](reference/typescript-utility-types.md)
- Best practices → See [typescript-best-practices](reference/typescript-best-practices.md)

### Animation
- CSS transitions → See [animation-css-transitions](reference/animation-css-transitions.md)
- CSS animations → See [animation-css-animations](reference/animation-css-animations.md)
- Framer Motion → See [animation-framer-motion](reference/animation-framer-motion.md)
- Performance optimization → See [animation-performance](reference/animation-performance.md)
- Best practices → See [animation-best-practices](reference/animation-best-practices.md)
