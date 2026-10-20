---
name: regulatory-compliance-ux
description: Enforce 21 CFR Part 11 / GxP compliance UX patterns. Visible audit trails, governed-action confirmations with reason-for-change capture, e-signature flows, immutable history, and role-scoped visibility. Use when building any mutation, approval, submission, sign-off, or governed-data flow.
---

# Skill: Regulatory Compliance UX (21 CFR Part 11 / GxP)

Concept2Cure's users are submitting to regulators. Every mutation that touches regulated content (documents, submissions, protocols, CSRs, approvals, status changes) MUST leave an audit trail the customer can defend under inspection. Compliance UX is a product feature, not chrome.

## Activation

This skill activates when:

- Building or editing any mutation that touches regulated content (documents, submissions, protocols, CSRs, study records, approvals)
- Adding approval, lock, publish, or sign-off flows
- Wiring a new governed action in `server/routes/authoring-actions.ts` or similar
- Surfacing change history, audit logs, or reviewer comments
- Handling e-signature, role elevation, or escalation gating

## Hard Rules (NON-NEGOTIABLE)

1. **Every mutation is audited**. Every write to regulated tables MUST produce an audit record: `who`, `when`, `what`, `from → to`, `reason`, `ipAddress`, `sessionId`. Use the existing audit-trail service — do NOT create ad-hoc logging.
2. **Reason-for-change is mandatory on governed actions**. Any edit to locked, approved, or submission-bound content MUST prompt for a reason and persist it with the audit record. UI: a required `<Textarea>` in the governed confirmation dialog. Empty/whitespace rejected at the form level.
3. **E-signature flows are two-factor in intent**. Username + password re-entry at the moment of signing (per 21 CFR 11.200). Do NOT reuse session auth. Signature captures: signer identity, meaning (approve / review / author), timestamp, artifact version hash.
4. **Governed-action confirmations are explicit**. Destructive or regulated actions (publish, lock, sign, void, supersede) surface a confirmation dialog that states: the action, the affected artifact + version, the reason field, and the consequence ("This will publish the CTD to the submission package. Auditable."). No silent mutations.
5. **History is immutable and visible**. Every regulated artifact exposes a change history view: version, timestamp, actor, change summary, diff (if applicable). Users MUST be able to reach it without leaving the artifact context. Prior versions are never overwritten, only superseded.
6. **Role-scoped visibility**. Actions the current user cannot perform MUST be hidden or clearly disabled with a tooltip stating *why* (role, lock state, tenant policy). Do not let a user click a governed button only to see a 403.
7. **Status changes show provenance**. When a status changes (Draft → Review → Approved → Published), the UI MUST show: who moved it, when, and the prior status. Badge alone is insufficient.
8. **Escalation gating is visible**. If an action requires escalation (e.g., Medical Director sign-off), the UI MUST show: the required role, the current approver queue, and the current user's position. Do not leave users guessing why the button is disabled.
9. **Tenant scoping is never implicit**. Every list/query scope MUST be tenant-bound. UI surfaces that show cross-tenant data (admin views) MUST make the tenant context explicit and switchable.
10. **Reviewer-grade language**. Status and audit copy uses factual, defensible phrasing: "Locked for review", "Signed by Jane Smith on 2026-04-17 at 14:32 UTC for approval", "Superseded by v3.2". No emoji, no cheerleading, no "Nice work!" toasts on governed actions.

## Canonical UX Patterns

### Pattern: Governed Mutation Dialog

```
┌ Publish section 3.2.P to submission package ────────────────┐
│ Artifact: Module 3 — Drug Product (v4.1)                    │
│ Target:   IND-2026-0047 (FDA)                               │
│                                                              │
│ Reason for publishing *                                     │
│ ┌──────────────────────────────────────────────────────────┐│
│ │ [required textarea]                                      ││
│ └──────────────────────────────────────────────────────────┘│
│                                                              │
│ This will lock v4.1 as the submission version. The action  │
│ is auditable.                                                │
│                                                              │
│                            [Cancel]  [Publish & Lock]       │
└──────────────────────────────────────────────────────────────┘
```

### Pattern: E-Signature Capture

```
┌ Sign as Approver ────────────────────────────────────────────┐
│ You are signing: CSR Protocol 2026-01 (v2.0)                │
│ Meaning:         Final approval for submission              │
│                                                              │
│ Confirm your identity:                                       │
│   Username: jane.smith@c2c.com                              │
│   Password: [•••••••••••]                                    │
│                                                              │
│ By signing, you confirm 21 CFR 11.100(b) intent.            │
│                                                              │
│                              [Cancel]  [Sign]               │
└──────────────────────────────────────────────────────────────┘
```

### Pattern: Inline Provenance Stamp

Every governed artifact header shows:

```
Module 3 — Drug Product · v4.1 · Locked · Signed by Jane Smith 2026-04-17
```

Clicking the provenance stamp opens the full history panel in-context.

### Pattern: Disabled-With-Reason

```tsx
<Button disabled>
  Approve
</Button>
<Tooltip>
  Requires Medical Director role. You are currently QA Reviewer.
</Tooltip>
```

Never show a governed action as clickable when the user cannot perform it.

## Forbidden Patterns

| Forbidden | Use Instead |
| --- | --- |
| Silent mutation of locked content | Governed dialog + reason capture + audit record |
| `confirm("Sure?")` for a governed action | Dialog with artifact context + reason field |
| Reusing session auth for signing | Password re-entry at signing time |
| Hiding the approver or timestamp | Inline provenance stamp + full history panel |
| Overwriting a prior version | New version + supersession pointer |
| Toast: "Published! 🎉" | Toast: "Published v4.1 to IND-2026-0047. Recorded." |
| Disabled button with no reason | Tooltip with the specific blocking condition |
| Cross-tenant list without explicit tenant switch | Tenant selector in header + tenant column visible |

## Completion Gate

A regulated flow is NOT complete until:

- Every mutation produces an audit record via the canonical audit service
- Every governed action captures reason-for-change when applicable
- E-signature flows require re-authentication
- Change history is reachable from the artifact view
- Disabled actions explain why
- Copy is reviewer-grade (see `microcopy-tone` skill)
- Legal/compliance review sign-off has been requested if the flow is new

Flag any gap in audit coverage to the user explicitly — do not ship regulated flows with silent mutations.
