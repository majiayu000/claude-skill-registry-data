---
name: react-development
description: Build, review, debug, and maintain production React interfaces and component systems. Use for React components, hooks, state management, forms, routing, data fetching, accessibility, rendering performance, SSR, hydration, testing, or React framework integration.
---

# React Development

Act as the React engineer responsible for an interface that remains correct through loading, failure, navigation, concurrent rendering, assistive technology, and future product changes. Build around user tasks and data ownership, not component count or hook cleverness.

## Execution Workflow

1. **Inspect the app architecture.** Identify React version, framework/rendering model, router, styling system, component library, state/query libraries, test stack, API conventions, and existing accessibility patterns.
2. **Model the flow and state.** Define the user task, server/client state, transitions, permissions, loading/empty/error/success states, URL state, and mutation recovery before coding.
3. **Compose the interface.** Create focused components around meaningful boundaries. Keep fetch and mutation ownership close to the feature boundary; pass explicit props and callbacks.
4. **Implement accessible behavior.** Use semantic HTML, native controls where possible, keyboard interactions, focus management, and clear feedback.
5. **Verify runtime behavior.** Test primary and failure paths, inspect responsive layouts, and check for hydration, render, and interaction regressions.

## Step 0: Ground the Feature in a User Flow

Before creating components, establish:

1. **User job:** What does a person need to see, decide, or complete?
2. **Route and rendering model:** Which route owns this feature and is it server-rendered, client-rendered, streamed, or static?
3. **State ownership:** What is server state, URL state, local draft state, shared UI state, and derived state?
4. **Permissions and outcomes:** Who can perform the action, what succeeds, and what can fail or be retried?
5. **Acceptance proof:** Which keyboard flow, viewport, data state, and test demonstrate completion?

Inspect the route, nearby components, styling/tokens, data/query layer, router, existing primitives, and tests before adding a new pattern. Preserve an intentional design system; do not create a competing button, dialog, fetch wrapper, or state store for one feature.

## Feature Plan Template

```markdown
## React Feature Plan

**User goal:** <task and success condition>
**Route / rendering boundary:** <route, server/client decision>
**State ownership:** <server, URL, local, shared, derived>
**Data contract:** <load, cache, mutation, permissions, errors>
**UI states:** <loading, empty, error, unauthorized, pending, success>
**Accessibility:** <semantic structure, keyboard, focus, announcements>
**Verification:** <tests, responsive viewports, browser checks>
```

Only ask questions that change the architecture, user experience, or public behavior. Otherwise, state a reasonable assumption and proceed.

## Component Boundaries and Composition

Use this decision rule:

| Need | Put it in | Do not |
|---|---|---|
| Route data and permission check | Route/framework data boundary | Fetch the same data independently in many children |
| Pure display | Presentational component with explicit props | Let it read global state unnecessarily |
| User interaction local to one component | Local state/reducer | Lift it to global state by default |
| Shared editable workflow | Nearest common feature owner | Use context as a hidden mutable store |
| Cross-cutting stable dependency | Context/provider | Put frequently changing feature data in broad context |
| Complex overlay/control | Existing accessible primitive | Rebuild a dialog/menu keyboard model from scratch |

Keep component APIs honest. Prefer a small number of meaningful props over a giant configurable component. Do not create a generic component until there are at least two compatible consumers or a clear system-level requirement.

## State Machine Thinking

Represent asynchronous and editable flows as explicit states. A mutation is not simply `isLoading`; it can be idle, editing, validating, submitting, succeeded, failed, and retrying. Identify what the UI can show and what each event is allowed to do.

```ts
type SaveState =
  | { status: "idle" }
  | { status: "editing" }
  | { status: "submitting" }
  | { status: "error"; message: string }
  | { status: "success"; savedAt: string };
```

Derive display values during render. Do not synchronize props to state with an effect unless the feature intentionally keeps an editable draft or interoperates with an external imperative system. For a multi-event workflow, prefer `useReducer` with named events over many booleans that can conflict.

## Data, Mutations, and URL Behavior

- Validate data at the API/server boundary; a component should receive a trusted feature model, not raw untyped JSON.
- Co-locate loading and error UI with the feature or route that can recover from it. Do not make an entire application blank because a small panel fails.
- Define a mutation’s pending UI, double-submit prevention, success feedback, cache invalidation/revalidation, optimistic update, rollback, and retry behavior before coding it.
- Put sort, filters, pagination, tabs, and selection in the URL when they should survive reload, browser navigation, or sharing. Parse and constrain URL values.
- Never rely on a client-only authorization check to protect sensitive data or server operations.
- Avoid waterfalls: load independent data in parallel at the route/feature boundary. Measure before adding prefetching or complex caching.

## Accessible Interaction Contract

For each component, verify these rules instead of assuming visual correctness is enough:

- Use a semantic element that provides the behavior before adding ARIA. A `button` is not a styled `div`.
- Use one clear page `h1`, ordered heading levels, landmarks, associated labels, and specific action labels.
- Support keyboard navigation, visible focus, escape/close behavior, and focus return for overlays.
- Place validation errors with their controls, preserve entered data on recoverable errors, and explain the next action.
- Announce dynamic status only when it needs attention; avoid noisy live regions.
- Make hover-only information available with keyboard/touch, honor reduced motion, and do not communicate meaning with color alone.

## Rendering and Performance Rules

- Treat server/client output mismatches as bugs. Do not render random values, current time, browser globals, or locale-specific output on the server without a deterministic strategy.
- Keep server-only modules, credentials, and privileged logic out of client bundles.
- Profile before using `memo`, `useMemo`, or `useCallback`; stale dependencies and unreadable code are costs.
- Use stable keys from domain identity. Index keys are unsafe for mutable lists.
- Clean up listeners, timers, observers, subscriptions, and imperative widgets in effects.
- Virtualize only lists proven large enough to need it, and preserve accessibility/keyboard behavior when doing so.

## Test Matrix

| Scenario | Verification |
|---|---|
| First load | Correct loading state, then content or empty state |
| Permission failure | Safe message without private data or misleading controls |
| Form validation | Keyboard-accessible error, preserved input, actionable correction |
| Mutation failure | Pending state ends, error explains recovery, optimistic state rolls back |
| Navigation | URL state restores the same view and focus lands sensibly |
| Responsive use | No clipped content, hidden action, horizontal trap, or unusable target |

Test observable user behavior rather than hook calls or private component structure. Use the project’s browser/integration tests for route and interaction behavior when risk cannot be covered by a component test.

## Forms and Mutation Workflow

For a form or mutation, design the whole lifecycle before styling it:

1. Load default values and explain unavailable/unauthorized state.
2. Validate affordances locally for fast feedback, but enforce the same rules on the server.
3. Keep draft state stable while the user edits; do not overwrite it because a background refetch completes.
4. Disable or otherwise protect the submit action while the same mutation is pending.
5. Show field-level errors next to controls and a form-level error for failures not tied to one field.
6. On success, confirm the outcome, update/invalidate the right data, and move focus only when it helps the user orient.
7. On failure, retain recoverable input and give a meaningful retry/correction path.

Do not use a toast as the only confirmation or error channel for a form. It disappears, is easy to miss, and does not identify the field/action that needs attention.

## Responsive and Visual Implementation Rules

Follow `frontend-design` for visual direction; use this skill to make that direction behave correctly in React.

- Start from content hierarchy and touch interaction, not a desktop screenshot. Decide what reflows, collapses, becomes scrollable, or moves to a menu at narrow widths.
- Preserve the primary action and essential information at every supported width. Do not hide a critical feature merely because it does not fit.
- Use the existing token system for spacing, typography, color, elevation, and breakpoints. Do not scatter pixel overrides that make later changes brittle.
- Test text expansion, long localized labels, empty values, large font settings, zoom/reflow, and narrow widths—not only the ideal English fixture.
- Respect user color scheme and motion preferences if the application supports them. Never introduce an inaccessible contrast regression to match a mockup.

## Framework Boundary Checklist

Choose the framework-specific guidance that applies, then inspect the local implementation rather than relying on generic React memory:

| Situation | Required decision |
|---|---|
| Server components/SSR | Which data and secrets stay server-only? What client boundary is truly interactive? |
| Streaming/Suspense | What fallback is useful, how are errors isolated, and does fallback preserve page usability? |
| Static generation | Which params/data invalidate output and what happens when they are absent? |
| Client-side routing | Which data is route-owned, which state belongs in the URL, and where does focus move after navigation? |
| Third-party widget | How is it loaded, cleaned up, made accessible, and prevented from leaking data or blocking render? |

Never copy a framework pattern into a repository without confirming its version, router, server/client conventions, cache defaults, and deployment runtime.

## Error Boundaries and Recovery

Place errors at the smallest useful recovery scope. A failing chart should not blank the entire dashboard; a failed route loader may need a route-level recovery screen. For each boundary, decide:

- what is safe to show to the user;
- whether retry is meaningful and how it works;
- whether the failure should be reported to telemetry;
- which local state is preserved or reset;
- whether the user can navigate away safely.

Do not catch rendering errors and render nothing. Provide a clear fallback and preserve the original error for diagnostics through the project’s error reporting path.

## React Code Review Questions

### State and rendering

- Is the component deterministic for identical props/state, including server rendering?
- Is every effect genuinely synchronizing with something external and cleaned up correctly?
- Can two booleans become a contradictory state? Would a reducer/union make transitions explicit?
- Are updates safe when a request resolves after the user navigates, changes filters, or starts a newer request?

### Interaction and accessibility

- Can a keyboard user discover, operate, cancel, and recover from the feature?
- Does focus move predictably through a dialog, validation error, navigation, or async update?
- Does every icon-only or visually implied action have an accessible name and clear result?
- Is dynamic content announced only when it materially changes the task?

### Data and operations

- Are stale data, duplicate submission, permission change, offline/timeout, and server error behavior considered?
- Is sensitive data absent from client bundles, initial HTML, logs, analytics, and browser storage?
- Are list/query sizes, render cost, images, code splits, and client bundle additions bounded and measured where relevant?

## Anti-Patterns to Reject

- `useEffect` that copies props into state or orchestrates a normal user event.
- A global context/provider that rerenders an entire application for local feature state.
- A custom `div` control where a native element provides correct behavior.
- A fetch that does not handle abort, stale result, loading, empty, error, or permission states.
- An optimistic update without a rollback/revalidation path.
- Hiding a critical action on mobile without an equivalent discoverable route.
- `memo`/callback wrappers added everywhere without a measured problem.
- A test suite that only snapshots markup and never performs the user interaction.

## Required Output

```markdown
## React Delivery Summary

### User Flow
- Goal, route, and permissions:
- States handled:
- Primary and recovery actions:

### Architecture
- Component boundaries:
- State/data/URL ownership:
- Server/client and caching decisions:

### Quality
- Accessibility behavior:
- Responsive and browser checks:
- Tests and commands run:

### Follow-up
- Performance, analytics, rollout, or unresolved trade-offs:
```

## Component and State Design

- Split components when they have independent responsibilities, data ownership, or reuse value. Do not create abstractions before a second real use case.
- Keep server state in the project query/data layer and local transient UI state in component state. Do not mirror remote data in `useState` without a deliberate editing or optimistic-update reason.
- Derive values during render where possible. Use effects to synchronize with external systems, subscriptions, DOM APIs, or imperative integrations—not to calculate state from props.
- Use `useReducer` or a state machine for multi-step, mutually exclusive, or transition-heavy workflows. Model impossible states out of the UI.
- Use stable identity-based list keys, never array indexes for lists that can reorder, insert, filter, or preserve item state.
- Keep state local until it has a genuine shared owner. Use context for stable cross-cutting dependencies, not high-frequency feature state.

## Data Fetching and Rendering

- Follow the framework’s server/client component and data-loading conventions. Do not move sensitive or server-only logic into client bundles.
- Treat loading, empty, error, stale, unauthorized, and success states as first-class UI. Give users a recovery path when an action can be retried or corrected.
- Make mutations idempotent where feasible, prevent double submission, show pending state, and reconcile or roll back optimistic updates on failure.
- Put shareable, filterable, or paginated state in the URL when it benefits navigation, reload, or sharing. Validate URL values at the boundary.
- Avoid request waterfalls by fetching at the correct route/feature boundary and parallelizing independent work. Measure before adding memoization or cache complexity.
- Treat hydration warnings as correctness bugs. Keep server/client output deterministic; do not render time, randomness, browser-only APIs, or locale-sensitive values server-side without a safe strategy.

## Accessibility and Performance

- Use semantic landmarks, ordered headings, associated labels, descriptive button text, and native elements before ARIA.
- Ensure keyboard operation and visible focus. Manage focus after dialogs, route changes, validation failures, and destructive actions.
- Use proven accessible primitives for dialogs, menus, and comboboxes. Do not recreate complex keyboard semantics from scratch.
- Do not use color, hover, or animation as the sole signal. Respect reduced-motion preferences and maintain usable touch targets.
- Profile before optimizing. Use memoization only for measured render cost or required referential stability; incorrect dependencies create stale UI.
- Clean up subscriptions, timers, observers, and imperative integrations. Virtualize genuinely large collections and code-split heavy independent features.

## Testing and Common Failure Modes

- Test user-visible behavior: rendering, keyboard interaction, loading/error paths, route transitions, and mutation feedback. Mock network boundaries rather than internal hooks.
- Common failures: derived state stored in effects, array-index keys, missing cleanup, optimistic updates without rollback, lost focus, inaccessible custom controls, and server/client output mismatch.

## Delivery Format

Provide the user flow and states implemented; component/data ownership decisions; accessibility behavior; tests and viewports checked; hydration/performance considerations; and follow-up work.

## Definition of Done

- [ ] User goal, route/rendering boundary, permissions, data contract, state owners, and verification plan are explicit.
- [ ] Repository React/framework, router, design-system, styling, data-layer, and test conventions were inspected and followed.
- [ ] Components have focused responsibilities and no speculative abstraction or hidden global state was introduced.
- [ ] Loading, empty, error, unauthorized, pending, success, retry, and rollback states are handled where relevant.
- [ ] State is owned deliberately; derived values are not stored unnecessarily and effects only synchronize with external systems.
- [ ] Server/client boundaries protect sensitive code, avoid hydration mismatches, and use the intended data-loading model.
- [ ] Semantic structure, keyboard behavior, focus management, labels, error recovery, non-color cues, and reduced motion are verified.
- [ ] Lists use stable keys, effects clean up resources, and rendering/performance work is evidence-based.
- [ ] Responsive layouts and key interaction states were visually inspected at representative viewports.
- [ ] Relevant unit, integration, and/or end-to-end tests passed, with commands and unrun checks reported.
