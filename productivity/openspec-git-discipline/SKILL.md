---
name: openspec-git-discipline
description: Use when OpenSpec propose, continue, apply, verify, archive, branch, merge, or worktree timing affects git history.
license: MIT
compatibility: Codex lazy-loaded skill for git-backed OpenSpec projects.
---

**Project context preflight before workflow actions**: before this skill takes a workflow action, follow the `project-constitution` skill. Read root `CONSTITUTION.md` when present, enforce relevant project rules, stop on material conflicts, and follow the strict missing-constitution bootstrap/diagnostic policy. For architecture-sensitive work, also read `ARCHITECTURE.md`, `adr/README.md`, and relevant in-force `adr/*.md`. Read `.secrets.local.env` only when the current workflow actually needs a listed external system, and never reveal secret values.


# OpenSpec Git Discipline

Use this skill whenever OpenSpec lifecycle state changes or git timing affects the workflow.

Project policy: checkpoint discipline is mandatory. Every completed artifact or coherent apply group must be checkpointed before the next lifecycle phase depends on it. Safe scaffold/artifact/apply-group checkpoint commits run automatically by default when session git discipline is `auto`; manual mode can still require approval.

Core rule: every OpenSpec state change must cross `main` before the next
lifecycle phase depends on it.

- Proposal artifacts may be drafted on a branch, but must be committed and
  merged to `main` before apply starts.
- Apply may run on `main`, a branch, or a worktree only if that exact proposal
  state is already available on `main`.
- Archive should run from `main` after implementation is merged back.
- Safe lifecycle checkpoint commits may be created automatically in `auto` mode after the changed paths and commit message are shown.
- Never create branches, merges, pushes, pull requests, archives, destructive git operations, or hard-gate bypasses unless the user explicitly asks.

## Gates

Hard gates that always require explicit approval: branch creation, merge, push, pull request creation, archive, destructive git operations, dirty unrelated work, and any one-time override of a required gate.


- Before propose: prefer `main`; otherwise warn and ask whether to continue.
- During continue: checkpoint completed artifact changes according to session git mode before the next artifact consumes them.
- Before apply: run `git status --short` and verify planning artifacts are not
  only local uncommitted state.
- Before archive: run `git branch --show-current` and `git status --short`;
  stop if not on `main` or implementation has not been merged.
- After archive: ask the user whether to commit archive/spec sync changes because archive remains an explicit hard gate.

## Required Language

If proposal state has not reached `main`:

> I should not apply this yet because the planning change has not reached
> `main`. A proposal can be drafted on a branch, but apply must start only after
> that proposal state is available on `main`.

If archive is not running from merged `main`:

> I should not archive this yet because archive must run from `main` after
> implementation is merged back. Verify makes a change eligible to merge; it
> does not replace the merge.


## Mandatory Checkpoint Boundaries

Checkpoint after each of these boundaries before a later lifecycle phase depends on the result:

1. `openspec new change` creates a change directory.
2. Each planning artifact is created or materially updated: proposal, specs, grill, design, design-review, adr, test-plan, tasks.
3. Each coherent apply task group is completed and verified.
4. Verify produces an archive-ready assessment.
5. Archive moves the change and/or syncs specs.

At every checkpoint:

- run `git status --short`;
- summarize changed files;
- in automatic mode, use `scripts/openspec-git-checkpoint` when available for safe scoped checkpoint commits; in manual mode, ask before `git add`/`git commit`;
- always show affected paths, commit message, resulting commit hash, and re-check status;

## Override Policy

Overrides are allowed only when the user explicitly names or clearly confirms the gate being bypassed. An override is one-time and does not disable future gates. Record the override in the response with:

- gate bypassed;
- files/state trusted despite the gate;
- risk accepted;
- next checkpoint where normal discipline resumes.
