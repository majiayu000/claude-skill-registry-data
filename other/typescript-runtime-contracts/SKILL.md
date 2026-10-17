---
name: typescript-runtime-contracts
description: DEPRECATED for new standalone React/TypeScript work; use react-agent-skills / typescript-runtime-contracts instead. Select only to maintain existing work during the deprecation window. Use when untrusted JSON, HTTP responses, environment values, browser storage, or dynamic JavaScript enters typed TypeScript code.
license: MIT
---

# TypeScript Runtime Contracts

## Purpose
Keep compile-time declarations and runtime truth separate. Validate untrusted data at the boundary before application code treats it as trusted.

## Activate when
- consuming HTTP or JSON responses;
- parsing environment variables or storage;
- processing dynamic JavaScript values;
- adding schemas or serialization contracts.

## Repository inspection
Inspect transport clients, existing validation libraries, generated types, error normalization, retry behavior, and current validation boundaries.

## Decision rules
- unknown is the default type for untrusted values.
- Validate once at a deliberate boundary, then pass narrowed domain data inward.
- Keep validation failures distinct from transport failures.
- Avoid duplicating the same schema in every consumer.
- Keep schema/version ownership explicit.
- Redact sensitive values before logging malformed payloads.

## Implementation procedure
1. Locate the trust boundary.
2. Define the accepted runtime shape.
3. Parse and validate.
4. Normalize transport representation where appropriate.
5. Test malformed, missing, extra, and version-drift input.
6. Keep validation failures safe and actionable.

## Anti-patterns / failure modes
- asserting a response is correct without validation;
- trusting generated types as proof of runtime data;
- validation scattered across unrelated UI components;
- logging full invalid responses containing secrets.

## Reference example

Type-checked with `tsc --strict` (plus `noUncheckedIndexedAccess` and `exactOptionalPropertyTypes`).

```ts
// Types vanish at runtime: data from the network is `unknown` until checked.
export type User = { id: string; email: string; roles: readonly string[] };

export type Result<T> = { ok: true; value: T } | { ok: false; error: string };

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

export function parseUser(input: unknown): Result<User> {
  if (!isRecord(input)) return { ok: false, error: "expected an object" };
  const { id, email, roles } = input;
  if (typeof id !== "string" || id === "") return { ok: false, error: "id must be a non-empty string" };
  if (typeof email !== "string" || !email.includes("@")) return { ok: false, error: "email is invalid" };
  if (!Array.isArray(roles) || !roles.every((role) => typeof role === "string")) {
    return { ok: false, error: "roles must be strings" };
  }
  return { ok: true, value: { id, email, roles } };
}

export async function fetchUser(id: string): Promise<Result<User>> {
  const response = await fetch(`/api/users/${encodeURIComponent(id)}`);
  if (!response.ok) return { ok: false, error: `HTTP ${response.status}` };
  return parseUser(await response.json());
}
```

## Agent review checklist
- Is the trust boundary explicit?
- Is external input validated before narrowing?
- Are validation and transport failures distinguishable?
- Are malformed and version-drift cases tested safely?

## Verification
Exercise malformed payloads and schema drift as well as successful input. Verify caller behavior after validation failures.

## Source foundation
- TypeScript Handbook: https://www.typescriptlang.org/docs/handbook/intro.html
- Fetch API: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
