---
name: forge-worktrees
description: Forge safe-parallel-work playbook using git worktrees. Use when more than one Boss writes code in the same repo at once — parallel agents, worktree, isolate, avoid conflicts.
---

# Forge playbook — Safe parallel work via git worktrees

**Do not duplicate ECC skills — defer to:** `using-git-worktrees` (detect existing isolation → native
tools → git worktree fallback, mechanics and commands). This file is the Forge-specific orchestration
wrapper: when Forge reaches for isolation, and who owns merging the result back.

## Hard rules
- **Never let two agents write concurrently to the same working tree.** If Head Chef dispatches parallel
  Bosses on the same repo, each gets its own worktree/branch — no exceptions, per the project's
  parallel-vs-serial doctrine (`CLAUDE.md` → "Parallel vs serial").
- Detect existing isolation before creating anything new (per `using-git-worktrees` Step 0) — don't nest
  worktrees or fight a harness that already manages workspace lifecycle.
- Only isolate genuinely **independent** subtasks (reference `dispatching-parallel-agents`). Dependent
  steps stay serial in the main tree — a worktree does not make a dependency parallel-safe.
- Never force-push, reset --hard, or otherwise destructively touch the integration branch without
  explicit owner approval, even when resolving a merge conflict.
- A **non-source hotspot** (event registries, sync manifests, dashboard files, doctor/config) that doesn't
  warrant a full worktree still needs the `forge-lock-guard.cjs acquire`/`release` protocol around its
  dispatch (see `forge-router` Step 4) — lock-guard and worktree isolation are complementary safeguards,
  not either/or.

## When to isolate
- Head Chef is running two or more Bosses concurrently against the same repo (e.g. Build Boss + UI Boss
  on different modules of the same app in the same run).
- A large/risky change (major refactor, dependency upgrade) that should stay reviewable as its own diff
  before merging into the main line.
- Codex write-delegation (`/codex:rescue` or any `--write` task) — per `CODEX_GLOBAL_POLICY.md` (an owner-level policy in `~/.claude` when present; on an install without it, the defaults stated in this skill apply — read-only, never a blocker), Codex
  runs on a **separate worktree/branch**, never concurrently with Claude in the same tree.

Do NOT isolate: single-agent sequential work, trivial 1-2 file edits, or tasks with no real parallelism
(isolation overhead without benefit).

## Create & integrate
1. **Create.** Detect existing isolation first; otherwise create a worktree per independent Boss/agent
   (`git worktree add <path> -b <branch>`), scoped to that Boss's exact work package.
2. **Dispatch.** Each Boss works only inside its own worktree, on files relevant to its own package —
   commits stay scoped, no unrelated files bundled in.
3. **Integrate.** The Lead (Head Chef, or whichever Boss owns the integration for that run) merges each
   worktree's branch back into the target branch, resolving any conflicts itself rather than leaving them
   for the next agent.

## Lead is the integration layer
Per the project's standing rule, the agent coordinating parallel work is the one responsible for merging
it back cleanly — an individual Boss does not merge its own worktree into main unilaterally when other
parallel work is still in flight. The Lead verifies the assembled result (a real integration check, not
just "each worktree's own tests passed") before treating the parallel build as done.

## Cleanup
After a successful merge: remove the worktree (`git worktree remove <path>`) and delete the now-merged
branch if the project's convention is to prune merged branches. Never delete a worktree/branch that still
has unmerged, uncommitted, or unreviewed work without explicit owner confirmation.
