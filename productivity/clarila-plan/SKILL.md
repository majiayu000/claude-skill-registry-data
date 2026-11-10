---
name: clarila-plan
description: "Develop a technical implementation plan for an issue with meaningful dependencies or uncertainty. Use when technical decomposition is needed, not as a mandatory predecessor for every small bug."
---

# Plan a checkable implementation

Read the [shared workflow contract](../clarila/references/contract.md) before substantive work. This skill is part of the locally installed Clarila suite. Its source is in `~/Developer/skills`; resolve sibling skills relative to this directory.

## Procedure

1. Resolve the accepted spec, current source and covering work. Inspect actual entry points, callers, stored data and repository test/build commands. Map the files that own each responsibility before proposing new ones. Distinguish observed source from planned additions.
2. Read [executable planning](references/executable-plan.md). Record the outcome and shared constraints once, preserving exact names, values, versions and public contracts fixed by the request. Choose the smallest design and explain only material tradeoffs.
3. Split the work into changes a fresh engineer can implement and verify independently. Keep a changed public signature and all affected callers in the same task so its checkpoint compiles and can be tested. State each task's prerequisites, responsible role, exact files, consumed and produced interfaces, concrete actions and expected results. Keep one implementation writer per workspace and fold setup into the deliverable it enables.
4. Plan compatibility and state transitions where the change affects data or external effects. Cover existing rows/callers, failed persistence, retries and concurrency when applicable. Keep queue acceptance, worker execution and external delivery tied to their own evidence. Preserve existing uncertain intents and holds.
5. Map requirements and meaningful original, negative and control cases to their owning tasks. Give the actual command and observable success condition for each check. Name unavailable provider/device/artifact prerequisites and continue the parts that can be planned from current evidence.
6. Self-review requirement coverage, dependency order, interface consistency and proportion. Name the first unblocked action and its completion observation. Save the readable plan at the user's requested location or the existing private task-output location, with source/spec references and remaining decisions. A plan-only request ends with that deliverable. Existing execution authorization continues within its original scope.

## Synchronization and handoff

Resolve the same issue/workspace/session association before substantive work, including direct invocation. Read and update the private handoff described in the shared contract using available native file tools. Record the actual stage, source, findings, evidence, outcome and next action. If no native session identity is available, retain an unbound record. Use the current host’s native tools during the invoked workflow.

## Deliverable

Return a source-bound design, dependency-ordered tasks with exact interfaces and checks, requirement coverage, the first executable action and unresolved decisions.

Load only the relevant specialist from the [catalog](../clarila/references/catalog.md). Missing tools change the available evidence, never its meaning.
