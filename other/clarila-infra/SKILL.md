---
name: clarila-infra
description: "Investigate and implement a scoped infrastructure or environment repair. Use for service configuration, routing, safe reload and rollback, and proving the original service stays available when a candidate fails."
---

# Repair the identified infrastructure path

Read the [shared workflow contract](../clarila/references/contract.md) before substantive work. This skill is part of the locally installed Clarila suite. Its source is in `~/Developer/skills`; resolve sibling skills relative to this directory.

## Procedure

1. Read the issue, actual environment, repository instructions and ownership. Distinguish local, preview, staging and production.
2. Diagnose with bounded read-only checks and safe redacted output. Identify the failing component and unaffected control.
3. Prepare the smallest configuration/code change with explicit target, blast radius, validation and rollback where relevant.
4. Apply only authorized changes. Preserve credentials, running services, unknown operations and unrelated configuration.
5. Verify the affected function with actual checks. A restart alone is not recovery. Hand off any production action separately.

## Make the repair recoverable

Follow one failing operation across its actual process, configuration, dependency and output boundaries. Establish a narrow health or behavior check and an unaffected control before the change. Record the exact owned process/service and the settings or bytes to replace.

For a cutover that can fail partway, choose the transaction or rollback points before applying it. Reconcile observed effects before retrying the same operation. Verify the requested function under the resulting process and configuration, then retain the executed check, rollback location and any unresolved dependency.

For reloads, replacement processes or interrupted configuration changes, read [service cutover decisions](references/service-cutover.md). Resolve `pstack-debugging` for an unresolved cause or `pstack-architecture` for a shared-state design decision through the [expert catalog](../clarila/references/expertise.md); these do not start a panel or widen operational authority by themselves.

## Synchronization and handoff

Resolve the same issue/workspace/session association before substantive work, including direct invocation. Read and update the private handoff described in the shared contract using available native file tools. Record the actual stage, source, findings, evidence, outcome and next action. If no native session identity is available, retain an unbound record.

## Deliverable

Return diagnosis, scoped changes, executed environment checks and outstanding operational actions.

Load only the relevant specialist from the [catalog](../clarila/references/catalog.md). Missing tools change the available evidence, never its meaning.
