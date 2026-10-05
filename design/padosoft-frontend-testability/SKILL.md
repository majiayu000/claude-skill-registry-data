---
name: padosoft-frontend-testability
description: >-
  Use this skill when writing or reviewing user-interface markup or components — a page, a form, a modal, a
  list, a widget, a screen — in a project that has end-to-end tests or will have them. Also when the user
  says a test broke after a purely visual refactor, that a test waits on a timer, that a selector depends on
  a generated class name, that a test cannot tell loading from empty, or asks how to make the interface
  testable. It gives the locator hierarchy the markup has to support, the eight contract rules, and the
  observable states every asynchronous action owes its test. Do not use it to write the tests themselves
  (padosoft-test-integrity), to design the interface, or to pick a testing framework.
license: MIT
compatibility: >-
  Web and native user interfaces. Examples use HTML roles and test identifiers; the same contract holds for
  a native component tree, where the accessible role and the test identifier are the equivalent anchors.
metadata:
  version: 0.1.0
  author: Padosoft
  summary: The markup owes the test a stable anchor and an observable state.
  profiles: laravel, node, react-native
  scope: project
  repository: https://github.com/padosoft/skills
  keywords: testability, e2e, playwright, selectors, accessibility, data-testid, aria, loading state
---

# Frontend testability contracts

A brittle end-to-end suite is usually not the tests' fault. The interface gave them nothing stable to hold
on to, so they held on to a class name and a delay.

**The rule: the markup owes the test a stable anchor and an observable state. Both are part of the
interface's contract, like an API response shape.**

---

## 1. The locator hierarchy the markup has to support

From most to least resilient. Whoever writes the interface decides how high the test can climb.

| # | Anchor | Survives |
|---|---|---|
| 1 | **the accessible role and name** | restyling, restructuring, copy changes in most cases |
| 2 | **the form label** | anything except renaming the label |
| 3 | the placeholder | last resort for a field with no label |
| 4 | visible text | only for **stable** text — page titles, fixed labels |
| 5 | **an explicit test identifier** | everything, because it exists for this |
| 6 | a style selector | nothing. Requires a written justification |

Markup that forces the test down to level 6 is a contract violation, and it is the interface that has to
change.

## 2. The eight rules

**A. Semantically stable markup.** Buttons, links, inputs, dialogs and checkboxes expose a role and an
accessible name that do not depend on a class or the shape of the tree.

```html
<!-- ❌ -->   <div class="btn-primary" onclick="addToCart()">🛒</div>
<!-- ✅ -->   <button type="button" aria-label="Add to cart">🛒</button>

<!-- ❌ -->   <div class="modal-wrapper-v2">…</div>
<!-- ✅ -->   <div role="dialog" aria-labelledby="checkout-title"><h2 id="checkout-title">Checkout</h2>
```

**B. Every input has a real label**, associated by identifier or via an accessible equivalent. Without one,
the field cannot be found by the anchor that is most stable for it.

**C. A test identifier is a public contract, not a dump.** Add one only where the semantic anchor is not
enough — an icon-only control, a repeated list item, a dynamic widget — and then treat it like a published
interface. One naming convention, `scope-element-variant`, and a separate attribute for the row key rather
than baking an identifier into the name.

**D. Never anchor to volatile copy.** Marketing text changes without warning, and a test that matches it
breaks on the next campaign. Give such elements a stable accessible name **and** a test identifier, so the
visible text is free to move.

**E. Never let a generated class name be the only way in.** Utility classes, hashed module classes and
component-library internals are rebuilt on every change. They may exist; they must not be the anchor.

**F. Loading, success and error are observable states**, not animations.

```html
<div role="status" aria-live="polite" data-testid="orders-loading">Loading…</div>
<div role="status" data-testid="save-success">Saved</div>
<div role="alert" data-testid="checkout-error">Payment refused</div>
<button type="submit" data-testid="checkout-submit" disabled>Processing…</button>
```

The submit control reflects the state too. A spinner with no role and no identifier tells a test nothing,
and "it looks done" is not a signal.

**G. Asynchronous work ends with a signal, not a duration.** A modern runner waits on the anchor by itself —
but only if the interface eventually exposes a finished state. When it does not, the test is forced to wait
a fixed time, which is both slow and flaky. Expose the end of the work; never make the test guess.

**H. The four states of a data view are all distinguishable.** Initial, loading, success and error each need
their own observable marker — and **empty is not the same as ready**, nor the same as failed. A test that
cannot tell them apart will pass on the broken one; see **`padosoft-test-integrity`** and, for the
back-office case, **`padosoft-admin-interface`**.

## 3. Native interfaces

Same contract, different names. The accessible role and label are the first anchor; the test identifier is
the explicit one. Two additions:

- **A test identifier on a list row must be stable across re-renders**, which means derived from the data,
  not from the index.
- **The state markers matter more**, because there is no document to inspect: if the screen does not expose
  that it is loading, the only alternative is a timer.

## 4. When the interface cannot change today

Write the exception down where the test is, with the reason and what would remove it. An undocumented style
selector is indistinguishable from an oversight, and the next refactor deletes it without knowing.

---

## Gotchas

- **The test that breaks on a restyle is evidence about the markup**, not about the test. Fix the anchor.
- **An accessible name is not the visible text.** Giving a promotional button a stable name lets the copy
  change freely — and it is the same work that makes the button usable with a screen reader.
- **A test identifier added everywhere stops meaning anything**, and becomes a second naming system nobody
  maintains. Few, deliberate, on business-critical nodes.
- **A generated identifier attribute changes between renders**, so it is the worst possible anchor while
  looking like a good one.
- **`aria-live` without a role is often not announced**, and is equally invisible to a test looking for the
  role.
- **Disabling the submit button during the request** is the single cheapest observable state, and it doubles
  as protection against a double submission.

## Checklist

- [ ] Interactive elements expose a role and an accessible name
- [ ] Every input has a real label or an accessible equivalent
- [ ] Test identifiers only where the semantic anchor is insufficient, with one naming convention
- [ ] No anchor on marketing copy; stable name plus identifier where the text may change
- [ ] No generated class name as the only way to reach an element
- [ ] Loading, success and error exposed with a role **and** an identifier; the submit control reflects state
- [ ] Every asynchronous action ends with an observable signal, never a duration
- [ ] Initial, loading, empty, success and error are all distinguishable
- [ ] List rows keyed by data, not by index
- [ ] Every style-selector exception documented with the reason and its exit condition

## Final report

```
Surface: <page / screen / component>
Anchors: role+name <n> · label <n> · testid <n> · style selector <n> (justified? <…>)
States exposed: initial <…> · loading <…> · empty <…> · success <…> · error <…>
Async signals: <what marks the end of each action>
Contract violations found: none | <element → what is missing>
Exceptions: <selector, reason, what would remove it>
```
