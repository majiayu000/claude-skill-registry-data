---
name: react-data-fetching
description: DEPRECATED for new standalone React/TypeScript work; use react-agent-skills / react-data-fetching instead. Select only to maintain existing work during the deprecation window. Use for React server-state fetching, caching, mutations, optimistic updates, loading states, and request races.
license: MIT
---

# React Data Fetching

## Purpose
Separate server state from local UI state and make request identity, freshness, error behavior, cancellation, and mutation consistency explicit.

## Activate when
- adding API calls to React;
- introducing query or cache infrastructure;
- implementing mutations or optimistic updates;
- fixing duplicate, stale, or racing requests.

## Repository inspection
Inspect the existing HTTP client, query/cache library, cache-key conventions, authentication context, retry policy, error model, and test utilities.

## Decision rules
- Prefer repository-standard fetching infrastructure.
- Treat query keys as cache identity.
- Make freshness and invalidation explicit when current data matters.
- Cancel or ignore obsolete requests when ordering matters.
- Optimistic updates require a rollback path.
- Distinguish loading, refreshing, error, empty, and success states.
- Never use cached UI state as authorization evidence.

## Implementation procedure
1. Identify query identity and owner.
2. Define freshness and invalidation.
3. Define error and retry behavior.
4. Define mutation consistency and rollback.
5. Add race and cache-invalidation tests.
6. Verify authentication and tenant context at the network boundary.

## Anti-patterns / failure modes
- one cache key for unrelated parameterized resources;
- automatic retries for non-idempotent mutations;
- optimistic UI without rollback;
- duplicated fetching logic in leaf components;
- server state placed in global UI context only for reachability.

## Reference example

Type-checked with `tsc --strict` (plus `noUncheckedIndexedAccess` and `exactOptionalPropertyTypes`).

```tsx
import { useEffect, useState } from "react";

type Order = { id: string; status: "pending" | "paid" };
type OrderState =
  | { kind: "loading" }
  | { kind: "error"; message: string }
  | { kind: "success"; order: Order };

// Cache identity includes every resource dimension: tenant and order id.
export const orderKey = (tenantId: string, orderId: string) => ["tenant", tenantId, "order", orderId] as const;

export function useOrder(tenantId: string, orderId: string): OrderState {
  const [state, setState] = useState<OrderState>({ kind: "loading" });

  useEffect(() => {
    const controller = new AbortController();
    setState({ kind: "loading" });
    fetch(`/api/tenants/${tenantId}/orders/${orderId}`, { signal: controller.signal })
      .then(async (response) => {
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return (await response.json()) as Order;
      })
      .then((order) => setState({ kind: "success", order }))
      .catch((error: unknown) => {
        // A superseded request must not overwrite newer state.
        if (controller.signal.aborted) return;
        setState({ kind: "error", message: error instanceof Error ? error.message : "Request failed" });
      });
    return () => controller.abort();
  }, [tenantId, orderId]);

  return state;
}

// Optimistic update with an explicit rollback path.
export async function markPaid(
  current: Order,
  apply: (order: Order) => void,
  send: (id: string) => Promise<Response>
): Promise<void> {
  apply({ ...current, status: "paid" });
  const response = await send(current.id).catch(() => undefined);
  if (!response?.ok) apply(current);
}
```

## Agent review checklist
- Is server-state ownership separate from local UI state?
- Do cache keys include every resource-identity dimension?
- Are retries and mutations safe for their semantics?
- Is rollback or reconciliation explicit for optimistic updates?

## Verification
Test initial load, refetch, failure, cancellation, cache hit, invalidation, mutation success, and mutation failure.

## Source foundation
- React Learn: https://react.dev/learn
- Fetch API: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
