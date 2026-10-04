---
name: lwc-focus-management
description: "Focus trap, restore, and programmatic focus in modals, wizards, and dynamic lists. Triggers: focus trap LWC, focus restore, tabindex modal. NOT for general LWC accessibility review — use lwc/lwc-accessibility."
category: lwc
salesforce-version: "Spring '25+"
well-architected-pillars:
  - User Experience
  - Security
triggers:
  - "lwc focus management"
  - "focus trap modal lwc"
  - "restore focus after close lwc"
  - "programmatic focus shadow dom"
  - "lwc focus after async callout"
tags:
  - lwc
  - focus
  - accessibility
  - shadow-dom
  - keyboard
inputs:
  - Component or subtree that manipulates focus
  - Expected keyboard flows
  - Accessibility requirement (WCAG 2.1 AA or stricter)
outputs:
  - Focus map per component state
  - Focus trap and restoration plan
  - Testing approach (keyboard + screen reader)
dependencies: []
version: 1.0.1
author: Pranav Nagrecha
updated: 2026-08-14
---

# LWC Focus Management

Focus management in LWC is not "the same as focus management on the web, plus a
framework". The shadow boundary changes what the DOM tells you, and almost every
focus bug in an LWC bundle traces back to one of two facts:

| Fact | What breaks | Correct instrument |
|---|---|---|
| `document.activeElement` retargets to the **host** element, not the focused control inside it | `document.activeElement === firstElement` is always `false`, so hand-rolled focus traps never engage | `this.template.activeElement` — the `ShadowRoot`'s own view |
| `this.template.querySelectorAll('input, button, …')` only sees **this** template | A trap over a form of `lightning-input`s finds zero focusable elements | Query the custom elements and let them focus themselves |

Both produce code that looks right, passes review, and does nothing. Neither
throws. That is the whole problem: a broken focus trap is indistinguishable from
a working one unless you test it with a keyboard.

**Scope.** This skill owns *where focus goes and when*: restoration across state
changes, traps, programmatic focus across the shadow boundary, and the timing
rules that decide whether `.focus()` lands on anything. Broad accessibility
review — labels, contrast, roles, alt text, the full WCAG sweep — is
`lwc/lwc-accessibility`. Modal structure and overlay behaviour is
`lwc/lwc-lightning-modal` and `lwc/lwc-modal-and-overlay`; this skill covers the
focus contract those components have to honour.

---

## Before Starting

1. **Ask whether you should be writing a trap at all.** `lightning/modal` ships
   one. The Lightning Component Reference documents where it places initial
   focus, in priority order, and it is maintained by people who test against
   screen readers you do not have. Hand-rolling is defensible only when the
   surface genuinely is not a modal.

2. **Enumerate the state transitions, not the components.** Open, close, submit,
   validation-failed, async-loaded, row-added, row-removed, step-forward,
   step-back, error, cancel. Each is a focus decision. A component with nine
   transitions and one `renderedCallback` focus call has eight unhandled cases.

3. **For each transition, write down three things**, not one: where focus goes,
   where it returns to when the state ends, and what assistive technology is told.
   A focus target without a return target is how users end up on `<body>`.

4. **Decide who owns restoration.** The element that opened the overlay is the
   only thing that reliably knows where focus came from — and it lives in a
   different shadow root from the overlay. Restoration is the *opener's* job.
   Designing it as the overlay's job is the root cause of "focus goes to the top
   of the page when I close the dialog".

---

## Core Concepts

### `document.activeElement` lies to you across the shadow boundary

This is standard shadow DOM retargeting, not an LWC quirk, and it is the single
highest-frequency defect in this area. When focus is on an `<input>` inside a
component's shadow tree, `document.activeElement` is the *host* custom element.

```javascript
// WRONG — inside c-my-modal, with focus on an inner button.
// document.activeElement is <c-my-modal>, so this is never true.
if (document.activeElement === first) { … }

// RIGHT — the ShadowRoot's own activeElement is scoped to this shadow tree.
if (this.template.activeElement === first) { … }
```

Saving `document.activeElement` as "the opener" has the same defect: you save the
host component, and calling `.focus()` on a custom element that has neither
`tabindex` nor `delegatesFocus` does nothing at all. See Pattern B.

### `this.template.querySelector` is scoped, and base components are opaque

`this.template.querySelector()` reaches into this component's shadow tree and
stops. A `<lightning-input>` in your template is one element to you; the actual
`<input>` lives in *its* shadow tree and your selector will never match it.

```javascript
// Finds nothing useful in a form made of base components.
this.template.querySelectorAll('button, input, select, textarea');

// Finds the base components themselves — which is what you want, because
// each one knows how to focus its own internals.
this.template.querySelectorAll('lightning-input, lightning-button, lightning-combobox');
```

Every relevant base component exposes `focus()` — `lightning-input`'s is
documented as "Sets focus on the input element." Delegate; do not reach in.

### `this.refs` is the modern way to name a target

`lwc:ref` marks an element in the template and `this.refs.<name>` retrieves it
without a selector. Two restrictions matter here, because focus targets are
frequently exactly the things they exclude:

- "If you place `lwc:ref` in a `for:each` or `iterator:*` loop, the template
  compiler throws an error." Focusing a row in a dynamic list therefore still
  needs `querySelector` with a `data-*` attribute.
- "If you call `this.refs` for a nonexistent ref, it returns `undefined`" — so
  `this.refs.firstField?.focus()` is the safe shape, and it is silently a no-op
  before first render.

### `delegatesFocus` is the documented way to make a component focusable

```javascript
export default class CoolButton extends LightningElement {
    static delegatesFocus = true;
}
```

With this set, calling `.focus()` on the host delegates to the first focusable
element inside, clicking a non-focusable area of the shadow tree delegates focus
inward, and `:focus` applies to the host as well as the focused element. The
documentation is explicit about one interaction: **"Don't use `tabindex` with
`delegatesFocus` because it throws off the focus order."** Pick one.

The alternative — an `@api focus()` method that calls
`this.template.querySelector(...).focus()` — also works and is common. Prefer
`delegatesFocus` for leaf components that wrap a single control, and an explicit
`@api focus()` when the component must choose between several internal targets
based on state.

### `tabindex` in LWC has exactly two legal values

Only `0` and `-1`. `0` puts the element in sequential keyboard navigation; `-1`
takes it out while leaving it programmatically focusable. Positive values are
rejected by the template compiler, which is the framework enforcing an
accessibility rule the rest of the web only recommends.

By default focus skips a component's container and moves to the elements inside
it. To make the component itself a tab stop, add `tabindex="0"` **to the
component tag in the parent template** — not inside the component.

### Timing: `renderedCallback`, guarded

`.focus()` on an element that has not rendered is a no-op with no error.
`connectedCallback` is too early — "You can't access child elements from the
callbacks because they don't exist yet." `renderedCallback` "flows from child to
parent" and fires after every render, and "A component is usually rendered many
times during the lifespan of an application."

The documented pattern for a one-time action is a boolean field:

> "To use this hook to perform a one-time operation, use a boolean field like
> `hasRendered` to track whether `renderedCallback()` has been executed."

Unguarded focus in `renderedCallback` re-focuses on every render, which eats
keystrokes as the user types. The same page carries the harder warning:
**"Updating the state of your component in `renderedCallback()` can cause an
infinite loop."** A focus flag is not reactive state, which is exactly why the
flag pattern is safe and setting a `@track` property there is not.

---

## Common Patterns

### Pattern A — let `lightning/modal` do it

`LightningModal` places initial focus by a documented rule: the step subtitle if
the modal has multiple steps, otherwise the header title, otherwise the first
interactive element in the body, otherwise the close button. Reproducing that
correctly by hand is more work than it looks and worse than it looks when you get
it wrong. Full example in [`references/examples.md`](references/examples.md),
Example 1.

### Pattern B — restoration belongs to the opener

The opener knows what was clicked; the overlay cannot. The overlay fires `close`,
the opener re-focuses its own trigger from its own shadow root.

```javascript
// Opener component
handleOpen()  { this.showDialog = true; }
handleClose() {
    this.showDialog = false;
    // Wait for the dialog to leave the DOM before focusing the trigger.
    Promise.resolve().then(() => this.refs.openButton.focus());
}
```

This is the correction to the common `this._opener = document.activeElement`
idiom, which stores a host element and restores focus to nothing.

### Pattern C — trap with `this.template.activeElement`, over custom elements

A trap needs the *first* and *last* focusable things in tab order, and in a base
component form those are `lightning-*` elements. See Example 2 for the full
implementation, including why `Tab` and `Shift+Tab` need different guards and why
the trap must be removed on close.

### Pattern D — validation errors: summary first, field on request

On a failed submit, move focus to a `role="alert"` summary with `tabindex="-1"`,
listing each error as a link that focuses its field. This announces the error
count once instead of announcing whichever field happened to be focused, and it
gives keyboard users a direct route to each problem. Example 3.

### Pattern E — async completion: announce, do not yank

When a wire or imperative call resolves, focus is wherever the user put it. Moving
it is hostile if they have started typing. Announce into a live region instead,
and move focus only when the resolution replaced the thing that had focus.

### Pattern F — row removal: next, then previous, then the heading

Deleting the focused row destroys the focused element, and focus falls to
`<body>`. Compute the successor *before* the mutation, and focus it after the
re-render. Example 4.

---

## Decision Guidance

| Situation | Approach |
|---|---|
| Dialog / overlay | `lightning/modal` — it has a maintained focus contract |
| Restoring focus after an overlay closes | The opener restores its own trigger via `this.refs` |
| Comparing "is this element focused" | `this.template.activeElement`, never `document.activeElement` |
| Focusing a child LWC | `static delegatesFocus = true` on the child, or an explicit `@api focus()` |
| Focusing a base component | Call its documented `focus()`; never query its internals |
| Focus target inside `for:each` | `data-*` attribute + `this.template.querySelector`; `lwc:ref` is a compile error in a loop |
| Focus target that is stable and unique | `lwc:ref` + `this.refs.name?.focus()` |
| Making a whole component a tab stop | `tabindex="0"` on the tag **in the parent template** |
| Component wraps exactly one control | `delegatesFocus`, and remove any `tabindex` |
| Async load finished | Live-region announcement; move focus only if the focused element was replaced |
| Validation failed | `role="alert"` summary, `tabindex="-1"`, focused once per submit |
| Row deleted | Next sibling → previous sibling → list heading, computed before the mutation |
| "It works but re-focuses constantly" | Add the `hasRendered`-style guard in `renderedCallback` |

---

## Recommended Workflow

1. **Build the focus map before writing code.** One row per state transition, with
   focus target, restoration target, and announcement. Use
   [`templates/focus-map.md`](templates/focus-map.md). Rows you cannot fill in are
   the bugs you would otherwise ship.
2. **Choose the framework's implementation where one exists** — `lightning/modal`
   for dialogs — and only hand-roll when the surface is genuinely not a modal.
   Record the decision, because "we wrote our own trap" is the kind of thing a
   later reviewer needs a reason for.
3. **Place every programmatic `.focus()` in `renderedCallback` behind a boolean
   flag**, or in a `Promise.resolve().then(...)` after the state change that
   causes the render. Never in `connectedCallback` — the children do not exist yet.
4. **Cross the shadow boundary with the supported instruments only**:
   `this.refs` / `this.template.querySelector` inside, `delegatesFocus` or an
   `@api focus()` outward, `this.template.activeElement` for comparisons. Treat
   any `document.querySelector` or `document.activeElement` in a component as a
   defect.
5. **Give assistive technology its own channel.** `role="status"`
   (`aria-live="polite"`) for progress and completion, `role="alert"`
   (`aria-live="assertive"`) for validation failures, and blank-then-set so an
   identical repeated message still announces.
6. **Test with the keyboard only, then with a screen reader.** Tab forward and
   backward through every transition in the focus map, confirm no state strands
   focus on `<body>`, and confirm every trap can be escaped — WCAG 2.1.2 No
   Keyboard Trap is failed by a trap with no exit, and a modal with a broken
   `Escape` handler is exactly that.
7. **Pin the behaviour in Jest.** Assert focus moved to the element you intended,
   not merely that some `focus` spy was called. See Example 5 and
   [`templates/lwc/jest.config.js`](../../../templates/lwc/jest.config.js).

---

## Review Checklist

- [ ] No `document.activeElement` and no `document.querySelector` in the bundle
- [ ] Comparisons against the focused element use `this.template.activeElement`
- [ ] Focus traps enumerate custom elements (`lightning-*`, `c-*`), not raw `input`/`button`
- [ ] Restoration is performed by the opener, on its own trigger element
- [ ] Every programmatic focus is guarded against re-firing on re-render
- [ ] No `.focus()` in `connectedCallback`
- [ ] No reactive-state mutation in `renderedCallback`
- [ ] `tabindex` values are only `0` or `-1`
- [ ] No `tabindex` on any component that sets `delegatesFocus`
- [ ] Every focusable custom child exposes `delegatesFocus` or `@api focus()`
- [ ] `lwc:ref` is not used inside `for:each` / `iterator:*`
- [ ] `Escape` closes every trapping surface, and the trap is removed on close
- [ ] Live regions are blanked before being re-set, so repeated text still announces
- [ ] Deletion of the focused item has a defined successor
- [ ] Jest asserts the *identity* of the focused element per transition
- [ ] Keyboard-only walk covers every row of the focus map, forwards and backwards

---

## Salesforce-Specific Gotchas

Full detail in [`references/gotchas.md`](references/gotchas.md).

1. **`document.activeElement` retargets to the host** — trap comparisons silently never match.
2. **`querySelectorAll('input')` finds nothing** in a form of base components.
3. **`.focus()` before render is a silent no-op**, with no error and no warning.
4. **Unguarded `renderedCallback` focus eats keystrokes.**
5. **`lwc:ref` inside `for:each` is a compile error**, and lists are where dynamic focus lives.
6. **`tabindex` accepts only `0` and `-1`.**
7. **`tabindex` plus `delegatesFocus` "throws off the focus order"** — the docs say so explicitly.
8. **A custom element with no `tabindex` and no `delegatesFocus` ignores `.focus()`.**
9. **`role="alert"` announces on insertion, not on text change** — identical repeats go unheard.
10. **A trap with no `Escape` route fails WCAG 2.1.2** and is worse than no trap.
11. **Deleting the focused row drops focus to `<body>`** unless a successor was computed first.
12. **Jest's jsdom is not a browser** — it will not tell you a real focus order is wrong.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Focus map | One row per state transition: trigger, focus target, restoration target, announcement, and the code location that implements it |
| Trap decision record | `lightning/modal` or hand-rolled, with the reason and — if hand-rolled — how `Escape` and teardown are handled |
| Component focus contract | For each child component: `delegatesFocus`, `@api focus()`, or "not focusable", stated in its JSDoc |
| Live-region plan | Which regions exist, `polite` vs `assertive`, and where the blank-then-set reset happens |
| Jest focus suite | One test per focus-map row asserting the identity of the focused element |
| Manual test record | Keyboard-only walk, forwards and backwards, plus the screen reader and browser combination used |

---

## Related Skills

- `lwc/lwc-accessibility` — the full accessibility review this skill is one slice
  of: labels, roles, contrast, and the rest of WCAG
- `lwc/lwc-lightning-modal` — `lightning/modal` itself, whose documented focus
  behaviour makes most hand-rolled traps unnecessary
- `lwc/lwc-modal-and-overlay` — overlay composition and stacking, which decides
  which surface owns the trap
- `lwc/lwc-accessibility-patterns` — ARIA patterns (listbox, grid, tablist) whose
  keyboard contracts constrain what your focus handlers may bind
- `lwc/lwc-jest-testing-with-accessibility` — the testing layer, including what
  jsdom can and cannot tell you about focus
- `templates/lwc/component-skeleton/` — the canonical component shell these
  patterns drop into
