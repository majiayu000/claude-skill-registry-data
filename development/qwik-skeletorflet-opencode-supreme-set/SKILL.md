---
name: qwik
description: Qwik framework resumability, lazy loading, $() suffix, and Qwik City routing. Use when building Qwik apps with instant startup and minimal JS.
---

## qwik

### Core Concepts
- Resumability: no hydration, serializes app state in HTML for instant resume
- $() suffix marks lazy-loaded boundaries serialized to chunks
- useSignal, useStore for local state, useTask for lifecycle effects
- useResource for server data fetching with streaming
- Qwik City: file-based router with loaders, actions, layouts

### Common Patterns
- Islands architecture with interactive widgets using component$
- Route loaders in src/routes for SSR data fetching
- Server actions with $() for form mutations and validation
- useServerMount() for server-only initialization code
- Optimizer automatically splits code at $() boundaries

### Best Practices
- Keep components outside $() boundaries static, wrap only interactive parts
- Use useVisibleTask$ sparingly (only for browser-specific code)
- Prefer useServerMount$ over useVisibleTask$ for init logic
- Leverage routeLoader$() for cacheable data fetching
- Use PrefetchServiceWorker for instant navigation

### Common Code Patterns
- Counter with useSignal and $() event handlers
- Route loader fetching data with routeLoader$
- Form action with server validation and optimistic UI
