---
name: abuse-case-testing
description: Perform authorized defensive testing of misuse and abuse scenarios by turning attacker or malicious-user goals into bounded hypotheses, evidence, impact, and remediation without exceeding the approved test scope.
---
# Abuse Case Testing

Use when a product or system can be intentionally misused even if ordinary functional behavior is correct.

## Procedure
1. Confirm written/explicit authorization, target environment, identities/accounts, prohibited actions, rate/volume limits, data-handling rules, and stop conditions before testing.
2. Identify assets and legitimate capabilities that could be abused: account creation, invitations, messaging, uploads, search, sharing, automation, billing/credits, resource creation, APIs, administrative functions, or AI/tool use as relevant.
3. Model realistic malicious goals such as bypassing quotas, acting on another user's resources, evading workflow safeguards, causing unwanted side effects, exhausting shared resources, or using a feature for a purpose outside its intended trust assumptions.
4. Convert each goal into the least-destructive hypothesis that can establish whether the control prevents or permits the abuse. Avoid unnecessary scale or persistence when one bounded proof is enough.
5. Test controls at the actual server/system boundary rather than relying on UI restrictions alone. Preserve stable evidence and operation IDs while minimizing sensitive data.
6. Check repeated, concurrent, reordered, and alternate-entry behavior when abuse depends on rate limits, idempotency, workflow state, or multiple channels.
7. Stop and escalate if a test begins affecting unrelated users/data, production stability, irreversible external effects, or any boundary excluded by the authorization.
8. Distinguish confirmed abuse, partial weakness, theoretical concern, and defense-in-depth recommendation. Record required preconditions and realistic impact.
9. Recommend the lowest-layer defensive control that addresses the abuse without breaking legitimate use, plus monitoring/detection when prevention alone is insufficient.
10. Re-test remediated high-impact cases within the same authorization and add a regression test/control where practical.

## Decision rules
- Misuse testing is authorized defensive validation, not permission to explore unrelated systems or increase impact for demonstration value.
- A feature behaving “as designed” can still contain an abuse case if the design omitted adversarial incentives or authority boundaries.
- Prefer a minimal proof over a realistic-volume attack simulation unless scale testing is explicitly authorized and necessary.
- Report exact control failure and impact rather than sensational attack narratives.

## Quality gate
The test is complete when scope and authorization are preserved, abuse hypotheses represent plausible misuse, confirmed findings use minimal reproducible evidence, unrelated users/systems are not harmed, impact and preconditions are explicit, remediation targets the responsible control, and critical fixes are revalidated defensively.