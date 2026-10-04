---
name: gatekeeper
description: >
  Implement a Creator-Reviewer quality gate loop. The Creator generates an artifact,
  and the Gatekeeper/Reviewer verifies it against quality criteria. If approved,
  it passes; if rejected, the Creator must perform rework and resubmit.
  Useful for strict code reviews, verification checks, or quality assurance.
  Triggers: "게이트키퍼", "리뷰 루프", "검증 게이트", "품질 검증", "gatekeeper", "reviewer loop", "quality gate".
---

# Gatekeeper

The Gatekeeper pattern sets up a loop between a Creator session and a Reviewer/Gatekeeper session. The reviewer audits the output against explicit quality criteria, approving it for delivery or rejecting it for rework.

## 4-Stage Workflow

```
 ┌───────────┐      Submit Artifact      ┌──────────────┐
 │  Creator  ├──────────────────────────►│  Reviewer/   │
 └─────▲─────┘                           │  Gatekeeper  │
       │                                 └──────┬───────┘
       │            Reject (Rework)             │
       └────────────────────────────────────────┤ Approve ──► Ship
                                                ▼
```

1. **Specs & Criteria**: Setup target task goals for the Creator and quality criteria for the Reviewer. See [criteria.md](references/criteria.md).
2. **Draft & Submit**: The Creator implements the code/artifact in the shared workspace and notifies the Reviewer.
3. **Audit**:
   - The Reviewer evaluates the artifact against criteria.
   - **Approve**: If all criteria pass, the loop exits.
   - **Reject**: List the failed rules and provide actionable feedback.
4. **Rework Loop**: The Creator modifies the files based on the feedback and resubmits. This loops until approved or loop count limit is reached.

## 🛠️ MCP Tools Guide

- **Feedback Delivery**: Inject the reviewer's audit report using `agent__messageToSession` to wake and direct the Creator to rework.
- **Infinite Loop Avoidance**: The parent session must track and enforce a **maximum rework limit (default: 3)** to prevent endless loops over minor stylistic differences. See [rework-limit-examples.md](references/rework-limit-examples.md).

## References

- [Quality criteria](references/criteria.md)
- [Rework limit examples](references/rework-limit-examples.md)
- [Troubleshooting](references/troubleshooting.md)
