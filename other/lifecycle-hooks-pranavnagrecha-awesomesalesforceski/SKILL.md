---
name: lifecycle-hooks
description: "Use when building or reviewing Lightning Web Components — specifically lifecycle. Triggers: 'LWC', 'connectedCallback', 'renderedCallback', 'memory leak', 'NavigationMixin', 'wire'. Triggers: 'LWC', 'connectedCallback', 'renderedCallback', 'memory leak', 'NavigationMixin', 'wire'. Also: 'disconnectedCallback', 'errorCallback', 'render()', 'multiple templates', 'hook order', 'parent child lifecycle', 'infinite rerender', 'component subscribes twice'. NOT for Aura components — use lwc/navigation-and-routing."
category: lwc
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Reliability
  - Security
  - Performance
  - User Experience
tags: ["lwc", "connectedcallback", "renderedcallback", "navigationmixin", "memory-leaks", "errorcallback", "disconnectedcallback", "hook-order"]
triggers:
  - "LWC component not loading data on first render"
  - "component behaves differently after navigating away and back"
  - "renderedCallback running too many times"
  - "wire adapter not refreshing after data change"
  - "event listener not being cleaned up causing memory leak"
  - "LWC component crashes on navigation in Experience Cloud"
  - "order lifecycle hooks fire between parent and child LWC"
  - "stop connectedCallback from subscribing twice"
  - "clean up setInterval when an LWC is removed from the page"
  - "catch an error thrown by a child LWC with errorCallback"
  - "switch templates with the render method in an LWC"
  - "write a Jest test that asserts disconnectedCallback ran"
inputs: ["component context", "data access pattern", "runtime environment", "which hooks the component currently implements"]
outputs: ["lifecycle review findings", "component design guidance", "navigation and cleanup recommendations", "deployable component bundle with hook-order Jest tests"]
dependencies: []
version: 1.1.0
author: Pranav Nagrecha
updated: 2026-09-05
---

You are a Salesforce expert in Lightning Web Component lifecycle design. Your goal is to build LWCs that are memory-safe, performant, accessible, and aligned with Salesforce runtime constraints.

## Before Starting

Check for `salesforce-context.md` in the project root. If present, read it first — particularly whether Experience Cloud is involved, whether the org uses standard Salesforce LWC, and whether third-party libraries are approved.

Gather if not available:
- Is this a new component or review of an existing one?
- Does it use Apex, wire adapters, or Lightning Data Service?
- Does it run in Lightning Experience, mobile, Experience Cloud, or multiple contexts?
- Does it add event listeners, timers, navigation, or external scripts?

## Questions to Ask Before Configuring

Ask these before writing a hook. Each one maps to a failure in `references/gotchas.md` that only appears after the component has shipped.

| Ask | Why it matters | What a good answer adds |
|---|---|---|
| "Can this component be removed and re-inserted without a page reload — behind an `lwc:if`, in a reorderable list, in a console tab?" | `connectedCallback()` fires again on every re-insertion; unguarded setup accumulates | The guard shape: `if (!this.subscription)`, and a matching teardown |
| "What does this component set up that lives outside its own template — a `window`/`document` listener, a timer, a message-channel subscription, a refresh handler?" | The framework cleans up only the listeners it owns from the template; everything else is yours | The exact `disconnectedCallback()` body, one line per setup line |
| "Does anything here need the rendered DOM — measuring, focusing, handing a container to a library?" | DOM work is only valid in `renderedCallback()`, which runs after *every* render | A boolean guard and the one-time block behind it |
| "Which fields does `renderedCallback()` write to?" | Every field is reactive; writing one there marks the component dirty and re-enters the hook | Either "none" or a guard that makes the write happen once |
| "Where should a failure in this subtree stop — at this component, its container, or the app shell?" | `errorCallback()` catches descendants only, and the throwing child is unmounted | The boundary's position and what its fallback template shows |
| "Are the two views different enough to need two HTML files, or is this an `lwc:if`?" | `render()` is a real fork with its own CSS-naming and `this.refs` consequences | A decision, plus the second template's filename if you take the fork |
| "How will we know the cleanup works — what test removes the element and asserts?" | Leaks are invisible in a demo and expensive in a console session | A Jest test that calls `removeChild` and asserts the teardown ran |

What a proper lifecycle design adds over just writing the hooks: the component survives being re-inserted, leaves nothing behind when it is removed, renders a finite number of times, and fails inside a boundary instead of blanking the page.

## How This Skill Works

### Mode 1: Build from Scratch

1. Define the public API and the data contract first.
2. Choose the lightest data pattern that fits: LDS, wire adapter, then Apex if needed.
3. Plan what belongs in each lifecycle hook before writing code.
4. Design loading, data, and error states together.
5. Use Salesforce-native navigation, notifications, and static resource loading patterns.

### Mode 2: Review Existing

1. Check `connectedCallback` and `disconnectedCallback` for cleanup symmetry.
2. Verify `renderedCallback` is guarded and not mutating reactive state blindly.
3. Confirm `@api` props are treated as immutable inputs.
4. Check wire handlers for both success and error branches.
5. Flag `window.location`, global DOM access, `alert()`, or raw external script tags.

### Mode 3: Troubleshoot

1. If the component leaks or misbehaves after navigation, inspect listener and timer cleanup.
2. If it rerenders endlessly, inspect `renderedCallback` and any reactive mutation it triggers.
3. If data appears stale or blank, compare the chosen data pattern with the actual use case.
4. If the UI breaks only in mobile or Experience Cloud, inspect navigation and CSP assumptions.
5. Fix the lifecycle contract first, then the cosmetic issue.

## LWC Lifecycle Rules

### Documented order

The guide states the direction for each hook individually. Read the table as: for one
parent with one child, in this order.

| # | Step | Direction | Source |
|---|---|---|---|
| 1 | `constructor()` | parent → child | `create-lifecycle-hooks-created` L4085 |
| 2 | Public properties assigned | — | `create-lifecycle-hooks-created` L4085 |
| 3 | Wire property seeded with `{ data: undefined, error: undefined }` | — | `data-wire-service-about` L6468 |
| 4 | `connectedCallback()` | parent → child | `create-lifecycle-hooks-dom` L4101 |
| 5 | `render()` | — | `data-wire-service-about` L6469 |
| 6 | `renderedCallback()` | **child → parent** | `create-lifecycle-hooks-rendered` L4127 |
| — | `disconnectedCallback()` on removal | parent → child | `create-lifecycle-hooks-dom` L4101 |

The reversal at step 6 is the one people get wrong: a parent's `renderedCallback` runs
*after* its children have rendered, which is why parent-level measurement works there
and child-level querying in the parent's `connectedCallback` does not.

### Hook Reference

| Hook | Use For | Avoid | Guide constraint |
|------|---------|-------|---|
| `constructor()` | Cheap local state only | DOM access; reading `@api` values; async work; adding host attributes | `super()` must be the first statement, with no parameters (L4087) |
| `connectedCallback()` | Environment work: listeners, subscriptions, kicking off a fetch | Querying child elements — they do not exist yet (L4112) | Can fire more than once (L4111); is synchronous, never `async` (L4117) |
| `renderedCallback()` | One-time DOM work behind a guard | Writing reactive fields; updating a wire config object | Runs after every render (L4136); wire-config writes here loop (L6408) |
| `disconnectedCallback()` | Undo exactly what `connectedCallback()` did | Business logic that should have happened earlier | Also synchronous (L4117) |
| `errorCallback(error, stack)` | Boundary for descendant failures | Treating it as a general try/catch | Descendants only; misses programmatically attached handlers (L4158, L4167) |
| `render()` | Returning a different imported template | Using it as a lifecycle notification | Not a hook — a protected method that must return a template reference (L4153) |

### High-Value Patterns

- Store bound event handlers and remove them in `disconnectedCallback`. This applies to `window` / `document` targets; the framework already manages listeners declared in the template (`events-handling` L5102).
- Guard `renderedCallback` with a boolean when doing one-time initialization.
- Treat `@api` objects as immutable. Clone before editing — a nested write on a passed-in object throws `Invalid mutation` (`create-components-data-flow` L2021).
- Prefer `NavigationMixin` over URL mutation.
- Prefer `ShowToastEvent` or inline states over blocking browser dialogs.
- Use Static Resources with `loadScript` and `loadStyle`; do not inject external scripts directly.
- Keep full code examples in `references/code-examples.md` rather than repeating them in the main skill.

#
## Recommended Workflow

1. **Inventory the hooks.** List every hook the component implements and, for each, one sentence saying what it does. Anything that cannot be described in one sentence is doing another hook's job.
2. **Answer the Questions table above.** The re-insertion question and the "what lives outside the template" question decide most of the design.
3. **Place the work.** Local state → `constructor()`. Environment and subscriptions → `connectedCallback()`. DOM and library initialisation → guarded `renderedCallback()`. Teardown → `disconnectedCallback()`, one line per setup line. Descendant failures → an `errorCallback()` boundary one level up. Template fork → `render()` only if two HTML files are genuinely warranted.
4. **Build from `references/code-examples.md`.** Copy the `caseBoundary` + `caseWatchList` pair and the `.js-meta.xml`; reference `templates/lwc/component-skeleton/` for the surrounding shell and `templates/lwc/jest.config.js` for mock wiring.
5. **Run the checker.** `python3 skills/lwc/lifecycle-hooks/scripts/check_lwc_lifecycle.py --manifest-dir force-app/main/default/lwc` — zero ERRORs before review, `--strict` in CI.
6. **Prove it with tests.** Port the three assertions from `references/code-examples.md`: hook order across parent and child, cleanup after `document.body.removeChild`, and `errorCallback` receiving a child's throw.
7. **Verify in the org.** Toggle the component's region and confirm exactly one live subscription and one pass through the guarded `renderedCallback` block, per the verification steps in `references/code-examples.md`.

---

## Review Checklist

- [ ] Listener or timer setup has matching cleanup
- [ ] `renderedCallback` is idempotent
- [ ] Wire or Apex data path handles loading, success, and error
- [ ] DOM access stays within `this.template`
- [ ] Navigation and feedback use Salesforce-supported APIs
- [ ] Third-party libraries load through Static Resources
- [ ] `super()` is the first statement in any declared `constructor()`
- [ ] No lifecycle hook is declared `async`
- [ ] Every `connectedCallback` subscription is behind an existence guard
- [ ] An `errorCallback` boundary exists at the level where a failure should stop

## Salesforce-Specific Gotchas

| Gotcha | What to do |
|---|---|
| `window.location` breaks across Salesforce containers | Use `NavigationMixin` so Lightning Experience, mobile, and Experience Cloud stay consistent. |
| `alert()` is not acceptable UX in Lightning | Use `ShowToastEvent` or deliberate inline UI states. |
| Lightning Web Security isolates DOM boundaries | Reaching into child shadow DOM is brittle and often blocked. |
| `renderedCallback` runs after every render | Guard reactive-state changes inside it; otherwise you create a rerender loop. |
| `@api` values are input contracts, not mutable local state | Clone them before changes. |
| External script loading fails silently without handling | Always catch `loadScript` or `loadStyle` failures. |
| `connectedCallback` is not a one-time initializer | Guard every subscription; re-insertion calls it again. |
| A hook marked `async` runs its tail at an unpredictable point | Keep the hook synchronous and call an async method from it. |

## Proactive Triggers

Surface these WITHOUT being asked:

| Pattern | Severity | Why / Fix |
|---|---|---|
| Global event listeners with no cleanup | Critical | Memory leak and Experience Cloud bug magnet. |
| `renderedCallback` with no guard | High | Infinite rerender risk. |
| `window.location` or raw anchor hacks for navigation | High | Use `NavigationMixin`. |
| `document.querySelector()` or child shadow DOM access | High | Violates component isolation. |
| External `<script>` tags or remote JS assumptions | Critical | Use Static Resources. |
| Data path with no error state | Medium | Blank components are an operational failure. |
| `super()` not first in the constructor | Critical | Breaks the prototype chain before `this` is usable. |
| `subscribe()` in `connectedCallback` with no null check | High | Duplicate subscriptions on every re-insertion. |

## Output Artifacts

| When you ask for... | You get... |
|---------------------|------------|
| New component scaffold | Lifecycle-safe JS and HTML guidance with state handling |
| LWC review | Findings on leaks, navigation, DOM isolation, and async state design |
| Troubleshoot memory leak | Root cause plus cleanup fix |
| Deployable example | The `caseBoundary` + `caseWatchList` bundles, `.js-meta.xml`, `package.xml`, and Jest tests from `references/code-examples.md` |

## Reference Files

| File | Read it when |
|---|---|
| `references/code-examples.md` | You are writing the component: full bundle, `.js-meta.xml`, `package.xml`, deploy order, and the three hook-order / cleanup / boundary Jest tests |
| `references/gotchas.md` | A hook is firing at the wrong time, more often than expected, or not at all |
| `references/llm-anti-patterns.md` | Reviewing generated LWC code, or self-checking your own output |
| `references/examples.md` | You want the shorter single-component patterns: wire + listener + guard, `@api` cloning, static-resource loading |
| `references/well-architected.md` | Mapping the review to Well-Architected pillars, or checking which official source backs a claim |
| `scripts/check_lwc_lifecycle.py` | Auditing an existing `lwc/` folder: `--manifest-dir <dir>`, add `--strict` in CI |

## Related Skills

- **lwc/lwc-error-boundaries**: where to place `errorCallback` boundaries across an app; this skill covers only the hook's contract.
- **lwc/static-resources-in-lwc**: owns `loadScript` / `loadStyle` and the static-resource CSP requirement.
- **lwc/lwc-testing**: Jest fundamentals — config, mocks, matchers, coverage.
- **lwc/wire-service-patterns**: what `@wire` provisions and when, relative to the hooks.
- **lwc/component-communication**: parent/child props and events instead of cross-boundary DOM access.
- **lwc/lwc-conditional-rendering**: `lwc:if` / `lwc:elseif` / `lwc:else`, the alternative to a `render()` fork.
- **lwc/message-channel-patterns**: message channel design; this skill covers only its subscribe/unsubscribe placement.
- **lwc/lwc-performance**: render cost and re-render budgets once the hooks are correct.
- **apex/soql-security**: Apex called from LWC still needs sharing and CRUD/FLS enforcement.
- **admin/flow-for-admins**: Screen Flows may replace simpler custom UI requirements.
