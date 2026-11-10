---
name: clarila-issue
description: "Read, create or enrich a GitHub issue and its acceptance criteria when asked to prepare or update an issue. Does not select engineering priority, implement a fix or close issues without authorization."
---

# Prepare a precise issue

Read the [shared workflow contract](../clarila/references/contract.md) before substantive work. This skill is part of the locally installed Clarila suite. Its source is in `~/Developer/skills`; resolve sibling skills relative to this directory.

## Procedure

1. Read the current issue, supplied report and repository issue conventions. Verify repository identity, current disposition, assignee and any existing covering issues or PRs.
2. Separate observed facts from hypotheses. Describe the affected user/system flow, expected and actual behavior, environment, reproducible steps, impact and acceptance criteria. Mark unrun scenarios and unavailable source identity.
3. For a complex issue, identify bounded child outcomes and dependencies. Link existing issues before proposing new ones. Do not create issues merely to give monitoring or internal coordination a forum home.
4. Prepare readable title/body using the repository template. Preserve useful existing text. A create/edit request authorizes only its stated issue change; use gh with structured input or a body file and verify provider readback.
5. Register or associate the issue workflow and request forum reconciliation. Issue publication, thread creation and worker execution are separate outcomes.

## Make acceptance observable

Express each material acceptance condition as a scenario with its input/action, expected result and evidence needed to check it. Tie the reported failure to a reproducible source/environment when available. Keep an unresolved cause as a hypothesis and identify the missing observation.

Before a requested create/edit, check covering work and retain the exact intended body and target. Read back the resulting issue and compare the requested fields. A partial or uncertain write keeps its existing intent for reconciliation. Link the next responsible role and its required input in the handoff.

## Synchronization and handoff

Resolve the same issue/workspace/session association before substantive work, including direct invocation. Read and update the private handoff described in the shared contract using available native file tools. Record the actual stage, source, findings, evidence, outcome and next action. If no native session identity is available, retain an unbound record.

## Deliverable

Return the verified issue identity, body or authorized provider change, acceptance criteria, unresolved questions and related work.

Load only the relevant specialist from the [catalog](../clarila/references/catalog.md). Missing tools change the available evidence, never its meaning.

Read the [operation-specific reference](references/issue.md) when performing this responsibility.
