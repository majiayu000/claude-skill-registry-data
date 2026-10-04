---
name: action-surface-audit
description: Audits a conversation, codebase, app, website, mobile UI, product workflow, or business system for missing buttons, actions, controls, shortcuts, command surfaces, recovery options, navigation paths, and user-facing affordances without overcrowding the interface. Use when the user asks what buttons/actions are missing, wants broad UI action opportunities, asks whether a page lets users do everything it should, asks to improve app success through controls, or provides the master action-surface prompt.
---

# Action Surface Audit

## Quick Start

Use this skill to find high-value missing or underdeveloped user actions. Treat "buttons" broadly: buttons, links, menu items, toolbar controls, mobile gestures, command palette actions, bulk actions, recovery actions, navigation paths, shortcuts, and role-specific controls all qualify.

Do not limit the answer to 10 items unless the user explicitly asks for a fixed count. Recommend only actions that improve real workflows, reduce friction, increase clarity, strengthen trust, support business outcomes, improve security, improve mobile usage, or make the product more complete.

The goal is the perfect interface, not the maximum number of visible buttons. Every legitimate page-level task should be possible in context, but actions must be delivered through clear hierarchy: primary buttons for dominant tasks, secondary controls for supporting tasks, grouped menus for related actions, collapsed categories for lower-frequency actions, and advanced settings for rare or nuanced controls.

## Audit Prompt

Audit the current conversation, product idea, codebase, app, website, mobile app, UI, business workflow, feature area, or system being discussed.

Identify missing, underdeveloped, unclear, or high-value buttons, actions, controls, shortcuts, command surfaces, recovery options, navigation paths, workflow improvements, or user-facing affordances that should exist but do not yet exist.

Also answer: can the user do everything this page, entity, workflow, or state implies they should be able to do? Does every important thing on the page have an intended action path, and is the action available where the user naturally needs it?

Primary evaluation lens:

Actionability, Prioritization, Urgency, Confidence, Context, Relevance, Workflow, Recovery, Reversibility, Undo, Escalation, Confirmation, Preview, Bulk actions, Shortcuts, Searchability, Filtering, Sorting, Comparison, Selection, Editability, Saveability, Shareability, Exportability, Importability, Collaboration, Notifications, Reminders, Status, Traceability, History, Versioning, Ownership, Handoff, Approval, Review, Moderation, Governance, Permissions clarity, Error prevention, Error recovery, Empty states, Loading states, Success states, Disabled states, Mobile reachability, Thumb zone, Cross-device continuity, Offline recovery, Data confidence, Data freshness, Decision support, Time-to-value, Task completion, Operational efficiency, User intent, Business intent, and System visibility.

Broader product-quality lens:

Clarity, Organization, Trust, Speed, Simplicity, Consistency, Reliability, Usability, Navigation, Feedback, Accessibility, Responsiveness, Polish, Security, Performance, Maintainability, Scalability, Personalization, Conversion, Delight, Intuitive, Useful, Helpful, Frictionless, Predictable, Learnable, Efficient, Comfortable, Forgiving, Human, Guided, Focused, Calm, Engaging, Familiar, Empowering, Seamless, Approachable, Convenient, Satisfying, Layout, Hierarchy, Contrast, Spacing, Alignment, Typography, Readability, Visibility, Density, Balance, Flow, Structure, Affordance, Discoverability, Scannability, Legibility, Restraint, Precision, Cohesion, Stability, Durability, Flexibility, Extensibility, Modularity, Robustness, Resilience, Compatibility, Interoperability, Adaptability, Testability, Observability, Recoverability, Accuracy, Completeness, Freshness, Availability, Continuity, Architecture, Infrastructure, Backend, Frontend, Database, APIs, Authentication, Authorization, Caching, Monitoring, Logging, Deployment, Automation, Integration, Validation, State, Routing, Synchronization, Optimization, Refactoring, Positioning, Differentiation, Value, Demand, Retention, Activation, Acquisition, Revenue, Pricing, Credibility, Reputation, Loyalty, Support, Onboarding, Adoption, Engagement, Growth, Momentum, Privacy, Protection, Compliance, Encryption, Permissions, Safety, Verification, Accountability, Transparency, Control, Consent, Auditability, Integrity, Confidentiality, Touchability, Portability, Offline support, Notifications, Gestures, Battery efficiency, Lightweight design, Native-feeling behavior, Thumb-friendly controls, Adaptive layout, Compact UI, Fast-loading screens, Syncing, Device-aware behavior, Confidence, Relief, Ease, Certainty, Warmth, Professionalism, Calmness, Enjoyment, Motivation, Reassurance, Ownership, Progress, Trustworthiness, and overall product success.

## What To Look For

- Places where users can see information but cannot act on it.
- Places where the page implies a task, object, state, or next step but lacks the right in-context control.
- Places where a workflow requires too many manual steps.
- Places where users may get stuck without a clear next action.
- Places where actions are hidden, inconsistent, weakly labeled, or unavailable on mobile.
- Places where users must leave the current page or entity context to continue the same task.
- Places where a contextual workspace should let users continue related work inside the same event, dinner, client, menu, recipe, project, or operational circle.
- Places where too many visible buttons would cloud the UI and should instead become grouped actions, dropdowns, segmented controls, tabs, drawers, collapsed categories, or advanced settings.
- Places where related buttons should be consolidated under one category, menu, toolbar, command palette, or settings surface.
- Places where primary, secondary, destructive, rare, and advanced actions are not clearly separated.
- Places where error, loading, empty, disabled, or success states lack useful recovery actions.
- Places where navigation could be more direct.
- Places where different user roles need role-specific controls.
- Places where repeated actions should become reusable command surfaces.
- Places where users need clearer confirmation, preview, undo, history, or status visibility.
- Places where users need search, filter, sort, compare, select, bulk edit, export, import, save, or share controls.
- Places where the business would benefit from clearer activation, retention, conversion, support, pricing, revenue, adoption, or engagement actions.
- Places where security, privacy, permissions, consent, auditability, verification, or compliance need clearer user-facing controls.
- Places where mobile users need better thumb-friendly, compact, adaptive, fast-loading, offline, syncing, notification, gesture, or device-aware behavior.
- Places where engineering quality would improve through better maintainability, scalability, observability, testability, reliability, resilience, validation, automation, or integration.

## Output Format

For each recommendation, include:

1. Proposed label or action name
2. Where it should appear
3. Which user, role, or situation needs it
4. What it does
5. Why it is missing or underdeveloped
6. Expected user value
7. Expected business value
8. Implementation complexity
9. Recommended placement tier: primary, secondary, contextual, grouped menu, collapsed category, advanced setting, navigation, or command palette
10. Grouping or progressive-disclosure strategy
11. Risks, edge cases, or permissions concerns
12. Acceptance criteria
13. Verification steps

Separate the output into:

1. Quick wins
2. High-impact product improvements
3. Structural or platform-level improvements
4. Mobile-specific improvements
5. Security, trust, and permission improvements
6. Workflow, recovery, and status improvements
7. Business growth, retention, and conversion improvements
8. Ideas that should not be built yet, with reasons

Rank recommendations by impact, urgency, confidence, implementation effort, and breadth of benefit.

End with the top recommended implementation batch: the smallest set of buttons, actions, controls, shortcuts, or command surfaces that would create the broadest improvement across the app, product, business, or conversation context.

## ChefFlow Routing

For ChefFlow, this skill is usually planning or product intake. Do not implement discovered actions unless the user explicitly says "fire the queue", "build the queue", "execute this queue item now", "direct hotfix now", or "do not queue this". If the user wants to preserve recommendations, turn them into build-queue items with goal, scope, acceptance criteria, risks, dependencies, and verification.
