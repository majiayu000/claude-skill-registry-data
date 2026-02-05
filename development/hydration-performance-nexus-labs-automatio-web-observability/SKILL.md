---
name: hydration-performance
description: Measure SSR hydration timing and issues. Use when tracking hydration performance, debugging hydration mismatches, or optimizing SSR/SSG applications.
triggers:
  - "hydration performance"
  - "hydration timing"
  - "hydration mismatch"
  - "SSR performance"
  - "time to interactive"
  - "server rendering"
priority: 2
---

# Hydration Performance

Measure the transition from server-rendered HTML to interactive client application.

## What is Hydration?

```
Server HTML → JavaScript Load → Hydration → Interactive
              |_______________________________|
                    Hydration Timeline
```

## Key Metrics

| Metric | Description | Good | Poor |
|--------|-------------|------|------|
| **TTH** | Time to Hydration | <1s | >3s |
| **Hydration Duration** | JS execution time | <200ms | >1s |
| **TTI** | Time to Interactive | <3s | >7s |

## Next.js Hydration Tracking

```typescript
// app/providers.tsx
'use client';

import { useEffect, useRef, useState } from 'react';

export function HydrationTracker({ children }: { children: React.ReactNode }) {
  const [isHydrated, setIsHydrated] = useState(false);
  const hydrationStart = useRef<number>();

  useEffect(() => {
    // Component mounted = hydration complete
    const hydrationEnd = performance.now();
    setIsHydrated(true);

    // Get navigation timing
    const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;

    trackHydration({
      hydration_duration_ms: hydrationEnd - (hydrationStart.current || navigation.responseEnd),
      time_to_interactive_ms: hydrationEnd - navigation.fetchStart,
      dom_content_loaded_ms: navigation.domContentLoadedEventEnd - navigation.fetchStart,
      document_complete_ms: navigation.loadEventEnd - navigation.fetchStart,
    });
  }, []);

  // Mark hydration start (runs during SSR, captured in HTML)
  if (typeof window === 'undefined') {
    return children;
  }

  if (!hydrationStart.current) {
    hydrationStart.current = performance.now();
  }

  return children;
}
```

## Nuxt Hydration Tracking

```typescript
// plugins/hydration.client.ts
export default defineNuxtPlugin((nuxtApp) => {
  const hydrationStart = performance.now();

  nuxtApp.hook('app:mounted', () => {
    const hydrationEnd = performance.now();

    trackHydration({
      hydration_duration_ms: hydrationEnd - hydrationStart,
      route: useRoute().path,
    });
  });

  // Track hydration errors
  nuxtApp.hook('app:error', (error) => {
    if (error.message?.includes('hydration')) {
      trackHydrationError({
        error_message: error.message,
        route: useRoute().path,
      });
    }
  });
});
```

## SvelteKit Hydration Tracking

```svelte
<!-- src/routes/+layout.svelte -->
<script lang="ts">
  import { onMount } from 'svelte';
  import { browser } from '$app/environment';
  import { page } from '$app/stores';

  let hydrationStart: number;

  if (browser) {
    hydrationStart = performance.now();
  }

  onMount(() => {
    const hydrationEnd = performance.now();

    trackHydration({
      hydration_duration_ms: hydrationEnd - hydrationStart,
      route: $page.route.id,
    });
  });
</script>

<slot />
```

## Remix Hydration Tracking

```typescript
// app/root.tsx
import { useEffect, useRef } from 'react';
import { useLocation } from '@remix-run/react';

function HydrationTracker() {
  const location = useLocation();
  const hydrationStart = useRef(performance.now());
  const hasTracked = useRef(false);

  useEffect(() => {
    if (!hasTracked.current) {
      const hydrationEnd = performance.now();

      trackHydration({
        hydration_duration_ms: hydrationEnd - hydrationStart.current,
        route: location.pathname,
      });

      hasTracked.current = true;
    }
  }, []);

  return null;
}

export default function App() {
  return (
    <html>
      <head>
        <Meta />
        <Links />
      </head>
      <body>
        <HydrationTracker />
        <Outlet />
        <Scripts />
      </body>
    </html>
  );
}
```

## Hydration Error Tracking

```typescript
// Capture hydration mismatch errors
function setupHydrationErrorTracking() {
  const originalError = console.error;

  console.error = (...args) => {
    const message = args.join(' ');

    // React hydration mismatch
    if (
      message.includes('Hydration failed') ||
      message.includes('Text content does not match') ||
      message.includes('did not match')
    ) {
      captureHydrationError({
        type: 'hydration_mismatch',
        message: message.slice(0, 500),
        route: window.location.pathname,
      });
    }

    originalError.apply(console, args);
  };
}
```

## Partial Hydration (Islands)

For frameworks with partial hydration (Astro, Qwik):

```typescript
// Astro - track island hydration
// src/components/TrackedIsland.astro
---
const componentName = Astro.props.name;
---

<div
  data-island={componentName}
  data-hydration-start={Date.now()}
>
  <slot />
</div>

<script>
  // Track when island becomes interactive
  const islands = document.querySelectorAll('[data-island]');

  islands.forEach((island) => {
    const observer = new MutationObserver(() => {
      const start = parseInt(island.dataset.hydrationStart || '0');
      const duration = Date.now() - start;

      trackIslandHydration({
        island_name: island.dataset.island,
        hydration_duration_ms: duration,
      });

      observer.disconnect();
    });

    observer.observe(island, { childList: true, subtree: true });
  });
</script>
```

## Common Hydration Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Long hydration | Large JS bundle | Code split, lazy load |
| Mismatch errors | Server/client divergence | Use useEffect for client-only |
| Layout shift | Hydration changes DOM | Reserve space, skeleton |
| Slow TTI | Blocking hydration | Progressive/selective hydration |

## Anti-Patterns

- Tracking before hydration (inaccurate timing)
- Missing hydration error capture
- Not tracking by route (aggregate hides issues)
- Ignoring partial hydration opportunities
- Large blocking JS causing slow hydration

## Related Skills

- See `skills/core-web-vitals` for LCP during hydration
- See `skills/bundle-performance` for JS size impact
- See `skills/route-transition-tracking` for navigation after hydration

## References

- `references/frameworks/nextjs.md` - Next.js hydration patterns
- `references/frameworks/nuxt.md` - Nuxt hydration patterns
- `references/performance.md` - Performance budgets
