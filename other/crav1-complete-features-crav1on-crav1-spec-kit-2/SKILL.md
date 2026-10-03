---
name: crav1-complete-features
description: >-
  Serial board: build several ready specs one slug after another in this
  checkout. Each slug is feat/<slug> from default, then the complete-tasks
  T# loop. Not parallel. One slug: use /crav1-complete-tasks. Do not push.
  Do not open a PR.
disable-model-invocation: true
icon: list
color: green
---

# Orchestrate several features (serial)

You **manage** a queue of **slugs**. You do **not** implement, verify, or `git commit` in this chat.

Each slug is one feature: `docs/specs/<slug>/` + branch `feat/<slug>` created from the **default** branch (not from the previous feature). Inside a slug, reuse the `/crav1-complete-tasks` loop: one **crav1-complete-task-agent** worker per `T#`, one at a time.

This is **not** parallel. Two `feat/` branches cannot share this working tree. True parallel (handoff / worktrees / Cloud Agents) is **out of scope** for this skill.

Command: `/crav1-complete-features`. One spec: `/crav1-complete-tasks`. One task: `/crav1-complete-task`.

Worker: `.cursor/agents/crav1-complete-task-agent.md` (plugin: `agents/crav1-complete-task-agent.md`). Protocol: `crav1-complete-task` [references/run.md](../crav1-complete-task/references/run.md). Style: [style-persist.md](../crav1-complete-task/references/style-persist.md). Approvals: [tool-approvals.md](../crav1-complete-task/references/tool-approvals.md). Branch rules: `/crav1-feature-branch` (drop-in: `.cursor/skills/crav1/crav1-feature-branch/SKILL.md`; plugin: sibling `skills/crav1-feature-branch/SKILL.md`).

## Which slugs

| They typed | Queue |
| --- | --- |
| `auth-login billing` / comma-separated | Those slugs, in that order |
| No names / “all” / “rest” | Every **ready** slug (below), `docs/specs/` directory order |

**Ready** (all must hold):

- Folder `docs/specs/<slug>/` with `spec.md`, `plan.md`, `tasks.md` (not `_template/`)
- At least one `- [ ]` in `tasks.md`
- Those spec files exist **on the default branch** (`git show <default>:docs/specs/<slug>/spec.md` works). If they exist only on `spec/<slug>` or only in this dirty tree, **skip** with reason: merge specify-only first
- Not a landscape-only path (`docs/system/` is not a slug)

If the queue has **0** slugs: stop. If it has **exactly 1**: stop and tell them `/crav1-complete-tasks` with that spec attached.

Unknown names: list, continue with the rest. Empty after skips: stop.

## Overlap (warn, then continue)

Before the first worker, union `plan.md` **Files likely touched** for queued slugs. If two slugs share paths (or clearly the same area), **warn** with the paths. Serial still runs in listed order (later merge/PR conflict is their problem). Do not drop a slug unless they say drop/skip.

## Style once

Before anything else that needs git commit, follow **style-persist.md**. If you must ask, this turn is style only.

Do not ask again per slug or `T#`. Workers must not ask style.

## Consent to branches (once)

Starting this command **is** consent to use `feat/<slug>` from **default** for each queued slug, in order. Do **not** re-run the feature-branch questions tool per slug.

One confirm if they are still on the default branch or on an unrelated branch: **continue** (first/top) = proceed with that checkout plan; **stop** = abort. If already on `feat/<first-slug>`, start there.

If currently on `spec/<anything>`: stop. No workers. Follow feature-branch **Build on a spec-only branch**.

## Tool approvals (once for the whole board)

Follow [tool-approvals.md](../crav1-complete-task/references/tool-approvals.md) **once before the first worker** (you are an orchestrator, same as complete-tasks).

Pass **`approvals: already-done`** and **`branch: already-done`** to every worker. Workers and nested `/crav1-complete-task` must **not** pause. Do not start a nested `/crav1-complete-tasks` skill (it would pause again); run its **T# loop yourself**.

Cloud Agents: skip the pause.

## Switch to a slug (before that slug’s first T#)

Default branch: same detect as feature-branch (`origin/HEAD`, else `main` / `master` / `develop`).

1. Working tree dirty except `agent-tools/` → **do not checkout**. Tell them `/crav1-finalize-commit` (or they clean it). Wait. Never stash unless they ask.
2. `git checkout <default>` then `git checkout feat/<slug>` if it exists, else `git checkout -b feat/<slug>` **from default**. Never create `feat/<slug>` from the previous feature branch.
3. If checkout fails, **block** this slug; do not start the next unless they skip.
4. Never `git push`. Never open a PR. Never `git commit` in this chat.

After a slug’s last worker, the tree should be clean (workers commit). Then switch to the next slug with this same procedure.

## Board (keep this updated)

```text
slug          branch           T#s      status
auth-login    feat/auth-login  T1–T4    running T2
billing       feat/billing     T1–T6    queued
```

Status: `queued` | `running` | `needs_fix` | `needs_ready` | `done` | `blocked` | `skipped`.

## Per slug (you stay in this chat)

For each queued slug, after switch:

Run the complete-tasks **T# loop** on **this** slug’s `tasks.md` (all remaining `- [ ]` unless they named a range **for that slug** — v1: all unchecked on that slug).

1. Launch **crav1-complete-task-agent** with this spec folder, this `T#`, `resume: start`, `approvals: already-done`, `branch: already-done`, style already set.
2. Wait for STATUS. Do not implement. Do not start `T+1` or the next slug while this worker is open.
3. Handle STATUS:

| STATUS | Orchestrator |
| --- | --- |
| `done` | Next `T#` on **this** slug. If no unchecked left → slug `done`, switch to next slug. |
| `needs_fix` | Ask `fix` / `skip-slug` / `stop`. `fix` → same `T#` worker `resume: fix`. |
| `needs_ready` | Ask them to refresh the live host, then `ready` / `skip-slug` / `stop`. `ready` → `resume: ready`. |
| `blocked` / `failed` | Slug `blocked`. **End the board.** Do not start the next slug. |
| User `skip-slug` | Mark skipped. Switch to next slug (if any). |
| User `stop` | End the board. |

Do not skip a blocked slug unless they `skip-slug`.

## After the board

TL;DR: slugs `done` / `blocked` + why / `skipped` / not started; which `feat/<slug>` tips you left on; commits workers reported.

Remind: **no push, no PR** from this skill. Next (optional): `/crav1-open-pr` when you want to push and open the PR (one PR per `feat/<slug>`; do not run it here).

Then **tool-approvals.md → Undo** once. Do not undo per slug or per `T#`.

## Hard rules

- Orchestration only: no product edits, no `git commit`, no push, no PR, no `spec.md` edits.
- Serial slugs. Serial `T#`s inside a slug. Never two workers at once.
- `feat/<slug>` always from **default**, never from the previous feature.
- Do not implement on `spec/<slug>`.
- Do not flatten the board into one implement pass.
- Do not invent Mode B (handoff/worktrees/Cloud Agents) in this skill.
