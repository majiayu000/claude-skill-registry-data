---
name: launch-risk
description: Build and maintain a launch-specific risk view covering failure scenarios, probability, impact, detectability, prevention, contingency, decision triggers, and accountable owners.
---
# Launch Risk

Use when a launch has enough technical, customer, operational, legal, commercial, or reputational exposure to require explicit risk management.

## Procedure
1. Define launch scope, rollout shape, affected audiences, timing, dependencies, and what failure would mean for users and the organization.
2. Generate concrete failure scenarios across product, infrastructure, data, security, compliance, support, communications, partners, and demand or capacity where relevant.
3. Rate likelihood and impact using a simple shared scale and include detectability or time-to-harm where it changes response urgency.
4. Separate prevention controls from detection and contingency so a risk is not marked mitigated merely because monitoring exists.
5. Assign one accountable owner and a practical mitigation, fallback, or acceptance decision to each material risk.
6. Define launch triggers such as error rate, latency, support volume, data inconsistency, conversion drop, or external dependency failure that should pause or roll back rollout.
7. Reassess risk after scope, timing, rollout percentage, dependency, or readiness evidence changes.
8. Carry only material residual risks into the go-live decision and post-launch watch plan.

## Decision rules
- Risks should be phrased as plausible events and consequences, not generic categories.
- A risk register with no owner or action is a list, not management.
- Monitoring reduces detection time; it does not necessarily reduce likelihood.
- Accepted risk needs the authority that owns the consequence.

## Quality gate
Launch risk is managed when material scenarios have realistic ratings, prevention, detection, contingency, and owners; stop or rollback triggers are explicit; residual risks reach the correct decision authority; and the risk view changes as readiness evidence changes.