---
name: progressive-enhancement
description: HTML-first development with CSS-only interactivity patterns. Use when building features that work without JavaScript, using native HTML elements, CSS pseudo-classes, and the View Transitions API.
allowed-tools: Read, Write, Edit
---

# Progressive Enhancement Skill

This skill covers HTML-first development patterns where functionality works without JavaScript. CSS provides visual feedback and interactivity through pseudo-classes, the `:has()` selector, and native HTML elements.

## Philosophy

Build in layers:
```
Layer 1: HTML      → Works in any browser, screen readers, search engines
Layer 2: CSS       → Layout, theming, validation feedback, animations
Layer 3: JS (opt)  → Enhanced interactions (only when truly necessary)
```

Every feature should have a **baseline HTML-only experience** that CSS enhances.

---

## Native HTML Elements for Interactivity

### `<details>` and `<summary>` for Accordions

No JavaScript needed for expand/collapse:

```html
<details>
  <summary>What is your return policy?</summary>
  <p>We offer a 30-day hassle-free return policy for all unused items.</p>
</details>
```

```css
details {
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: var(--spacing-md);

  & summary {
    cursor: pointer;
    font-weight: var(--font-weight-semibold);

    &::marker {
      color: var(--primary);
    }
  }

  &[open] summary {
    margin-bottom: var(--spacing-md);
  }
}
```

### `<dialog>` for Modals

Native modal with backdrop and focus trapping—**fully declarative with `command`/`commandfor`**:

```html
<button commandfor="settings-dialog" command="show-modal">
  Open Settings
</button>

<dialog id="settings-dialog">
  <h2>Settings</h2>
  <form method="dialog">
    <!-- Form content -->
    <button type="submit">Close</button>
    <!-- Or explicit close button -->
    <button commandfor="settings-dialog" command="close">Cancel</button>
  </form>
</dialog>
```

```css
dialog {
  border: none;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  max-width: 32rem;
  padding: var(--spacing-lg);

  &::backdrop {
    background: oklch(0% 0 0 / 0.5);
  }
}
```

**No JavaScript required.** The browser handles:
- Opening/closing
- Focus management
- `aria-expanded` states
- Backdrop clicks (with `method="dialog"`)

### Popover API

Popovers provide lightweight, non-modal overlays:

```html
<button commandfor="user-menu" command="toggle-popover">
  Menu
</button>

<div popover id="user-menu">
  <nav>
    <a href="/profile">Profile</a>
    <a href="/settings">Settings</a>
    <a href="/logout">Logout</a>
  </nav>
</div>
```

```css
[popover] {
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: var(--spacing-md);
  box-shadow: var(--shadow-md);

  /* Entry animation */
  opacity: 0;
  transform: translateY(-0.5rem);
  transition: opacity 0.2s, transform 0.2s, display 0.2s allow-discrete;

  &:popover-open {
    opacity: 1;
    transform: translateY(0);
  }

  /* Starting style for animation */
  @starting-style {
    &:popover-open {
      opacity: 0;
      transform: translateY(-0.5rem);
    }
  }
}
```

#### Popover Commands

| Command | Behavior |
|---------|----------|
| `toggle-popover` | Toggle open/closed |
| `show-popover` | Open only |
| `hide-popover` | Close only |

#### Dialog vs Popover

| Feature | `<dialog>` | `popover` |
|---------|-----------|-----------|
| Modal blocking | Yes (with `show-modal`) | No |
| Backdrop | Yes | Optional |
| Light dismiss | With `method="dialog"` | Yes (click outside) |
| Focus trapping | Yes | No |
| Use case | Confirmations, forms | Menus, tooltips, dropdowns |

### The `command` and `commandfor` Attributes

These attributes enable **declarative button behaviors** without JavaScript:

```html
<button commandfor="target-id" command="action">Label</button>
```

#### Built-in Commands

| Command | Target | Effect |
|---------|--------|--------|
| `show-modal` | `<dialog>` | Opens as modal |
| `close` | `<dialog>` | Closes dialog |
| `toggle-popover` | `[popover]` | Toggles popover |
| `show-popover` | `[popover]` | Opens popover |
| `hide-popover` | `[popover]` | Closes popover |

#### Custom Commands

Define custom behaviors with `--` prefix:

```html
<button commandfor="gallery" command="--next-slide">Next</button>
<button commandfor="gallery" command="--prev-slide">Previous</button>

<div id="gallery">
  <!-- Gallery content -->
</div>
```

```javascript
// JavaScript handles custom commands
document.getElementById('gallery').addEventListener('command', (event) => {
  switch (event.command) {
    case '--next-slide':
      // Next slide logic
      break;
    case '--prev-slide':
      // Previous slide logic
      break;
  }
});
```

#### Benefits Over onclick

| `onclick` | `command`/`commandfor` |
|-----------|------------------------|
| Inline JavaScript | Declarative HTML |
| CSP violations possible | CSP-friendly |
| Manual aria management | Automatic accessibility |
| Framework state needed | Browser handles state |

### `<datalist>` for Autocomplete

```html
<label for="browser">Choose a browser:</label>
<input list="browsers" id="browser" name="browser"/>
<datalist id="browsers">
  <option value="Chrome"/>
  <option value="Firefox"/>
  <option value="Safari"/>
  <option value="Edge"/>
</datalist>
```

---

## CSS-Only Interactivity Patterns

### The Checkbox Hack

Use hidden checkboxes to toggle state without JavaScript:

```html
<input type="checkbox" id="menu-toggle" hidden/>
<label for="menu-toggle" data-menu-trigger>Menu</label>
<nav data-mobile-nav>
  <ul>
    <li><a href="/">Home</a></li>
    <li><a href="/about">About</a></li>
  </ul>
</nav>
```

```css
nav[data-mobile-nav] {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease;
}

#menu-toggle:checked ~ nav[data-mobile-nav] {
  max-height: 500px;
}

/* Toggle icon state */
[data-menu-trigger]::before {
  content: "☰";
}

#menu-toggle:checked ~ [data-menu-trigger]::before {
  content: "✕";
}
```

### Theme Toggle with Radio Buttons

```html
<fieldset data-theme-selector>
  <legend>Theme</legend>
  <label>
    <input type="radio" name="theme" id="theme-light" checked/>
    Light
  </label>
  <label>
    <input type="radio" name="theme" id="theme-dark"/>
    Dark
  </label>
  <label>
    <input type="radio" name="theme" id="theme-auto"/>
    Auto
  </label>
</fieldset>
```

```css
:root {
  --bg: white;
  --text: #1f2937;
}

:root:has(#theme-dark:checked) {
  --bg: #1f2937;
  --text: #f9fafb;
}

:root:has(#theme-auto:checked) {
  @media (prefers-color-scheme: dark) {
    --bg: #1f2937;
    --text: #f9fafb;
  }
}

body {
  background: var(--bg);
  color: var(--text);
}
```

### Tab Panels with Radio Buttons

```html
<div data-tabs>
  <input type="radio" name="tabs" id="tab-1" checked hidden/>
  <input type="radio" name="tabs" id="tab-2" hidden/>
  <input type="radio" name="tabs" id="tab-3" hidden/>

  <nav>
    <label for="tab-1">Overview</label>
    <label for="tab-2">Features</label>
    <label for="tab-3">Pricing</label>
  </nav>

  <section data-tab="1">Overview content...</section>
  <section data-tab="2">Features content...</section>
  <section data-tab="3">Pricing content...</section>
</div>
```

```css
[data-tabs] {
  & section {
    display: none;
  }

  &:has(#tab-1:checked) section[data-tab="1"],
  &:has(#tab-2:checked) section[data-tab="2"],
  &:has(#tab-3:checked) section[data-tab="3"] {
    display: block;
  }

  & nav label {
    cursor: pointer;
    padding: var(--spacing-sm) var(--spacing-md);
  }

  &:has(#tab-1:checked) label[for="tab-1"],
  &:has(#tab-2:checked) label[for="tab-2"],
  &:has(#tab-3:checked) label[for="tab-3"] {
    background: var(--primary);
    color: white;
  }
}
```

---

## The `:has()` Selector

The `:has()` selector enables parent-based styling:

### Conditional Parent Styling

```css
/* Style parent when it contains a specific child */
article:has(img) {
  display: grid;
  grid-template-columns: 1fr 2fr;
}

/* Form field styling based on input state */
form-field:has(input:required) label::after {
  content: " *";
  color: var(--error);
}

/* Card highlight when checkbox is checked */
product-card:has(input:checked) {
  border-color: var(--primary);
}
```

### Sibling-Based Styling

```css
/* Style elements when sibling checkbox is checked */
input:checked + label {
  font-weight: bold;
}

/* Style nav based on hidden checkbox state */
#nav-toggle:checked ~ nav {
  max-height: 500px;
}
```

---

## Form Validation Pseudo-Classes

### `:user-valid` and `:user-invalid`

These apply only **after user interaction**, preventing premature error states:

```css
/* Only show valid state after user has typed */
input:user-valid {
  border-color: var(--success);
}

/* Only show error after user has interacted */
input:user-invalid {
  border-color: var(--error);
}

/* Parent styling based on input state */
form-field:has(input:user-valid) output {
  color: var(--success);
}

form-field:has(input:user-invalid) output {
  color: var(--error);
}
```

### `:valid` and `:invalid` (Immediate)

These apply immediately, even before interaction:

```css
/* Use for optional "preview" validation */
input:valid {
  /* Subtle indication */
}

input:invalid {
  /* Avoid strong error styling - user hasn't finished */
}
```

### `:placeholder-shown`

Style based on whether input has content:

```css
input:placeholder-shown {
  /* Empty input styles */
}

input:not(:placeholder-shown) {
  /* Has content */
}
```

### `:required` and `:optional`

```css
input:required {
  /* Required field indicator */
}

label:has(+ input:required)::after {
  content: " *";
  color: var(--error);
}
```

---

## View Transitions API

Smooth page-to-page animations without JavaScript:

### Enable View Transitions

```html
<meta name="view-transition" content="same-origin"/>
```

### Default Transition

With the meta tag, all same-origin navigations get a crossfade by default.

### Named Transitions

```css
/* Assign transition names */
.hero-image {
  view-transition-name: hero;
}

/* Or use data attributes */
[data-vt="card-1"] {
  view-transition-name: card-1;
}

/* Custom animation */
::view-transition-old(hero) {
  animation: fade-out 0.3s ease-out;
}

::view-transition-new(hero) {
  animation: fade-in 0.3s ease-in;
}

@keyframes fade-out {
  to { opacity: 0; }
}

@keyframes fade-in {
  from { opacity: 0; }
}
```

### Card-to-Detail Transition

```html
<!-- List page -->
<article data-vt="product-123">
  <img src="product.jpg" style="view-transition-name: product-123-img"/>
  <h2 style="view-transition-name: product-123-title">Product Name</h2>
</article>

<!-- Detail page -->
<article>
  <img src="product.jpg" style="view-transition-name: product-123-img"/>
  <h1 style="view-transition-name: product-123-title">Product Name</h1>
</article>
```

---

## Animation Patterns

For CSS animations including scroll-driven animations, transitions, and motion accessibility (`prefers-reduced-motion`), see the **`animation-motion`** skill.

---

## CSS-Only Show/Hide Patterns

### Content Reveal on Focus

```css
/* Hidden by default */
[data-tooltip] {
  position: relative;

  &::after {
    content: attr(data-tooltip);
    position: absolute;
    opacity: 0;
    visibility: hidden;
    transition: opacity 0.2s;
  }

  &:hover::after,
  &:focus::after {
    opacity: 1;
    visibility: visible;
  }
}
```

### Disclosure Widget

```css
/* Summary arrow rotation */
details summary::before {
  content: "▶";
  display: inline-block;
  transition: transform 0.2s;
  margin-right: 0.5em;
}

details[open] summary::before {
  transform: rotate(90deg);
}
```

---

## Accessibility Considerations

### Focus Management

CSS can style focus, but focus order requires HTML structure or JS:

```css
/* Visible focus indicators */
:focus-visible {
  outline: 2px solid var(--primary);
  outline-offset: 2px;
}

/* Remove default outline only when using custom */
:focus:not(:focus-visible) {
  outline: none;
}
```

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Hidden Checkbox Labels

When using checkbox hacks, ensure labels are accessible:

```html
<input type="checkbox" id="toggle" hidden/>
<label for="toggle">
  <span class="sr-only">Toggle menu</span>
  <span aria-hidden="true">☰</span>
</label>
```

```css
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

---

## When JavaScript IS Needed

Progressive enhancement means JavaScript enhances, not enables. Use JS when:

1. **Complex state management** - More than simple on/off
2. **Async operations** - Fetching data, form submission
3. **Focus management** - Moving focus programmatically
4. **Real-time updates** - WebSocket, polling
5. **Complex animations** - Scroll-triggered, gesture-based

Even then, provide a baseline:
- Forms should submit without JS
- Navigation should work without JS
- Content should be readable without JS

---

## Graceful Degradation for JS-Required Applications

When an application **requires** JavaScript to function (SPAs, complex editors, real-time apps), provide graceful degradation patterns.

### The `<noscript>` Element

#### Error Message in Body

Display a clear message when JavaScript is disabled:

```html
<body>
  <noscript>
    <div class="js-required-notice">
      <h2>JavaScript Required</h2>
      <p>This application requires JavaScript to function.
         Please enable JavaScript in your browser settings.</p>
    </div>
  </noscript>
  <!-- App content -->
</body>
```

#### Hide JS-Only UI in Head

Use `<noscript>` in `<head>` to inject styles hiding JS-dependent elements:

```html
<head>
  <noscript>
    <style>
      [data-js-required] { display: none !important; }
      .js-required-notice { display: block !important; }
    </style>
  </noscript>
</head>
```

```html
<body>
  <div class="js-required-notice" hidden>JavaScript is required.</div>
  <main data-js-required>
    <!-- JS-only app content -->
  </main>
</body>
```

#### Redirect with Fallback Link

For full-page JS apps, redirect to a static fallback:

```html
<head>
  <noscript>
    <meta http-equiv="refresh" content="0; url=/no-javascript.html"/>
  </noscript>
</head>
<body>
  <noscript>
    <p>Redirecting... <a href="/no-javascript.html">Click here</a> if not redirected.</p>
  </noscript>
</body>
```

### CSS Scripting Media Query

Modern CSS can detect JavaScript availability:

```css
/* When JS is disabled */
@media (scripting: none) {
  [data-js-required] {
    display: none;
  }

  .no-js-message {
    display: block;
  }
}

/* When JS is enabled */
@media (scripting: enabled) {
  .no-js-message {
    display: none;
  }
}
```

**Browser support:** Chrome 120+, Firefox 113+, Safari 17+

### Server-Side JS Detection

Track JavaScript-disabled users for analytics:

```html
<!-- Image beacon in noscript -->
<noscript>
  <img src="/api/analytics?js=disabled" alt="" width="1" height="1"/>
</noscript>
```

Or check for a JS-set cookie on the server:

```javascript
// In your app initialization
document.cookie = 'js_enabled=true; path=/';
```

### When to Use These Patterns

| Scenario | Recommended Pattern |
|----------|---------------------|
| Content-first pages | Don't need `<noscript>` - progressive enhancement handles it |
| SPA/complex web apps | `<noscript>` message + CSS hiding |
| Full-page JS apps | Redirect to static fallback |
| Analytics needs | Image beacon |

---

## CSS Feature Detection with `@supports`

Use `@supports` for non-Baseline CSS features. This applies the same progressive enhancement philosophy to CSS itself.

### Pattern: Baseline Fallback + Enhancement

```css
/* Base: Baseline-safe fallback */
p {
  word-break: break-word;
}

/* Enhancement: non-Baseline feature */
@supports (text-wrap: pretty) {
  p {
    text-wrap: pretty;
  }
}
```

### Common Progressive CSS Enhancements

```css
/* Typography enhancement */
@supports (text-wrap: balance) {
  h1, h2, h3 {
    text-wrap: balance;
  }
}

/* Color enhancement */
@supports (color: oklch(50% 0.2 260)) {
  :root {
    --primary: oklch(55% 0.22 260);
  }
}

/* Container query fallback */
@supports not (container-type: inline-size) {
  /* Fallback layout when container queries unavailable */
  product-card {
    display: block;
  }
}
```

### Multiple Feature Detection

```css
/* Combine features with and/or */
@supports (display: grid) and (container-type: inline-size) {
  product-grid {
    display: grid;
    container-type: inline-size;
  }
}

/* Negation for fallbacks */
@supports not (gap: 1rem) {
  .flex-container > * + * {
    margin-inline-start: 1rem;
  }
}
```

### JavaScript Feature Detection

For features that can't be detected with `@supports`, use JavaScript with data attributes:

```javascript
// Detect and expose to CSS
if (CSS.supports('view-transition-name', 'test')) {
  document.documentElement.dataset.viewTransitions = 'supported';
}
```

```css
[data-view-transitions="supported"] {
  /* Enhanced styles */
}
```

---

## Checklist

When building interactive features:

- [ ] Does it work without JavaScript?
- [ ] Is there semantic HTML structure?
- [ ] Are native elements used where applicable (`<details>`, `<dialog>`, `[popover]`)?
- [ ] Are `command`/`commandfor` used for dialogs and popovers (not `onclick`)?
- [ ] Is state managed via checkboxes/radios for CSS access?
- [ ] Are data attributes used instead of classes for state?
- [ ] Is `:has()` used appropriately for parent styling?
- [ ] Are `:user-valid`/`:user-invalid` used over `:valid`/`:invalid`?
- [ ] Is `prefers-reduced-motion` respected?
- [ ] Are focus states visible and clear?
- [ ] Is View Transitions meta tag included?
- [ ] If JS is required, does `<noscript>` provide a fallback message?
- [ ] Are non-Baseline CSS features wrapped in `@supports`?

## Related Skills

- **css-author** - Modern CSS organization with native @import, @layer casca...
- **javascript-author** - Write vanilla JavaScript for Web Components with function...
- **data-attributes** - Using data-* attributes as the HTML/CSS/JS bridge for sta...
- **forms** - HTML-first form patterns with CSS-only validation
