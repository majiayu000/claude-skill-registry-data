---
name: add-unit-tests
description: Add focused Bun unit tests for mission-critical behavior and edge cases — not blanket coverage.
---

# add-unit-tests

Adds **high-signal** unit tests using the **Bun test runner** (`bun test`). Optimize for correctness on critical paths, invariants, and failure modes — **not** chasing 100% line coverage.

## When to Use

- Implementing or changing logic that must not regress (parsers, validators, hooks, scripts, auth, money, concurrency boundaries)
- Fixing a bug — add a test that fails without the fix
- A PR or quality gate expects test evidence for the touched surface

## When Not to Use

- Purely cosmetic or copy-only changes with no executable behavior
- Integration/E2E suites — use the repo’s existing patterns instead
- Generated code — test the generator or hand-written seams, not every generated line

## Principles

1. **Mission-critical first** — pure functions, validation, state machines, error mapping, JSON envelopes (`ok` / `error`), idempotency, security-sensitive branches.
2. **Edge cases that matter** — empty input, boundary values, malformed data, `null`/`undefined`, duplicate keys, unicode, very large strings **when** the code promises behavior there.
3. **Deterministic tests** — no real network, clock, or filesystem unless the repo already provides fakes; use `mock` / injected dependencies.
4. **Colocate** — `foo.ts` → `foo.test.ts` beside it, or `__tests__/foo.test.ts` if the repo already does that. Match existing layout in the target package.
5. **Strict typing** — no `any` without a `// justification:` comment (harness rules).
6. **No noise** — avoid trivial “it imports” tests; each test should fail for a concrete, plausible mistake.

## Before Writing

1. Read `AGENTS.md` and the sub-repo’s `AGENTS.md` if working under `repos/<name>/`.
2. Find how tests are run: `package.json` scripts and any `bunfig.toml` / Vitest config — default harness expectation is **`bun test`**.
3. Skim the module under test; list **public API**, **invariants**, and **documented edge behavior** to cover.

## Steps

### 1. Pick targets

List 3–8 behaviors worth locking in (happy path + failures + one boundary each). Skip low-value branches.

### 2. Add test file(s)

Use Bun’s built-in `describe` / `test` / `expect` API (Jest-compatible).

```typescript
import { describe, expect, test } from "bun:test";
import { parseEnvelope } from "./envelope.ts";

describe("parseEnvelope", () => {
  test("accepts valid ok envelope", () => {
    const input = JSON.stringify({ ok: true, data: { id: 1 }, error: null });
    expect(parseEnvelope(input)).toEqual({ ok: true, data: { id: 1 }, error: null });
  });

  test("rejects malformed JSON", () => {
    expect(() => parseEnvelope("{")).toThrow();
  });
});
```

### 3. Run the narrow suite, then full suite

```powershell
bun test path/to/module.test.ts
bun test
```

Fix failures before claiming the task is done.

### 4. Gate with typecheck

```powershell
bun run typecheck
```

If the repo defines `bun run lint`, run it too.

### 5. Evidence for Beads / PR

- Note which behaviors are covered (bullet list in PR or `worklog:` comment).
- Do **not** claim “100% coverage”; say **critical paths + listed edge cases**.

## Checklist (self-review)

- [ ] Every new test would catch a real regression or documents an explicit contract
- [ ] No flaky timing or network
- [ ] No `console.log` left in committed tests
- [ ] `bun test` passes; TypeScript strict clean for new code

## Sub-repos (`repos/<name>/`)

Follow that repo’s test runner and conventions if they differ from Bun. Still apply the same **critical-path-first** prioritization.

## Optional references

Put long fixtures or golden files in `references/` only when it keeps tests readable — prefer small inline data for unit tests.
