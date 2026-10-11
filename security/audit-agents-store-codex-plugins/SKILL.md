---
name: audit
description: 'Full fleet audit in an isolated agent — one prioritised report with a ready repair line under every finding Arguments: [selector] [--focus auth|versions|memory|cron|secrets|security|shared|all].'
---

# OpenClaw fleet audit

Read-only, end to end. Nothing here changes an instance.

Parse `[selector]` (default: managed) and `[--focus …]` (default `all`) from "$ARGUMENTS".

It runs in an agent for cost, not subject: minutes of probes, fetches and intermediate output that
would be noise here. `/openclaw-ops:status` stays in the conversation. The full contract the agent
works under is `agents/openclaw-fleet-auditor.md`.

## Process

1. **Load the model** — `Skill` `fleet-model` for the selector grammar and the four states, then
   `fleet-diagnostics` for the catalog that every finding must resolve to.

2. **Resolve the target set** (reads may use `all`):
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/fleet.py" resolve "<selector>" --table
   ```
   Exit 2 = no usable config, run `/openclaw-ops:init` first. Exit 4 = nothing matched; stop.

3. **Collect the deterministic evidence yourself**, so the agent interprets rather than gathers:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/healthcheck.py" "<selector>" --snapshot --json > /tmp/oc-health.json
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/versions.py"   "<selector>" --json         > /tmp/oc-versions.json
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/report.py" --input /tmp/oc-health.json \
       --versions /tmp/oc-versions.json --compare-with auto --format md > /tmp/oc-report.md
   ```
   Exit 5 means a `critical` or `high` finding exists, 6 means `warn` only — that is the payload, not
   a failure. Skip the versions call only when `--focus` excludes it; skip nothing else, because a
   focus narrows attention and never the evidence.

4. **Dispatch the auditor** — `Task` with `subagent_type: openclaw-fleet-auditor`, handing it the
   selector, the focus, and the three artefact paths. Restate the contract it already carries:
   read-only, every finding on a catalog id or a verbatim upstream `checkId`, anything else cited.

5. **Present what comes back**, unchanged in substance and ordered by severity, then by
   `criticality` of the instance carrying it. Under each finding print the exact line:
   `/openclaw-ops:repair <instance> --issue <finding-id>`. A finding with no catalog row is printed
   as **not repairable yet** with what its row would need — never with an improvised fix.

6. **Name what the delta says**: findings new since the last snapshot, findings resolved, and
   findings nobody has moved on for weeks. The last group is the most useful section of the report
   and the easiest to skip.

## Constraints

- The audit proposes; `/openclaw-ops:repair` and `/openclaw-ops:update` dispose. Never apply a fix
  from inside this command, and never add `--yes` to a line you just printed.
- The report is the most-copied artefact this plugin produces: it carries fingerprints, presence and
  expiry dates, never a secret value.
- An unreachable or alien instance appears in the report as a row with its reason. Silent omission
  is the one failure mode an inventory tool is not allowed to have.