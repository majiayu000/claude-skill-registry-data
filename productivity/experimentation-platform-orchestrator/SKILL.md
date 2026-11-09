---
name: "experimentation-platform-orchestrator"
description: "A platform decision framework for experimentation. When to use Statsig vs PostHog vs GrowthBook vs Optimizely vs Amplitude vs Eppo vs Kameleoon. How to migrate between them. How to coordinate when multi-platform is genuinely warranted. The decisions that compound for years and the ones you can defer. Triggers on which experimentation platform, choose Statsig vs PostHog, evaluate experimentation tools, switch experimentation platform, migrate from Optimizely, consolidate experimentation tools, multi-platform experimentation, experimentation platform decision, ab test platform selection, feature flag platform vs experiment platform, warehouse-native experiments, vendor lock-in experimentation. Also triggers when a team is asking about cost, governance, or migration cost across experimentation tools, or when an evaluation is starting."
---

# Experimentation Platform Orchestrator

A senior product and engineering leader's playbook for making the experimentation platform decision and recovering from making it wrong.

Picking an experimentation platform is one of those decisions that looks easy at the start and compounds for years afterward. The wrong choice costs you in lost experiments (because the team avoids the painful workflow), in cost (because the wrong pricing model penalizes your usage shape), in vendor lock-in (because migration is real engineering work, not a config change), and in cultural drift (because the platform's defaults shape what your team thinks experimentation is).

This skill is the discipline that makes the decision well the first time and the migration plan when you didn't.

When to use this skill: choosing a platform from scratch, evaluating whether to switch, deciding whether to consolidate from multi-platform to single, or planning a migration that has already been approved.

---

## What this skill is for

This skill spans platform selection, multi-platform decisions, migration planning, and governance setup. It does not cover experiment design (use `experiment-design`), result interpretation (use `experimentation-analytics`), or feature flag operations (use `feature-flagging`). Pair this skill with the relevant integrations microsite when you need platform-specific MCP details.

The audience is a PM, engineering leader, or data lead who is making the decision or recovering from a previous one. The voice is decisive. There is no "it depends, evaluate them all yourself." The decision space has real shape, and a senior advisor can map your situation to a defensible answer in an afternoon.

---

## Reference files

- [`references/platform-decision-matrix.md`](references/platform-decision-matrix.md) - Context-to-platform matrix with worked examples for the most common decision contexts.
- [`references/migration-playbook.md`](references/migration-playbook.md) - Step-by-step migration patterns for the five common migrations including effort estimates and validation approaches.
- [`references/mcp-capability-comparison.md`](references/mcp-capability-comparison.md) - Side-by-side MCP capability matrix across the seven platforms.
- [`references/multi-platform-orchestration.md`](references/multi-platform-orchestration.md) - Ownership boundaries, shared metric definitions, and reconciliation dashboards for genuine multi-platform setups.
- [`references/cost-and-pricing-models.md`](references/cost-and-pricing-models.md) - Pricing shapes, real-world cost ranges at different traffic tiers, and finance conversation patterns.
- [`references/governance-and-team-setup.md`](references/governance-and-team-setup.md) - Permission tiers, audit trail requirements, environment promotion rules, and team fit assessment.
- [`references/common-mistakes.md`](references/common-mistakes.md) - Twelve failure patterns with symptom, root cause, fix, and prevention for each.

---


## Conditional methods

Before applying a method below, read its linked section. For a narrow task select only relevant methods; for a full audit/design use the framework and relevant failure patterns. Existing references remain available for deeper details.

- The 7 considerations for the platform decision: [method](references/domain-guide.md#the-7-considerations-for-the-platform-decision).
- Statsig: [method](references/domain-guide.md#statsig).
- PostHog: [method](references/domain-guide.md#posthog).
- GrowthBook: [method](references/domain-guide.md#growthbook).
- Optimizely: [method](references/domain-guide.md#optimizely).
- Amplitude: [method](references/domain-guide.md#amplitude).
- Eppo: [method](references/domain-guide.md#eppo).
- Kameleoon: [method](references/domain-guide.md#kameleoon).
- Decision matrix: which platform for which context: [method](references/domain-guide.md#decision-matrix-which-platform-for-which-context).
- Multi-platform: when warranted, when a mess: [method](references/domain-guide.md#multi-platform-when-warranted-when-a-mess).
- Migration patterns: [method](references/domain-guide.md#migration-patterns).
- The cost reality: [method](references/domain-guide.md#the-cost-reality).
- Governance and team fit: [method](references/domain-guide.md#governance-and-team-fit).
- The MCP capability layer: [method](references/domain-guide.md#the-mcp-capability-layer).
- When to defer the decision: [method](references/domain-guide.md#when-to-defer-the-decision).
- Common mistakes: [method](references/domain-guide.md#common-mistakes).
- The framework: 11 considerations for sustainable platform choice: [method](references/domain-guide.md#the-framework-11-considerations-for-sustainable-platform-choice).
- Closing: when in doubt, pick boring: [method](references/domain-guide.md#closing-when-in-doubt-pick-boring).
