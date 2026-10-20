---
name: make-ui-accessible
description: >-
  Load this skill when writing or reviewing component markup with interactive elements, images,
  forms, or navigation in any web frontend. Auto-load when a .svelte or .tsx file's HTML structure
  is written.
disable-model-invocation: false
user-invocable: false
paths:
  - "**/*.svelte"
  - "**/*.tsx"
  - "**/*.html"
license: Apache-2.0
---

# Make the UI Accessible

Write markup that works from the keyboard and a screen reader without extra effort. Done when every
interactive element is reachable, labelled, and passes the a11y lint for the framework.

## Procedure

1. Start from the native HTML element for the job, and add ARIA only where none fits.
2. Check that every action is keyboard-reachable with a visible focus indicator.
3. Label every form control and every image.
4. Fix all a11y lint warnings before opening a PR.

## Rules

### Baseline

- All interactive elements must be keyboard-accessible
- Images must have `alt` attributes (empty `alt=""` for decorative images)
- Use semantic HTML (`<button>`, `<nav>`, `<main>`, `<section>`, `<header>`) — not `<div>` for everything
- Fix all a11y lint warnings before opening a PR: `svelte-check` (SvelteKit) or `eslint-plugin-jsx-a11y` (React)
- Only the attribute and event syntax differs by framework: `onclick` / `bind:value` / `for` in Svelte, `onClick` / `value` + `onChange` / `htmlFor` in React. The ARIA attributes are identical.

### Keyboard navigation

- Every action reachable by mouse must be reachable by keyboard
- Visible focus indicator must never be removed (`outline: none` without a replacement is forbidden)
- Tab order must follow the visual reading order
- Modal dialogs must trap focus while open and return focus to the trigger on close

### ARIA

Use native HTML semantics first. Add ARIA only when no native element fits:

```html
<button>Submit</button>
<button aria-label="Close dialog">✕</button>
<p aria-live="polite" aria-atomic="true">Saved</p>
<button aria-expanded="false" aria-controls="details">Details</button>
```

Bind dynamic values with the framework's expression syntax: `aria-expanded={open}` in both Svelte and JSX.

Do not add `role="button"` to a `<div>` — use `<button>`. Never use `aria-hidden="true"` on a focusable element.

### Forms

```html
<label for="topic">Topic</label>
<input id="topic" type="text" />

<input id="email" aria-describedby="email-error" aria-invalid="true" />
<span id="email-error" role="alert">Enter a valid email address</span>
```

In JSX the label attribute is `htmlFor`. Set `aria-invalid` from the validation state, and render the error element only while it is set.

### Color and contrast

- Text contrast ratio: 4.5:1 minimum (3:1 for large text ≥ 18px or bold ≥ 14px)
- Do not rely on color alone to convey information — pair with an icon or text label
