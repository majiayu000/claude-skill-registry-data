---
name: test-deslop
description: One-shot cleanup of low-signal tests in an existing repo — tests that restate the code, mirror constants, or mock the unit under test, so they pass on bugs and break on refactors. Deletes by default, keeps only tests that catch a named plausible bug nothing else catches, fans out per area, and ends with an inventory table plus prevention rules in the project CLAUDE.md. Use when the user says "test slop", "deslop the tests", "too many useless tests", "prune the test suite", or complains that agent-written tests are brittle or slow.
---

# Test deslop

A test is worth keeping only if it fails against a plausible bug that no other
test catches. Everything else is cost: CI time, refactor friction, agent turns
spent fixing tests instead of features.

## 0. Baseline — before touching anything

- Clean worktree, new branch per area (`git.md`).
- Record: test files, test lines, test count, suite wall time, pass/fail state.
  Run the real command (e.g. `bunx vitest run`); a red baseline is fixed or
  reported first, never cleaned around.
- Map the higher-level coverage that exists **today**: E2E, integration, smoke.
  Name the flows it covers. This map is what deletions lean on.

**No E2E or integration suite → stop the "default delete" rule.** Delete only the
tautological class below, and report the gap. Removing the only guard on a flow
is not cleanup.

## 1. Classify every test

| Verdict | Criterion |
|---|---|
| **delete** | Tautological: restates a literal or constant, mirrors the implementation's logic, mocks the unit under test, snapshots internals, asserts only types or shape, duplicates another test. |
| **delete** | Real assertion, but the bug is caught by a higher-level test that exists now. Name that test. |
| **keep** | Catches a named plausible bug that nothing else catches. Security, money, and data loss first; pure logic with many edge cases second. |
| **trim** | File mixes both — keep only the cases that meet **keep**. |
| **frozen** | Area under an open PR or active redesign. Leave it, list it. |

Every **keep** carries its bug in one line: "fails if expired tokens are
accepted". No bug named → not a keep.

## 2. Fan out

Partition by area (top-level directory or package), one subagent per area, no
shared files, at most 5 in parallel. Each works on its own branch. Brief:

```
Goal: apply test-deslop classification to <area>. Default is delete.
Coverage map: <flows covered by E2E/integration, with test paths>.
Frozen: <paths>.
Tools: Read, Grep, Glob, Edit, Bash (test runner only).
Return: one row per test file — path, verdict, cases kept / total, lines removed,
and for each kept case the bug it catches. Then: suite command, exit code, tail.
```

## 3. Verify

- Full suite, typecheck, and E2E green on each branch. Paste the evidence.
- Spot-check falsifiability: in 3 kept tests per area, inject the named bug by
  hand, confirm the test goes red, revert. A keep that stays green is a delete.
- `reviewer` reads each area's diff against this skill. Builder ≠ verifier.

## 4. Report

```
| Area | PR | Files before | Kept | Deleted | Frozen | Lines removed |
```

Then before → after: files, lines, tests, suite wall time. The time delta shows
speed only, not safety — say so in the report.

## 5. Prevent the regrowth

Append to the project's CLAUDE.md (or AGENTS.md if that is what it uses):

```markdown
## Tests
- Write a test before the code it covers; watch it fail first.
- Keep a test only if you can name the plausible bug it catches.
- Test through the public interface. Never restate constants or implementation logic.
- Prefer the highest level that stays fast: E2E/integration for flows, unit for
  pure logic with many edge cases.
```
