---
name: check-code-hygiene
description: Check code for standardization, readability, maintenance complexity, and defensive coding practices
allowed-tools: Read, Grep, Glob, Bash, Agent
---

Analyze the apple-fm codebase for code hygiene issues. Generate a report on
standardization, readability, maintenance complexity, and defensive coding.

Scope: `src/`, `apple-fm-helper/main.swift`, and (where relevant) `tests/`.

## Analysis Areas

### 1. Standardization
- **File naming**: `src/` is lowercase/camelCase matching the primary concept
  (`cliArgs.ts`, `protocol.ts`, `session.ts`). Flag a name that matches neither.
- **Identifier casing**: camelCase values, PascalCase types, SCREAMING_SNAKE
  constants. Flag inconsistencies.
- **Import style**: all relative imports use `.js`; `import type` for type-only
  imports (eslint enforces order — if lint passes, order is fine). The `.js`
  check is your responsibility.
- **Error messages**: throws should be descriptive and actionable (e.g.
  `--temp expects a number, got "abc"`). Flag terse `throw new Error('failed')`.
- **Protocol parity**: the event names / error codes in `src/protocol.ts`,
  `apple-fm-helper/main.swift`, `tests/fixtures/stub-helper.js`, and
  `docs/4-protocol.md` must all agree. Flag any divergence.

### 2. Readability
- **File length**: flag any `src/*.ts` over ~200 LOC.
- **Function length / nesting**: flag functions over ~50 lines or nesting deeper
  than 3.
- **Magic numbers**: defaults like the compaction threshold, keep-recent count,
  timeout, and chars-per-token live as named constants — flag any new inline
  literal that should be one.
- **Comments**: house style is *why*, not *what*. Flag both noise comments and
  missing rationale on non-obvious code (e.g. the cumulative-partial diffing in
  the Swift streaming path).

### 3. Maintenance Complexity
- **Layering**: only `apple-fm-helper/main.swift` may touch `FoundationModels`;
  only `helper.ts` spawns the process; pure logic stays in `protocol.ts` /
  `session.ts` / `cliArgs.ts`. Flag any layer violation (e.g. `session.ts`
  spawning directly instead of going through an injected `GenerateFn`).
- **Dependencies**: `package.json` `dependencies` stays empty. Flag additions.
- **Duplicate patterns**: spot-check with grep for repeated spawn/JSON idioms.

### 4. Defensive Coding
- **Boundary validation**: `parseArgs` rejects unknown commands/flags and bad
  numbers; `parseEvent` throws on malformed lines; `helper.ts` bounds the
  subprocess with a timeout and captures stderr. Verify these still hold.
- **`any` / non-null**: grep `src/` for `: any`, `as any`, `<any>`, and `!`
  non-null assertions (tests get a pass). House style is `unknown` + narrowing.
- **Subprocess safety**: stdin EPIPE swallowed; timeout kills the child; nonzero
  exit surfaces stderr. Flag any regression.
- **Swift helper**: every failure path emits an `error` event (not a bare crash)
  and exits nonzero; availability is checked before generation.

## Report Format

For each finding: **File** (path + lines), **Category**
(standardization | readability | maintenance | defensive), **Severity**
(high | medium | low), **Description**, **Suggestion**.

End with a prioritized top-N (apple-fm is small — expect 0–5 in a healthy state).
Suggest Hot Sheet tickets (`hs-task` for cleanups, `hs-bug` for defects) for
non-trivial findings.
