---
name: lwc-accessibility
description: "Use when designing or reviewing LWCs for keyboard access, semantic labeling, focus. Triggers: LWC accessibility, keyboard nav, aria-label, aria-labelledby, aria-describedby, label for id, focus order, delegatesFocus, tabindex, shadow DOM label association, live region, screen reader. NOT for specific ARIA/datatable implementation patterns — use lwc/lwc-accessibility-patterns. NOT for SLDS styling with no assistive-tech impact — use lwc/lwc-css-and-styling."
category: lwc
salesforce-version: "Spring '25+'"
well-architected-pillars:
  - User Experience
  - Security
tags:
  - lwc-accessibility
  - keyboard-navigation
  - aria
  - focus-management
  - screen-reader
  - shadow-dom
  - delegates-focus
  - label-association
triggers:
  - "keyboard navigation is broken in my lwc"
  - "screen reader cannot understand this component"
  - "how should i manage focus in an lwc modal"
  - "need aria labels or alternative text in lwc"
  - "custom lwc is not accessible"
  - "we're having issues with lwc accessibility"
  - "label is not read by the screen reader in my lwc"
  - "associate a label with an input across the lwc shadow boundary"
  - "aria-describedby is not working in my lightning web component"
  - "set focus on an lwc input from the parent component"
  - "delegatesfocus is not moving focus into my component"
  - "tabindex is being ignored in my lightning web component"
  - "write a jest test that asserts aria attributes and focus"
  - "make a custom lightning-datatable cell keyboard accessible"
  - "announce an lwc validation error to a screen reader"
  - "audit an lwc bundle for accessibility before release"
inputs:
  - "which base components, custom markup, and interactive states the component uses"
  - "whether the issue affects keyboard users, screen readers, or both"
  - "where focus should land on open, error, save, and close transitions"
outputs:
  - "accessibility review findings for semantics, labels, focus, and keyboard behavior"
  - "remediation plan for WCAG-aligned LWC interaction design"
  - "recommended component or markup changes to reduce accessibility risk"
  - "a deployable component bundle with in-template label/error association and a Jest suite that asserts it"
dependencies: []
version: 1.1.0
author: Pranav Nagrecha
updated: 2026-09-05
---

Use this skill when a Lightning Web Component looks correct visually but may fail for keyboard users or assistive technology. The highest-value move in LWC accessibility work is usually to remove custom interaction code and return to accessible base components, then handle the few remaining focus and labeling gaps deliberately.

---

## Before Starting

Gather this context before working on anything in this domain:

- Which parts of the UI are interactive: buttons, menus, tabs, dialogs, inline actions, or custom pickers?
- Is the component built mostly from `lightning-*` base components, SLDS blueprint markup, or custom HTML?
- Where should focus move after the user opens a modal, triggers validation errors, saves, or cancels?

---

## Questions to Ask Before Configuring

Ask these before writing markup. Each one maps to a failure in `references/gotchas.md` that renders
without an error and is invisible in a mouse-only demo.

| Ask | Why it matters | What a good answer adds |
|---|---|---|
| "Can `lightning-input` / `lightning-combobox` / `lightning-record-edit-form` express this control, and if not, exactly what stops it?" | Base components already associate the label, update ARIA on interaction, and meet WCAG 2.1 AA contrast; a custom control re-inherits all of that | A written justification for custom markup, or the decision not to build it |
| "Which component owns the label, the help text, and the error text?" | `for` / `aria-describedby` link only inside one template; across templates in native shadow DOM they cannot link at all | The component boundary drawn around the whole form element, not around each visual part |
| "Where must focus be after open, after a validation failure, after save, and after close?" | Focus skips the custom element container by default, so an unstated contract means focus goes nowhere | Four named focus targets that become four Jest assertions |
| "Does a parent need to call `focus()` on this component?" | That decides `delegatesFocus` vs an `@api` focus method — and `delegatesFocus` forbids `tabindex` inside the component | The focus mechanism chosen once, up front, instead of both being half-applied |
| "Which state changes must be announced without moving focus?" | Save confirmations, async result counts, and inline validation are silent to a screen reader unless a live region carries them | The list of announcements and which are polite (`role="status"`) vs assertive (`role="alert"`) |
| "Which icons carry meaning, and which are decorative?" | `alternative-text` on a decorative icon is noise; its absence on a meaningful one is a WCAG 1.1.1 failure | A per-icon decision instead of a blanket rule applied in either direction |
| "Will this run in Experience Cloud, Lightning Out, or a native-shadow context?" | Lightning Experience and Experience Builder use synthetic shadow today; outside them LWC renders in native shadow, where cross-template id linking is impossible | The environment list that decides whether a cross-component ARIA reference can ship at all |

What a proper accessibility design adds over "adding ARIA at the end": the label association survives
id transformation, focus has a named destination at every state change, the keyboard contract is
asserted by tests rather than by a manual pass, and the component does not silently degrade when the
org moves from synthetic to native shadow.

---

## Core Concepts

Accessibility in LWC is easiest when the component stays close to platform primitives. The farther a team moves toward clickable `div` elements, custom focus logic, and manual ARIA, the more likely it is to recreate a solved problem badly.

| Principle | Default | Anti-pattern | Why it matters |
|---|---|---|---|
| Base components first | Use `lightning-*` base components or SLDS blueprints | Custom menu/button/toggle in raw HTML | Base components ship tested keyboard, label, and AT support |
| Accessible name | Real button text, label on inputs, `alternative-text` on meaningful icons | ARIA-patching a clickable `span` or `div` | ARIA cannot repair structurally wrong markup |
| Focus contract | Land on first actionable element, trap inside modals, return to launcher on close | Letting focus stay wherever the browser last placed it after rerender/save | Lost focus = component is broken for keyboard users |
| Programmatic validation | Use base-component validation; programmatic error association on custom inputs | Error state shown only in color or layout text | Color-only errors fail screen readers and color-blind users |
| One template per form element | Label, control, help text, and error text in the same template | Splitting the label into its own component for reuse | Id-based association is linked automatically only inside one template |
| One focus mechanism | `delegatesFocus` for a field wrapper, an `@api` method for a composite widget | `delegatesFocus` plus `tabindex` in the same component | The guide states the two combined throw off focus order |

---

## Common Patterns

### Base-Component Replacement For Custom Click Targets

**When to use:** The component currently uses custom HTML such as a clickable `div`, icon-only action, or hand-rolled toggle.

**How it works:** Replace the interactive surface with `lightning-button`, `lightning-button-icon`, `lightning-input`, or another standard base component. Keep any remaining custom markup decorative, not interactive.

**Why not the alternative:** Adding `tabindex`, `role`, and key handlers to arbitrary markup usually creates incomplete keyboard behavior and inconsistent screen-reader output.

### Deliberate Focus Management Around Dialogs

**When to use:** The component opens a modal, quick action surface, or blocking overlay.

**How it works:** Use `LightningModal` or another supported dialog surface, set focus on meaningful content or the first actionable control, and return focus to the launch element when the interaction closes.

**Why not the alternative:** Leaving focus wherever the browser last had it makes the overlay hard to use and easy to lose.

### Accessible Composite Widget Boundary

**When to use:** A real business need requires a custom picker, listbox, or multi-step composite component.

**How it works:** Choose a known WAI-ARIA interaction pattern, document the keyboard contract, and test it with both tab order and screen-reader announcements before shipping.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Standard action, toggle, or input | Use a `lightning-*` base component | Accessible behavior is already implemented and maintained by the platform |
| Need branded layout but normal semantics | Use an SLDS blueprint with minimal custom behavior | Keeps semantics closer to supported interaction models |
| Need a modal or blocking overlay | Use `LightningModal` with an explicit focus plan | Modal semantics and dismissal behavior are easier to keep correct |
| Considering ARIA on a clickable `div` | Replace it with semantic HTML or a base component | ARIA does not fully repair incorrect structure |
| Custom composite widget is unavoidable | Implement and test a formal keyboard model | Composite controls need a documented accessibility contract |
| Label must live in a different component from its input | Redesign to one template, or render both in light DOM | Cross-template id linking is impossible in native shadow DOM; light DOM is the guide's stated remedy and carries a security cost |
| Parent needs to focus a child component | Set `delegatesFocus`, or expose an `@api` focus method | Focus skips the custom element container, so the host's `focus()` does nothing by default |
| Custom cell type inside `lightning-datatable` | Wire `data-navigation="enable"` and `internalTabIndex` through the cell template | Custom data types do not participate in the datatable's keyboard navigation until they opt in |

---


## Recommended Workflow

1. **Inventory the interactive surface.** List every element a user can activate, and for each one
   record: is it a base component, semantic HTML, or a `div`/`span` with a handler? Fill in the
   Component Scope and Accessibility Contract sections of
   `templates/lwc-accessibility-template.md` as you go — the unanswered lines are the design gaps.
2. **Delete before you add.** For each custom interactive surface, answer the first question in
   *Questions to Ask*. Anything a `lightning-*` component can express goes back to that component;
   the remainder is what you are actually designing.
3. **Draw the labelling boundary.** Put the label, control, help text, and error text of one field
   in one template. Read `references/gotchas.md` § *Id-Based ARIA Association Stops At The Shadow
   Boundary* before splitting anything across components, and § *Id-Referencing ARIA Attributes Are
   Not Ordinary Reflected Properties* before exposing an `aria-*` property with `@api`.
4. **Build from the reference bundle.** Copy the component in `references/code-examples.md` — HTML,
   JS, CSS, `js-meta.xml` — and its `package.xml`. Start from
   `templates/lwc/component-skeleton/` for the bundle shape. Pick one focus mechanism
   (`delegatesFocus` *or* explicit `tabindex`), never both.
5. **Assert the accessibility, don't eyeball it.** Port the Jest suite from
   `references/code-examples.md`: `for`/`id` relationship, `aria-describedby` target,
   `aria-invalid` flip, live-region text, `shadowRoot.activeElement` after an error, and zero
   `tabindex` when `delegatesFocus` is set. Run with `npm run test:unit`.
6. **Run the checker over the source tree.**
   `python3 skills/lwc/lwc-accessibility/scripts/check_lwc_accessibility.py --manifest-dir force-app/main/default/lwc`
   It fails on unresolvable id references (A4), unsupported `tabindex` values (A5),
   `tabindex` beside `delegatesFocus` (A6), unlabelled controls (A2, A7, A9), and incomplete
   bundles (B1, B2). Every finding is a real defect, not a style opinion.
7. **Do the two things no script can do.** Tab the whole component with the mouse untouched, and
   run it once with a screen reader, checking the four focus destinations from step 3 of
   *Questions to Ask*. Record the result in the Sign-Off Checklist of the template.

---

## Review Checklist

Run through these before marking work in this area complete:

- [ ] Every interactive surface is semantic HTML or a supported base component.
- [ ] Inputs, buttons, and meaningful icons have a clear accessible name.
- [ ] Focus order matches the visible reading order and business flow.
- [ ] Modal or overlay interactions trap and restore focus intentionally.
- [ ] Validation feedback is programmatic and not color-only.
- [ ] Keyboard-only testing covers open, close, save, cancel, and error states.
- [ ] Every `for` / `aria-labelledby` / `aria-describedby` target id is declared in the same template.
- [ ] No `id` appears in a JS or CSS selector; element lookup uses `lwc:ref` or `data-*`.
- [ ] `tabindex` is absent, `0`, or `-1` — and absent entirely if `delegatesFocus` is set.
- [ ] `js-meta.xml` declares `apiVersion`, and it is not pinned below what the component needs.
- [ ] `check_lwc_accessibility.py` reports no issues over the bundle's source tree.
- [ ] Jest asserts the label/id relationship, `aria-invalid`, and `shadowRoot.activeElement` after an error.

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **`lightning-icon` needs deliberate text when it carries meaning** - icon-only affordances look obvious visually but become vague or silent to assistive technology without `alternative-text`.
2. **Custom HTML can regress below the platform baseline quickly** - moving away from `lightning-*` components often removes built-in keyboard and label behavior teams assumed they still had.
3. **Focus can get lost after rerender** - conditional templates, async state changes, and modal open or close transitions can strand keyboard users unless focus is restored deliberately.
4. **ARIA does not replace semantic structure** - adding roles to the wrong element can still produce confusing navigation and announcement behavior.
5. **Template `id` values are rewritten at render time** - `#myInput` selectors in JS and CSS miss; only `for` / `aria-*` associations survive, and only within one template.
6. **`for` and `aria-labelledby` do not cross a shadow boundary** - the attribute renders, nothing links, and no error appears.
7. **`tabindex` supports only `0` and `-1`** - and must not be combined with `delegatesFocus`.
8. **A custom element is not focusable by default** - `focus()` on the host is a no-op until you set `delegatesFocus` or expose a focus method.
9. **Base components always render in shadow DOM** - switching your component to light DOM does not open up theirs.
10. **`lightning-datatable` custom cell types opt out of keyboard navigation** - until `data-navigation` and `internalTabIndex` are wired through.

Full detail, with guide line citations, is in `references/gotchas.md`.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Accessibility review | Findings on semantic markup, labels, keyboard interaction, and focus behavior |
| Remediation plan | Concrete changes to base components, ARIA usage, and focus handling |
| Test checklist | Keyboard and screen-reader scenarios that should pass before release |
| Component bundle | HTML / JS / CSS / `js-meta.xml` with in-template label and error association (`references/code-examples.md`) |
| Jest suite | Assertions on `for`/`id`, `aria-describedby`, `aria-invalid`, live-region text, and focus destination |
| Checker report | `check_lwc_accessibility.py --manifest-dir <lwc root>` output, clean before deploy |

---

## Reference Files

| File | Read it when |
|---|---|
| `references/code-examples.md` | You are building or fixing a bundle — accessible input wrapper (HTML/JS/CSS), `js-meta.xml`, Jest suite, `package.xml`, deploy and verification commands |
| `references/gotchas.md` | Something renders correctly and behaves wrongly: id rewriting, cross-boundary ARIA, `tabindex`, `delegatesFocus`, datatable cell types, synthetic vs native shadow |
| `references/examples.md` | You want the worked before/after: clickable card → button, focus return after a modal, and the label-across-two-components failure with both fixes |
| `references/llm-anti-patterns.md` | You are reviewing AI-generated LWC markup, or you are the AI generating it — eight detection hints for the mistakes that pass a visual check |
| `references/well-architected.md` | You are justifying the design in a review: pillar framing, tradeoffs, and the official sources with the claim each one supports |
| `templates/lwc-accessibility-template.md` | You are running the review — the scope, contract, labelling, and sign-off worksheet |
| `scripts/check_lwc_accessibility.py` | Before every deploy — `--manifest-dir <lwc source root>` |

---

## Related Skills

- `lwc/lwc-modal-and-overlay` - use when the main problem is dialog choice and overlay lifecycle rather than general accessibility posture.
- `lwc/lwc-forms-and-validation` - use when the accessibility issue is mainly inside form validation and record-edit UX.
- `lwc/lwc-testing` - use alongside this skill to turn accessibility expectations into repeatable component tests.
- `lwc/lwc-focus-management` - use when focus order, traps, and restoration are the whole problem and labelling is already correct.
- `lwc/lwc-accessibility-patterns` - use when you need a specific WAI-ARIA composite-widget implementation (listbox, combobox, tabs) rather than the posture and boundary decisions here.
- `lwc/lwc-jest-testing-with-accessibility` - use when the goal is a broader accessibility test harness rather than the per-component assertions in this skill's Jest suite.
- `lwc/lwc-shadow-vs-light-dom-decision` - use before choosing light DOM to fix a cross-component ARIA reference; that choice has security consequences this skill only summarises.
