---
name: ls-herdr-pane-layout
description: "Create temporary Herdr panes below the caller, resize and move owned panes, and clean up without stealing focus or overwriting user layout changes. Start with ls-herdr-task-routing."
metadata:
  version: "1.1"
---

# Herdr layout

Read the master first if it is not already loaded:
[ls-herdr-task-routing](localsetup://package/ls-herdr-task-routing/SKILL.md)

Use `localsetup herdr pane --help` for the current argument contract.

For a temporary work area in the caller's managed pane:

```bash
localsetup herdr --workspace "$HERDR_WORKSPACE_ID" --pane "$HERDR_PANE_ID" \
  --state-dir "$task_state" pane ensure --cwd "$PWD"
```

Here `task_state` is the existing task's absolute private state directory.
Keep the returned `result.owner_id` and `result.pane.pane_id`. Pass that owner
back as `pane ensure --owner-id <owner-id>` to reuse the same verified pane,
or `pane cleanup <owner-id>` when finished. Read the handles from JSON; do not
predict IDs or clear a pane after a reuse conflict.

## Pick the outcome

- **Temporary work area:** ensure one task-owned child below the explicit caller,
  keeping the caller's working directory and user focus. Reuse a verified owned
  idle child for the same task rather than repeatedly splitting.
- **More room for output:** resize the owned split. Honor requested direction or
  dimensions; let the deterministic planner constrain geometry. Do not rebalance
  unrelated panes to make a task fit.
- **Move work:** move the owned pane to the requested explicit destination and
  continue with the returned pane ID. Cross-workspace moves change IDs.
- **Finish:** clean up only verified owned panes with no active or uncertain
  operation. Leave a pane with a useful continuing server or agent running when
  that is the task's intended result.

The default temporary split is downward at 30%, without focus. If the geometry
cannot support the request, report the concrete space limit and available
owned-pane alternatives. Do not silently create a new workspace or worktree.

Managed sudo operations use the shared `ls.core.terminal_ops` lifecycle rather
than this general temporary-pane route. They look up the exact controller's
child before creating a one-third-height lower pane and bind native identity,
machine, directory and controlled Bash readiness. Never adopt a similarly
named pane or clear unknown input. The root label is `<repo>-sudo`; an admitted
host checkout uses `<repo>-<exact-host-alias>-sudo`.

## Preserve the operator's work

The tool records endpoint, parent, child, ownership, and relevant geometry.
Use those records instead of pane labels as ownership proof. A label identifies
display intent; it is not authorization to close or replace the occupant.

Restore prior geometry only when the affected topology still matches the
tool's expected layout. Never apply a stale whole-tab snapshot after a user
resize, move, or split. If ownership, occupant, or a mutation result is uncertain,
inspect read-only and retain the record; do not close a guessed pane.

Use native JSON IDs and the shared core. Never resize through screenshots,
keyboard simulation, sidebar order, or duplicated client-specific algorithms.
