---
name: luke-fix
description: >
  Incremental fix-verify loop for the Luke codebase. Runs an audit, takes the
  highest-severity finding, proposes a fix, applies it after confirmation, then
  re-runs the audit to verify no regressions were introduced. Repeats until no
  HIGH or CRITICAL findings remain.
  Use after vibe coding sessions to systematically fix audit findings.
  Optional: specify which audit to run — /luke-fix audit | bugs | security | full
  Default: runs /luke-audit (architectural compliance).
argument-hint: '[audit|bugs|security|full] [path]'
disable-model-invocation: true
---

# Luke Fix-Verify Loop

You are running an incremental fix-verify loop on the Luke codebase.
At each iteration: find → propose → confirm → fix → verify → repeat.

**Read `.claude/skills/luke-shared/audit-protocol.md` first** and apply the
sections its applicability table assigns to `/luke-fix`: §1 scoping and §7
concurrent sessions. You modify application code, not test files, so §7.2 and
§7.4 are the ones that bite.

## Configuration

**Invocation arguments:** $ARGUMENTS

The first token of the bound value above selects which audit to use:

- `audit` or empty → use Skill(luke-audit)
- `bugs` → use Skill(luke-bugs)
- `security` → use Skill(luke-security)
- `full` → use Skill(luke-full)

**Any other first token fails closed.** Matching is exact and case-sensitive,
and the scope always follows the audit name (`/luke-fix audit apps/api`, never
`/luke-fix apps/api`). Print

```
luke-fix: usage — [audit|bugs|security|full] [<scope>]
```

and stop, having invoked nothing.

Store the chosen audit skill as AUDIT_SKILL for use throughout the loop.
Store the second token, if present, as the scope path (e.g. `/luke-fix bugs apps/api`).

---

## Loop

### Iteration Start

**Step 1 — Run audit, then route**
Invoke AUDIT_SKILL (with scope if provided).

**Route before you queue.** Every finding has a remediation owner, and it is not
always this skill (`.claude/skills/luke-shared/governance-map.md` §3). When the
audit was `/luke-full`, its structured footer states the owner per finding
(`.claude/skills/luke-shared/result-contract.md`); otherwise derive it from the
producing skill.

| Finding                                    | Remediation owner   | This skill does                  |
| ------------------------------------------ | ------------------- | -------------------------------- |
| application architecture / runtime / app security | `luke-fix`   | fix it, after approval           |
| platform, dependency, toolchain            | `luke-deps`         | **hand off** — never edit        |
| missing or inadequate evidence (QA GAP)    | `luke-test write`   | **hand off** — never write tests |
| README / JSDoc / Prisma docs / ADR index   | `luke-docs`         | **hand off**                     |

A finding this skill does not own is listed in the report with its owner and the
command that addresses it. Editing outside this authority is how a fixer starts
bumping dependency versions to make an audit quiet.

**Then build the queue**, from the findings this skill owns:

1. `CRITICAL` (sorted by file path for reproducibility)
2. `HIGH`
3. Stop.

`MEDIUM` and `LOW` are **never queued**. They appear in the completion summary,
and the user may ask for one by name. The queue used to include MEDIUM while the
hard rules forbade processing it — both statements could not be true, and the
one that survives is the conservative one.

**Status gates eligibility, not severity.** Only findings whose status is
`CONFIRMED` are eligible. A `NEEDS DECISION` is a question for the user and is
never auto-queued however severe it looks; `ALREADY RESOLVED`, `SUPERSEDED` and
`NOT REPRODUCIBLE` are reported and skipped. Severity says how bad it would be;
status says whether we know it is real.

Being queued means **eligible for the loop**, never authorisation to edit: every
change still waits for explicit approval at Step 3.

If the queue is empty: print the completion message (see below) and stop.

---

**Step 2 — Pick next finding**
Take the first unresolved finding from the prioritized list.
Skip any finding that was already attempted in a previous iteration
(track attempted findings by file:line across iterations).

If all findings have been attempted: print the completion message and stop.

---

**Step 3 — Present finding and proposed fix**

Show this to the user:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Iteration N  |  Remaining: X CRITICAL, Y HIGH, Z MEDIUM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[SEVERITY] — <finding title>
File: `path/to/file.ts:line`
Problem: <one sentence explanation>

Proposed fix:
<show the exact code change as a diff or before/after>

Options:
  [Y] Apply fix and continue
  [S] Skip this finding (mark as known, move to next)
  [E] Edit the proposed fix before applying
  [Q] Quit loop (keep changes made so far)
```

**Wait for user response before proceeding.**
Do not apply any change without explicit confirmation.

---

**Step 4 — Handle response**

**Y (Apply)**:

- If the file is in another live session's ledger (§7.2), **do not apply**:
  mark the finding `skipped — file owned by another session`, say so, and move
  to the next finding. The loop continues.
- Apply the fix to the file, then append its path to your ledger (§7.1)
- Run the **static** gate the change needs — this is the cheap first pass, not
  the proof:
  - TypeScript error? → `pnpm --filter <app> typecheck`
  - Prisma schema? → check schema syntax only, do not run migration
  - ESLint violation? → `pnpm --filter <app> lint <file>`
- **If the fix changes behavior, static gates are not evidence.** Hand the
  verification to `/luke-test`, which owns what proof is adequate
  (`.claude/skills/luke-test/references/evidence-matrix.md`):
  - `/luke-test assess <scope>` — what would catch this being wrong?
  - `/luke-test verify <scope>` — run it, and read the result
  - if the evidence does not exist, that is a **QA GAP**: offer
    `/luke-test write <scope>`. Do not write the test here — test files are
    `/luke-test`'s to write, application code is this skill's
- A fix whose only evidence is a green typecheck is **not proven**. `lessons.md`
  records a dialog whose submit never fired: typecheck, lint and the whole suite
  were green, because nothing about it was a type error
- If verification fails: show the error, revert the change — **by undoing your own
  Edit, never with `git checkout`/`git restore` on the file** (§7.4) — mark finding
  as "attempted/failed", move to next
- If verification passes: mark finding as "fixed", continue to Step 5

**S (Skip)**:

- Mark finding as "skipped — user decision"
- Go back to Step 1 (re-run audit to get fresh list)

**E (Edit)**:

- Show the proposed fix as editable text
- Wait for user to provide the corrected fix
- Apply the corrected fix
- Run verification as in Y
- Continue to Step 5

**Q (Quit)**:

- Print the session summary and stop

---

**Step 5 — Re-verify with full audit**

After applying a fix, re-run AUDIT_SKILL scoped to the **affected file(s) only**
(not the full codebase — keep it fast).

Check:

1. The original finding is gone ✅
2. No new CRITICAL or HIGH findings appeared in the same file ✅

**A disappeared finding is not correct behavior.** The audit proves the
prohibited pattern is gone; only the QA step above proves the replacement works.
Report both, and if the behavioral evidence is missing say so as a QA GAP rather
than calling the remediation proven.

If a new finding appeared in the fixed file:

- Show it immediately: "⚠️ Fix introduced a new issue:"
- Offer to fix it in the same iteration or queue it for next

Go back to Step 1 for the next iteration.

---

## Completion Message

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Luke Fix Loop — Session Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Fixed:   N findings
Skipped: N findings
Failed:  N findings (reverted)
Remaining MEDIUM/LOW: N (not auto-processed)

Files modified:
  - path/to/file.ts (N fixes)
  - path/to/other.ts (N fixes)

Not owned by this skill (handed off):
  - <finding> → <owner> — run: <command>

Needs decision (never auto-queued):
  - <finding> — <the question it poses>

Suggested next step:
  Run /luke-full for a complete health check before committing.
  Then: show diff → ask "Ready to commit?" → wait for approval.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Hard Rules

- NEVER apply a fix without explicit user confirmation (Y, E)
- NEVER batch-apply multiple fixes without re-running the audit in between
- NEVER run `git commit` — that is the user's decision
- NEVER revert with `git checkout`/`git restore` on a file: it discards the other
  session's uncommitted work and the user's, not just yours (§7.4)
- NEVER process MEDIUM or LOW findings automatically — present them in the
  completion summary only
- NEVER queue a finding whose status is NEEDS DECISION, however severe it looks
- NEVER edit outside this skill's remediation authority: platform findings go to
  `/luke-deps`, missing evidence to `/luke-test`, documentation to `/luke-docs`
- NEVER call a behavior-bearing fix proven because lint and typecheck are green
- If the same file is fixed 3+ times in one session, warn:
  "⚠️ This file has been modified 3 times — consider reviewing the full file
  before continuing."
