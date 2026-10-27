---
name: git-worktree-generic
description: "Create, manage, and clean up git worktrees using native git commands only. Works with any language, any repo, any platform — no custom scripts, no framework assumptions, no workspace-specific conventions. Use when the user says: 'create a worktree', 'worktree session', 'parallel branches', 'work on multiple features', 'new branch without switching', 'clean up worktree', 'remove worktree', 'git worktree', 'detached worktree', or any request involving working on two branches at once."
---

# Git Worktree (Generic)

Use git worktrees to run parallel development sessions without switching branches or stashing changes. Each worktree is an independent working copy linked to the same repository.

This skill uses **only native `git worktree` commands**. Optional helper scripts are in `scripts/` for convenience but are never required.

---

## Prerequisites

- Git 2.5+ (worktree support)
- A clean repo on the integration branch (usually `main`, `master`, or `develop`)

---

## Core Concept

```
Primary repo (integration surface, read-only during sessions)
├── .git/
├── src/
└── ...
    └── .worktrees/          ← sibling directory (auto-created by git worktree add)
        ├── feature-login-redesign/
        │   └── (full working copy, own index, own branch)
        └── hotfix-urgent-patch/
            └── (full working copy, own index, own branch)
```

- **Primary repo** = integration surface. Never edit directly during a session.
- **Worktree** = disposable working copy. Edit, build, test, commit here.
- **One branch per worktree** — never share a branch across worktrees.

---

## Naming Conventions

| Use case | Branch pattern | Example |
|---|---|---|
| Feature work | `feature/<date>-<slug>` | `feature/250715-login-redesign` |
| Fix/bug | `fix/<date>-<slug>` | `fix/250715-null-pointer` |
| Experiment | `experiment/<slug>` | `experiment/rust-backend` |
| OpenSpec delta | `openspec/<date>-<slug>` | `openspec/250726-add-pagination` |
| Release | `release/<version>` | `release/2.5.0` |
| Hotfix | `hotfix/<slug>` | `hotfix/login-timeout` |

Use `YYYYMMDD` date prefix to keep branches sorted and avoid collisions.

Slash (`/`) in branch names becomes dash (`-`) in worktree folder names:
- `feature/250715-login-redesign` → folder `feature-250715-login-redesign`
- `hotfix/login-timeout` → folder `hotfix-login-timeout`

---

## Quick Start

```bash
# 1. Fetch latest and create a detached worktree from the integration branch
git fetch origin
git worktree add --detach ../<repo>.worktrees/<branch-as-folder> origin/main

# 2. Enter the worktree and create your task branch
cd ../<repo>.worktrees/<branch-as-folder>
git checkout -b feature/250715-login-redesign

# 3. Work normally (edit, build, test, commit)
git add . && git commit -m "feat(login): redesign login page"

# 4. Stay up to date
git fetch origin && git rebase origin/main

# 5. Merge back (from primary repo)
cd <primary-repo>
git merge --no-ff feature/250715-login-redesign

# 6. Clean up
git worktree remove ../<repo>.worktrees/feature-250715-login-redesign
git worktree prune
git branch -d feature/250715-login-redesign
```

> **Why `--detach` first?** Creates the worktree from a clean base ref even when the primary repo has uncommitted changes. Branching happens inside the clean worktree.

---

## Guardrails

| Rule | Why |
|---|---|
| One branch per worktree | Prevents confusion and merge conflicts |
| Never edit the primary repo during a session | The primary repo is the integration surface |
| Create worktree detached first | Works even when the primary repo has dirty state |
| Always rebase before merging | Keeps history linear and clean |
| Merge with `--no-ff` | Preserves branch topology for traceability |
| Remove worktrees after merging | Avoids stale working copies and disk waste |
| No merging task branches into each other | Always merge into the integration branch |
| Lock worktrees you want to protect | `git worktree lock <path>` prevents accidental removal |

---

## Safety Protocol

### Pre-action verification (three checks)

Before edit/build/test/commit when worktrees exist:

1. **Inside the worktree?** `pwd` must resolve under the worktree path, not the primary repo's root.
2. **Correct branch?** `git rev-parse --abbrev-ref HEAD` must show the task branch, not the integration branch.
3. **Correct repo root?** `git rev-parse --show-toplevel` must resolve under the worktree path.

> If any check fails, stop. The primary repo is **read-only** during a session.

For full recovery procedures (wrong-worktree recovery, dropped changes, conflict handling), see [references/safety-protocol.md](references/safety-protocol.md).

---

## Common Operations Reference

| Action | Command |
|---|---|
| List active worktrees | `git worktree list` |
| List in scriptable format | `git worktree list --porcelain` |
| Create detached worktree | `git worktree add --detach <path> <base-ref>` then `git checkout -b <branch>` |
| Lock a worktree | `git worktree lock <path>` (prevents accidental removal) |
| Unlock a worktree | `git worktree unlock <path>` |
| Remove a worktree | `git worktree remove <path>` && `git worktree prune` |
| Force-remove (uncommitted) | `git worktree remove --force <path>` && `git worktree prune` |
| Find merged branches | `git branch --merged <integration-branch>` |
| Move a worktree | Not supported — remove and recreate |

---

## QA Evidence & Binary Artifact Preservation

Files committed in the worktree survive through the merge. Gitignored binary artifacts (screenshots, videos, compiled binaries, logs) do not — copy them to the primary repo before worktree removal.

For detailed guidance, see [references/qa-evidence.md](references/qa-evidence.md).

---

## Detailed Workflow Examples

End-to-end walkthroughs with full context (create, rebase, integrate, conflict resolution): see [references/workflow-examples.md](references/workflow-examples.md).

---

## Optional Automation Scripts

This skill provides optional PowerShell scripts in `scripts/` to automate repetitive multi-step workflows. They are **never required** — every operation is achievable with native git commands — but they reduce copy-paste effort and enforce consistency.

| Script | What it does | Key parameters |
|---|---|---|
| `New-GitWorktreeSession.ps1` | Fetches origin, creates detached worktree, creates task branch | `-Slug` (required), `-Mode` (feature/fix/experiment/openspec/release/hotfix/branch), `-BaseBranch`, `-SessionId`, `-Branch`, `-WorktreeName`, `-SyncBase`, `-BootstrapCommand` |
| `Integrate-GitWorktreeBranch.ps1` | Rebases onto integration branch, merges with configurable mode, optionally pushes | `-Branch` (required), `-BaseBranch`, `-MergeMode` (NoFastForward/FastForwardOnly/Squash), `-SkipFetch`, `-SkipRebase`, `-ValidationCommand`, `-Push` |
| `Remove-GitWorktreeSession.ps1` | Removes worktree, prunes, optionally deletes local branch | `-Branch` or `-WorktreePath` (required, mutually exclusive), `-BaseBranch`, `-DeleteBranch`, `-Force` |

See each script's `--help` for usage examples.

---

## Comparison: Native Git vs Scripted Approaches

| Aspect | Native git commands (primary) | Optional scripts |
|---|---|---|
| Setup | Zero — git only | Clone the skill or copy scripts |
| Portability | Works everywhere git works | PowerShell (Windows; cross-platform via pwsh) |
| Learning curve | Uses familiar git commands | Learn script parameters |
| Automation | Manual copy-paste | One command per workflow |
| Consistency | Depends on operator discipline | Enforced by script logic |

Use the native approach when you want zero dependencies beyond git. Use scripts when you perform the same multi-step workflow repeatedly.
