---
name: apply-aria-roles
description: Use when building custom UI components that native HTML cannot represent — to give assistive technology the correct role, state, and property information for non-native interactive elements.
source: W3C WCAG 2.1 SC 4.1.2 Name, Role, Value (Level A); WAI-ARIA 1.2 specification; WAI-ARIA Authoring Practices 1.2; MDN ARIA guide
tags: [accessibility, wcag, a11y, aria, roles, states, properties, screen-reader]
related: [apply-keyboard-accessibility, write-semantic-html-structure, design-accessibility-standards]
---

# Apply ARIA Roles

Give custom UI components a valid ARIA role, accessible name, and required states — so screen readers understand and announce them correctly.

## Why This Is Best Practice

**Adopted by:** WCAG 2.1 SC 4.1.2 (Level A) is the robustness principle — required by
all accessibility laws. WAI-ARIA 1.2 is the W3C specification implemented in all modern
screen readers (NVDA, JAWS, VoiceOver, TalkBack). React Aria (Adobe), Headless UI
(Tailwind), Radix UI, and Angular CDK all implement WAI-ARIA patterns — used in millions
of production applications.
**Impact:** Deque Systems research found custom widgets without ARIA account for 38% of
critical accessibility defects in enterprise applications. A `<div>` with `onclick` and
no ARIA is announced as nothing (or as the text content) — users cannot determine the
element is interactive. ARIA provides the "what is it" signal that screen readers need
to announce controls correctly.
**Why best:** The alternative — styling `<div>` elements as buttons and hoping screen
readers infer their purpose — is unreliable. ARIA provides an explicit contract:
"this element is a tab", "this element is expanded", "this element is required".

Sources: W3C WCAG 2.1 SC 4.1.2 (2018); WAI-ARIA 1.2 (2023); WAI-ARIA Authoring
Practices 1.2; Deque Systems 2024 State of Digital Accessibility

## Steps

### Step 1: Follow the First Rule of ARIA — use native HTML first

```html
<!-- Wrong — custom button needs manual ARIA + keyboard + focus -->
<div role="button" tabindex="0" onclick="submit()">Submit</div>

<!-- Right — native button has all of this by default -->
<button type="submit">Submit</button>
```

WAI-ARIA First Rule: "If you can use a native HTML element or attribute with the
semantics and behavior you require already built in, instead of re-purposing an element
and adding an ARIA role, state or property to make it accessible, then do so."

### Step 2: Match role to the component pattern exactly

Use WAI-ARIA Authoring Practices (w3.org/WAI/ARIA/apg) as the source of truth.
Common patterns:

```html
<!-- Tab panel -->
<div role="tablist" aria-label="Account settings">
  <button role="tab" aria-selected="true" aria-controls="panel-profile" id="tab-profile">Profile</button>
  <button role="tab" aria-selected="false" aria-controls="panel-security" id="tab-security">Security</button>
</div>
<div role="tabpanel" id="panel-profile" aria-labelledby="tab-profile">...</div>
<div role="tabpanel" id="panel-security" aria-labelledby="tab-security" hidden>...</div>

<!-- Accordion -->
<h3>
  <button aria-expanded="true" aria-controls="section-1">Section 1</button>
</h3>
<div id="section-1" role="region" aria-labelledby="...">...</div>

<!-- Alert dialog (requires immediate focus) -->
<div role="alertdialog" aria-modal="true" aria-labelledby="dlg-title" aria-describedby="dlg-desc">
  <h2 id="dlg-title">Delete account</h2>
  <p id="dlg-desc">This action cannot be undone.</p>
  <button>Cancel</button>
  <button>Delete</button>
</div>
```

### Step 3: Provide accessible names for all interactive elements

Every interactive element needs an accessible name via one of these methods (in priority order):
1. `aria-labelledby` — references visible text in the DOM
2. `<label>` — for form inputs
3. `aria-label` — for elements with no visible text label
4. `title` — last resort, not reliably announced by all AT

```html
<!-- Icon button — no visible text, needs aria-label -->
<button aria-label="Delete item">
  <svg aria-hidden="true" focusable="false">...</svg>
</button>

<!-- Region labeled by heading -->
<section aria-labelledby="search-heading">
  <h2 id="search-heading">Search results</h2>
  ...
</section>
```

### Step 4: Update ARIA states when UI changes

States must be kept in sync with the UI. Stale states confuse screen readers.

```javascript
// Accordion expand/collapse
function toggleAccordion(button, panel) {
  const expanded = button.getAttribute('aria-expanded') === 'true';
  button.setAttribute('aria-expanded', String(!expanded));
  panel.hidden = expanded;
}

// Loading state
function startLoading(button) {
  button.setAttribute('aria-busy', 'true');
  button.setAttribute('aria-label', 'Saving…');
}

function stopLoading(button) {
  button.removeAttribute('aria-busy');
  button.setAttribute('aria-label', 'Save');
}
```

Common states to keep in sync: `aria-expanded`, `aria-selected`, `aria-checked`,
`aria-disabled`, `aria-invalid`, `aria-busy`.

### Step 5: Validate ARIA against the specification — avoid invalid combinations

```html
<!-- Wrong — aria-required on a div is invalid (not a form field role) -->
<div role="button" aria-required="true">Submit</div>

<!-- Wrong — role="presentation" on a focusable element -->
<a href="/home" role="presentation">Home</a>   <!-- removes link semantics -->

<!-- Wrong — conflicting roles -->
<button role="link">Click</button>   <!-- button IS a role; overriding with link is valid
                                          but confusing — just use <a href> -->
```

Use the axe-core browser extension to validate ARIA — it flags invalid role/attribute
combinations that are invisible to manual testing.

## When NOT to Use

- **When a native element exists** — never use `role="button"` when `<button>` is available. Never use `role="checkbox"` when `<input type="checkbox">` is available.
- **`aria-hidden` on focusable elements** — never hide a focusable element with `aria-hidden="true"`. It removes the element from the AT tree while leaving it in the Tab order, creating a "ghost" interactive element.

## Common Mistakes

**ARIA without keyboard support.** `role="button"` makes an element look like a button to screen readers — but without `tabindex="0"` and keyboard event handlers, it's not keyboard operable. Role + keyboard support are inseparable.

**`aria-label` on non-interactive elements.** `aria-label` on a `<div>` with no role has no effect. ARIA attributes only apply to elements with an explicit or implicit ARIA role.

**Not hiding decorative SVGs from AT.** An inline SVG without `aria-hidden="true"` and `focusable="false"` will be announced by some screen readers. Decorative SVGs must be hidden: `<svg aria-hidden="true" focusable="false">`.