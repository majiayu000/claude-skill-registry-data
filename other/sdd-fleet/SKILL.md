---
name: sdd-fleet
description: >
  Launch, inspect, or tear down an isolated fleet of ready SDD Composy tasks: one
  branch and Git worktree per member, a bound LOOP, cmux/tmux/headless presentation,
  no automatic merge. Use to run several ready tasks in parallel — 'rodar várias
  tarefas em paralelo', 'lançar o fleet', 'fleet status', 'tear down member X'. Do
  NOT use for a single task (sdd-execute, sdd-loop) or for merging without the
  explicit teardown token.
metadata:
  version: 0.1.0
---

# SDD Fleet

Launch, inspect, and tear down an isolated fleet of approved SDD task contracts. Fleet accepts
only `ready` tasks from the canonical task projection of a human-approved TechSpec, with complete
dependencies, explicit acceptance criteria, known verification commands, and no confirmed path
overlap. It never infers approval and never merges fleet branches
automatically.

Language: when an operation emits human-facing summaries, run `scripts/sdd_language.py <repo-root>` and use the persisted language; on `not_initialized`, return it with `next_action: run_init`. Localization rules: `references/language.md`.

Interactivity belongs only to fleet: each member owns one task, one isolated worktree, and exactly
one existing bound LOOP; UI presentation never changes that binding or grants lifecycle authority.

## Operations

- `launch`: validate contracts and create recoverable branches and worktrees
  (`scripts/fleet/launch.sh --task .planning/sdd-composy/tasks/<prd-slug>.json`). Before launch,
  report the selected tasks, runtime, UI adapter, branch and worktree paths, verification
  commands, and safety checks. A headless launch runs unattended: pass `--human-approved
  --approved-by <kind:actor>` only after the human approved this exact run.
- `status`: inspect fleet and member records without changing state (`scripts/fleet/dashboard.sh`).
  It projects the authoritative member JSON as recorded, including unknown fields, without
  filling in missing optional fields and without any UI mutation. Terminal capture is
  diagnostic only and never satisfies an evidence, review, verification, or approval gate.
- `teardown`: stop a member's UI and runner, or merge a `completed` member only with `--merge
  --confirm CONFIRM-SDD-MERGE` after identity, base-branch, and result verification
  (`scripts/fleet/teardown.sh`).

`scripts/fleet/run.sh` runs a headless member's bound LOOP and publishes its result (a commit
restricted to `allowed_paths` when the LOOP completes). Provider command vectors live only in the
engine adapters listed in `references/runtime.md`; a runtime without an engine is `NOT_RUN`, never
a fallback. The UI adapter is presentation only: it never owns process lifecycle truth, and its
operations stay inside the workspace this fleet created. Prefer cmux when available, with tmux or
headless as explicit fallbacks.

Never read or adopt an existing `.env.fleet`; preserve recoverable branches and worktrees after
any failure. A pane, terminal capture, or UI state is never completion.

## Read when

- `references/fleet.md` — before `launch` or `teardown`, for the launch gate, headless result,
  record schema, Compose, and merge rules.
- `references/cmux.md` — the selected UI is cmux.

Safety: Do not commit, push, or publish. Do not read or expose `.env`, credentials, tokens, private keys, certificates, or fleet environment files. Full contract: `references/safety.md`.
