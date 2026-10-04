---
name: accessible-components
description: This skill should be used when the user wants to build or fix accessible UI components or set up accessibility tooling — triggers like "make this modal accessible", "build an accessible dropdown", "add ARIA to this", "accessible tabs/combobox/tooltip/accordion", "set up a11y linting", or "fix keyboard navigation". It scaffolds WAI-ARIA APG component patterns adapted to the detected framework and wires up automated a11y linting.
version: 0.1.0
---

# Accessible components

Scaffold accessible UI component patterns that match the project's stack, then install automated accessibility linting so regressions get caught. Build on semantic HTML, add ARIA only to fill gaps, and ship correct keyboard support and focus management.

## When to use

Use this skill for requests such as:

- "Make this modal/dialog accessible"
- "Build an accessible dropdown / menu / tabs / combobox / tooltip / accordion / switch"
- "Add ARIA to this component"
- "Fix keyboard navigation" or "this can't be used without a mouse"
- "Set up a11y linting" / "add accessibility checks to CI"

## Workflow

1. **Detect the stack.** Read `../ux-foundations/references/stack-detection.md` and run that procedure before writing any code. Hold the resulting `framework`, `styling`, `language`, and `rootDir`. Report what was detected in one line. With no project, fall back to framework-agnostic HTML + vanilla JS + CSS custom properties (see `examples/disclosure.html`).

2. **Pick the correct APG pattern.** Map the requested component to its WAI-ARIA Authoring Practices (APG) pattern and read `references/aria-patterns.md` for required roles/attributes, the full keyboard map, focus rules, and common mistakes. Do not invent ARIA — use the established pattern.

3. **Implement, semantics first.**
   - Reach for native elements before ARIA: `<button>`, `<a href>`, `<dialog>`, `<details>/<summary>`, `<input type="checkbox">`, `<select>`, `<fieldset>/<legend>`. They bring behavior, focusability, and state for free.
   - Add ARIA only to express what HTML can't: correct `role`, and live state (`aria-expanded`, `aria-selected`, `aria-checked`, `aria-current`, `aria-disabled`).
   - Provide an accessible name for every interactive element (visible `<label>`, `aria-label`, or `aria-labelledby`).
   - Implement the complete keyboard interaction map from the pattern — not just Tab. Composite widgets (tabs, menus, listboxes, grids) use **roving tabindex** or `aria-activedescendant`, not a tab stop per child.
   - Manage focus: **focus trap** inside modal dialogs, **focus restoration** to the triggering element on close, send focus to a sensible target when content appears, and never strand focus on a hidden element.

4. **Wire to design tokens.** Style via classes that consume token variables (e.g. `var(--color-...)`, `var(--space-...)`, `var(--radius-...)`). Do not hardcode colors, spacing, or motion values — match the project's token system found during detection.

5. **Set up automated a11y linting** matched to the stack, and add a lint script entry. Do not silence or weaken existing warnings.
   - **React/JSX:** add `eslint-plugin-jsx-a11y`; extend `plugin:jsx-a11y/recommended` (or `strict`).
   - **Vue:** add `eslint-plugin-vuejs-accessibility`; extend `plugin:vuejs-accessibility/recommended`.
   - **Svelte:** the Svelte compiler emits a11y warnings by default — keep them enabled (do not set `enableSourcemap`/`compilerOptions` to suppress them); surface them in the build/lint output.
   - **Angular:** enable Angular template a11y lint rules via `@angular-eslint/template` (e.g. `accessibility-*` rules).
   - **Optional runtime checks:** add `@axe-core/react`, `@axe-core/playwright`, or `jest-axe`/`vitest-axe` to component tests so violations fail tests.
   - Add or extend a `"lint"` (and optionally `"lint:a11y"`) script in `package.json`.

## Core rules

Apply these to every component, regardless of framework:

- **Keyboard operability.** Everything actionable with a mouse must work with the keyboard alone. Follow the pattern's key map. Avoid positive `tabindex`.
- **Visible focus.** Never remove a focus outline without an equal-or-better replacement. Prefer `:focus-visible`. Ensure the focus indicator meets contrast against its background.
- **Accessible names.** Every control, region, and image needs a name via `<label>`, `aria-label`, `aria-labelledby`, or alt text. Icon-only buttons must have a name.
- **State communication.** Reflect state with ARIA, not just visuals: `aria-expanded`, `aria-selected`, `aria-checked`, `aria-pressed`, `aria-current`, `aria-disabled`/`disabled`, `aria-invalid`.
- **Focus management.** Trap focus in modals, restore it to the trigger on close, and move it deliberately when UI appears or disappears.
- **Reduced motion.** Gate non-essential animation behind `@media (prefers-reduced-motion: reduce)`; tie durations/easings to motion tokens.
- **Target size.** Interactive targets should be at least 24x24 CSS px (WCAG 2.2 AA), ideally 44x44 for touch.
- **Don't rely on color alone.** Pair color with text, icon, or shape to convey meaning or state.

## References and examples

- `references/aria-patterns.md` — condensed, accurate APG reference for Dialog, Disclosure, Tabs, Menu/Menu button, Combobox, Tooltip, Accordion, and Switch.
- `examples/README.md` — index of all worked examples. Match a new component to the closest one and adapt it to the detected stack. Coverage: Dialog (React/Vue/Svelte), Tabs (React/vanilla), Menu button (React/vanilla), Combobox (vanilla), Disclosure (vanilla).
