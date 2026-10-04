---
name: lwc-template-refs
description: "Use when an LWC needs a stable, typed handle to a specific DOM element it owns — focusing inputs, imperatively validating a known form field, invoking a `@api` method on a child component, or migrating fragile. NOT for querying elements inside `for:each` iterators — refs do not work there — and NOT — use lwc/lwc-focus-management."
category: lwc
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Reliability
  - Performance
  - Operational Excellence
triggers:
  - "this.template.querySelector is fragile and keeps breaking when the class name changes"
  - "lwc:ref not working inside for:each loop and refs is undefined for each row"
  - "how to focus an input from an lwc when a modal opens"
  - "refs undefined in connectedCallback on first render"
  - "migrating querySelector to lwc:ref across the component library"
  - "need a stable reference to a child component to call an @api method"
tags:
  - lwc-template-refs
  - lwc-ref
  - query-selector
  - dom-queries
  - focus-management
inputs:
  - "current DOM-query pattern the component is using (e.g. querySelector, querySelectorAll, getElementsByTagName)"
  - "list of elements that need a named reference and whether they sit inside iterators or conditional branches"
  - "lifecycle timing requirement — when the ref is accessed (connectedCallback, renderedCallback, user event)"
  - "whether the target is an owned element or inside a child custom component's shadow DOM"
outputs:
  - "refactored template and JS using `lwc:ref` with safe lifecycle access"
  - "migration plan for replacing brittle class-selector queries"
  - "checker output flagging refs inside `for:each`, refs used in `connectedCallback`, and duplicate ref names"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-23
---

# LWC Template Refs

Use this skill when a component needs a deterministic handle to one of its own DOM elements — the classic "focus this input, call this child's `@api` method, read this element's value" problem — and the existing code leans on `this.template.querySelector('.some-class')`. The `lwc:ref` directive was introduced specifically to replace that brittle pattern with a typed, name-based lookup.

---

## Before Starting

Gather this context first:

- Which element needs a reference, and is it a single owned element or part of a repeated list? Refs only work for single elements — lists belong on a different pattern.
- Where is the ref accessed in the lifecycle? If the code needs to touch the DOM in `connectedCallback`, `this.refs` will be undefined — first render has not happened yet.
- Is the target element wrapped in a `lwc:if` branch? If the branch is false, the ref is undefined, and any code that assumes it exists will throw.
- Is the target inside a child custom element's shadow DOM? `this.refs` stops at the shadow boundary and cannot reach into `<c-child>`'s internals — that is by design.

---

## Core Concepts

Template refs in LWC are a declarative replacement for class-based `querySelector` lookups. They are simple, but timing and scope rules catch people off guard.

### The `lwc:ref` Directive Declares A Named Handle

In the template, mark an element with `lwc:ref="<name>"` — for example `<lightning-input lwc:ref="emailInput">`. In the component's JavaScript, access it with `this.refs.emailInput`. The directive value must be a literal string, must be unique within a given template root, and resolves to the single element that rendered with that name. The directive can be placed on any element, including base components, standard HTML, and child custom components.

### Refs Are Only Available After The First Render

`this.refs` is populated by the rendering engine as part of the render pass. That means it is undefined in `constructor` and `connectedCallback`, and it is only reliably usable in `renderedCallback` and any handler that runs after at least one render — click handlers, input events, setters invoked after mount. Code that touches `this.refs` in `connectedCallback` will throw. The documented workaround is to do the work in `renderedCallback`, usually guarded by a boolean flag so it runs once.

### Refs Respect Shadow Boundaries And Conditional Rendering

`this.refs` only sees elements that belong to this component's own template. It does not traverse into a child custom element's shadow DOM — that is intentional encapsulation, and the correct way to interact with a child is through its `@api` properties, methods, and events. Refs also live and die with conditional rendering: if an element is wrapped in `lwc:if={showPanel}` and `showPanel` is false, `this.refs.<name>` is undefined until the branch becomes true and re-renders.

### Refs Do Not Work Inside Iterators

The LWC documentation is explicit: `lwc:ref` must not be used inside `for:each` or `iterator` templates. The name would collide for every iteration, so the platform does not support it. For per-row interactions use `data-*` attributes on the row element and resolve them with `event.target.closest('[data-id]')` inside a delegated listener, or use `this.template.querySelectorAll(...)` when you truly need the whole list.

### `this.refs` Is A Fresh Lookup, Not A Long-Lived Cache

Each access of `this.refs.<name>` is a fresh read against the current render. Do not stash `const input = this.refs.emailInput` in a class property across renders — re-read on use. Names are also scoped per template root, so the same name can reappear in a different template (for example an inner template returned from `render()`) without collision.

### Migrating From `this.template.querySelector`

For single known elements, the migration is mechanical: add `lwc:ref="x"` to the element, replace the selector call with `this.refs.x`, and move the access out of `connectedCallback` if needed. `this.template.querySelector` is still valid and still required for collections, complex CSS selectors, and iterator children — refs and selectors coexist cleanly.

---

## Common Patterns

### Focus-On-Open With A Render Guard

**When to use:** A modal, inline edit, or wizard step needs to focus a known input the first time it renders.

**How it works:** Declare `lwc:ref="firstInput"` on the input. In `renderedCallback`, check a `_focused` boolean; if false, call `this.refs.firstInput?.focus()` and flip the flag. Reset the flag when the modal closes so the next open focuses again.

**Why not the alternative:** Calling `this.template.querySelector('.input')` relies on an unstable class name and races with the first render if called from `connectedCallback`.

### Imperative Form Validation Via Named Refs

**When to use:** The form has a small, known set of required fields and needs to call `reportValidity()` on each on submit.

**How it works:** Name each `lightning-input` with a distinct `lwc:ref`. On submit, iterate over the named refs (`['email', 'phone', 'amount']`) and call `reportValidity()` on each through `this.refs[name]`. Aggregate the boolean results.

**Why not the alternative:** `querySelectorAll('lightning-input')` sweeps in inputs that may not be required and hides intent; a named-ref list documents the contract in the template.

### Imperative Handle To A Single Child Component

**When to use:** A parent needs to call an `@api` method on exactly one child instance — for example `this.refs.chart.refresh()`.

**How it works:** Put `lwc:ref="chart"` on `<c-chart>` and invoke `this.refs.chart.refresh()` after render. The ref resolves to the child's host element, which exposes the `@api` surface.

**Why not the alternative:** A class-based lookup duplicates intent in CSS and breaks silently when the class is renamed by a refactor.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Need to focus or invoke a method on one known element | `lwc:ref="name"` + `this.refs.name` | Declarative, typed, survives refactors |
| Need to query N items rendered inside `for:each` | `data-*` + `event.target.closest('[data-*]')` or `template.querySelectorAll` | Refs explicitly do not work inside iterators |
| Need to inspect a child custom component's internal DOM | Do not — add an `@api` method or event to the child | Shadow boundary is intentional encapsulation |
| Element is inside `lwc:if` that may be false | Null-check `this.refs.x?.focus()` and access after the branch renders | Ref is undefined when the branch is not in the DOM |
| Code runs in `connectedCallback` | Move DOM work to `renderedCallback` with a one-shot flag | `this.refs` is not populated until after first render |

---

## Recommended Workflow

1. Identify each DOM access point in the component and categorize as single-element, list, conditional, or cross-shadow.
2. For single-element accesses on owned elements, add `lwc:ref="<name>"` with a meaningful, unique name and replace the selector call with `this.refs.<name>`.
3. Move any ref access out of `constructor` and `connectedCallback` into `renderedCallback` (or a user-event handler) and guard one-shot work with a boolean flag.
4. For list accesses or iterator children, keep `querySelector`/`querySelectorAll` or switch to `data-*` + event delegation — do not put `lwc:ref` inside `for:each`.
5. Run `scripts/check_lwc_template_refs.py` to catch refs inside `for:each`, refs used in `connectedCallback`, and duplicate names; fix findings and re-run.

---

## Review Checklist

- [ ] No `lwc:ref` appears inside a `for:each` or `iterator` template.
- [ ] No component accesses `this.refs` inside `constructor` or `connectedCallback`.
- [ ] Every `lwc:ref` name is unique within its template root.
- [ ] Refs that sit inside a `lwc:if` branch are accessed with optional chaining or an explicit guard.
- [ ] Migrated components no longer carry both `lwc:ref` and the legacy class-based `querySelector` for the same element.
- [ ] Cross-component interactions go through `@api` and events, not through reaching into a child's shadow DOM.

---

## Salesforce-Specific Gotchas

1. **`this.refs` is undefined in `connectedCallback`** — the lifecycle docs are explicit: refs are only populated after the first render pass, so code that assumes they exist on mount throws.
2. **Refs inside `for:each` are unsupported** — the docs forbid it because the name would repeat per iteration; use `data-*` attributes instead.
3. **A false `lwc:if` branch means no ref** — conditional rendering removes the element from the DOM, and `this.refs.<name>` becomes undefined until the branch renders again.
4. **Refs stop at the child component's shadow root** — you cannot reach into `<c-child>` to grab one of its internal nodes; expose the behavior with `@api` instead.
5. **`this.template.querySelector` is still valid and sometimes required** — for lists, complex selectors, or dynamic children, the legacy API is still the right tool; refs do not replace it universally.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Refactored template/JS | Component pairs using `lwc:ref` with lifecycle-safe access |
| Migration notes | Summary of which selectors were replaced, which remain, and why |
| Checker report | Line-numbered findings for refs-in-iterators, refs-in-`connectedCallback`, and duplicate ref names |

---

## Related Skills

- `lwc/lwc-focus-management` — use when focus sequencing, accessibility, and keyboard navigation are the primary concerns, not just the ref mechanics.
- `lwc/lifecycle-hooks` — use when the underlying issue is lifecycle timing (`connectedCallback` vs `renderedCallback`) rather than DOM lookup style.
- `lwc/lwc-accessibility` — use when refs are being added specifically to drive ARIA state, screen-reader announcements, or focus traps.
