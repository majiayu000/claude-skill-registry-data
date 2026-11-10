---
name: clarila-pr
description: "Prepare, publish or maintain a requested issue PR with accurate source-bound description and evidence. Not permission to merge, assign human reviewers or release."
---

# Make the candidate reviewable

Read the [shared workflow contract](../clarila/references/contract.md) before substantive work. This skill is part of the locally installed Clarila suite. Its source is in `~/Developer/skills`; resolve sibling skills relative to this directory.

## Procedure

1. Resolve the actual issue, repository, head/base, existing PR and worktree ownership. Reuse the covering PR when appropriate.
2. Inspect the final diff and actual checks. Draft a title/body describing the problem, resulting behavior, review map and validation with material limits.
3. For a requested create/update operation, use gh with a body file and exact head/base. Preserve draft status unless changing it is authorized.
   When the Clarila control service started the run, leave the PR in draft. The service alone marks it ready after green CI and separate Verify and Review PASS verdicts at the current head, with provider readback. A completed Codex turn does not establish PR readiness.
4. Recheck provider readback and CI/review state. Do not claim another reviewer's approval, request a human review or enable merge merely from queue membership.
5. Update the verified issue workflow thread in the configured Clarila server with the useful PR outcome and remaining checks. Keep source-report conversations separate; do not post in HeyAmara or another server unless the user explicitly names that destination.
6. With the PR-card service enabled, publish the actual PR finding through the PR role and let the service maintain its one persistent card. Report the exact current commit and remaining requirements. Refresh reads status; Update from the base branch changes commits. Direct Merge is repository- and permission-dependent; within HeyAmara it is limited to ats-mobile into dev. A displayed button or this skill never grants another repository merge authority.

## Synchronization and handoff

Resolve the same issue/workspace/session association before substantive work, including direct invocation. Read and update the private handoff described in the shared contract using available native file tools. Record the actual stage, source, findings, evidence, outcome and next action. If no native session identity is available, retain an unbound record. Use the current host’s native tools during the invoked workflow.

## Deliverable

Return accurate PR draft or confirmed authorized provider update, source identity, checks and remaining readiness.

Load only the relevant specialist from the [catalog](../clarila/references/catalog.md). Missing tools change the available evidence, never its meaning.

Read the [operation-specific reference](references/publication.md) when performing this responsibility.
