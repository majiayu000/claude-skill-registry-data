---
name: clarila-reproduce
description: "Reproduce a reported bug or check whether it still exists using source, browser, API or device evidence. Use for investigation before repair; does not implicitly authorize product edits."
---

# Establish the actual failure

Read the [shared workflow contract](../clarila/references/contract.md) before substantive work. This skill is part of the locally installed Clarila suite. Its source is in `~/Developer/skills`; resolve sibling skills relative to this directory.

## Procedure

1. Read the original scenario and acceptance criteria. Pin source, environment, prerequisites, account fixture and artifact where relevant. Inspect the responsible code path before choosing the reproduction.
2. Execute the original case in a permitted controlled environment. Record method, inputs, observations, exit/results and retained evidence. If a device, account or artifact is missing, report the exact prerequisite.
3. Run relevant negative and unaffected controls to distinguish the claimed defect from environment failure, intended behavior or an already-fixed scenario.
4. Narrow the responsible path and competing explanations using actual observations. Do not change product source in this read-only mode or upgrade a hypothesis to a finding.
5. Save a source-bound report and useful real media. Hand off reproduction steps and controls to the responsible engineer.

## Synchronization and handoff

Resolve the same issue/workspace/session association before substantive work, including direct invocation. Read and update the private handoff described in the shared contract using available native file tools. Record the actual stage, source, findings, evidence, outcome and next action. If no native session identity is available, retain an unbound record. Use the current host’s native tools during the invoked workflow.

## Deliverable

Return reproduced, not reproduced or inconclusive, with exact scenario/source/environment, controls, evidence and missing prerequisites.

Load only the relevant specialist from the [catalog](../clarila/references/catalog.md). Missing tools change the available evidence, never its meaning.

Read the [operation-specific reference](references/scenario.md) when performing this responsibility.
