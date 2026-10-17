---
name: typescript-type-design
description: DEPRECATED for new standalone React/TypeScript work; use react-agent-skills / typescript-type-design instead. Select only to maintain existing work during the deprecation window. Use when modeling TypeScript domain states, discriminated unions, generics, branded identifiers, utility types, or public APIs.
license: MIT
---

# TypeScript Type Design

## Purpose
Design types that express domain invariants and API contracts without turning the type system into accidental architecture.

## Activate when
- a feature needs new domain types;
- boolean flags create invalid combinations;
- a library exposes reusable generic types;
- structurally identical primitives need stronger distinctions.

## Repository inspection
Inspect existing exported types, naming, strict null checks, generated API types, utility-type conventions, and package ownership.

## Decision rules
- Model mutually exclusive states as discriminated unions.
- Use branded or opaque-style types only where mixing primitives is materially risky.
- Use generics when a real relationship must be preserved across inputs and outputs.
- Prefer narrow object types over catch-all records when keys are known.
- Derive small variants from stable source types instead of duplicating large shapes.
- Separate transport and domain types when their lifecycle or ownership differs.

## Implementation procedure
1. Write the valid-state table.
2. Identify discriminants and shared fields.
3. Separate transport, domain, and UI representations where useful.
4. Make nullability explicit.
5. Add compile-time contract examples for critical exports.
6. Add runtime tests where external data can violate the declared type.

## Anti-patterns / failure modes
- overlapping union members;
- Partial used as a domain model;
- branded types propagated without a concrete risk;
- generic abstractions that hide the real API;
- assuming a type declaration validates runtime data.

## Reference example

Type-checked with `tsc --strict` (plus `noUncheckedIndexedAccess` and `exactOptionalPropertyTypes`).

```ts
// Branded identifiers: an OrderId cannot be passed where a CustomerId is expected.
declare const brand: unique symbol;
type Brand<T, B extends string> = T & { readonly [brand]: B };
export type OrderId = Brand<string, "OrderId">;
export type CustomerId = Brand<string, "CustomerId">;

export const orderId = (value: string): OrderId => value as OrderId;
export const customerId = (value: string): CustomerId => value as CustomerId;

// Model states so invalid combinations cannot be constructed.
export type Payment =
  | { state: "unpaid"; orderId: OrderId }
  | { state: "paid"; orderId: OrderId; paidAt: Date }
  | { state: "refunded"; orderId: OrderId; paidAt: Date; refundedAt: Date };

export function refund(payment: Extract<Payment, { state: "paid" }>, at: Date): Payment {
  return { state: "refunded", orderId: payment.orderId, paidAt: payment.paidAt, refundedAt: at };
}

export function loadOrder(id: OrderId, owner: CustomerId): string {
  return `${owner}/${id}`;
}
// loadOrder(customerId("c1"), orderId("o1")); // compile error: arguments swapped
```

## Agent review checklist
- Are invalid states unrepresentable where practical?
- Do generics express real relationships?
- Are transport and domain types separated where needed?
- Could the same contract be simpler without losing safety?

## Verification
Use typecheck-focused tests, exported API compilation checks, and runtime boundary tests for serialized or user-controlled data.

## Source foundation
- TypeScript Narrowing: https://www.typescriptlang.org/docs/handbook/2/narrowing.html
- TypeScript Generics: https://www.typescriptlang.org/docs/handbook/2/generics.html
