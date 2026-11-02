---
name: agent-human-approval-gates
description: Define human approval points for irreversible, externally visible, costly, or privilege-changing actions in agent workflows.
---

# Agent Human Approval Gates

## Goal

Let agents automate routine work while retaining human control over high-impact decisions.

## Inputs to inspect

Action inventory, permissions, reversibility, user intent, data sensitivity, and existing review/approval mechanism.

## Workflow

1. Inventory actions by impact, reversibility, visibility to others, financial/resource cost, and sensitivity of data involved.
2. Specify which action classes require explicit user approval, what preview/evidence must be shown, and whether approval is single-use or scoped to a bounded set of operations.
3. Separate prepare/dry-run from commit/execute so users can inspect the intended diff, recipients, data scope, and likely side effects before approving.
4. Bind approval to the exact operation inputs and version; invalidate approval if the diff, target, permissions, or scope changes materially.
5. Test cancellation, stale approval, repeated confirmation, partial execution, and tool failures after approval; provide an audit trail without secrets.

## Validation checklist

- [ ] Approval cannot be inferred from silence or a vague prior request when policy requires confirmation.
- [ ] The approved action is bound to the inspected parameters and scope.
- [ ] A material diff change requires renewed approval.
- [ ] Dry-run and actual execution are visibly distinguished.
- [ ] Cancellation and failure leave a clear state and do not falsely claim rollback.

## Required output

Deliver an action risk matrix, approval UX/contract, stale-approval rules, audit fields, and failure-path tests.

## Boundaries and failure handling

Do not design bypasses that treat stored credentials or prompt text as broad consent; do not require repeated approvals for harmless reads without justification.

When repository evidence is incomplete, label the gap explicitly and request only the missing information that changes the decision. Do not claim commands, benchmarks, tests, or runtime checks passed unless their outputs were observed.
