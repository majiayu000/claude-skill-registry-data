---
name: callesnikov-design-checklist
description: Use Checklist Design as a focused UX and UI quality gate when Codex designs, implements, reviews, or refines mobile apps, web apps, websites, design systems, components, screens, and user flows. Trigger for app planning, screen or flow design, UI implementation, design reviews, UX audits, acceptance criteria, missing-state analysis, interaction polish, or requests to make an application more complete and usable.
---

# Callesnikov Design Checklist

Use [Checklist Design](https://www.checklist.design/) to expose missing states, unclear actions, broken transitions, weak copy, dead ends, and incomplete user flows before they become expensive defects. Treat its checklists as prompts for engineering judgment, not as a universal specification.

## Core principle

Connect three levels of product quality:

1. **Surface**: the screen or product area, such as mobile onboarding or a web-app empty state.
2. **Component**: the controls involved, such as buttons, inputs, modals, loading indicators, or toasts.
3. **Flow**: what happens before, during, after, and when the action fails.

A polished component does not rescue an incomplete flow. A complete flow still needs accessible, platform-appropriate components.

## Workflow

### 1. Establish the review target

Identify the platform, user goal, current artifact, and delivery stage. Inspect available code, screenshots, prototypes, requirements, or running UI before making claims.

Choose one mode:

- **Design mode**: derive requirements and states before or during implementation.
- **Audit mode**: compare an existing artifact against relevant checklists and cite evidence.
- **Repair mode**: implement the highest-impact missing behavior, then verify it.

Ask a question only when an unknown would materially change the product behavior. Otherwise state the assumption and continue.

### 2. Select focused checklists

Read [references/site-routing.md](references/site-routing.md) before browsing the site.

Choose:

- one primary checklist for the screen, component, or flow being worked on;
- zero to three related checklists for controls or adjacent steps that materially affect the same user goal.

Do not load every vaguely related checklist. Prefer the smallest set that covers the real interaction.

### 3. Inspect Checklist Design live

Open the exact checklist page when its route is known. Otherwise use `/browse` or the site's search rather than guessing many URLs.

For each selected page:

1. Read its purpose statement.
2. Read every checklist item and its rationale.
3. Open the **Documentation** tab when present and inspect its examples.
4. Inspect related links only when they expose a missing component or flow dependency.
5. Record the source URL and access date for findings that depend on the site.

Prefer live content because the catalog can change. Paraphrase the guidance; do not bulk-copy or mirror the site.

If the site cannot be reached, say so. Continue from the available artifact and general UX engineering knowledge, but do not label unverified advice as Checklist Design guidance.

### 4. Adapt rather than copy

For every candidate item, decide whether it is applicable to this product, platform, audience, and risk level.

Reconcile the checklist with:

- the product's established design system and interaction patterns;
- current official platform guidance when behavior is platform-specific;
- accessibility, localization, privacy, security, and legal constraints;
- technical architecture and data lifecycle;
- the user's explicit scope and product decisions.

Mark irrelevant items `N/A` with a reason. Never invent a feature merely to satisfy a checklist.

### 5. Turn guidance into executable work

Read [references/review-framework.md](references/review-framework.md) and produce only the detail needed for the task.

For design work, define:

- the user's entry point and intended outcome;
- the happy path and navigation;
- loading, empty, error, offline, permission, and recovery behavior where relevant;
- component states and feedback;
- concise acceptance criteria.

For audits, classify each relevant item as `Pass`, `Partial`, `Missing`, `N/A`, or `Unknown`. Attach concrete evidence and prioritize by user impact. Separate observed defects from recommendations.

For implementation tasks, change the existing project conservatively, preserve its architecture and visual language, and verify the behavior in proportion to risk.

### 6. Close the loop

End with:

- what is already sound;
- the highest-impact gaps;
- what changed, if implementation was requested;
- what was verified and what remains unverified;
- direct links to the Checklist Design pages actually used.

Do not claim the app is complete merely because all selected checklist items pass. Checklists reduce omissions; they do not replace user testing, platform validation, analytics, accessibility testing, or domain expertise.

## Output discipline

- Match the user's language.
- Lead with product consequences, not generic design theory.
- Prefer a short prioritized review over a long unranked checklist.
- Ground claims in code, screenshots, runtime behavior, requirements, or an explicit unknown.
- Write acceptance criteria as observable behavior, not visual adjectives.
- Preserve intentional product tradeoffs and record why an item is `N/A`.
