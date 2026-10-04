---
name: diagnose
description: Structured 6-phase debugging. Build feedback loop first, reproduce deterministically, hypothesize with ranked falsifiable theories, instrument one variable at a time, fix with regression test, cleanup. Use when a bug exists, tests fail unexpectedly, or behavior is wrong and cause is unknown.
mcp: codebase-memory-mcp
---

# /supergraph:diagnose

Systematic debugging. Never guess and patch — build a feedback loop, prove the hypothesis, fix once.

Announce: "🐛 /supergraph:diagnose — building feedback loop..."

## Setup

**Read `.supergraph-env` for test/lint commands (if exists):**
```bash
[ -f .supergraph-env ] && source .supergraph-env
```
This sets `$TEST_CMD`, `$FOCUSED_TEST_CMD`, `$LINT_CMD`. If absent, detect from project config (package.json → jest/vitest, pubspec.yaml → flutter test, etc.) same as `/supergraph:scan`.

## Phases

### Phase 1 — Build Feedback Loop

Before touching any code, establish a fast, deterministic way to observe the bug.

```bash
# Identify the smallest command that shows the failure
$TEST_CMD --grep "<failing test name>"   # focused test run
# or
<minimal repro command>
```

**Goal:** failure visible in < 5 seconds. If not, slim down the repro.
Do NOT skip this phase. Debugging without a feedback loop is guessing.

### Phase 2 — Reproduce Cleanly

- Run the feedback loop 3 times — confirm it fails consistently
- Capture exact error output, stack trace, exit code
- Note any flakiness → treat as separate bug before continuing
- Add a failing regression test if one doesn't exist:
  ```
  test("<bug description>", () => { ... }) // RED
  ```

### Phase 3 — Hypothesize (3-5 ranked theories)

List falsifiable hypotheses, ordered most-to-least likely:

```
1. [Most likely] — [reason] — [how to falsify]
2. [Second]      — [reason] — [how to falsify]
3. [Third]       — [reason] — [how to falsify]
```

Rules:
- Each hypothesis must be falsifiable (observable test to disprove it)
- No implementation yet — only theories
- Use graph context if available:
  ```
  search_graph(project=CBM_PROJECT, name_pattern=<suspect>)
  trace_path(project=CBM_PROJECT, direction="inbound")
  trace_path(project=CBM_PROJECT, direction="outbound")
  ```

### Phase 4 — Instrument (one variable at a time)

Test hypothesis #1 first. Change ONE thing to observe ONE signal:

- Add targeted log/assertion near the suspect code
- Run feedback loop → confirm or refute
- Remove instrumentation after each test — never accumulate debug logs
- If refuted → move to hypothesis #2
- Stop when hypothesis is confirmed

**Rule:** Never change the code under test and the instrumentation simultaneously.

### Phase 5 — Fix + Regression Test

Once root cause is confirmed:

1. Write/update the regression test first (stays RED)
2. Apply minimal fix
3. Run feedback loop → GREEN
4. Run full test suite → no regressions
5. Run lint: `$LINT_CMD`

Minimal fix means: fix the cause, not the symptom. If the fix touches a hub node → get user approval first.
If search/trace returns empty, label graph evidence unavailable and fall back to
Serena/filesystem evidence. Use the validated `test-gaps` recipe for missing tests.

### Phase 6 — Cleanup + Post-mortem

- Remove all debug instrumentation and temp files
- Update CONTEXT.md if bug revealed a hidden domain invariant
- One-sentence post-mortem:
  ```
  Root cause: [X]
  Fix: [Y]
  Prevented recurrence by: [regression test / invariant documented]
  ```
- Checkpoint:
  ```bash
  git add [exact files]
  git commit -m "fix: <description>"
  ```

## Report

```
✅ /supergraph:diagnose complete
- Root cause: [confirmed hypothesis]
- Fix: [what changed]
- Regression test: [test name / path]
- Tests: PASS | Lint: PASS
- Next: /supergraph:fix (if more issues) or /supergraph:verify
```

## Rules

- Never skip Phase 1 — feedback loop is mandatory
- Never change two variables simultaneously in Phase 4
- Never commit without a regression test
- If hypotheses exhausted with no match → stop, report to user with all observations
