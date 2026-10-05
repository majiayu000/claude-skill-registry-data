---
name: wcag-remediation
description: This skill should be used when the user mentions "accessibility", "a11y", "WCAG", "ARIA", "screen reader", "keyboard navigation", "focus", "focus trap", "color contrast", "alt text", "aria-label", "aria-expanded", "accessible name", or making a component usable by assistive technology. It provides the WCAG 2.2 remediation methodology and the cross-element fixes that automated tools miss.
---

# WCAG Remediation

## Purpose
Provide a standardized, static methodology for *fixing* accessibility failures, not just detecting them. Automated scanners are structurally limited: axe-core catches roughly a third to a half of WCAG issues, and linters like `jsx-a11y` reason about one element at a time, so they are blind to relationships (a control and its label in different subtrees), to behavior over time (focus when a dialog opens/closes), and to whether a chosen ARIA pattern is *complete*. This skill encodes the fixes that require reading the whole component.

## The Remediation Order of Operations
Apply fixes in this priority, a lower step often removes the need for a higher one:

1. **Use the right native element.** A `<button>`, `<a href>`, `<label>`, `<input>`, `<dialog>`, or `<nav>` brings a role, keyboard behavior, and focusability for free. Replacing a `<div onClick>` with a `<button>` fixes 2.1.1, 2.4.7, and 4.1.2 in one edit.
2. **Establish relationships.** Associate inputs with `<label for>`; name controls with visible text via `aria-labelledby` before inventing an `aria-label`; group with `<fieldset>`/`<legend>`.
3. **Add ARIA only where native falls short**, and add the *complete* pattern, all required roles, states, and keyboard interactions from the APG, never a lone `role`.
4. **Fix focus behavior**: trap, move-in, restore, background inertness, visible focus.
5. **Fix perceivability**: contrast, text alternatives, heading/landmark structure.

## The First Rule of ARIA
No ARIA is better than bad ARIA. Prefer removing incorrect ARIA over adding more. A redundant `role="button"` on a `<button>`, an `aria-label` that overrides good visible text, or `aria-hidden="true"` on a focusable element are each *worse* than nothing.

## Cross-Element Fixes Linters Miss

| Failure | Why linters miss it | The fix | WCAG SC |
|---|---|---|---|
| Icon button, no name | Element is valid in isolation | `aria-labelledby` to nearby text, else `aria-label` | 1.1.1, 4.1.2 |
| Input labeled by distant text | Label lives in another subtree | `aria-labelledby` / `<label for>` | 1.3.1, 3.3.2 |
| Custom widget missing state | State belongs on a *different* element | `aria-expanded`/`aria-selected`/`aria-checked` on the right node | 4.1.2 |
| Focus lost on dialog close | It is a runtime behavior, not an attribute | store & restore the trigger element | 2.4.3 |
| Contrast fails against a token | Colors resolve through the theme | remap to nearest passing design token | 1.4.3, 1.4.11 |
| Reading order ≠ DOM order | Requires understanding layout intent | reorder DOM or fix `tabindex`/`order` | 1.3.2, 2.4.3 |

## Never Fabricate
Never invent `alt` text or a label for a meaningful image or control whose purpose cannot be read from context, insert a clearly marked placeholder and flag it for a human. Never assert a contrast ratio for a color that is only resolved at runtime.

## Additional Resources
### Reference Files
- **`references/aria-patterns.md`**: the ARIA Authoring Practices patterns (dialog, menu/menu-button, combobox, tabs, disclosure, listbox) with their correct roles, states, and full keyboard-interaction contract.
- **`references/focus-management.md`**: focus-order, focus-trap, focus-restoration, skip-link, `:focus-visible`, and roving-tabindex / `aria-activedescendant` recipes across React, Vue, Svelte, Angular, and plain HTML.
