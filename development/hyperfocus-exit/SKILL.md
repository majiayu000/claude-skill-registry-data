---
name: hyperfocus-exit
category: exec-function
codex-short-description: "Park a deep session before an interrupt, so re-entry is cheap instead of impossible"
description: >
  Park a deep work session before an interruption — capture what is only in your head, write
  a park file, drop a breadcrumb at the cursor. Use when the user says "I have to stop",
  "meeting in 10", "park this", "save my place", or invokes /hyperfocus-exit.
version: 1.0.0
license: MIT
compatibility: claude-code codex opencode
allowed-tools:
  - Bash
  - Read
  - Write
  - Grep
  - Glob
  - AskUserQuestion
related-skills:
  - hyperfocus-recovery
  - task-initiation
  - interest-capture
  - i-have-adhd
loop-eligible: false
---

# Hyperfocus Exit

The user is deep in something and has to stop **now** — a meeting, a school pickup, the end of the day. Dropping cold means the working-memory half of the context evaporates and re-entry costs an hour tomorrow.

Your job is to capture the half that lives only in their head, in less time than they have.

## The clock rules everything

Ask exactly one thing first: **how many minutes do you have?** Then run the matching tier. Never run a longer tier than the clock allows.

| Time | Tier | What you do |
| :--- | :--- | :--- |
| <1 min | **Slam** | Ask nothing. Snapshot artifacts, write the park file with a `[not captured]` head-state section, done. |
| 1–3 min | **Standard** | One question (below), snapshot, park file, breadcrumb. |
| 3+ min | **Full** | Standard, plus loose-end sweep and a stated re-entry action. |

## The one question

> **What were you about to try next, and what have you already ruled out?**

That single answer carries most of the value — it is the part that exists nowhere on disk. If they answer with only half, take the half.

## Snapshot pass

Run in parallel; take what works:

1. `git status` and `git diff --stat` — what is dirty
2. `git branch --show-current` — where they are
3. `git stash list` — anything already parked
4. Files modified in the last 60 minutes
5. The open editor file and cursor line, from IDE context if available

## Write the park file

Write to `.ink-and-agency/park/<YYYY-MM-DD-HHmm>.md` in the workspace (create the directory if needed). [`hyperfocus-recovery`](../hyperfocus-recovery/) reads the newest file in that directory first.

```markdown
---
parked: <YYYY-MM-DD HH:mm>
branch: <branch>
tier: slam | standard | full
---

## The thread
[One paragraph: what they were doing and what for. Reconstructed from artifacts.]

## In my head, not in the repo
[The one-question answer: what they were about to try, what they already ruled out.
 Highest-value section. Write "[not captured — slam exit]" if the clock forbade asking.]

## Re-entry action
[One literal action, ≤2 minutes, that restarts the loop. Same shape as task-initiation output.]

## State of the tree
[Dirty files, staged vs unstaged, current branch, failing test if known.]

## Do not lose
[Anything that will silently disappear: uncommitted experiments, a running process,
 a modified env var, an unsaved buffer, a browser tab that matters, a temporary hack
 that must be reverted.]
```

## Drop the breadcrumb

Where the IDE reports a cursor line, or in the most recently modified file, insert a comment at that exact line using the file's comment syntax:

```
// PARKED <YYYY-MM-DD HH:mm>: <the one-question answer, one line>
```

`hyperfocus-recovery` scans for `PARKED` alongside TODO/FIXME/XXX, so this is what points the reader back at the precise spot. Skip it in the slam tier if writing would risk an unsaved conflict.

## Report back

Under 5 lines. The user is already walking away.

> **Parked.** `.ink-and-agency/park/2026-07-28-1450.md` — breadcrumb at `src/auth.ts:47`.
> **Do not lose:** dev server still running on :3000; `DEBUG_AUTH=1` still set in your shell.
> **Re-entry:** run `/hyperfocus-recovery`.

## What NOT to do

- Do not stash, commit, or revert anything unless the user asks — the hot, dirty state *is* the context. Offer a WIP commit only if they have time and ask.
- Do not produce a plan for tomorrow. Park the present; do not schedule the future.
- Do not ask a second question when the clock says one.
- Do not tidy, format, or fix anything on the way out.
- Do not let the park file grow past one screen. It gets read by a brain that has lost the thread.

> **Host portability:** tool names in this skill follow Claude Code conventions; on other hosts (Codex, opencode) map them by intent — see [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/hyperfocus-exit.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
