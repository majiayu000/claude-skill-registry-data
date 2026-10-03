---
name: design-spec
description: Produce implementation-ready UI and UX specifications covering structure, states, behavior, content, responsive rules, accessibility expectations, tokens, components, and acceptance details without over-prescribing engineering internals.
---
# UI/UX Design Specification

Use when approved interface design must be handed to implementation.

## Procedure
1. Reference the accepted product requirements, user flow, and design artifacts so scope and decision provenance are clear.
2. Specify component hierarchy and content regions using existing design-system components where appropriate.
3. Document every material state: loading, empty, populated, validation, error, success, disabled, permission, offline or slow, destructive confirmation, and interruption or recovery as relevant.
4. Specify interactions and transitions including triggers, selection, navigation, keyboard or focus expectations, drag or gesture alternatives, and cancellation.
5. Define responsive or reflow behavior, minimum and maximum sizing, overflow, localization expansion, and density changes.
6. Record content or copy placeholders only where wording is unresolved; route owned copy to the appropriate content specialist.
7. Annotate accessibility-relevant semantics, names or labels, state announcements, focus order or management, contrast-sensitive behavior, and reduced-motion expectations.
8. List assets, tokens, variants, edge cases, dependencies, and acceptance criteria, then review the spec with engineering for ambiguity before build.

## Decision rules
- A design spec explains product behavior and visual or interaction contract, not private engineering architecture.
- Do not omit failure states because the mockup looks cleaner without them.
- Use design-system names that map to actual implementation where possible.
- Ambiguity found during handoff should be resolved in the spec, not buried in chat.

## Quality gate
The spec is ready when engineers can implement every important state and interaction without inventing product behavior, responsive and accessibility expectations are explicit, dependencies and assets are traceable, and unresolved questions are clearly owned rather than hidden.