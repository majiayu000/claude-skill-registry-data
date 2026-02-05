---
name: route-transition-tracking
description: Measure time from navigation to page fully loaded and interactive. Use when tracking SPA navigation, route changes, or slow page transitions.
triggers:
  - "route transition"
  - "page navigation"
  - "slow page load"
  - "SPA navigation"
  - "track route changes"
  - "navigation performance"
priority: 2
---

# Route Transition Tracking

Time from navigation start to destination page interactive.

## Phases

```
CLICK/NAV → ROUTE_CHANGE → DATA_FETCH → RENDER → INTERACTIVE
           |_______________________________________________|
                        Route Transition Time
```

## When to Use

- Tab/menu navigation
- Link clicks within SPA
- Programmatic navigation
- Back/forward browser buttons
- Deep links

## Key Thresholds

| Rating | Duration |
|--------|----------|
| Good | <400ms |
| Acceptable | <1s |
| Poor | >1s |

## React Router

```typescript
import { useLocation, useNavigationType } from 'react-router-dom';
import { useEffect, useRef } from 'react';

function RouteTracker() {
  const location = useLocation();
  const navigationType = useNavigationType();
  const navigationStart = useRef<number>();

  useEffect(() => {
    navigationStart.current = performance.now();
  }, [location.pathname]);

  useEffect(() => {
    // Called after render completes
    if (navigationStart.current) {
      const duration = performance.now() - navigationStart.current;
      trackRouteTransition({
        from: document.referrer,
        to: location.pathname,
        duration_ms: duration,
        navigation_type: navigationType, // 'PUSH', 'POP', 'REPLACE'
      });
    }
  });

  return null;
}
```

## Next.js App Router

```typescript
// app/providers.tsx
'use client';

import { usePathname, useSearchParams } from 'next/navigation';
import { useEffect, useRef } from 'react';

export function RouteChangeTracker() {
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const startTime = useRef<number>();
  const previousPath = useRef<string>();

  useEffect(() => {
    startTime.current = performance.now();
  }, [pathname, searchParams]);

  useEffect(() => {
    if (startTime.current && previousPath.current) {
      const duration = performance.now() - startTime.current;
      trackRouteTransition({
        from: previousPath.current,
        to: pathname,
        duration_ms: duration,
        has_search_params: searchParams.toString().length > 0,
      });
    }
    previousPath.current = pathname;
  });

  return null;
}
```

## Vue Router

```typescript
// plugins/route-tracking.ts
import { watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';

export function useRouteTracking() {
  const router = useRouter();
  const route = useRoute();
  let navigationStart: number;

  router.beforeEach((to, from) => {
    navigationStart = performance.now();
  });

  router.afterEach((to, from) => {
    // Wait for next tick to ensure render complete
    nextTick(() => {
      const duration = performance.now() - navigationStart;
      trackRouteTransition({
        from: from.path,
        to: to.path,
        duration_ms: duration,
        route_name: to.name as string,
      });
    });
  });
}
```

## SvelteKit

```typescript
// src/routes/+layout.svelte
<script lang="ts">
  import { page, navigating } from '$app/stores';
  import { onMount } from 'svelte';

  let navigationStart: number;

  $: if ($navigating) {
    navigationStart = performance.now();
  }

  $: if (!$navigating && navigationStart) {
    const duration = performance.now() - navigationStart;
    trackRouteTransition({
      to: $page.url.pathname,
      duration_ms: duration,
      route_id: $page.route.id,
    });
  }
</script>
```

## Nuxt

```typescript
// plugins/route-tracking.client.ts
export default defineNuxtPlugin((nuxtApp) => {
  let navigationStart: number;

  nuxtApp.hook('page:start', () => {
    navigationStart = performance.now();
  });

  nuxtApp.hook('page:finish', () => {
    const route = useRoute();
    const duration = performance.now() - navigationStart;
    trackRouteTransition({
      to: route.path,
      duration_ms: duration,
      route_name: route.name as string,
    });
  });
});
```

## With Data Loading

Track data fetching as part of transition:

```typescript
function ProductPage() {
  const { data, isLoading } = useQuery(['product', id], fetchProduct);
  const renderStart = useRef(performance.now());

  useEffect(() => {
    if (!isLoading && data) {
      trackRouteTransition({
        route: `/products/${id}`,
        total_duration_ms: performance.now() - renderStart.current,
        data_fetch_complete: true,
      });
    }
  }, [isLoading, data]);

  // ...
}
```

## Common Mistakes

- Measuring only route change (missing data load)
- Not distinguishing warm vs cold loads
- Ignoring prefetched routes (artificially fast)
- Missing back/forward navigation
- Not tracking by route pattern (aggregate hides issues)

## Related Skills

- See `skills/core-web-vitals` for LCP during navigation
- See `skills/hydration-performance` for SSR page loads
- See `skills/api-tracing` for data fetch timing
- See `skills/user-journey-tracking` for correlating with user intent

## References

- `references/ui-performance.md` - Navigation performance patterns
- `references/frameworks/*.md` - Framework-specific routing
