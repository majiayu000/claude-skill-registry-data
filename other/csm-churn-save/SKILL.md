---
name: csm-churn-save
version: 1.0.0
description: Run a structured churn-save play for an at-risk account to diagnose root cause and reverse the decision.
author: matrixx0070
tags: [customer-success, churn, retention, risk, save-play]
capabilities: []
---

## When to use

Use this when an account has signaled intent to leave or downgrade, or a health score/renewal risk flags imminent churn. Reach for it the moment risk is real: a stated cancellation, a non-response near renewal, a departed champion, or a collapsing usage trend.

**Not for:** routine dissatisfaction that support can resolve (that is customer-support); healthy accounts you simply want to grow (see csm-expansion-play); standard renewal prep with no risk signal (see csm-renewal-prep).

## Method

1. Confirm the churn is real and name the trigger: price, value gap, competitor, org change, or product gap. Decision point: if you cannot name the root cause, run a diagnostic call before proposing any save — solving the wrong cause wastes your one shot.
2. Assess salvageability honestly: is there a viable path, or is this account structurally lost (acquired, product sunset)? If lost, plan a graceful exit and reference-preservation, not a save.
3. Re-establish the sponsor or find a new one. A save with no internal advocate rarely holds.
4. Match the play to the cause: value gap → targeted re-onboarding + quick win; price → repackage/right-size scope; competitor → differentiation + switching-cost reality; org change → re-sell the value to the new stakeholder.
5. Deliver a fast, visible quick win within days to reset the relationship trajectory. Decision point: if you cannot ship a quick win, escalate for exec-to-exec engagement or commercial concession.
6. Get a mutual action plan with dates and a commitment checkpoint before renewal.
7. Loop in your manager/exec early on high-ARR saves; do not freelance concessions.

## Example

Account signals cancellation citing "not seeing ROI." Diagnostic reveals only 1 of 4 bought modules is in use and the original champion left. Cause: value gap + sponsorless. Play: identify the new ops lead, re-onboard on the highest-value unused module, ship a quick win (automate their weekly reconciliation in 5 days). Mutual plan: 30-day adoption sprint, checkpoint 2 weeks before renewal. Outcome: usage recovers, renewal held flat.

## Pitfalls

- **Leading with a discount.** Price cuts mask value problems and train customers to threaten churn for money.
- **Skipping root-cause diagnosis.** Fixing the loudest complaint instead of the real cause burns your credibility.
- **Saving structurally-lost accounts.** Pouring effort into an acquired/sunset account starves salvageable ones.
- **Going solo on big concessions.** Uncoordinated promises create precedent and internal conflict.

## Output format

```
CHURN-SAVE PLAY — <account> | ARR: <$> | renewal: <date>
Trigger: <what happened> | Root cause: <price|value|competitor|org|product>
Salvageable: <yes — path | no — graceful exit>
Sponsor: <existing/new name>
Save play: <cause-matched action>
Quick win: <deliverable — by date>
Mutual action plan: <steps + dates> | Checkpoint: <date>
Escalation: <manager/exec involved? concession authority>
```
