---
id: angular.docs.angular-review-packet
name: Angular Review Packet
description: Build a compact review packet for Angular PRs that highlights architecture, risk, validation, and rollback points for human or agent review.
stack:
  - Angular
category: docs
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - review packet
  - PR summary
  - agent review
---

# Angular Review Packet

Use this skill when a PR or change needs a review-ready summary.

## Core Rule

```txt
Review packets should make risk visible before the diff is merged.
```

## Packet Contents

- change summary
- files touched
- architecture impact
- validation evidence
- rollback notes
- open risks

## Purpose

Build a compact review packet for humans or agents.

## When to Use

Use this skill when a PR or change needs a review-ready summary.

## Do

- make the risk visible
- include rollback notes

## Do Not

- bury important risks in the diff
- omit validation evidence

## Review Checklist

- [ ] The change summary is concise.
- [ ] Risks are visible.
- [ ] Validation is documented.
- [ ] Rollback or follow-up is clear.

## Output

Return:

1. A concise review packet.
2. The main risks.
3. The validation performed.
4. The rollback or follow-up path.

## Expected Output

Return:

1. A concise diagnosis.
2. The minimal safe change or decision.
3. Validation steps.
4. Risks or rollback notes.
