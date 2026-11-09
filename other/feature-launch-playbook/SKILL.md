---
name: "feature-launch-playbook"
description: "The operational playbook for launching a feature well. Positioning, internal alignment, customer comms, sales enablement, support readiness, rollout strategy, monitoring with pre-defined rollback triggers, post-launch measurement against spec hypotheses, and the discipline that distinguishes shipping from releasing from actually launching. Triggers on launch plan, feature launch, launch checklist, ship vs release, rollout strategy, gradual rollout, sales enablement, support readiness, launch announcement, post-launch measurement, launch failure, declared victory too early. Also triggers when planning a launch (any size, any segment), auditing an existing launch process, fixing the we shipped it but the metric did not move problem, or building a launch checklist for the team."
---

# Feature Launch Playbook

A veteran PM-leader's playbook for launching features well, not just shipping them.

Most teams conflate shipping, releasing, and launching. Shipping means engineering work is complete. Releasing means users can access it, even if it is behind a flag at 1 percent. Launching is the discipline of positioning, internal alignment, customer comms, sales enablement, support readiness, rollout strategy, monitoring, and post-launch measurement that turns "feature exists" into "feature lands."

A feature that ships without launching costs you the same engineering investment but captures a fraction of the value. Sales does not know how to sell it. Support does not know how to help with it. Customers do not notice it. The metric you said you would move does not move because nobody knows the feature is there.

This skill is the operational playbook. It assumes you have already written the spec (`pm-spec-writing`), prioritized it onto the roadmap (`roadmap-planning`), instrumented it (`product-analytics-setup`), and possibly tested it (`experiment-design`). The launch is the next discipline: how to actually get the feature in front of the right users, with the right context, in a way that lets you measure whether it worked.

When to use this skill: planning a launch (any size, any segment), auditing an existing launch process, fixing the "we shipped it but the metric did not move" problem, or building a launch checklist for the team.

---

## What this skill is for

This skill spans the operational launch discipline. It composes with the rest of the Product skill suite.

- `pm-spec-writing` defines the launch hypotheses; this skill validates them.
- `roadmap-planning` provides the launch context (what came before, what comes next).
- `product-analytics-setup` is the instrumentation prerequisite; without it you cannot measure the launch.
- `experiment-design` and `data-warehouse-experimentation` provide the methodology for testing whether the launch worked.
- `feature-flagging` provides the rollout infrastructure this skill depends on.

This skill does not cover pricing decisions, brand campaigns, or full GTM strategy. Those need a marketing team partner; this is the PM operational playbook for the engineering and product side.

The audience is broad: every PM ships features, every PM has launched poorly at least once, every PM benefits from a checklist that stops the worst failure modes from recurring. The voice is veteran PM-leader to PM. Specific, opinionated, honest about what discipline matters at what stage.

---

## If required data is unavailable

This skill's output depends on data, measurements, or tool results it cannot generate on its own. When a required input, tool, or data source is unavailable or unverifiable, the sanctioned output is the deliverable with the gap stated: what was needed, what was actually obtained or verified, and which parts of the output are affected. Fabricating, estimating, or interpolating a required number to complete the deliverable is never sanctioned. A stated gap is a complete answer.

---

## Reference files

- [`references/launch-tier-decision.md`](references/launch-tier-decision.md) - Tier 1, 2, 3 decision framework with worked examples.
- [`references/positioning-canvas.md`](references/positioning-canvas.md) - One-page positioning template with B2B SaaS, B2C, and developer feature examples.
- [`references/internal-alignment-checklist.md`](references/internal-alignment-checklist.md) - Stakeholders, brief structure, distribution timing by tier.
- [`references/customer-comms-playbook.md`](references/customer-comms-playbook.md) - Channels, calendar, owners, gates.
- [`references/sales-enablement-template.md`](references/sales-enablement-template.md) - Battlecard, demo, deal coaching, training (B2B). Skip note for B2C and PLG.
- [`references/support-readiness-checklist.md`](references/support-readiness-checklist.md) - Training, FAQ, escalation, monitoring access.
- [`references/rollout-strategy-patterns.md`](references/rollout-strategy-patterns.md) - Four patterns matched to feature types. Decision framework: blast radius times confidence times external commitments.
- [`references/monitoring-readiness-checklist.md`](references/monitoring-readiness-checklist.md) - Metrics dimensions, alert thresholds, pre-defined rollback triggers.
- [`references/post-launch-measurement-framework.md`](references/post-launch-measurement-framework.md) - Adoption, engagement, outcome, side effects. Time horizons. Tying back to spec hypotheses.
- [`references/common-launch-failures.md`](references/common-launch-failures.md) - Twelve failure patterns with diagnoses and fixes.

---


## Conditional methods

Before applying a method below, read its linked section. For a narrow task select only relevant methods; for a full audit/design use the framework and relevant failure patterns. Existing references remain available for deeper details.

- Ship vs release vs launch: [method](references/domain-guide.md#ship-vs-release-vs-launch).
- Launch tiers: [method](references/domain-guide.md#launch-tiers).
- Pre-launch: positioning: [method](references/domain-guide.md#pre-launch-positioning).
- Pre-launch: internal alignment: [method](references/domain-guide.md#pre-launch-internal-alignment).
- Pre-launch: customer comms plan: [method](references/domain-guide.md#pre-launch-customer-comms-plan).
- Pre-launch: sales enablement (B2B): [method](references/domain-guide.md#pre-launch-sales-enablement-b2b).
- Pre-launch: support readiness: [method](references/domain-guide.md#pre-launch-support-readiness).
- Launch day: rollout strategy: [method](references/domain-guide.md#launch-day-rollout-strategy).
- Launch day: monitoring: [method](references/domain-guide.md#launch-day-monitoring).
- Launch day: comms execution: [method](references/domain-guide.md#launch-day-comms-execution).
- Post-launch: measurement against spec hypotheses: [method](references/domain-guide.md#post-launch-measurement-against-spec-hypotheses).
- Post-launch: iteration and follow-ups: [method](references/domain-guide.md#post-launch-iteration-and-follow-ups).
- Common failure modes: [method](references/domain-guide.md#common-failure-modes).
- The framework: 12 considerations for a real launch: [method](references/domain-guide.md#the-framework-12-considerations-for-a-real-launch).
- Closing: most failed launches are unlaunched: [method](references/domain-guide.md#closing-most-failed-launches-are-unlaunched).
