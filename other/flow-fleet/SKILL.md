---
name: flow-fleet
description: Launch, inspect, and tear down autonomous phase fleets in isolated Git worktrees, on the Codex or the Claude runtime. Use when approved Flow phase slugs should run in parallel, when fleet status is requested, or when a fleet member must be stopped or explicitly merged.
---

# Operate a Flow Fleet

Read [fleet](../../references/fleet.md), [safety](../../references/safety.md), [artifacts](../../references/artifacts.md), and [collaboration](../../references/collaboration.md) before acting.

## Route

Interpret only these routes:

- `<slugs>`: launch one or more approved lowercase phase slugs.
- `--status`: invoke packaged `fleet-dashboard.sh --once`.
- `--teardown <slug>`: invoke packaged `fleet-teardown.sh <slug>` and preserve its branch and worktree.
- `--teardown --all`: enumerate validated `.planning/flow/fleet/<slug>.json` entries and invoke packaged teardown once per slug.

Pass `--merge` to teardown only when the user explicitly requests it. Never merge a non-`DONE` member or translate state into legacy paths.

## Launch

1. Inspect repository status, confirm a named current branch, inspect `.planning/flow/config.json`, and inspect the requested approved `spec.md` and `decisions.md` contracts. Never read `.env.fleet`.
2. Resolve scripts from this installed skill at `../../scripts/`; call only packaged fleet and audit scripts for lifecycle operations.
3. Use the launcher of the runtime you are running as, and never the other one. The runtime is fixed by that choice, is recorded in the central member, and is refused by a runner bound to a different one. Before the first launch, display the exact autonomous command shape of that runtime:

   Codex — `fleet-up.sh`:

   ```text
   codex exec --dangerously-bypass-approvals-and-sandbox --ephemeral --cd <worktree> --output-schema <fleet-result-schema> --output-last-message <result-file> <autonomous-prompt>
   ```

   Claude — `claude-fleet-up.sh`:

   ```text
   claude -p --dangerously-skip-permissions --no-session-persistence --output-format json <autonomous-prompt>
   ```

4. Require explicit acknowledgement of the dangerous flag of that runtime — `--dangerously-bypass-approvals-and-sandbox` for Codex, `--dangerously-skip-permissions` for Claude. Do not persist a missing fleet block or launch a member before acknowledgement. Reject a configured `permission_mode` other than `danger-full-access`.
5. After acknowledgement, require the configuration root and any existing `.fleet` value to be objects. Reject an existing `permission_mode` unless it is exactly `danger-full-access`; require the exact JSON boolean `auto_simplify: false` and exact packaged Compose filename before launch.
6. Merge the exact defaults from [fleet](../../references/fleet.md) into both absent and partial fleet blocks with `jq`: set `.fleet = ($fleet_defaults * (.fleet // {}))`. Write through a same-directory temporary file and atomically rename it only after validation. This defaults-first recursive merge fills missing known fields while every existing known or unknown field wins; never overwrite permission mode to dangerous.
7. For multiple slugs, compare their specification and decision text for repeated repository paths. Emit an advisory overlap warning with the matching paths; let the human decide and never block automatically.
8. Invoke the packaged launcher of your runtime once per acknowledged slug — `fleet-up.sh <slug>` as Codex, `claude-fleet-up.sh <slug>` as Claude. Either one binds exact contract hashes and initiating branch/base identity, records the runtime, and rejects unsafe symlinked state paths. Both route their tmux pane to the same autonomous runner, which owns locks, process-group ownership, structured result validation, per-stage commits, and the two-cycle correction cap. Stop launching further members after any failure and report the recovery state.

## Report

Invoke the one-shot dashboard and report each slug, worktree, app/database ports, stage, status, branch, and concise message. Do not load or reproduce full fleet logs, prompts, or result payloads. When audit is enabled, record only the allowed semantic metadata described in [audit](../../references/audit.md).
