---
name: clarila-verify
description: "Independently verify an issue candidate against its original scenario and acceptance criteria. Use for behavior acceptance, not implementation self-checks or code-only review."
---

# Assess actual candidate behavior

Read the [shared workflow contract](../clarila/references/contract.md) before substantive work. This skill is part of the locally installed Clarila suite. Its source is in `~/Developer/skills`; resolve sibling skills relative to this directory.

## Procedure

1. Use a separate assessment context from the implementer. Test writing/maintenance belongs to clarila-test; its authored suite and self-checks are upstream evidence, not an independent acceptance verdict. Read the issue, accepted scope, full upstream report and current source/artifact rather than trusting a summary.
2. Confirm source, environment, fixture and device/browser/API applicability. New source or artifact changes invalidate affected prior evidence.
3. Execute the original acceptance scenario, relevant negative paths and unaffected controls. Use the actual application or API when required; compilation is not behavior verification.
4. Classify product failures separately from missing tooling/access/environment and inconclusive observations. Retain actual commands/results, traces and source-bound artifacts.
5. Return PASS only for the checked acceptance scope, otherwise FAIL, BLOCKED or INCONCLUSIVE with concrete evidence and next action.
6. For a control-service assessment, follow the [native assessment contract](references/control-assessment.md). Return the requested source-bound final JSON and substantive report from the separate service-created Verify context. The coordinator observes completed native commands and retains the report and receipt. A writer-created `verify.json` file or a supplied context ID cannot establish independent verification. Only PASS for the exact current source and base can satisfy that gate.

For a PR-card assessment, report behavior failures separately from missing environment or capability, using the exact checked commit. Do not implement fixes in the independent Verify context. The existing engineer receives admitted repair work, and the updated commit needs new verification and review. The PR bot edits the existing card; Verify publishes its own substantive finding once.

## Synchronization and handoff

Resolve the same issue/workspace/session association before substantive work, including direct invocation. Read the private handoff described in the shared contract. When independently delegated, save an assessor-owned report and return it to the workflow owner for incorporation; do not compete to write the shared handoff. Otherwise update only the handoff you actually own using native file tools. Record the actual stage, source, findings, evidence, outcome and next action. If no native session identity is available, retain an unbound record. Use the current host’s native tools during the invoked workflow.

## Deliverable

Return an independent behavior verdict with source/artifact, executed cases, controls, evidence and scope limits.

Load only the relevant specialist from the [catalog](../clarila/references/catalog.md). Missing tools change the available evidence, never its meaning.

Read the [operation-specific reference](references/verdict.md) when performing this responsibility. For reproducible frontend UI changes, follow [interactive web evidence](references/interactive-web-evidence.md) and verify the actual reported scenario through the runnable page.
