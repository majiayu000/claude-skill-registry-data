---
name: analyze-code-quality
description: Run all available tests and linters, check for anti-patterns, and generate a comprehensive code quality report
allowed-tools: Read, Grep, Glob, Bash, Agent
---

Analyze the overall quality of the apple-fm source. Generate a comprehensive
report.

## Steps

1. **Run unit tests with coverage**
   ```
   npm test
   ```
   Report total tests, pass/fail, and coverage per file. The thresholds in
   `vitest.config.ts` (statements 80 / branches 75 / functions 80 / lines 80) are
   the floor; flag any file that drags the suite under them. `cli.ts` and
   `repl.ts` are intentionally excluded (thin I/O) — confirm they have no
   testable logic that crept in.

   **Coverage is a floor, not a ceiling.** A line/branch/function/statement
   percentage only proves each line *ran* during the suite — it says nothing about
   whether the right *behavior* was asserted, or whether *sequences of operations
   across internal state boundaries* were exercised. A module can sit at 100% on
   every metric and still ship basic bugs, because every operation was tested once
   from a clean initial state while the transitions *between* states were never
   tried. So treat high coverage as the **trigger** for the behavioral /
   state-transition audit (step 6) — not as a stopping point. Never report a
   coverage number as if it were a proof of correctness.

2. **Run the linter**
   ```
   npm run lint
   ```
   Report errors/warnings grouped by rule.

3. **Run typecheck**
   ```
   npm run typecheck
   ```
   Report any type errors.

4. **Build the helper (best-effort)**
   ```
   npm run build:helper
   ```
   On a macOS 26 machine this should emit `bin/apple-fm-helper`. On other
   machines the script no-ops with exit 0 by design — note which happened. If it
   built, run `bin/apple-fm-helper --probe` and report the availability line.

5. **Check anti-patterns** (conventions from `CLAUDE.md`):
   - **Relative imports missing `.js`** — grep `src/`/`tests/` for relative
     imports without a `.js` suffix.
   - **`any` leaks** — grep `src/` for `: any\b`, `as any\b`, `<any>`. The house
     style is `unknown` + a narrowing check.
   - **Truthy string checks** — `strict-boolean-expressions` is on; flag any
     `if (someString)` style test (use `=== undefined` / `.length`).
   - **Runtime dependencies** — `package.json` `dependencies` must stay empty
     (the Node layer only spawns the helper). Flag any addition.
   - **Node imports the model directly** — only the Swift helper (any `.swift`
     file under `apple-fm-helper/`, currently `main.swift`, `GuidedGeneration.swift`,
     and `Tools.swift`) may reference `FoundationModels`. Grep `src/` for
     `FoundationModels` (should be zero hits outside comments).
   - **Protocol drift** — `tests/fixtures/stub-helper.js` must still implement the
     same events as `docs/4-protocol.md` and the Swift helper.
   - **File length** — flag any `src/*.ts` over ~200 LOC; prefer splitting.

6. **Behavioral / state-transition audit** (the part coverage % can't see)

   Static checks and a coverage number verify that lines *ran*; they cannot tell
   you a *behavior* or a *transition between internal states* is missing. This step
   hunts exactly those gaps.

   **6a. Identify the stateful modules.** A module is "stateful" if its behavior
   depends on something that persists or changes *between* calls, not just on the
   current arguments. Heuristics — flag any module that has:
   - multiple code paths keyed on an internal mode / flag / phase field,
   - an explicit state machine or lifecycle (create → use → tear down → recreate),
   - a cache with hit/miss/fallback paths, or lazy init / respawn on failure,
   - accumulated history that is later mutated, summarized, evicted, or reset.

   In apple-fm the prime suspects are:
   - **`src/liveSession.ts`** (`LiveSession`) — the long-lived
     `apple-fm-helper --session` process: **no-process → spawned → busy → dead →
     lazy respawn**, with id-correlated in-flight commands. Transitions: first
     command spawns; a crash mid-command must reject *that* command and respawn on
     the *next*; overlapping/out-of-order command ids; dispose while busy.
   - **`src/session.ts`** (`ChatSession`) — multi-turn history with automatic
     compaction: **below `compactAtTokens` → over threshold → summarize older turns,
     keep `keepRecentTurns` verbatim → continue appending**. Transitions: cross the
     threshold exactly once vs. repeatedly; a summary that itself pushes back over
     threshold; empty history then refill; compaction interleaved with new turns.
   - **`src/tools/permissions.ts`** (`PermissionPolicy`) and
     **`src/tools/registry.ts`** (`ToolRegistry`) — per-call mode + remembered
     allow/deny decisions accumulating across calls.

   **6b. For each, build a small state/transition map** — list the states and the
   legal (and illegal) transitions between them. This is quick prose or a table,
   not a formal FSM.

   **6c. Check the tests against the *transitions*, not the operations.** Read the
   corresponding test file and ask: does it only ever drive each operation *once,
   from a clean initial state*? Or does it exercise multi-step **sequences that
   cross state boundaries**? Concretely, look for tests that try:
   - **out-of-order** — a teardown/late operation before the setup that "should"
     precede it (e.g. respond to a command after the process died),
   - **interleaved** — two flows in flight at once (overlapping command ids, a new
     turn arriving mid-compaction),
   - **repeated** — the same transition twice (compact, then compact again; respawn
     after a second crash),
   - **empty-then-refill** — drain to empty, then add again (history cleared then
     regrown; registry emptied then repopulated).

   **6d. Flag and recommend.** For every stateful module whose tests only cover
   single-operation-from-clean-state, flag it — **even if its line/branch coverage
   is 100%** — and recommend an *adversarial transition-matrix test*: enumerate the
   states on both axes and assert the behavior of each state→state move, including
   the illegal ones. Give the concrete example sequences from 6c so the follow-up
   is actionable. File these as `hs-task`/`hs-bug` tickets.

7. **Check the build shape**
   ```
   npm run build && ls dist/
   ```
   Verify `dist/index.js`, `dist/cli.js`, and their `.d.ts` files exist, and that
   `dist/cli.js` keeps its `#!/usr/bin/env node` shebang.

## Report Format

- **Summary**: tests pass/fail, coverage %, lint clean, typecheck clean, helper
  build outcome (built / skipped-by-guard). State the coverage number *with* the
  reminder that it is a floor, not a proof of behavioral correctness.
- **Coverage**: per-file table, highlighting anything under threshold.
- **Behavioral / State-Transition Assessment**: **required, not optional** — one
  row per stateful module (`liveSession.ts`, `session.ts`, `permissions.ts`,
  `registry.ts`, plus any others found in 6a) with: its states, whether the tests
  exercise transitions vs. only single-operation-from-clean-state, and a
  transition-coverage verdict (Covered / Partial / **Untested-transitions**). This
  section must be able to flag a module as having untested transitions **even when
  its line/branch coverage is 100%**. For each flagged module, give the concrete
  adversarial sequences to add.
- **Lint / Type issues**: grouped.
- **Anti-Pattern Violations**: file + line, severity, one-line fix.
- **Build Shape**: pass/fail per check.
- **Recommendations**: prioritized. File Hot Sheet tickets (`hs-task`/`hs-bug`)
  for non-trivial findings.
