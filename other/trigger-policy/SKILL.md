---
name: trigger-policy
description: "Enforce FlowTrigger safety rules — no autonomous merge, no recursive trigger creation, max active triggers, allowed_actions / forbidden_actions ACLs. Validates trigger YAMLs at `<runtime dir>/triggers/*.trigger.yaml` against `schemas/v1/trigger.schema.json` AND cross-checks policy.forbidden_actions includes merge + release; refuses triggers that grant Tier 3 autonomy. Use when /flow:trigger enable, /flow:trigger run, /flow:run, or /flow:watch is invoked. This skill MUST be consulted because triggers can fire without user supervision — a trigger granting merge autonomy is the single fastest path to an untrusted-merge incident, and recursive trigger creation is the loop-bomb shape of the runtime layer."
allowed-tools: Bash, Read
agent: general-purpose
---

# Trigger Policy

## Contract

Iron law: `merge` and `release` MUST appear in every trigger's `policy.forbidden_actions` unless the user's own settings allow otherwise, and the tier hook still asks before any merge or release. Invoked in `validate` mode (read-only) by `/flow:trigger enable` and by `/flow:watch` (every mode) before a trigger YAML is kept or enabled, and in `enforce` mode by `/flow:run` step 3 and `/flow:trigger run` before the target command is dispatched. Returns the JSON report below with exit 0 (pass or soft warning), 1 (policy violation), or 2 (schema invalid); the caller aborts on non-zero. Permitted skips: none — every step runs; the only non-blocking outcome is `concurrency_warning`.

## Inputs

1. **Trigger YAML path** — a plugin template (`triggers/templates/`) or a project's `<runtime dir>/triggers/<id>.trigger.yaml` (`<runtime dir>`: `bin/flow-runtime-dir.sh` output).
2. **Mode** — `validate | enforce`.

## Output

A JSON report: `trigger_id`, `schema_valid`, one list per violation kind (`tier3_violations`, `recursion_violations`, `missing_required_forbidden`, `cross_reference_violations`, `concurrency_violations`) and `overall` (step 8). Example: `references/flow-triggers.md`.

## Steps

1. **Schema validation**: validate the YAML against `schemas/v1/trigger.schema.json` (one `SCHEMA_ERROR=` line per error). Exit 2 → `overall: schema_invalid`; exit 1 means the check could not run: stop.

   ```bash
   "$(__fr="${CLAUDE_PLUGIN_ROOT:-}";[ -x "$__fr/bin/cascade-resolve.sh" ]||__fr=$({ printf '%s\n' plugins/flow;ls -d "${CLAUDE_CONFIG_DIR:-$HOME/.claude}"/plugins/cache/synapti-marketplace/flow/*/ 2>/dev/null|sort -Vr;printf '%s\n' "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/plugins/marketplaces/synapti-marketplace/plugins/flow"; }|while read -r __p;do [ -x "${__p%/}/bin/cascade-resolve.sh" ]&&{ printf '%s\n' "${__p%/}";break;};done);printf '%s\n' "$__fr")/bin/flow-trigger-schema-check.sh" "${TRIGGER_YAML}"
   ```
2. **Tier 3 deny**: `policy.forbidden_actions` must contain `merge` and `release`, unless `flow.triggers.allowAutonomousMerge` is `true` in the user's settings, not a repository's; the tier hook still asks. Exit 2 → each `TIER3_VIOLATION=<action>` goes into `tier3_violations`, a hard fail; exit 1: stop.

   ```bash
   "$(__fr="${CLAUDE_PLUGIN_ROOT:-}";[ -x "$__fr/bin/cascade-resolve.sh" ]||__fr=$({ printf '%s\n' plugins/flow;ls -d "${CLAUDE_CONFIG_DIR:-$HOME/.claude}"/plugins/cache/synapti-marketplace/flow/*/ 2>/dev/null|sort -Vr;printf '%s\n' "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/plugins/marketplaces/synapti-marketplace/plugins/flow"; }|while read -r __p;do [ -x "${__p%/}/bin/cascade-resolve.sh" ]&&{ printf '%s\n' "${__p%/}";break;};done);printf '%s\n' "$__fr")/bin/flow-trigger-tier3-check.sh" "${TRIGGER_YAML}"
   ```
3. **Recursion policy**: `recursion_policy.triggered_runs_may_modify_triggers` and `_enable_triggers` must be `false` or unset; `_create_triggers` too, unless `flow.triggers.allowTriggerCreationFromTriggeredRun` is `true`. Exit 2 → each `RECURSION_VIOLATION=<flag>` goes into `recursion_violations`; exit 1: stop.

   ```bash
   "$(__fr="${CLAUDE_PLUGIN_ROOT:-}";[ -x "$__fr/bin/cascade-resolve.sh" ]||__fr=$({ printf '%s\n' plugins/flow;ls -d "${CLAUDE_CONFIG_DIR:-$HOME/.claude}"/plugins/cache/synapti-marketplace/flow/*/ 2>/dev/null|sort -Vr;printf '%s\n' "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/plugins/marketplaces/synapti-marketplace/plugins/flow"; }|while read -r __p;do [ -x "${__p%/}/bin/cascade-resolve.sh" ]&&{ printf '%s\n' "${__p%/}";break;};done);printf '%s\n' "$__fr")/bin/flow-trigger-recursion-check.sh" "${TRIGGER_YAML}"
   ```
4. **Allowed types**: `trigger.type` must be in `flow.triggers.allowedTypes` (cascade-resolved; default `[manual, hook, loop_prompt]`). Any other schema-valid type (`github_actions`, `local_cron`, `local_daemon`) not listed there → `tier3_violations`.
5. **Active-trigger count**: count `<runtime dir>/triggers/*.trigger.yaml` with `metadata.enabled: true` and lifecycle != disabled. If count >= `flow.triggers.maxActiveTriggers` (cascade-resolved; default 5), refuse to enable another.
6. **Concurrency sanity**: `cancel_previous` (from `concurrency.policy`, else `flow.triggers.defaultConcurrency`) on a trigger whose target pushes → `concurrency_violations` warning (a cancelled push can leave partial commits); never a hard fail.
7. **Target workflow cross-reference**: when `target.workflow` is set, the workflow must exist in the flow plugin, `PLUGIN_PATH="$(__fr="${CLAUDE_PLUGIN_ROOT:-}";[ -x "$__fr/bin/cascade-resolve.sh" ]||__fr=$({ printf '%s\n' plugins/flow;ls -d "${CLAUDE_CONFIG_DIR:-$HOME/.claude}"/plugins/cache/synapti-marketplace/flow/*/ 2>/dev/null|sort -Vr;printf '%s\n' "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/plugins/marketplaces/synapti-marketplace/plugins/flow"; }|while read -r __p;do [ -x "${__p%/}/bin/cascade-resolve.sh" ]&&{ printf '%s\n' "${__p%/}";break;};done);printf '%s\n' "$__fr")/workflows/${WF}.workflow.yaml"` (plugin-root resolution, `references/plugin-root-resolution.md`), or in the project, `LOCAL_PATH="$("${PLUGIN_PATH%/workflows/*}/bin/flow-runtime-dir.sh")/workflows/${WF}.workflow.yaml"` (`[ -f "$PLUGIN_PATH" ] || [ -f "$LOCAL_PATH" ]`). Missing → `cross_reference_violations.append({"type": "missing_target_workflow", "name": target_workflow, "checked_paths": [PLUGIN_PATH, LOCAL_PATH]})`. **Hard fail** (exit 1) — a trigger pointing at a non-existent workflow is broken by construction; this catches typos (`address` vs `address-pr`) at creation rather than when `/flow:run trigger <id>` dispatches. When `target.workflow` is absent (`target.command` only), this step is a no-op.
8. **Overall verdict**:

| Condition | overall |
|---|---|
| schema fails | `schema_invalid` (exit 2) |
| `tier3_violations` non-empty | `tier3_violation` (exit 1; HARD FAIL) |
| `recursion_violations` non-empty | `recursion_violation` (exit 1) |
| `cross_reference_violations` non-empty | `cross_reference_failed` (exit 1; HARD FAIL — missing target workflow) |
| `concurrency_violations` non-empty | `concurrency_warning` (exit 0 — soft warning) |
| else | `pass` (exit 0) |
