---
name: progressive-enhancement-planner
description: Plans progressively enhanced web features by defining the baseline semantic HTML experience, optional JavaScript enhancements, dependency and failure behavior, and accessibility requirements. Use when a user asks how a page, form, navigation flow, widget, or interaction should remain usable before JavaScript loads, when JavaScript fails, or when enhanced capabilities are unavailable.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: project-planning
  task_type: planner
  audience: frontend-developers-and-product-teams
  tags:
    - progressive-enhancement
    - semantic-html
    - javascript
    - resilience
    - failure-states
    - accessibility
    - frontend-planning
  status: draft
  side_effects: none
---

# Progressive Enhancement Planner

## Purpose

Turn a web feature or interaction into an implementation-ready progressive enhancement plan. Define a complete server-and-HTML baseline first, then layer JavaScript behavior without making core content, navigation, or task completion depend unnecessarily on enhancement code.

## When to use this skill

Use this skill when:

- A feature must remain useful before JavaScript loads or when it fails.
- A team needs to separate native HTML behavior from enhanced client-side behavior.
- The task involves forms, navigation, disclosure, filtering, search, validation, uploads, dialogs, tabs, live updates, or other interactive UI.
- The user asks for fallback behavior, resilience, graceful degradation, or a no-JavaScript experience.
- Accessibility requirements must be defined for both baseline and enhanced states.
- A proposed component depends on browser APIs, network requests, third-party scripts, hydration, or client-side rendering.

Do not use this skill when:

- The user only wants implementation and an existing approved plan already defines baseline and enhanced behavior.
- The task is a native application with no HTML-delivered experience.
- The request is solely a code-level accessibility audit of an implemented feature; use a focused accessibility review skill instead.
- The request only needs a broad user-flow map without technical enhancement boundaries; use `user-flow-planner` instead.

## Inputs to inspect

Start with the smallest relevant set:

- The feature brief, user story, acceptance criteria, or existing implementation plan.
- Current templates, routes, server handlers, and HTML output.
- Relevant components, event handlers, client state, and data-fetching code.
- Forms, links, buttons, status messages, validation rules, and error responses.
- CSS that hides, reveals, reorders, or otherwise changes content based on JavaScript state.
- Browser API, framework hydration, network, authentication, storage, and third-party dependencies.
- Accessibility requirements, supported browsers, performance constraints, and analytics needs.

If no repository or implementation exists, work from the supplied feature description and label assumptions explicitly.

## Workflow

1. **Define the essential user outcome.**
   - State the primary task in one sentence.
   - Identify the content and actions required to complete it.
   - Separate essential outcomes from convenience, speed, animation, personalization, and visual polish.

2. **Map dependencies and capability assumptions.**
   - List required server, network, JavaScript, browser API, storage, authentication, and third-party capabilities.
   - Mark which dependencies are unavoidable and which can be enhancement-only.
   - Do not treat JavaScript availability as proof that every API, request, import, or hydration step will succeed.

3. **Design the baseline HTML experience.**
   - Use semantic elements and native controls with meaningful document order.
   - Give navigation real URLs and give data-changing actions an appropriate form submission path.
   - Define server-rendered content, input labels, instructions, constraints, status messages, validation, errors, and success responses.
   - Ensure the essential task can be understood and completed through ordinary page loads where technically feasible.
   - Identify any genuinely impossible no-JavaScript capability and provide the clearest useful alternative.

4. **Define the enhancement boundary.**
   - State exactly what JavaScript adds: reduced page loads, inline feedback, richer controls, optimistic updates, live regions, focus coordination, or other improvements.
   - Preserve the baseline URLs, form semantics, names, methods, and server contracts unless a change is explicitly justified.
   - Describe when enhancement activates and how capability detection is performed.
   - Add enhancement hooks without using them as the sole source of semantics or styling meaning.

5. **Specify enhanced interaction behavior.**
   - Describe triggers, state transitions, loading behavior, cancellation, completion, and recovery.
   - Define keyboard operation, focus placement, focus return, accessible names, relationships, and announcements.
   - Prevent duplicate submissions and conflicting baseline and enhanced actions.
   - Explain how history, URLs, refresh, back/forward navigation, and deep links behave when relevant.

6. **Plan failure and interruption states.**
   Cover failures independently rather than using one generic “JavaScript failed” case:
   - Script never loads, is blocked, or has a syntax/runtime error.
   - Hydration is delayed or fails after HTML appears.
   - Dynamic import or browser API is unavailable.
   - Network is offline, slow, interrupted, timed out, or returns an error.
   - A third-party dependency is blocked or unavailable.
   - Storage, permissions, authentication, or session state is unavailable.
   - An enhanced action fails after the user has entered data or changed state.

   For each relevant failure, define the preserved baseline path, visible feedback, data retention, retry behavior, and safe recovery route.

7. **Define accessibility requirements for every layer.**
   - Baseline content and controls must be perceivable, operable, understandable, and robust without enhancement.
   - Enhanced behavior must preserve semantic roles, names, values, relationships, reading order, and expected keyboard behavior.
   - Dynamic updates must provide timely, non-duplicative feedback without unexpected focus movement.
   - Loading, disabled, invalid, busy, success, and error states must be communicated beyond color or motion.
   - Respect zoom, reflow, text resizing, reduced motion, forced colors, and input method differences where relevant.
   - Do not use ARIA to recreate behavior already supplied reliably by native HTML.

8. **Create an implementation sequence.**
   - Build and verify the server/HTML path first.
   - Add stable enhancement hooks and CSS states.
   - Layer JavaScript behavior in independently testable increments.
   - Add recovery handling before optional polish.
   - Identify checkpoints where the baseline must be re-tested after enhancement work.

9. **Write layered acceptance tests.**
   Include tests for:
   - HTML response before JavaScript executes.
   - JavaScript disabled or blocked.
   - Enhancement loaded successfully.
   - Slow loading and partial initialization.
   - Each material dependency or request failure.
   - Keyboard-only and screen-reader-relevant behavior.
   - Refresh, history, duplicate action, and data preservation behavior where applicable.

10. **Record tradeoffs and unresolved decisions.**
    - Distinguish confirmed requirements from assumptions.
    - Explain any essential outcome that cannot have a practical baseline equivalent.
    - Flag architecture choices that would make the baseline disproportionately costly or impossible.
    - Do not claim resilience unless the plan includes a verifiable recovery path.

## Output format

Return the plan using this structure:

```md
## Outcome and assumptions

- Essential user outcome: ...
- Assumptions: ...
- Unresolved decisions: ...

## Capability layers

| Layer | Available capabilities | User experience | Required dependencies |
|---|---|---|---|
| Baseline HTML | ... | ... | ... |
| Enhanced JavaScript | ... | ... | ... |

## Baseline HTML contract

- Content and document structure: ...
- Navigation and actions: ...
- Server behavior: ...
- Validation, errors, and success: ...

## Enhancement contract

- Activation and detection: ...
- Added behavior: ...
- State, focus, and announcements: ...
- URL and history behavior: ...

## Failure and recovery matrix

| Failure condition | User-visible result | Preserved baseline path | Recovery and data retention |
|---|---|---|---|

## Accessibility requirements

- Baseline: ...
- Enhanced: ...
- Dynamic feedback: ...
- Display and input adaptations: ...

## Implementation sequence

1. ...

## Acceptance checklist

- [ ] ...
```

Keep the plan proportional. Omit irrelevant failure categories, but never omit the baseline, enhancement boundary, accessibility requirements, and validation for enhancement failure.

## Quality bar

The task is complete only when:

- The essential outcome is explicit and separated from optional enhancement.
- The baseline is a concrete HTML/server behavior, not a vague promise that content “still works.”
- Links and forms retain meaningful native behavior wherever appropriate.
- Enhancement activation, state changes, and dependency assumptions are defined.
- Material failures have visible feedback and a recovery path that preserves user effort when feasible.
- Accessibility requirements cover both baseline and enhanced layers.
- Acceptance tests can prove the baseline before and after JavaScript is introduced.
- Assumptions, unavoidable limitations, and unresolved decisions are visible.
- The output remains a plan and does not modify files unless the user separately requests implementation.

## Edge cases

- **Client-only product:** Define the smallest server-rendered orientation, authentication, status, or recovery experience possible; explain why the essential application cannot operate without JavaScript.
- **Offline capability:** Do not promise offline support merely because a service worker exists. Define cached resources, stale data behavior, queued actions, conflict handling, and reconnection recovery.
- **File uploads and payments:** Prefer native submission where supported, preserve entered metadata, and never imply that retrying a non-idempotent action is automatically safe.
- **Real-time interfaces:** Provide an initial snapshot and a manual refresh or reconnect path when live transport fails.
- **Third-party widgets:** Provide first-party content, links, contact routes, or equivalent task paths when the embed is blocked.
- **Sensitive data:** Do not persist user input in client storage without a clear privacy and security basis.
- **CSS-dependent disclosure:** Ensure baseline content is not permanently hidden when the class or attribute that signals successful enhancement is never applied.
- **Framework hydration:** Treat server-rendered markup as interactive only when its native semantics genuinely work before hydration.

## Related skills

- `user-flow-planner`
- `implementation-plan-writer`
- `constraint-mapper`
- `requirements-gap-finder`
- `interface-state-coverage-review`
