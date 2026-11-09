---
name: "content-refresh-system"
description: "Systematic content refresh discipline. Quarterly audits, refresh prioritization (which pieces, when, how deep), refresh-vs-merge-vs-delete decisions, the lifecycle that distinguishes intentional refresh from set-and-forget decay. Builds on the refresh sections of pillar-content-architecture and editorial-qa with a program-level discipline. Triggers on content refresh, content decay, content audit, refresh prioritization, content lifecycle, refresh strategy, traffic decay, ranking drop, content freshness, evergreen content, content maintenance. Also triggers when traffic is eroding silently across an aging content library, when teams cannot decide which pieces to refresh, or when refresh work is happening but the impact is unclear."
---

# Content Refresh System

A senior editorial leader's playbook for systematic content refresh. The discipline that distinguishes intentional refresh programs from set-and-forget decay, and the prioritization framework that prevents both over-refresh (refresh-everything-on-calendar) and under-refresh (refresh-nothing-until-traffic-collapses).

Content decays. Search behavior shifts; SERP intent reshapes; facts go stale; competitors publish stronger pieces; the brand's own positioning evolves past what older pieces represent. Programs that ignore this reality watch traffic erode silently across the library. Programs that overreact (rewriting everything on calendar) burn editorial capacity that should be producing new flagship work. The discipline is in the middle: refresh what matters when signals say so, and document the decisions so the program is auditable.

This skill is the program-level refresh discipline across the whole content library. It builds on `pillar-content-architecture`'s hub-level refresh consideration (refresh as ONE consideration in hub design) and `editorial-qa`'s pre-publish quality gate (this skill is post-publish lifecycle, not pre-publish QA). Together those skills cover content quality at the moments quality decisions get made; this skill covers the moments between, when content is in the field and decaying or holding.

The voice is the senior editorial leader who has watched refresh programs fail in both directions and who has shipped the systems that produced durable refresh discipline.

When to use this skill: building a refresh program from scratch, auditing why refresh work is happening but traffic is not responding, designing the prioritization that keeps refresh tractable across a 200-piece or 2,000-piece library, or fixing a refresh program that is eating editorial capacity without clear results.

---

## What this skill covers

This skill spans the post-publish lifecycle of content. The content suite distinction:

- `content-strategy` is program scope: what to produce.
- `pillar-content-architecture` is HUB scope; refresh appears as ONE consideration in hub design.
- `content-brief-authoring` is per-piece scope at production time.
- `content-and-copy` is execution scope at production time.
- `editorial-qa` is gate scope: pre-publish verification.
- **`content-refresh-system` (this skill)** is lifecycle scope: program-level refresh discipline across the whole content library, after pieces are in the field.

The audience: editorial leads, content directors, content ops managers, in-house teams running content libraries of 50-5,000+ pieces, agencies maintaining client content programs across years.

What is not in scope: writing the refreshed pieces themselves (that is `content-and-copy`), the brief that drives the refresh (that is `content-brief-authoring`), the pre-publish gate on the refreshed piece (that is `editorial-qa`). This skill is the prioritization and lifecycle discipline; the actual content work plugs into the existing skills.

---

## If required data is unavailable

This skill's output depends on data, measurements, or tool results it cannot generate on its own. When a required input, tool, or data source is unavailable or unverifiable, the sanctioned output is the deliverable with the gap stated: what was needed, what was actually obtained or verified, and which parts of the output are affected. Fabricating, estimating, or interpolating a required number to complete the deliverable is never sanctioned. A stated gap is a complete answer.

---

## Reference files

- [`references/refresh-signals-checklist.md`](references/refresh-signals-checklist.md) - Five signal categories with detection patterns. Traffic decay, ranking drops, factual staleness, SERP intent shift, content drift. The audit pattern that surfaces signals across the library.
- [`references/audit-cadence-patterns.md`](references/audit-cadence-patterns.md) - Quarterly audit vs continuous monitoring vs hybrid. Tradeoffs, integration patterns, alert-threshold design.
- [`references/refresh-prioritization-matrix.md`](references/refresh-prioritization-matrix.md) - 2x2 matrix with quadrant strategies. High-value-decaying as top priority; low-value-decaying audited for merge or delete; the discipline of NOT refreshing the high-value-stable quadrant.
- [`references/refresh-depth-decision.md`](references/refresh-depth-decision.md) - Light edit, substantial revision, full rewrite, structural redesign. Time investment per depth, signal-to-depth matching, depth-creep anti-pattern.
- [`references/refresh-vs-merge-vs-delete.md`](references/refresh-vs-merge-vs-delete.md) - Disposition criteria. When to refresh, when to merge, when to delete and redirect. The under-recognized failure of refreshing pieces that should have been merged.
- [`references/refresh-execution-patterns.md`](references/refresh-execution-patterns.md) - Single owner per refresh, editorial-workflow integration, capacity allocation, batching vs integration tradeoffs.
- [`references/re-promotion-after-refresh.md`](references/re-promotion-after-refresh.md) - Schema markup, visible-date update, search-engine resubmission, audience re-share, internal linking refresh.
- [`references/effectiveness-measurement.md`](references/effectiveness-measurement.md) - Per-refresh tracking, 30/90-day recovery measurement, pattern detection, the refresh-that-did-not-work review.
- [`references/common-refresh-failures.md`](references/common-refresh-failures.md) - 11+ failure patterns with diagnoses and fixes.

---


## Conditional methods

Before applying a method below, read its linked section. For a narrow task select only relevant methods; for a full audit/design use the framework and relevant failure patterns. Existing references remain available for deeper details.

- Refresh-everything vs refresh-nothing vs triaged-refresh: [method](references/domain-guide.md#refresh-everything-vs-refresh-nothing-vs-triaged-refresh).
- Refresh signals: [method](references/domain-guide.md#refresh-signals).
- The audit cadence: [method](references/domain-guide.md#the-audit-cadence).
- Refresh prioritization: [method](references/domain-guide.md#refresh-prioritization).
- Refresh depth options: [method](references/domain-guide.md#refresh-depth-options).
- Refresh vs merge vs delete decisions: [method](references/domain-guide.md#refresh-vs-merge-vs-delete-decisions).
- Refresh execution patterns: [method](references/domain-guide.md#refresh-execution-patterns).
- Re-promotion after refresh: [method](references/domain-guide.md#re-promotion-after-refresh).
- Refresh tracking and effectiveness measurement: [method](references/domain-guide.md#refresh-tracking-and-effectiveness-measurement).
- Common failure modes: [method](references/domain-guide.md#common-failure-modes).
- The framework: 12 considerations for content refresh: [method](references/domain-guide.md#the-framework-12-considerations-for-content-refresh).
- Closing: refresh is content's immune system: [method](references/domain-guide.md#closing-refresh-is-contents-immune-system).
