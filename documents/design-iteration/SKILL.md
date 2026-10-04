---
name: design-iteration
description: 'One-fix-at-a-time, approval-gated design fix recovery. Given a checklist of fixes (handover doc, CHECKLIST.md, or inline list), applies each individually, presents a diff, and waits for an explicit APPROVE / REJECT / NO CHANGES decision before committing. Trigger phrases: /design-iteration, "go through the checklist one by one", "fix these one at a time", "bucket recovery", "design fix pass".'
---

# /design-iteration

A **one-fix-at-a-time, approval-gated** design fix recovery skill. Given a checklist of
fixes (a handover doc, CHECKLIST.md, or inline list), applies each fix individually,
presents a diff, and waits for an explicit **APPROVE / REJECT / NO CHANGES** decision
before committing or moving on. Never batches. Never self-merges.

## When to invoke

- `/design-iteration` — start or resume a fix pass on the current branch
- "go through the checklist one by one"
- "fix these one at a time, show me each before committing"
- "bucket recovery" / "design fix pass" with a list of items

## Invocation

```
/design-iteration [path/to/checklist-or-handover.md]
```

If no path is given, look for the active handover in:
1. An explicit path in the conversation context
2. `founder/reports/design-review-<today>/HANDOVER*.md`
3. Ask the user to specify

## Operating contract

### The one rule that governs everything

**One fix at a time. After each fix, STOP and present it for a decision.**

- **APPROVE** → commit that fix (one commit, one fix), push, move to next
- **REJECT** → `git restore` touched files, move to next
- **NO CHANGES** → fix was already present or unnecessary; touch nothing, note it, move to next

Never batch. Never "do them all and summarize." The checkpoint exists because these fixes
touch files that may have been rewritten by a migration, and a wrong port can silently
regress a shipped fix.

### Loop for each fix

1. **Verify it is still missing.** Re-run the check from the handover (grep, line read).
   If already present → **NO CHANGES**; report and skip.
2. `git show <ref-sha>` (if provided) to see original intent. Do not blind-apply.
3. Port the intent onto the current file(s) by hand. Do NOT paste stale patches wholesale
   when target files were rewritten since the source SHA.
4. Read the edited file(s) back. Confirm:
   - No duplicated or merged lines
   - No new hardcoded hex (use design tokens; fallback to `var(--token, fallback)` only)
   - No banned patterns (gradient text, dead enum reads, client-side branch derivation if
     the project has an emitted-branch architecture)
5. **STOP. Present to the user:**
   - Fix ID + description
   - Files changed
   - `git diff` output (or key hunks if very large)
   - One-line rationale: why this matches the intent without introducing regressions
   - Ask explicitly: **APPROVE / REJECT / NO CHANGES?**
6. On decision:
   - **APPROVE** → `git add <only those files>` → commit with message
     `fix(design): <fix-id> — <one-line summary>` → `git push origin <branch>` →
     report SHA → next fix
   - **REJECT** → `git restore <those files>` → next fix
   - **NO CHANGES** → touch nothing → next fix
7. Never proceed to the next fix before a decision on the current one.

### After all fixes

Open one PR from the current branch to the target base branch. PR body must list:
- Each fix + its outcome (approved / rejected / no-change)
- Any Bucket-2 / "do not re-apply" items that were deliberately skipped, and why

Then stop — the human merges.

## Branch + scope rules

- Always work on the branch specified in the handover or by the user. Never create a
  new branch mid-pass without asking.
- Respect CI branch-scope (e.g. `design/` branches may only touch `docs/` + `*.md`).
  When a fix crosses scope, surface the conflict and ask: split across branches, or add
  `[skip-scope-check]` to the commit message per the user's call.
- Never push to `main` directly.

## Presenting the diff

For each fix, show:
```
--- Fix N: <title> ---
Files: <list>
---
<git diff or key hunks>
---
Why this is safe: <one sentence>

APPROVE / REJECT / NO CHANGES?
```

If the diff is very large (e.g. 48-file sweep), show the full file list + one
representative sample diff, then ask for approval before running the bulk operation.

## Token discipline

- Verify before editing (one read + grep). Edit. Verify after (read-back). That's the
  full cycle — do not re-read files already confirmed.
- For bulk deletions (e.g. removing a dev tag from N files), use a single shell command
  rather than N individual edits, then confirm count = 0 with a follow-up grep.

## Reference implementation

This skill was extracted from the 2026-07-20 Bucket-1 recovery session
(`design/ygg2-bucket1-recovery` → `dev/yggdrasil-ii-staging`, PR #1241).
Handover doc: `founder/reports/design-review-2026-07-20/HANDOVER-bucket1-recovery.md`.
INSIGHTS source-of-truth: `founder/reports/design-review-2026-07-20/INSIGHTS.md`.
