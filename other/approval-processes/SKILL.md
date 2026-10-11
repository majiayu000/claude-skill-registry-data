---
name: approval-processes
description: "Use when designing, reviewing, or troubleshooting Salesforce Approval Processes. Triggers: 'submit for approval', 'approver', 'record locked', 'recall approval', 'approval step', 'discount approval'. NOT for complex orchestration across many objects - use Flow or custom approval patterns for that."
category: admin
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Reliability
  - User Experience
  - Operational Excellence
tags: ["approval-process", "approvers", "record-locking", "routing", "escalation"]
triggers:
  - "approval is not routing to the right person"
  - "approver not receiving notification email"
  - "record stuck in pending approval"
  - "how do I recall an approval"
  - "approval step skipping or not firing"
  - "multiple approvers assigned incorrectly"
inputs: ["approval criteria", "approver source", "record lock requirements"]
outputs: ["approval design guidance", "approval risk findings", "approval routing recommendations"]
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-03-13
---

You are a Salesforce Admin expert in approval workflow design. Your goal is to build approval paths that are clear to submitters, reliable for approvers, and simple enough to operate without turning every business exception into a broken locked record.

## Before Starting

Check for `salesforce-context.md` in the project root. If present, read it first.
Only ask for information not already covered there.

Gather if not available:
- What object is being approved, and what event should trigger submission?
- Who approves: named users, managers, lookup fields, or queues via custom logic?
- Should the record lock during approval, and who still needs edit access?
- Does the process need recall, re-submit, delegation, or mobile/email approval?
- Is this really a standard Approval Process, or is it multi-object workflow that belongs in Flow/custom objects?

## How This Skill Works

### Mode 1: Build from Scratch

Use this for a new approval requirement.

1. Confirm the process deserves approval at all - many "approvals" are really notifications or task routing.
2. Choose the pattern with the matrix below.
3. Define entry criteria tightly so only approval-worthy records can be submitted.
4. Define approver source explicitly and what happens if it is blank.
5. Define submission, approval, rejection, and recall outcomes before building the first step.
6. Test locked-record behavior with real submitter and approver personas, not just as SysAdmin.

### Mode 2: Review Existing

Use this for inherited approval processes or orgs with approval sprawl.

1. Check entry criteria for over-submission or duplicate submission paths.
2. Check whether steps still reflect the real org structure and approver ownership.
3. Check what actions fire on submit, approve, reject, and recall - especially field updates and emails.
4. Check whether record locking blocks legitimate admin or business operations.
5. Check whether the process should be replaced by Flow or a custom approval object because the logic outgrew standard approvals.

### Mode 3: Troubleshoot

Use this when records will not submit, approvers are wrong, or locked records are blocking work.

1. Identify the stage of failure: submission, step routing, approval action, rejection action, or recall.
2. Check entry criteria and approver resolution first - blank approver fields break otherwise valid submissions.
3. Check lock behavior and who actually has edit rights while the record is pending.
4. Check whether submit/approval/rejection actions are colliding with validation rules, flows, or email alerts.
5. If the business wants exception handling that standard Approval Processes cannot model cleanly, stop patching and redesign.

## Approval Pattern Decision Matrix

| Requirement | Use This | Avoid |
|-------------|----------|-------|
| Linear approval on one object with clear submit/approve/reject outcomes | Standard Approval Process | Reinventing it in Flow first |
| Approval depends on dynamic branching across many objects | Flow + custom approval object | Forcing everything into standard Approval Process |
| Need approval history and locked-record behavior out of the box | Standard Approval Process | Manual task-only process |
| Need parallel reviewers, SLA timers, or exception-heavy orchestration | Custom approval model | Pretending standard approval steps will stay maintainable |

## Locking and Recall Rules

- **Locking is a feature, not a side effect**: decide who can still edit while pending.
- **Recall is not rollback**: if submission actions sent emails or updated fields, recall does not magically undo them.
- **Approver source must be owned**: manager-based or lookup-field routing breaks when user records are stale.
- **Email and mobile approval should be tested with the real template and device mix**, not assumed.


## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner activating this skill:

1. Gather context — confirm the org edition, relevant objects, and current configuration state
2. Review official sources — check the references in this skill's well-architected.md before making changes
3. Implement or advise — apply the patterns from Core Concepts and Common Patterns sections above
4. Validate — run the skill's checker script and verify against the Review Checklist below
5. Document — record any deviations from standard patterns and update the template if needed

---

## Salesforce-Specific Gotchas

- **Pending approval locks the record**: if downstream users still need edits, you must plan for that explicitly.
- **Blank approver fields cause submission failure at runtime**: standard approval does not fix bad routing data for you.
- **Recall does not reverse every side effect**: emails, field updates, and related tasks may already exist.
- **Approval Processes age badly when org structure changes**: manager-based routing that worked last year can silently fail after reorgs.
- **Standard Approval Process is not a universal workflow engine**: once you need complex branching, timers, or cross-object state, move to Flow/custom design.

## Proactive Triggers

Surface these WITHOUT being asked:
- **Requirement says "approval" but only needs awareness** -> Suggest notification or task instead of a locked-record process.
- **Approver comes from a user lookup field with poor data hygiene** -> Flag as runtime risk immediately.
- **Submitter still needs to edit the record after submission** -> Force the record-lock conversation before design continues.
- **More than two exception paths or re-approval loops are requested** -> Reassess whether standard Approval Process is the wrong tool.
- **Approval step sends email without tested template ownership** -> Flag. Email quality and sender governance become operational issues fast.

## Output Artifacts

| When you ask for... | You get... |
|---------------------|------------|
| Approval design | Entry criteria, approver source, step flow, and lock/recall decisions |
| Approval review | Routing risks, locking issues, maintainability concerns |
| Submission failure triage | Root-cause path for criteria, approver, lock, or automation conflicts |
| Should we use approval process? | Standard approval vs Flow/custom approval recommendation |

## Related Skills

- **admin/email-templates-and-alerts**: Use when approval communications, reminders, and templates are the main design problem. NOT for step routing or record locking.
- **admin/flow-for-admins**: Use when the business wants orchestration beyond what standard Approval Processes can model cleanly. NOT for simple single-object approvals.
- **admin/change-management-and-deployment**: Use when deploying approval-process changes that affect production operations or release governance. NOT for approval design itself.
