---
name: "source-command-fix"
description: "Migrated source command `fix`"
---

# source-command-fix

Use this skill when the user asks to run the migrated source command `fix`.

## Command Template

# /fix — Structured Bug-Fix Pipeline

## Usage

```
/fix [--auto | --quick | --review | --parallel] <bug description>
```

Auto-detect mode if no flag given based on description:

- **Review** (default) — pause for approval at each step
- **Auto** (`--auto`) — auto-approve fixes if confidence ≥ 9.5 with 0 critical
- **Quick** (`--quick`) — fast cycle for trivial issues (lint, type errors, build errors); skip review + docs
- **Parallel** (`--parallel`) — scout 3 areas simultaneously for complex multi-file bugs

---

### Step 0 — Scope Detect

```
# Scope (Step 0):
#   Description: {what the user said}
#   Quick? → {yes/no — reason}
#   Mode: {Review | Auto | Quick | Parallel}
```

If `--quick` or description is clearly a build/compiler/lint error: skip scout, go straight to Step 2 with the error message as input.

For performance-related bugs:
- prefer root-cause fixes at query shape/data flow level before infra-level tuning,
- preserve API contract compatibility by default,
- and return explicit verification evidence (tests plus at least one measurable signal) before marking fixed.

---

### Step 1 — Scout

Spawn the **`scout`** agent with the bug description:

- Greps for error patterns in logs and stack traces
- Reads affected source files and maps dependencies
- Checks recent git changes for related commits

```
// spawning scout agent
//
// Evidence:
//   Error pattern: NullReferenceException at auth.ts:45
//   Affected files: auth.ts, session.ts
//   Recent change: commit a3f2b1 modified auth.ts (2h ago)
```

---

### Step 2 — Diagnose

Spawn the **`debugger`** agent with the scout evidence report:

- Forms 2–3 hypotheses from the evidence
- Confirms or rejects each against the codebase
- Applies the minimal fix at the confirmed root cause location
- Returns debug report with root cause + fix applied

```
// spawning debugger agent
//
// Hypothesis A: null check missing in auth.ts:45 → CONFIRMED ✓
// Hypothesis B: race condition in session init   → REJECTED ✗
//
// Root cause: missing null guard on req.user before .validate()
// Fix applied: auth.ts:45 — added null guard before validate()
// Severity: HIGH | Scope: 1 file
```

---

### Step 3 — Review (code-reviewer)

Spawn **`code-reviewer`** (skip in `--quick`):

- Correctness — does the fix address the root cause?
- Security — no new vulnerabilities introduced?
- Regressions — does anything else break?
- Code quality — follows project standards?

```
// spawning code-reviewer agent
//
// Correctness: ✓ Root cause addressed
// Security:    ✓ No new vulnerabilities
// Regressions: ✓ No side effects
// Score: 9.8/10 — APPROVED
```

**Auto mode**: auto-approve if score ≥ 9.5, 0 critical. Up to 3 fix/re-review cycles, then escalate.
**Review mode**: always pause for approval with full findings.
**Quick mode**: skipped entirely.

---

### Step 4 — Finalize (MANDATORY)

Always required — fix is incomplete without git-manager:

**`project-manager`** (skip in `--quick`) — syncs plan progress if bug was tracked  
**`docs-manager`** (skip in `--quick`) — updates docs if the fix changes a public contract  
**`git-manager`** (always) — conventional commit + asks to push

```
// MANDATORY finalize:
// project-manager → task marked resolved (if tracked)
// docs-manager    → no doc changes needed
// git-manager     → fix(auth): add null guard on req.user before validate
//                → Push to remote? [y/N]
```

---

## Agents

| Agent             | Step                     | Modes                                 |
| ----------------- | ------------------------ | ------------------------------------- |
| `scout`           | 1 — evidence gathering        | All (skip if --quick + obvious error) |
| `debugger`        | 2 — root cause + apply fix    | All                                   |
| `code-reviewer`   | 3 — quality check             | Skip in --quick                       |
| `project-manager` | 4 — sync plan/tasks           | Skip in --quick                       |
| `docs-manager`    | 4 — update docs               | Skip in --quick                       |
| `git-manager`     | 4 — commit + push             | Always (mandatory)                    |

---

## Integration

- `/plan` → `/cook` → `/fix` — fix regressions found after cooking
- `/code-review` — standalone review without the full fix pipeline
