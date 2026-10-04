---
name: pipeline-bugfix
version: 1.0.0
description: "Bug fix pipeline — investigate root cause, apply fix with scope lock, critique, QA verification, ship. Chains investigate, guard, verification, critique skills, qa-only, and ship into a disciplined fix workflow."
---

# Pipeline: Bug Fix

You are orchestrating a bug fix pipeline. The iron law: no fix without root cause. Execute each stage sequentially.

## Pipeline State

Create a pipeline tracker at `.gstack/pipeline-bugfix-{date}.md` at the start.

```markdown
## Pipeline: Bug Fix
Started: {timestamp}
Bug: {description}

| # | Stage | Status | Gate | Duration | Notes |
|---|-------|--------|------|----------|-------|
| 1 | INVESTIGATE | pending | — | — | — |
| 2 | FIX | pending | — | — | — |
| 3 | CRITIQUE | pending | — | — | — |
| 4 | QA | pending | — | — | — |
| 5 | SHIP | pending | — | — | — |
```

---

## Stage 1: INVESTIGATE

Invoke `/investigate` with the bug description, error message, or reproduction steps.

The investigate skill enforces:
- Root cause identification before any fix
- 3-strike rule: 3 failed hypotheses → STOP and escalate
- PreToolUse hooks lock the debug scope via `/freeze`

**Gate:** Root cause must be identified. A DEBUG REPORT must be produced with:
- Symptom (what the user observed)
- Root cause (what was actually wrong)
- Proposed fix (what needs to change)

**On pass:** Update tracker row 1 → PASS, extract the root cause and proposed fix for Stage 2.
**On fail:** If 3 strikes hit → update tracker row 1 → BLOCKED, report to user with findings so far.

---

## Stage 2: FIX

### 2a: Scope lock
Identify the directory containing the affected files. Invoke `/guard {directory}` to activate:
- Edit/Write boundary lock (freeze)
- Destructive command interception (careful)

### 2b: Apply the fix
Implement the fix identified in Stage 1. Write a regression test that:
1. Fails WITHOUT the fix (red)
2. Passes WITH the fix (green)

### 2c: Verify
Apply the CLAUDE.md evidence gate (Verification Before Done) — never claim fixed without fresh evidence produced this session:
- Run the regression test → must pass
- Run the full test suite → must pass
- Demonstrate the fix with evidence (command output, not assertions)

**Gate:** Regression test passes the red-green cycle. Full test suite passes.

**On pass:** Update tracker row 2 → PASS, proceed to Stage 3.
**On fail:** If tests fail, investigate further. Do NOT proceed with a broken test suite.

---

## Stage 3: CRITIQUE

Detect which critique applies based on the files changed by the fix:

```bash
git diff main...HEAD --name-only
```

| Changed files | Critique skill |
|---|---|
| Backend/API/server files | `/backend-critique` |
| Auth, secrets, crypto, user data | `/security-critique` |
| UI/frontend files | `/design-critique` |
| Infra/CI/deploy files | `/operations-critique` |

Run the most relevant critique (one is usually enough for a bugfix). If files span multiple domains, run the top 2 as parallel subagents.

**Gate:** Critique grade **B or above**.

If grade C or below:
1. Report findings
2. Fix the issues raised (they're usually small for a bugfix)
3. Re-run critique to confirm B+

**On pass:** Update tracker row 3 → PASS (include grade), proceed to Stage 4.
**On skip:** If the fix is < 5 lines and touches only one file, skip critique (update tracker → SKIPPED). This override must be noted.

---

## Stage 4: QA

Invoke `/qa-only` (report-only mode — no additional fixes at this stage).

If the project has a running dev server, use it. Otherwise start one.

The QA skill runs browser testing and produces a health score. Since this is a bugfix, focus on:
1. The specific area where the bug was found (regression check)
2. Adjacent features that could be affected
3. Overall health score

**Gate:** Health score >= 70. No NEW issues introduced (compare against baseline if available).

**On pass:** Update tracker row 4 → PASS (include health score).
**On fail:** If new issues found, they were likely introduced by the fix. Go back to Stage 2, refine the fix.

---

## Stage 5: SHIP

Invoke `/ship`.

For bugfixes, the ship skill should produce:
- A commit message starting with `fix:` or `fix(scope):`
- A PR with the DEBUG REPORT from Stage 1 included in the description
- The regression test included in the PR

**Gate:** PR created. Tests pass.

**On pass:** Update tracker row 5 → PASS (include PR URL).

---

## Final Report

```markdown
## Pipeline Report: Bug Fix
Bug: {description}
Root Cause: {root cause from Stage 1}
Fix: {summary of changes}
Run: {timestamp}
Duration: {total elapsed}

| # | Stage | Skill(s) | Result | Gate | Duration |
|---|-------|----------|--------|------|----------|
| 1 | INVESTIGATE | investigate | {result} | Root cause: {found/blocked} | {time} |
| 2 | FIX | guard, verification | {result} | Red-green: {pass/fail} | {time} |
| 3 | CRITIQUE | {critique skill} | {result} | Grade: {letter} | {time} |
| 4 | QA | qa-only | {result} | Score: {N}/100 | {time} |
| 5 | SHIP | ship | {result} | {PR URL} | {time} |

Overall: {PASS / BLOCKED}
Regression test: {file path}
```
