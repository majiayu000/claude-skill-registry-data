---
name: sdd-resolving-merge-conflicts
description: Use when a merge, rebase, or cherry-pick has conflicts that need resolution
disable-model-invocation: true
metadata:
    opencode/autoinvoke: false
---

# Resolving Merge Conflicts

## Overview

**Core principle:** Understand both sides before choosing. Preserve both intents where possible. Never invent behavior. Resolve rather than abort.

**Announce at start:** "I'm using the sdd-resolving-merge-conflicts skill to resolve these conflicts."

A conflict means two changes touched the same lines with different intents. Resolution merges two histories into one coherent result — not by picking a side, and not by redesigning.

## Step 1: See the State

Know which operation you are inside before touching a hunk:

```bash
git status
git log --oneline --graph -20
git diff --name-only --diff-filter=U
```

List the conflicting files and hunks. Merge, rebase, and cherry-pick resume differently, so establish which one is in progress first.

## Step 2: Find the Primary Sources

For each side of each conflict, understand **why** the change was made and what the original intent was:

- Read both sides' commits — merge: `git log --oneline --left-right HEAD...MERGE_HEAD`; rebase: `git show REBASE_HEAD` (the commit currently being replayed) and the surrounding replay commits when their intent matters; cherry-pick: `git show CHERRY_PICK_HEAD`.
- Follow the references: PRs, issues, specs, plan documents.
- If intent is not recoverable from the sources, ask your human partner — never guess from the diff alone.

## Step 3: Resolve Each Hunk

- **Preserve both intents where possible.** Many conflicts are additive at the edges; both changes can coexist.
- **Where incompatible, pick the side that serves the operation's stated goal** and record the trade-off — what was dropped and why — in the merge commit message (for rebase or cherry-pick, in the PR or handoff).
- **Never invent behavior.** Conflict resolution is not a refactor and not an opportunity to fix unrelated code. If the resolution seems to require new behavior, that is a separate change after the operation completes.
- **Resolve rather than abort.** `--abort` is not a convenience exit; it is correct only when the operation itself is wrong (wrong base, changed goal) or your human partner asks to back out — and the reason gets recorded and surfaced, not swallowed.
- Remove every conflict marker; `git diff --check` flags leftover markers and whitespace errors in tracked changes.

## Step 4: Run the Project's Checks

Discover the project's automated checks and run them — typically typecheck, then tests, then format. Fix what the resolution broke; when a failure's cause is not obvious, investigate before fixing.

```bash
git diff --check     # leftover markers, whitespace
<typecheck> && <test> && <format --check>
```

A resolution that compiles but fails tests is not resolved. Preserve the failure output and investigate it with `sdd-systematic-debugging` — the cause may be the resolution, the updated base, or the environment. Correct the resolution only when the investigation shows it is the cause.

## Step 5: Finish the Operation

Stage the resolved paths only — `git add <resolved paths>`, never `-A` blindly (the tree may hold unrelated work, generated files, or secrets) — then inspect the staged diff for markers and whitespace (`git diff --cached --check`) before completing:

- Merge: `git commit` (or `git merge --continue`).
- Rebase: `git rebase --continue`, repeating until every commit is rebased. Commits keep their own messages, so the trade-off lives in the PR or handoff.
- Cherry-pick: `git cherry-pick --continue`; same message rule as rebase.

Never leave a half-finished operation behind unannounced: finish it, or — if debugging is blocked — stop and report exactly where it stands (operation in progress, evidence preserved). Never commit a red resolution or guess it green.

## Quick Reference

| Situation                     | Action                                                                                                    |
| ----------------------------- | --------------------------------------------------------------------------------------------------------- |
| Conflict in progress          | Identify merge/rebase/cherry-pick before resolving (Step 1)                                               |
| Unclear why a side changed    | Read commits, PRs, issues; ask if unrecoverable (Step 2)                                                  |
| Both changes compatible       | Keep both (Step 3)                                                                                        |
| Incompatible intents          | Pick by the operation's goal; record the trade-off (Step 3)                                               |
| Tempted to fix something else | Don't — resolve only, then a separate change (Step 3)                                                     |
| Tempted to `--abort`          | Not a convenience exit; abort only for a wrong operation/goal or at your human partner's request (Step 3) |
| Checks fail after resolving   | Investigate with `sdd-systematic-debugging`; fix the resolution if it is the cause (Step 4)               |
| Operation half-finished       | Finish it; if debugging is blocked, report exactly where it stands (Step 5)                               |

## Common Rationalizations

| Excuse                                        | Reality                                                                                                                                                                                                                                                          |
| --------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "Ours is newer — just take ours"              | A conflict is a question about intent; newer isn't the same as correct, and dropping the other side's intent silently is how regressions land.                                                                                                                   |
| "I'll merge both sides into a cleaner design" | That is a redesign smuggled into a merge. Resolve first; improve later in its own change.                                                                                                                                                                        |
| "`--abort` is the safe move"                  | Abort restores the pre-operation state — it doesn't lose either side's committed history — but it discards the context you just gathered and defers the work. Resolve; abort only when the operation itself is wrong or your human partner asks, and record why. |
| "It compiles, so the merge is fine"           | Compiling proves nothing about the paired intent. Run the project's checks.                                                                                                                                                                                      |
| "I'll finish the rebase later"                | Half-finished operations are inherited by a context with none of yours. Finish now.                                                                                                                                                                              |
| "That post-merge test failure is flaky"       | Don't name a cause before investigating — preserve the output and follow Step 4; it may be the resolution, the updated base, or the environment.                                                                                                                 |
