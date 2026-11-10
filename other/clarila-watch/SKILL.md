---
name: clarila-watch
description: "Perform an on-demand operational, workflow-health or incident check and report actionable observations. Not a permanent monitoring agent or automatic incident repair."
---

# Observe and explain current health

Read the [shared workflow contract](../clarila/references/contract.md) before substantive work. This skill is part of the locally installed Clarila suite. Its source is in `~/Developer/skills`; resolve sibling skills relative to this directory.

## Procedure

1. Resolve the requested system/workflow, environment, time window and authoritative sources.
2. Read current provider/session/CI facts with official CLIs or supported native tools. Check freshness and complete coverage before interpreting counts.
3. Distinguish production incidents from preview/simulator/internal failures, and liveness from source or product correctness.
4. Report meaningful changes, affected scope and concrete next diagnostic action. A recurring count cannot reopen closed work or prove fix inclusion.
5. Store observations and route an explicitly requested investigation through existing ownership. Do not restart workers, deploy, or claim recovery from zero errors alone.

Retain the requested target, time window, cohort/version filters and collection coverage with each observation. If a page budget, permission failure or provider backoff leaves part unread, describe that scope as incomplete even when returned pages contain zero errors. Keep the latest attempted check separate from the last successful complete check. Name the next bounded read or missing capability that would resolve the gap.

For Expo observations, follow the official [Observe query guidance](https://github.com/expo/skills/blob/a9e5bd3fa00b4e61f632e43f85da73aee1942582/plugins/expo/skills/eas-observe/SKILL.md) and verify metric units and cohort applicability with its current documentation. Use the owner's required official CLI lane.

## Synchronization and handoff

Resolve the same issue/workspace/session association before substantive work, including direct invocation. Read and update the private handoff described in the shared contract using available native file tools. Record the actual stage, source, findings, evidence, outcome and next action. If no native session identity is available, retain an unbound record. Use the current host’s native tools during the invoked workflow.

## Deliverable

Return current health observations, freshness/coverage, actionable changes and next checks.

Load only the relevant specialist from the [catalog](../clarila/references/catalog.md). Missing tools change the available evidence, never its meaning.
