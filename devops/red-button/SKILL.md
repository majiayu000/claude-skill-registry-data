---
name: red-button
description: Use when an action could cause material, hard-to-reverse harm to production, data, security, finances, users, or external systems.
---

# Red Button

Some changes deserve a slower agent. Apply a focused gate only where consequence requires it.

## Classify the operation

1. Name the exact action, target environment, affected users or assets, and externally visible effect.
2. Classify the operation as `ordinary` or `high-risk`. Mark it high-risk when a credible failure could materially destroy or expose important state, cross a security or authorization boundary, move money, contact many people, break external consumers, disrupt production, or resist timely recovery.
3. Keep reversible local edits, read-only inspection, isolated test work, and draft pull requests ordinary unless they themselves create consequential side effects.
4. When risk is uncertain, use read-only checks to resolve the target, blast radius, rollback, and authority. Uncertainty alone does not make ordinary work high-risk.
5. For an ordinary operation, proceed with the normal workflow. Do not load a reference or manufacture a risk review.
6. For a high-risk operation, name the risk category and load only the matching reference.

## Load the focused reference

| Risk category | Reference |
| --- | --- |
| Production schema or data migration; deletion or bulk repair | [data-operations.md](references/data-operations.md) |
| Force push, rebase of published work, or history rewrite | [repository-history.md](references/repository-history.md) |
| Authentication, authorization, IAM, secrets, or credentials | [identity-and-secrets.md](references/identity-and-secrets.md) |
| Charges, refunds, subscriptions, invoices, pricing, or payment flows | [billing-and-payments.md](references/billing-and-payments.md) |
| Infrastructure, networking, capacity, or production configuration | [infrastructure.md](references/infrastructure.md) |
| Public API contracts, events, schemas, or compatibility | [public-apis.md](references/public-apis.md) |
| Email, notification, campaign, or other bulk outreach | [mass-communication.md](references/mass-communication.md) |
| Production model, prompt, retrieval, guardrail, or tool-policy deployment | [model-and-prompt-deployments.md](references/model-and-prompt-deployments.md) |
| Other consequential operation with no matching category | Apply the core gate below; do not load an unrelated reference |

Load multiple references only when risks truly cross categories: public API plus identity for an auth-scope change, billing plus data for a ledger migration, or model deployment plus identity for a privileged tool.

## Apply the gate

Analysis, coding, local tests, plans, and isolated rehearsal may proceed without execution approval when they create no consequential side effect. Before crossing the real side-effect boundary:

1. Resolve the target, blast radius, reversibility, monitoring, and authority with concrete evidence. Satisfy any loaded reference's additional preconditions and keep unknowns explicit.
2. Prefer the smallest reversible action, staged rollout, and bounded exposure that can achieve the goal.
3. Define observable success, stop conditions, and a recovery owner before creating side effects.
4. Obtain authorization for the exact action, target, and scope from the responsible owner, plus any approval named by a loaded reference. Existing user authorization counts only where that user has the relevant authority. Never infer authority from technical access.

For a declared incident, use the established incident-command approval path and record the decision. Urgency does not remove scope bounds, stop conditions, or post-change verification.

During execution, verify the resolved target again, preserve the safety bounds, observe the chosen signals, and stop when a stop condition fires. Do not improvise past a failed guardrail.

After execution, verify the real effect and recovery posture. Report what changed, the scope reached, the evidence observed, any remaining risk, and whether rollback remains available.
