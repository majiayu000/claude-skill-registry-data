---
name: ck-fix
description: >-
  Fix a bug using Scout → Diagnose → Fix → Review → Finalize. Use when the user pastes an error message, stack trace, or test failure, or says "fix this bug", "something's broken", "tests are failing", "I'm getting an error". Also accepts `--from-quality <report>` or `--from-test <report>` to fix exactly the findings/failures a report lists. Modes (pick one): --fast (trivial errors — lint, type, build — skip scout and review), --hard (mandatory review, no auto-approve).
user-invocable: true
---

# ck:fix — Structured Bug-Fix Pipeline

Modes — mutually exclusive, pick one (default = Standard: auto-approve on `code-reviewer`'s own `APPROVED` verdict):
- **`--fast`** — trivial issues (lint, type errors, build errors); skip scout, review, docs
- **`--hard`** — mandatory review, no auto-approve

Report-scoped input (either replaces Step 0's free-text description):
- **`--from-quality <report-path>`** — the target is exactly the blocking findings in a `ck:quality` report (`plans/{slug}/quality/{phase}-quality-report.json`).
- **`--from-test <report-path>`** — the target is exactly the failures in a `ck:test` failure report.

With either flag, fix strictly what the report lists — no expanding scope to adjacent code the report doesn't cite, even if it looks related.

---

### Step 0 — Prerequisites + Scope

`--from-quality`/`--from-test`: read the report; its findings/failures *are* the scope. Skip straight to Step 2 (report evidence replaces Scout).

Otherwise, if no error message, stack trace, or concrete description provided:
→ "Paste the error message or stack trace." Wait before continuing.

```
# Scope:
#   Description: {what the user said, or "from {report-path}"}
#   Quick?      → {yes/no — reason}
#   Mode:       {Standard | Quick | Hard}
```

If `--fast` or clearly a build/compiler/lint error: skip Step 1 → go directly to Step 2.

---

### Step 1 — Scout

Skip if `--from-quality`/`--from-test` (the report already is the evidence).

Spawn **`scout`** with the bug description:
- Greps for error patterns in logs and stack traces
- Reads affected source files and maps dependencies
- Checks recent git changes for related commits

```
// Evidence:
//   Error pattern: NullReferenceException at auth.ts:45
//   Affected files: auth.ts, session.ts
//   Recent change: commit a3f2b1 modified auth.ts (2h ago)
```

---

### Step 2 — Diagnose

Spawn **`debugger`** with the scout evidence report, or with the report's findings/failures directly for `--from-quality`/`--from-test`:
- Forms 2–3 hypotheses from the evidence (or takes the report's `required_action`/`expected` vs `actual` directly — it's already a confirmed root cause, not a hypothesis)
- Confirms or rejects each against the codebase
- Applies the minimal fix at the confirmed root cause, scoped to exactly what the report/evidence names

```
// Hypothesis A: null check missing in auth.ts:45 → CONFIRMED ✓
// Hypothesis B: race condition in session init   → REJECTED ✗
//
// Root cause: missing null guard on req.user before .validate()
// Fix applied: auth.ts:45
// Severity: HIGH | Scope: 1 file
```

---

### Step 2.5 — Quality Re-verification (when applicable)

If the fix touched any file already covered by an issued quality receipt (`plans/{slug}/quality/{phase}-receipt.json`), that receipt is now stale — its fingerprint no longer matches the file's bytes. Run `ck:quality --verify plans/{slug}/quality/{phase}-quality-report.json` before Step 3. `CHANGES_REQUIRED` sends the fix back to Step 2; do not proceed to Review or Finalize on a stale or rejected receipt.

Skip this step only when the fix touched no file with an existing receipt.

---

### Step 3 — Review

**`--fast`**: skip → Step 4.

Spawn **`code-reviewer`**: correctness, security, regressions. `code-reviewer` does not re-score maintainability that `ck:quality` already approved in Step 2.5 — it checks the bug fix itself, not architecture.

**Standard**: auto-approve on `code-reviewer`'s `APPROVED` verdict. Up to 3 fix/re-review cycles (different approach each), then escalate.
**`--hard`**: no auto-approve — human must explicitly approve before Step 4.

---

### Step 4 — Finalize (MANDATORY)

**`project-manager`** (skip `--fast`): sync plan progress if bug was tracked.
**`docs-manager`** (skip `--fast`): update docs if fix changes a public contract.
**`git-manager`** (always): conventional commit + ask to push.

```
// git-manager → fix(auth): add null guard on req.user before validate
//            → Push to remote? [y/N]
```

---

## Agents

| Agent             | Step | Modes |
|-------------------|------|-------|
| `scout`           | 1    | Standard, `--hard` (skip if `--fast` or `--from-quality`/`--from-test`) |
| `debugger`        | 2    | All |
| `ck:quality --verify` | 2.5 | All (only when a touched file has an existing receipt) |
| `code-reviewer`   | 3    | Standard, `--hard` (skip for `--fast`) |
| `project-manager` | 4    | Standard, `--hard` (skip for `--fast`) |
| `docs-manager`    | 4    | Standard, `--hard` (skip for `--fast`) |
| `git-manager`     | 4    | Always (mandatory) |
