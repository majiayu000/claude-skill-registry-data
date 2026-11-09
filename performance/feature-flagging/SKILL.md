---
name: "feature-flagging"
description: "Operational discipline for feature flags as production infrastructure. Flag types, naming, targeting rules, rollout strategy, lifecycle, governance, stale flag management, and the technical debt patterns that bite teams who weren't deliberate about it."
---

# Feature Flagging

A senior engineer's playbook for using feature flags well, not just frequently.

Feature flags are infrastructure. Treated as such, they enable kill switches, gradual rollouts, A/B experiments, permission gates, and operational toggles without redeploys. Treated casually, they become the largest accumulating technical debt in your codebase: thousands of dead flags, conflicting evaluation logic, brittle targeting, and a permission surface no one fully understands.

This skill is the discipline that prevents the second outcome. It assumes you have a feature flag platform (LaunchDarkly, Flagsmith, Split.io, VWO FME, GrowthBook, Statsig, PostHog, Optimizely; the platform does not matter for the principles). It assumes your engineering team can implement targeting rules and SDK integration. The hard part is the operational discipline, and that is what is here.

When to use this skill: any time you are about to introduce a flag, modify a flag, audit existing flags, or design a flag-related governance policy.

---

## What this skill is for

The skill spans the operational lifecycle of a flag from creation through retirement. Flag types and the discipline of not mixing them. Naming conventions that survive code review. Lifecycle expectations baked in at creation, not bolted on later. Targeting rules that compose without fragility. Rollout strategies that match the risk profile of the launch. Stale flag management on a quarterly cadence. Governance and permissions that balance access with audit. Performance considerations so flags do not become a latency tax. Testing patterns that cover both branches. Rollback discipline. Observability across rollouts.

The skill does not cover experiment design; for hypothesis writing, sample size, MDE, and the discipline of arriving at a defensible decision, see the `experiment-design` skill. It does not cover statistical analysis or variance reduction; those live in the `experimentation-analytics` skill. It does not cover platform-specific tooling; for MCP commands, auth, and platform-specific configuration, consult the chosen platform's documentation. This skill produces the operational shape; the platform implements it.

---

## If required data is unavailable

This skill's output depends on data, measurements, or tool results it cannot generate on its own. When a required input, tool, or data source is unavailable or unverifiable, the sanctioned output is the deliverable with the gap stated: what was needed, what was actually obtained or verified, and which parts of the output are affected. Fabricating, estimating, or interpolating a required number to complete the deliverable is never sanctioned. A stated gap is a complete answer.

---

## Reference files

The following reference files extend this skill:

- [`references/flag-naming-conventions.md`](references/flag-naming-conventions.md): typed prefixes, owner prefixes, semantic naming patterns, and the migration plan for existing badly-named flags.
- [`references/flag-lifecycle-checklist.md`](references/flag-lifecycle-checklist.md): birth-to-death checklist organized by lifecycle phase.
- [`references/flag-types-reference.md`](references/flag-types-reference.md): the five flag types in detail with worked examples and common pitfalls.
- [`references/stale-flag-cleanup-playbook.md`](references/stale-flag-cleanup-playbook.md): quarterly cleanup process and the orphan-ownership pattern.
- [`references/targeting-rule-patterns.md`](references/targeting-rule-patterns.md): common patterns and anti-patterns for targeting rules.
- [`references/flag-rollout-strategies.md`](references/flag-rollout-strategies.md): percentage, cohort, geo, time-based, and combination strategies with a worked example.
- [`references/governance-and-permissions.md`](references/governance-and-permissions.md): permission tiers, environment promotion, approval workflows, and emergency override.

---


## Conditional methods

Before applying a method below, read its linked section. For a narrow task select only relevant methods; for a full audit/design use the framework and relevant failure patterns. Existing references remain available for deeper details.

- The five flag types: [method](references/domain-guide.md#the-five-flag-types).
- Flag naming conventions: [method](references/domain-guide.md#flag-naming-conventions).
- The flag lifecycle: [method](references/domain-guide.md#the-flag-lifecycle).
- Targeting rules and segmentation: [method](references/domain-guide.md#targeting-rules-and-segmentation).
- Rollout strategies: [method](references/domain-guide.md#rollout-strategies).
- Stale flag management: [method](references/domain-guide.md#stale-flag-management).
- Governance and permissions: [method](references/domain-guide.md#governance-and-permissions).
- Flag dependencies and conflicts: [method](references/domain-guide.md#flag-dependencies-and-conflicts).
- Performance considerations: [method](references/domain-guide.md#performance-considerations).
- Testing flag-gated code: [method](references/domain-guide.md#testing-flag-gated-code).
- Rollback discipline: [method](references/domain-guide.md#rollback-discipline).
- Observability on flags: [method](references/domain-guide.md#observability-on-flags).
- Common failures (rapid-fire): [method](references/domain-guide.md#common-failures-rapid-fire).
- The framework: 14 considerations for sustainable feature flagging: [method](references/domain-guide.md#the-framework-14-considerations-for-sustainable-feature-flagging).
- Closing: when to remove a flag: [method](references/domain-guide.md#closing-when-to-remove-a-flag).
