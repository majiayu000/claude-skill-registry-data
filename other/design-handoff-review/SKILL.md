---
name: design-handoff-review
description: Review product designs before engineering handoff or release for flow and state coverage, business-rule alignment, implementation clarity, accessibility, responsiveness, analytics, and testability.
---

# Design Handoff Review

Assess whether a design package is sufficiently complete and unambiguous for engineering and QA, and produce an actionable handoff gap list.

## Working rules

- Review only what can be observed in the supplied designs, prototypes, requirements, component documentation, and implementation evidence.
- Separate a confirmed defect, a conflict with requirements, a missing specification, and a recommendation.
- Do not claim pixel-perfect comparison, responsive behavior, interaction behavior, or component usage when the available artifact cannot prove it.
- Label inferred behavior and ask for confirmation instead of inventing states or business rules.
- Prioritize user harm, blocked implementation, irreversible actions, accessibility, and likely rework over cosmetic preferences.
- Respect the existing design system. Recommend a new pattern only when the current system does not cover the need or creates a concrete usability problem.
- Do not edit design files, tickets, or code unless the user explicitly requests those changes.

## Review workflow

1. Establish the handoff boundary: platforms, breakpoints, target flows, release scope, supplied requirements, design-system version, and artifacts available for inspection.
2. Map the intended user journey and enumerate screens, transitions, roles, entry points, exits, and irreversible actions.
3. Check coverage where relevant:
   - happy, alternate, cancellation, recovery, and back-navigation paths;
   - loading, skeleton, empty, error, offline, timeout, partial-success, disabled, and success states;
   - permissions, authentication, destructive confirmations, concurrency, and duplicate actions;
   - business rules, data formats, limits, validation, sorting, filtering, pagination, and extreme content;
   - components, tokens, variants, naming, reusable patterns, and implementation annotations;
   - responsive layouts, touch targets, keyboard behavior, focus order, contrast, labels, and assistive technology;
   - content, localization expansion, dates, numbers, currencies, and error-message recovery guidance;
   - analytics events, acceptance criteria, feature flags, dependencies, and rollout behavior.
4. Cross-check designs against requirements and identify mismatches in scope, terminology, state transitions, rules, and success conditions.
5. Classify findings:
   - **Blocker**: engineering or QA cannot implement or verify the core behavior responsibly.
   - **Major**: likely user harm, accessibility failure, rule conflict, or expensive rework.
   - **Minor**: clarity, consistency, or polish issue with limited implementation risk.
6. Convert the review into handoff-ready decisions, questions, state coverage, and acceptance scenarios.

## Default deliverable

Use the smallest useful format, normally:

1. Handoff readiness recommendation
2. Scope and artifacts reviewed
3. Findings by severity, with location, evidence, impact, and owner
4. Flow and state coverage matrix
5. Requirement-to-design conflicts
6. Open implementation questions
7. Acceptance scenarios and analytics gaps
8. Final handoff checklist

When code or a running product is also supplied, clearly distinguish design-package completeness from implementation conformance.
