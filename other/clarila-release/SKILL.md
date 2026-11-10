---
name: clarila-release
description: "Prepare or perform an explicitly authorized merge or distribution operation for an identified candidate. Use for landing/release requests, not as an automatic result of passing checks."
---

# Deliver only the authorized candidate

Read the [shared workflow contract](../clarila/references/contract.md) before substantive work. This skill is part of the locally installed Clarila suite. Its source is in `~/Developer/skills`; resolve sibling skills relative to this directory.

## Procedure

1. Read the current owner request, source/audience-bound grant, holds, repository policy and exact requested operation. Determine eligibility from that current evidence and preserve each active hold.
2. Bind issue, PR, full source/base, artifact, platform/runtime, destination/audience and rollback when applicable. Recheck independent QA/review, CI and provider capability.
3. Inspect actual merge/build/upload auto-delivery triggers. Prepare a reviewable operation and execute only within the user's authorization, target and spend limits.
4. Persist immutable operation intent before provider writes. Use official CLIs and current forge head matching. An uncertain outcome requires original-operation readback, never a blind retry.
5. Verify actual availability and the original flow after distribution. Report merge, build, upload/submission, audience availability, adoption and recovery separately.

## Synchronization and handoff

Resolve the same issue/workspace/session association before substantive work, including direct invocation. Read and update the private handoff described in the shared contract using available native file tools. Record the actual stage, source, findings, evidence, outcome and next action. If no native session identity is available, retain an unbound record. Use the current host’s native tools during the invoked workflow.

## Deliverable

Return readiness or confirmed scoped delivery receipts, exact inclusion/target and post-delivery limits.

Load only the relevant specialist from the [catalog](../clarila/references/catalog.md). Missing tools change the available evidence, never its meaning.

Read the [operation-specific reference](references/readiness.md) when performing this responsibility.
