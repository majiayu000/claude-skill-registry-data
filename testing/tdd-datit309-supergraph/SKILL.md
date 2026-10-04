---
name: tdd
description: Strict test-driven development for behavior changes. Requires verified RED before production code, minimal GREEN, and refactor only after passing tests.
mcp: codebase-memory-mcp
---

# /supergraph:tdd

Requires healthy `index_status` for `CBM_PROJECT` (see `references/codebase-memory-contract.md` with `codebase-memory-mcp`); if stale/degraded → `index_repository` before graph calls.

Strict TDD for features, bug fixes, refactors.

**Iron Law:** `NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST`

**Delete means delete:** Production code written before verified failing test → delete and restart from RED.

## When

**Full TDD:** new features, behavior changes, refactoring.
**Fast TDD:** bug fixes (add regression test → RED verify → minimal fix).
**Ask to skip:** config-only, generated code, throwaway prototype, docs-only.

## State Machine (in order, never skip)

`needs_test` → `red_verified` → `green_verified` → `refactor_allowed` → `complete`

## Steps

### 0. Announce
"🔴 /supergraph:tdd — TDD: [full|fast] for [behavior]..."

### 1. Identify One Behavior
```
Behavior: [single externally visible behavior]
Test file: [path] | Test name: [name]
Command: [focused test command]
Expected RED: [why it should fail before implementation]
```

**One behavior per test. Public behavior, not internals. Real code over mocks.**

For a falsifiability checklist, read [`writing-good-tests.md`](writing-good-tests.md) before finalizing a test.

### 2. 🔴 RED — Write + Verify in One Round

Write one failing test, then run immediately:

```bash
<write test> && $TEST_CMD <focused command>
```

Valid 🔴 RED: fails **for the expected missing behavior**, not syntax/import/typo.

Record evidence:
```markdown
## TDD Evidence — 🔴 RED
- 🔴 RED: `[command]` → FAIL ([expected missing behavior])
```

**Serena diagnostics (optional):** See `serena/SKILL.md:Setup` — `get_diagnostics_for_file` before/after GREEN; use `replace_symbol_body`/`rename_symbol` over raw edits. Skip if `SERENA_ACTIVE=false` or unavailable.

Invalid RED → fix test setup, don't write production code yet.

### 3. 🟢 GREEN — Minimal Implementation

Write only enough code to pass the test. No abstractions, no cleanup, no extra features.

Delete any production code written before RED.

### 4. 🟢 GREEN Verify

Run focused test → broader suite:
```markdown
## TDD Evidence — 🟢 GREEN
- 🟢 GREEN: `[command]` → PASS
- Suite: PASS
```

Failing test → fix code, not test. Other tests fail → fix now.

### 5. REFACTOR — Only After 🟢 GREEN

Rename, deduplicate, extract. No behavior changes. Re-run tests.

### 6. Complete

Before marking complete:
```markdown
## TDD Complete
- Behavior: [behavior]
- Mode: full|fast
- RED verified: yes | GREEN verified: yes | Refactor: yes|none
- Tests: PASS
```

### 7. Report

Per behavior: `✅ /supergraph:tdd — behavior N: [brief]`

Final:
```
✅ /supergraph:tdd complete
- Behaviors: N | Mode: full|fast | Tests: PASS | Lint: PASS
- Next: /supergraph:fix → /supergraph:verify → /supergraph:review
```

## Fast TDD Path (Bug Fixes)

For bugs, skip full TDD ceremony:
1. Write **one regression test** that reproduces the bug
2. Verify it fails (RED) — the bug is proved
3. Write **minimal fix only** (GREEN)
4. Verify test passes — bug is fixed
5. No REFACTOR needed unless specified

## Plan Integration

Plans must include TDD metadata per behavior task:
```markdown
TDD:
- Behavior: [single behavior] | Test file: [path] | Test name: [name]
- RED command: `[focused test command]` | Expected RED failure: [missing behavior]
- Minimal GREEN change: [smallest implementation] | Mocking: none | [why unavoidable]
```

## Executor Enforcement
- No production edits before `red_verified`
- Stop if RED passes immediately or fails for wrong reason
- Allow implementation only after valid RED, refactor only after GREEN

## Review Triggers — Reject When
- Tests after implementation | No RED evidence | RED passed immediately | RED failed for wrong reason
- Implementation exceeds tested behavior | Bug fix lacks regression test
- Tests assert internals | Mocks hide integration risk

## Anti-Patterns — Stop & Return to RED

| Symptom | Fix |
|---|---|
| Production code before failing test | Delete, start RED |
| Tests after implementation | Next behavior test-first, remove untested code |
| "Too small to test" | Write one-liner test |
| Immediate pass accepted as RED | Test is wrong — revise |
| Pre-written implementation kept as reference | Delete, start fresh |
| Over-building before tests need it | YAGNI — remove |

### Mock Gate — Answer Before Mocking
1. What behavior is under test?
2. Is this mock isolating an external, slow, or flaky boundary?
3. What side effects does the real dependency provide?
4. Would this test fail if real behavior broke?

**Reject tests that only prove mocks exist or were called.**
