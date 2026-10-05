---
name: typescript
description: Use when writing or hardening TypeScript in strict mode. Covers advanced types, discriminated unions, runtime validation at trust boundaries, generics, and removing `any` from an existing codebase.
metadata:
  category: languages
  version: 1.0.0
  tags: [typescript, types, strict, zod, generics]
---

# TypeScript

## Purpose

Use the type system to make invalid states unrepresentable. This skill covers strict-mode TypeScript, the advanced type features worth reaching for, and the discipline of validating untrusted data exactly once — at the boundary.

## When to Use

- Starting a TypeScript project or tightening `tsconfig.json`.
- Removing `any` and unchecked casts from an existing codebase.
- Modeling a domain with discriminated unions and exhaustive matching.
- Writing a typed API client or SDK.
- Debugging inference failures in generic code.

## Capabilities

- Strict compiler configuration and incremental adoption paths.
- Discriminated unions, template literal types, conditional and mapped types.
- Generic constraints, inference control, and `satisfies`.
- Runtime schema validation with Zod, wired to inferred static types.
- Type-safe error handling with `Result`-style unions.

## Inputs

- Source files and the current `tsconfig.json`.
- Runtime target (Node, browser, edge, Deno, Bun).
- External data shapes: API responses, environment variables, user input.

## Outputs

- Source that compiles under `strict: true` with zero `any`.
- Schemas for every trust boundary, with static types derived from them.
- A `tsconfig.json` reflecting the target runtime.

## Workflow

1. **Set the gate** — Enable `strict`, `noUncheckedIndexedAccess`, and `exactOptionalPropertyTypes`. Everything else follows from the compiler's complaints.
2. **Type the boundaries** — Define schemas for every input that crosses into your program: HTTP payloads, env vars, config files, message queues.
3. **Model the domain** — Replace boolean flags and optional grab-bags with discriminated unions.
4. **Implement inward** — Internal code trusts its types because the boundary already validated them.
5. **Verify** — `tsc --noEmit` and lint with `@typescript-eslint`, `no-explicit-any` set to error.

## Best Practices

- Never use `as` to silence the compiler. It is an assertion, not a check; it lies at runtime.
- Prefer `unknown` over `any` at every boundary, then narrow.
- Derive types from schemas (`z.infer`), never maintain both by hand.
- Use `satisfies` to validate an object literal against a type while preserving its narrow inferred type.
- Add an exhaustiveness check (`never`) to every union switch — it turns a future missing case into a compile error.
- Do not export types you do not intend to support. A public type is an API contract.

## Examples

**Boundary validation with derived types:**

```ts
import { z } from "zod";

const Config = z.object({
  port: z.coerce.number().int().positive(),
  databaseUrl: z.string().url(),
  logLevel: z.enum(["debug", "info", "warn", "error"]).default("info"),
});

export type Config = z.infer<typeof Config>;

export function loadConfig(env: NodeJS.ProcessEnv): Config {
  const parsed = Config.safeParse({
    port: env.PORT,
    databaseUrl: env.DATABASE_URL,
    logLevel: env.LOG_LEVEL,
  });
  if (!parsed.success) {
    throw new Error(`Invalid configuration:\n${parsed.error.message}`);
  }
  return parsed.data;
}
```

**Exhaustive discriminated union:**

```ts
type Job =
  | { status: "queued"; queuedAt: Date }
  | { status: "running"; startedAt: Date; workerId: string }
  | { status: "failed"; error: string; attempts: number };

function describe(job: Job): string {
  switch (job.status) {
    case "queued":
      return `Queued at ${job.queuedAt.toISOString()}`;
    case "running":
      return `Running on ${job.workerId}`;
    case "failed":
      return `Failed after ${job.attempts} attempts: ${job.error}`;
    default: {
      const unreachable: never = job;
      throw new Error(`Unhandled job status: ${JSON.stringify(unreachable)}`);
    }
  }
}
```

## Notes

- `noUncheckedIndexedAccess` is the single highest-value flag most codebases are missing: it makes `arr[i]` return `T | undefined`, which is the truth.
- Declaration files (`.d.ts`) from `DefinitelyTyped` are frequently wrong. Verify against runtime behavior before trusting them.
- Type-level programming is a cost. If a conditional type takes more than a minute to read, prefer a simpler runtime check.
