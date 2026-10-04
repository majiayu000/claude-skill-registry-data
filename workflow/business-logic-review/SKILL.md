---
name: business-logic-review
description: Review an authorized application for business-logic vulnerabilities, workflow abuse, approval bypasses, replay conditions, quota circumvention, plan enforcement bugs, and state-transition errors. Use for billing, invites, approvals, refunds, admin actions, and multi-step workflows.
---

# Business Logic Review

## Focus

- state machine gaps
- approval or refund bypasses
- replay and duplicate processing
- quota and entitlement circumvention
- race conditions around credits, inventory, or invitations
- UI-only controls missing server-side enforcement

## Method

1. Identify the invariant the product is trying to preserve.
2. Trace where the invariant is enforced.
3. Look for alternate paths, retries, replays, and admin shortcuts.
4. Confirm whether enforcement survives background jobs and webhooks.
