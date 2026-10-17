---
name: plan-to-execution-handoff
description: "Convert an approved plan into scoped work items, dependencies, acceptance checks and a durable handoff for the available execution workflow."
---
# Approved plan to execution handoff

Identify the approved plan and its exact revision. Do not select an arbitrary recently modified plan. Read current source and related work to avoid duplicating implementation or overriding active ownership.

For each work item capture ID, requirement, scope, owner, dependencies, acceptance checks, expected evidence, rollback constraints and status. Split work into complete vertical slices. Assign compute/platform requirements only from known needs and available capacity; do not invent hosts or lanes.

Validate unique IDs, all dependency references and absence of cycles. A plan can legitimately have every item blocked by an external dependency: report that instead of inventing ready work. Missing estimates stay unknown; do not derive time promises from keywords.

Use the repository's existing task schema. If none exists, a human-readable handoff under `plans/` can contain:

```yaml
schema_version: 1
source_plan: plans/approved-plan.md
source_revision: FULL_REVISION
items:
  - id: item-1
    title: Implement the agreed consumer path
    status: pending
    owner: unassigned
    requires: []
    acceptance:
      - Describe an observable, reproducible pass/fail check
    evidence: []
    rollback: Describe applicable recovery constraints
```

This is a documentation schema, not a claim that an executor can ingest it. Confirm the receiving tool's contract before automation. Execute independent authorized ready work through `software-development-lifecycle`; record blockers and exact next actions. Do not dispatch agents, spend money, merge or deploy solely because a handoff exists.
