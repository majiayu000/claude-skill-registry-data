---
name: react-architecture
description: DEPRECATED for new standalone React/TypeScript work; use react-agent-skills / react-architecture instead. Select only to maintain existing work during the deprecation window. Use when designing React application boundaries, feature modules, dependency direction, shared UI infrastructure, and frontend architecture.
license: MIT
---

# React Architecture

## Purpose
Define stable frontend boundaries so features can evolve without turning the UI into a shared mutable dependency graph.

## Activate when
- reorganizing React feature structure;
- introducing shared hooks, contexts, components, or services;
- setting dependency direction between UI, domain, and infrastructure;
- evaluating monolithic component or state structures.

## Repository inspection
Inspect source layout, feature boundaries, import graph, routing, state/query infrastructure, design-system ownership, build tooling, and test boundaries.

## Decision rules
- Keep dependency direction explicit.
- Feature code should depend inward on stable contracts rather than importing arbitrary implementation details from unrelated features.
- Shared modules need a demonstrated reuse boundary; do not create a common folder by default.
- Keep server state, local UI state, and domain transformations distinguishable.
- Avoid barrel exports when they obscure ownership or create cycles.
- Prefer incremental migration over whole-tree restructuring without evidence.

## Implementation procedure
1. Map current dependency edges.
2. Identify the stable ownership boundary.
3. Define public module APIs.
4. Move code in small slices.
5. Add import-cycle and integration checks where tooling permits.
6. Verify affected features after each architectural change.

## Anti-patterns / failure modes
- global context as the default escape hatch;
- cross-feature imports into private implementation files;
- shared utility modules that become dumping grounds;
- architecture-only refactors with no measurable reduction in coupling.

## Reference example

Type-checked with `tsc --strict` (plus `noUncheckedIndexedAccess` and `exactOptionalPropertyTypes`).

```tsx
// features/orders/api.ts, hooks.ts, and OrderTable.tsx shown together.
// Dependency direction: page -> hook -> api client; the table only renders props.
import { useEffect, useState } from "react";

export type OrderRow = { id: string; total: string };

// api.ts: the single place that knows the endpoint and payload shape.
export async function fetchOrders(signal: AbortSignal): Promise<OrderRow[]> {
  const response = await fetch("/api/orders", { signal });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return (await response.json()) as OrderRow[];
}

// hooks.ts: feature-local server state; no global store for one screen.
export function useOrders(): OrderRow[] | undefined {
  const [orders, setOrders] = useState<OrderRow[]>();
  useEffect(() => {
    const controller = new AbortController();
    fetchOrders(controller.signal).then(setOrders).catch(() => undefined);
    return () => controller.abort();
  }, []);
  return orders;
}

// OrderTable.tsx: presentational, testable without network.
export function OrderTable({ orders }: { orders: readonly OrderRow[] }) {
  return (
    <table>
      <tbody>
        {orders.map((order) => (
          <tr key={order.id}>
            <td>{order.id}</td>
            <td>{order.total}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export function OrdersPage() {
  const orders = useOrders();
  return orders ? <OrderTable orders={orders} /> : <p role="status">Loading orders…</p>;
}
```

## Agent review checklist
- Are dependency directions explicit?
- Does shared infrastructure have demonstrated reuse?
- Are server state, local UI state, and domain logic separated?
- Did the change reduce coupling without unnecessary restructuring?

## Verification
Run typecheck, tests, lint, dependency/cycle checks when available, and inspect the final import graph for unintended coupling.

## Source foundation
- React Learn: https://react.dev/learn
- TypeScript Modules: https://www.typescriptlang.org/docs/handbook/2/modules.html
