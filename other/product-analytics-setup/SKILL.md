---
name: "product-analytics-setup"
description: "How to actually instrument product analytics correctly. Event taxonomy, property design, naming conventions, schema versioning, identity stitching, funnel design, retention cohorts, North Star metric selection, dashboard hygiene, instrumentation debt, and the failure modes that produce data nobody trusts. Triggers on product analytics setup, event taxonomy, tracking plan, instrumentation, schema versioning, North Star metric, retention cohorts, funnel design, naming conventions, instrument new feature, audit existing analytics, dashboard reconciliation, instrumentation debt, Mixpanel setup, Amplitude setup, PostHog setup, warehouse-native analytics. Also triggers when the team has data but cannot trust it, or when designing instrumentation for a new feature, or when auditing an existing setup that has drifted."
---

# Product Analytics Setup

A senior PM and analyst's playbook for instrumenting product analytics correctly the first time.

Most product analytics setups are some combination of inherited mistakes, dashboard sprawl, and events nobody trusts. The team launches a new feature; instrumentation gets bolted on under deadline pressure; naming drifts; properties are inconsistent; six months later nobody can answer simple questions because the answer depends on which event you trust.

This skill is the discipline that prevents that. It assumes you have answered the strategic questions about what to measure (see `analytics-strategy`). It assumes you have a tool connected (Mixpanel, Heap, PostHog, Amplitude, or warehouse-native via BigQuery, Snowflake, or dbt). The hard part is the systematic execution: naming conventions, property design, schema versioning, funnel construction, cohort definitions, retention measurement.

When to use this skill: setting up product analytics from scratch, auditing an existing instrumentation, fixing a "we have data but cannot trust it" problem, or designing instrumentation for a new feature.

---

## What this skill is for

This skill spans instrumentation execution. It does not cover measurement strategy (use `analytics-strategy`), experimentation result interpretation (use `experimentation-analytics`), paid media analytics (use `ads-performance-analytics`), or platform decisions (use `experimentation-platform-orchestrator`). Pair this skill with the relevant integrations microsite for your specific tool.

The clean distinction from analytics-strategy. That skill (Growth category) is strategic: what to measure and why, KPI hierarchy, dashboard architecture, attribution models. This skill (Product category) is execution: how to actually instrument the product correctly. The two compose. Read analytics-strategy first to decide what matters; read this skill to instrument it.

---

## If required data is unavailable

This skill's output depends on data, measurements, or tool results it cannot generate on its own. When a required input, tool, or data source is unavailable or unverifiable, the sanctioned output is the deliverable with the gap stated: what was needed, what was actually obtained or verified, and which parts of the output are affected. Fabricating, estimating, or interpolating a required number to complete the deliverable is never sanctioned. A stated gap is a complete answer.

---

## Reference files

- [`references/event-taxonomy-template.md`](references/event-taxonomy-template.md) - Canonical event spec for typical SaaS: account, user, activation, engagement, conversion, retention events with required properties.
- [`references/property-design-patterns.md`](references/property-design-patterns.md) - Event-level vs user-level patterns. Type discipline. Worked example: `product_viewed` right vs wrong.
- [`references/naming-convention-reference.md`](references/naming-convention-reference.md) - Complete style guide. snake_case, past tense, object-action. Boolean prefixes. Money in cents. Timestamps with `_at` suffix. Do/don't side-by-side.
- [`references/schema-versioning-patterns.md`](references/schema-versioning-patterns.md) - Additive vs breaking changes. `_v2` suffix pattern. Data contract in TypeScript. CI lint patterns.
- [`references/funnel-design-templates.md`](references/funnel-design-templates.md) - Activation, conversion, engagement, feature adoption funnels. Time windows, anchor events, drop-off interpretation.
- [`references/cohort-definition-patterns.md`](references/cohort-definition-patterns.md) - Acquisition, behavioral, property, combined cohorts. SQL examples plus tool-specific examples.
- [`references/north-star-metric-selection.md`](references/north-star-metric-selection.md) - NSM rules with examples by product type. Anti-patterns. Migration patterns when changing NSM.
- [`references/instrumentation-audit-checklist.md`](references/instrumentation-audit-checklist.md) - Quarterly audit playbook: schema review, volume sanity checks, dashboard freshness, owner audit, deprecation candidates.
- [`references/common-failures.md`](references/common-failures.md) - Twelve failure patterns with symptom, root cause, fix, prevention.

---


## Conditional methods

Before applying a method below, read its linked section. For a narrow task select only relevant methods; for a full audit/design use the framework and relevant failure patterns. Existing references remain available for deeper details.

- The instrumentation hierarchy: [method](references/domain-guide.md#the-instrumentation-hierarchy).
- Event taxonomy design: [method](references/domain-guide.md#event-taxonomy-design).
- Property design: event-level vs user-level: [method](references/domain-guide.md#property-design-event-level-vs-user-level).
- Naming conventions: [method](references/domain-guide.md#naming-conventions).
- Schema versioning: [method](references/domain-guide.md#schema-versioning).
- Funnel design: [method](references/domain-guide.md#funnel-design).
- Cohort definitions: [method](references/domain-guide.md#cohort-definitions).
- Retention measurement: [method](references/domain-guide.md#retention-measurement).
- North Star and supporting metrics: [method](references/domain-guide.md#north-star-and-supporting-metrics).
- The trustable dashboard principle: [method](references/domain-guide.md#the-trustable-dashboard-principle).
- Instrumentation debt: [method](references/domain-guide.md#instrumentation-debt).
- Common failure modes: [method](references/domain-guide.md#common-failure-modes).
- The framework: 12 considerations for trustable product analytics: [method](references/domain-guide.md#the-framework-12-considerations-for-trustable-product-analytics).
- Closing: when in doubt, instrument less: [method](references/domain-guide.md#closing-when-in-doubt-instrument-less).
