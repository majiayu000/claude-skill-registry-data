---
name: wt
description: Session worktree — isolate the whole current session in a git worktree, then land it back to the parent branch. Use for "worktree로 작업", "이 세션을 worktree에서", "격리해서 작업하고 부모로 머지", "/xm:wt", or when the user wants the ENTIRE session (not one task) to run in an isolated worktree and later merge back.
model: sonnet
allowed-tools:
  - Bash
  - EnterWorktree
  - ExitWorktree
  - AskUserQuestion
---

# x-wt — Session Worktree

## Overview

`/xm:wt` runs the WHOLE current session inside an isolated git worktree, then
lands that work back onto the branch you started from. Two verbs:

- **`/xm:wt`** (or `/xm:wt start [name]`) — create a worktree, switch the session into it.
- **`/xm:wt land`** — merge the worktree branch into its parent (no push), return the session.

This is session-scoped isolation. It is NOT x-build's worktree mode
(`/xm:build run --worktrees`), which fans ONE worktree out PER task from a
project's task DAG. `/xm:wt` has no tasks and no gate panel — it is the thin
"work aside, then merge back" wrapper.

**Mechanism split** (do not blur):
- The harness tools `EnterWorktree` / `ExitWorktree` own the SESSION cwd switch.
- `git-kit worktree finish` owns the merge-back: it wraps `promote` (commit + one-hop merge into `gk-parent`, no push) AND owns worktree/branch cleanup.
- The skill just sequences them and records the parent so `land` merges correctly.

> `EnterWorktree` / `ExitWorktree` are harness (Claude Code) tools, not xm CLIs.
> If they are not already available, load them first:
> `ToolSearch("select:EnterWorktree,ExitWorktree")`.

## When to Use

- "worktree로 (전체) 작업하자", "이 세션을 worktree에서 돌려", "격리해서 작업 후 부모로 머지"
- The user wants the current session's ongoing work isolated on a throwaway branch, mergeable later.
- `/xm:wt`, `/xm:wt start`, `/xm:wt land`, `/xm:wt status`.

## Do NOT Use When

- The user wants ONE task or parallel tasks isolated → `/xm:build run --worktrees`.
- The user wants a plain branch (no separate working directory) → `git switch -c` / git-kit.
- The user only wants a subagent isolated → the Agent tool's `isolation: "worktree"`.
- The user never said "worktree" — do not put a session into a worktree unprompted.

## Core Process — route on the first token

`start` (empty / `start` / `go` / `new`) → §Start. `land` (`land` / `finish` / `done`) → §Land.
`status` → §Status.

### Start

1. **Preconditions.**
   - In a git repo (`git rev-parse --is-inside-work-tree`). If not, stop and say so.
   - Not already in a `/xm:wt` worktree — if `git config --get branch.$(git branch --show-current).gk-parent` returns a value, you are already in one; tell the user to `/xm:wt land` (or `status`) instead of nesting.
   - Warn if the working tree is dirty: uncommitted changes stay in the CURRENT directory and do NOT follow into a fresh worktree (see Rationalizations for `worktree.baseRef`). Offer to commit first, or proceed.
2. **Record the parent branch** BEFORE entering:
   ```bash
   PARENT=$(git branch --show-current)   # the branch land will merge back into
   ```
3. **Enter the worktree** — call the `EnterWorktree` tool (pass `name` only if the user named it; otherwise let it generate one). This switches the session cwd into a new worktree on a new branch.
4. **Persist the parent** so `land` (a separate invocation) knows the target:
   ```bash
   NEW=$(git branch --show-current)
   git config branch."$NEW".gk-parent "$PARENT"
   ```
5. **Report** (normal mode → Korean):
   ```
   🌿 worktree 진입: <NEW>  (parent: <PARENT>)
      경로: <worktree path>
      작업 후 /xm:wt land 로 <PARENT>에 머지하세요.
   ```

### Land

1. **Confirm you are in a `/xm:wt` worktree**: `PARENT=$(git config --get branch.$(git branch --show-current).gk-parent)`. If empty, this session was not started by `/xm:wt` — do NOT ExitWorktree; say so and stop.
2. **Verify before merge** (announce, keep light): run the project's quick check if one exists (`bun test` here, or the repo's verify). Report failures; ask before merging broken code.
3. **Dirty-tree gate BEFORE finish.** Run `git status --porcelain`. If it is non-empty, list the files to the user and ask them to choose: commit the intended work first, OR acknowledge that `finish` will auto-commit EVERYTHING — including unrelated and untracked files (e.g. `package-lock.json`) — via the kiro classifier as separate, unreviewed commits onto the parent. gk's OWN gated finish path refuses a dirty tree for exactly this reason ("gate must review exactly what merges"); the ungated default path has no such guard, so you are the guard. Do not proceed silently.
4. **Merge + clean up — one command.** `git-kit worktree finish` wraps `promote` (commit + one-hop merge into `gk-parent`, no push) and then removes the worktree and deletes the branch.
   ```bash
   GK_AGENT=1 git-kit worktree finish --cleanup --delete-branch
   ```
   Branch STRICTLY on the JSON `state` — NEVER the exit code (the shell exits 1 when cleanup removes the cwd even on success, and gated finish uses exit 3 as a normal paused flow):
   - `ok` → merged and cleaned. Note `removed` / `branch_deleted` from `result`; continue to step 5.
   - `error` whose message contains `promote failed` / `exit 3` → a merge CONFLICT paused in disguise: the child promote exited paused but the ungated wrapper flattened it to a plain error, so the resume contract is lost and the merge is mid-flight INSIDE the worktree. Do NOT ExitWorktree and do NOT discard anything: run `GK_AGENT=1 git-kit context` in the worktree, report the conflict state and the resume/abort options, then **STOP**.
   - `blocked` / any other `error` → check whether the parent already contains the branch (`git branch --contains`). If yes, the merge STANDS and only cleanup failed (a `git branch -d` refusal or a `git worktree remove` blocked on leftover untracked files) — report that distinction, do not re-merge. If no, follow `error.remedies[0]` after checking its `safety`. Never remove the worktree yourself.
5. **Return the session** — call `ExitWorktree` with `action: "keep"`. It restores the session cwd to the parent directory. Its "Your work is preserved at <path>" message is FALSE after `--cleanup` (that directory is already deleted) — never relay it; report from the finish JSON fields (`branch`, `to`, `removed`, `branch_deleted`).
6. **Report** (normal mode → Korean):
   ```
   ✅ <NEW> → <PARENT> 머지 완료 (push 안 함).
      worktree / 브랜치 정리됨 (removed / branch_deleted).
      세션이 <PARENT>로 복귀했습니다.
      원격 반영은 git-kit land / push 로 직접 하세요.
   ```

### Status

Report where the session is: `git branch --show-current`, whether it is a
`/xm:wt` worktree (gk-parent set?), and `git-kit worktree` list for the repo.
Read-only — never create or remove anything under `status`.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "I'll just `git merge` the branch by hand." | Use `git-kit worktree finish`: it wraps `promote` (commits, resolves the fast-forward / merge-tree path, needs no parent checkout, reads `gk-parent` so it merges into the branch you actually started from) and owns cleanup. Raw merge loses that and can land on the wrong base. |
| "I'll skip recording the parent — land will figure it out." | `land` is a SEPARATE invocation; nothing carries the parent across turns except the `branch.<name>.gk-parent` config you set at start. Skip it and `finish`'s inner `promote` falls back to the configured base, merging into the wrong branch. |
| "The tree is dirty but I'll enter a fresh worktree anyway." | With `worktree.baseRef=fresh` (default) the new worktree branches from origin/<default>; uncommitted changes in the current dir do NOT come along. Commit first, or set `worktree.baseRef=head` to branch from where you are. |
| "I'll push after promote to be safe." | `promote` is deliberately no-network (local integration), and `finish` inherits that. Never push without the user asking — pushing the parent is their call. |
| "Only one vendor / no gate, so I'll add a panel review here." | `/xm:wt` is the ungated wrapper by design. Gated per-task merges are `/xm:build run --worktrees`. Don't reinvent the gate here. |
| "I'll define a shell alias for the long git-kit command." | The Bash tool is stateless per call — an alias/function from one call is gone in the next. Call `git-kit` (or `GK_AGENT=1 git-kit`) directly every time. |
| "I'm in a worktree already, I'll just start another." | `EnterWorktree` refuses a nested create, and a `gk-parent` already set means you are mid-session. Land or exit first. |
| "A couple of unrelated dirty files can ride along." | `finish` auto-commits them via the kiro classifier as separate, unreviewed commits on the parent; gk's own gated path refuses dirty trees for exactly this reason. Gate on `git status --porcelain` first. |
| "Non-zero exit code, so the finish failed." | The shell exits 1 when cleanup removes the cwd even on `state:"ok"`, and gated finish uses exit 3 as its normal paused flow. Branch only on the `state` field. |
| "finish returned an error, so the worktree is junk — I'll remove it." | An error containing `exit 3` is a wrapped merge conflict: the merge is half-done inside the worktree. Preserve it and surface the conflict; do not discard. |
| "I'll pass ExitWorktree's message through to the user." | Its "preserved at <path>" claim points at a directory gk already deleted by `--cleanup`. Report from the finish JSON instead. |

## Red Flags

- You called `EnterWorktree` without recording the parent branch first.
- You judged `finish` by its exit code instead of the `state` field.
- You exited/removed the worktree after a finish `error` without checking for a wrapped conflict (`exit 3`).
- You relayed ExitWorktree's "preserved at" message to the user.
- You ran `finish` on a dirty tree without showing the file list to the user first.
- You pushed (`git push` / `git-kit land`) during `land` without the user asking.
- You put the session into a worktree when the user never said "worktree".
- You inlined a task-gate / panel review — that belongs to `/xm:build run --worktrees`, not here.
- You defined a shell alias/function and reused it across Bash calls.

## Verification

- After `start`: `git branch --show-current` is the new branch AND `git config --get branch.<new>.gk-parent` returns the original branch.
- After `land` success: `git-kit worktree finish` returned `state:"ok"` with `removed:true` (and `branch_deleted:true`), the parent branch now contains the worktree branch's commits (`git branch --contains` / the parent log shows them), the session cwd is back on the parent via `ExitWorktree(keep)`, and nothing was discarded.
- You never pushed unless the user asked.
- On a wrapped conflict (`error` containing `exit 3`) you stopped, preserved the worktree, and surfaced the resume/abort options instead of removing anything.
