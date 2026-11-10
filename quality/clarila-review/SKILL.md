---
name: clarila-review
description: "Review a candidate code diff locally, or run an explicitly requested iterative Codex review loop on an existing GitHub PR. Use for code assessment and verified review repairs, not runtime acceptance or automatic merge/release."
---

# Assess the actual code change

Read the [shared workflow contract](../clarila/references/contract.md) before substantive work. This skill is part of the locally installed Clarila suite. Its source is in `~/Developer/skills`; resolve sibling skills relative to this directory.

## Select the review mode

For an ordinary local review, use the procedure below and return an independent assessment. For an explicit request to run/continue a Codex PR review loop, read and follow the [Codex loop protocol](references/codex-loop.md): synchronize the live base, verify current-head feedback, repair valid findings within the grant, and require two attributable clean rounds. Its external comments, commits and normal pushes are covered by the explicit loop request; ordinary local review does not trigger them. Keep the full ledger and stop conditions in that protocol.

## Procedure

1. Use an independent context. Resolve the live base/head and inspect the complete relevant diff, requirements and upstream reports.
2. Trace changed behavior through callers, state/data boundaries, error handling and affected tests. Seek actionable defects rather than stylistic preferences.
3. Validate suspected findings against actual code and realistic scenarios. Include precise file/line references and user/system consequence.
4. Run focused checks when they materially test a concern. State uninspected areas and unavailable checks. A clean code review does not prove app behavior.
5. Return current-head findings by severity or a scoped PASS with residual risks. Use the Codex loop mode above only when that remote workflow is requested.
6. For a control-service assessment, follow the [native assessment contract](../clarila-verify/references/control-assessment.md). Return the requested source-bound final JSON and substantive report from the separate service-created Review context. The coordinator observes completed native commands and retains the report and receipt. A writer-created `review.json` file or a supplied context ID cannot establish independent review. Only PASS for the exact current source and base can satisfy that gate.

For a PR-card assessment, return the actual findings and their checked commit to the coordinator. Do not repair source in the independent review context. The existing engineer handles admitted, in-scope repairs; a new commit invalidates prior-head evidence. A stopped repair cycle needs an owner decision, not a new reviewer or an unlimited restart loop. This local workflow is separate from the explicitly invoked hosted Codex loop above.

## Synchronization and handoff

Resolve the same issue/workspace/session association before substantive work, including direct invocation. Read the private handoff described in the shared contract. When independently delegated, save an assessor-owned report and return it to the workflow owner for incorporation; do not compete to write the shared handoff. Otherwise update only the handoff you actually own using native file tools. Record the actual stage, source, findings, evidence, outcome and next action. If no native session identity is available, retain an unbound record. Use the current host’s native tools during the invoked workflow.

## Deliverable

Return independent source-bound findings, evidence, validation and residual review limits.

Load only the relevant specialist from the [catalog](../clarila/references/catalog.md). Missing tools change the available evidence, never its meaning.

Read the [operation-specific reference](references/findings.md) when performing this responsibility.
