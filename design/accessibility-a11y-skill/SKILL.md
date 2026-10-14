---
name: accessibility-a11y-skill
description: >-
  Implement and audit web accessibility — WCAG 2.1, ARIA, keyboard navigation,
  contrast, screen readers, axe-core/Lighthouse audits, semantic HTML, focus
  management.
license: Apache-2.0
compatibility: opencode
category: Framework-Specific
---

## What I do

I help you build accessible web applications that work for everyone:

1. **WCAG 2.1 Compliance**: Systematic review against A/AA/AAA criteria
2. **ARIA Patterns**: Correct use of roles, states, and properties
3. **Keyboard Navigation**: Focus management and keyboard shortcuts
4. **Color Contrast**: Verify contrast ratios and color independence
5. **Automated Audits**: Configure axe-core and Lighthouse in CI
6. **Semantic HTML**: Proper element selection for meaning and structure
7. **Screen Reader Testing**: Testing strategies for NVDA, VoiceOver, JAWS

## When to use me

Use this skill when:
- Building UI components that must be accessible
- Auditing an existing application for WCAG compliance
- Setting up automated accessibility testing in CI/CD
- Implementing keyboard navigation for complex widgets
- Fixing accessibility violations reported by Lighthouse or axe-core
- Creating ARIA patterns for custom components
- Ensuring color contrast meets WCAG requirements
- Adding screen reader support to dynamic content

## Related Skills

- **frontend-design-skill**: UI creation and visual design. This skill ensures that UI is accessible.
- **uiux-review-skill**: Peer — surfaces a11y basics at axis 10 of its 13-axis rubric (alt text, labels, contrast samples, axe-core checks) and **delegates deep WCAG 2.1 compliance work here**. If a UI/UX review surfaces a Critical a11y finding, follow up with this skill for the full fix pattern.
- **civiltekk-nextjs-skill** (route `scaffold`): Project scaffolding. This skill adds accessibility to the built components.
- **testing-subagent**: Can generate accessibility-specific tests.

---

## Step 1: Semantic HTML

### Document Structure

```html
<header role="banner">
  <nav aria-label="Main navigation">
    <ul>
      <li><a href="/" aria-current="page">Home</a></li>
      <li><a href="/about">About</a></li>
      <li><a href="/contact">Contact</a></li>
    </ul>
  </nav>
</header>

<main id="main-content">
  <h1>Page Title</h1>
  <section aria-labelledby="features-heading">
    <h2 id="features-heading">Features</h2>
    <article>
      <h3>Feature One</h3>
      <p>Description of feature one.</p>
    </article>
  </section>
</main>

<footer role="contentinfo">
  <p>&copy; 2024 Company Name</p>
</footer>
```

### Element Selection Rules

| Use | Instead Of | Why |
|-----|-----------|-----|
| `<button>` | `<div onclick>` | Native focus, keyboard, semantics |
| `<a href>` | `<span onclick>` | Native link behavior |
| `<input type="checkbox">` | Styled `<div>` | Native form control |
| `<label>` | Placeholder text | Always visible label |
| `<fieldset>` + `<legend>` | Grouped `<div>` | Form group semantics |
| `<table>` with `<th>` | CSS grid for data | Table semantics |
| `<dialog>` | Custom modal | Native focus trap, escape |

---

## Step 2: ARIA Patterns

### Rules of ARIA

1. **Don't use ARIA** if a native HTML element provides the semantics
2. **Don't change native semantics** — use `<button>` not `<div role="button">`
3. **All interactive ARIA elements must be keyboard accessible**
4. **Don't use `role="presentation"` or `aria-hidden="true"`** on focusable elements

### Common Patterns

#### Live Regions (Dynamic Content)

```html
<div aria-live="polite" aria-atomic="true">
  <p>3 results found</p>
</div>

<div aria-live="assertive" role="alert">
  <p>Form submission failed. Please check your inputs.</p>
</div>
```

#### Dynamic Error Banners (`aria-alert-dynamic-errors`)

Conditionally rendered error banners are invisible to screen readers unless announced via `role="alert"`. Icon-only dismiss buttons need an explicit `aria-label`.

```tsx
// BEFORE: Error banner not announced, dismiss button has no label
{error && (
  <div className="rounded-md bg-red-50 p-4">
    <p className="text-sm text-red-700">{error}</p>
    <button onClick={() => setError(null)}>
      <XIcon className="h-5 w-5 text-red-500" />
    </button>
  </div>
)}

// AFTER: role="alert" announces changes, aria-label on dismiss button
{error && (
  <div role="alert" className="rounded-md bg-red-50 p-4">
    <p className="text-sm text-red-700">{error}</p>
    <button
      onClick={() => setError(null)}
      aria-label="Dismiss error"
      className="ml-2 text-red-500 hover:text-red-700"
    >
      <XIcon className="h-5 w-5" />
    </button>
  </div>
)}
```

**Key points**:
- `role="alert"` makes the container a live assertive region — screen readers announce content immediately on render
- Icon-only buttons require `aria-label` describing the action (e.g., "Dismiss error", "Close notification")
- Do NOT place `role="alert"` on a permanently visible container — only on dynamically shown/hidden content

#### Disclosure/Accordion

```html
<h3>
  <button
    aria-expanded="false"
    aria-controls="section-1"
    id="section-1-trigger"
  >
    Section Title
  </button>
</h3>
<div
  id="section-1"
  role="region"
  aria-labelledby="section-1-trigger"
  hidden
>
  <p>Section content</p>
</div>
```

```typescript
function toggleDisclosure(trigger: HTMLButtonElement) {
  const expanded = trigger.getAttribute("aria-expanded") === "true"
  const content = document.getElementById(trigger.getAttribute("aria-controls")!)

  trigger.setAttribute("aria-expanded", String(!expanded))
  content.hidden = expanded
}
```

#### Dialog/Modal

```html
<dialog aria-labelledby="dialog-title" aria-describedby="dialog-desc">
  <h2 id="dialog-title">Confirm Action</h2>
  <p id="dialog-desc">Are you sure you want to delete this item?</p>
  <button>Cancel</button>
  <button>Confirm</button>
</dialog>
```

#### Tabs

```html
<div role="tablist" aria-label="Account settings">
  <button role="tab" aria-selected="true" aria-controls="panel-profile" id="tab-profile">
    Profile
  </button>
  <button role="tab" aria-selected="false" aria-controls="panel-security" id="tab-security" tabindex="-1">
    Security
  </button>
</div>
<div role="tabpanel" aria-labelledby="tab-profile" id="panel-profile">
  <p>Profile settings</p>
</div>
<div role="tabpanel" aria-labelledby="tab-security" id="panel-security" hidden>
  <p>Security settings</p>
</div>
```

---

## Step 3: Keyboard Navigation

### Focus Management

```typescript
function trapFocus(container: HTMLElement) {
  const focusable = container.querySelectorAll<HTMLElement>(
    'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
  )
  const first = focusable[0]
  const last = focusable[focusable.length - 1]

  container.addEventListener("keydown", (e) => {
    if (e.key !== "Tab") return

    if (e.shiftKey) {
      if (document.activeElement === first) {
        e.preventDefault()
        last.focus()
      }
    } else {
      if (document.activeElement === last) {
        e.preventDefault()
        first.focus()
      }
    }
  })

  first.focus()
}
```

### Skip Navigation

```html
<a href="#main-content" class="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-white focus:text-black">
  Skip to main content
</a>
```

### Keyboard Shortcuts Table

| Key | Action |
|-----|--------|
| Tab | Move to next focusable element |
| Shift+Tab | Move to previous focusable element |
| Enter | Activate button or link |
| Space | Activate button, toggle checkbox |
| Escape | Close modal, cancel action |
| Arrow keys | Navigate tabs, menus, listboxes |
| Home/End | First/last item in group |

---

## Step 4: Color Contrast

### WCAG Requirements

| Level | Normal Text | Large Text (18pt+/14pt bold) | UI Components |
|-------|-------------|-------------------------------|---------------|
| AA | 4.5:1 | 3:1 | 3:1 |
| AAA | 7:1 | 4.5:1 | Not specified |

### Tailwind Contrast Utilities

```css
.text-primary-900.bg-primary-50 { /* 18:1 contrast ratio */ }
.text-gray-700.bg-white { /* 8.5:1 contrast ratio */ }
.text-gray-400.bg-white { /* 2.8:1 — FAILS AA */ }
```

### Don't Rely on Color Alone

```html
<div class="flex items-center gap-2">
  <span class="inline-block w-3 h-3 rounded-full bg-green-500" aria-hidden="true"></span>
  <span class="text-green-700">
    <svg class="inline w-4 h-4" aria-hidden="true"><path d="M5 13l4 4L19 7" /></svg>
    Active
  </span>
</div>

<div class="flex items-center gap-2">
  <span class="inline-block w-3 h-3 rounded-full bg-red-500" aria-hidden="true"></span>
  <span class="text-red-700">
    <svg class="inline w-4 h-4" aria-hidden="true"><path d="M6 18L18 6M6 6l12 12" /></svg>
    Error
  </span>
</div>
```

---

## Step 5: Automated Audits

### axe-core with Jest

```typescript
import { axe, toHaveNoViolations } from "jest-axe"

expect.extend(toHaveNoViolations)

test("button has no accessibility violations", async () => {
  const { container } = render(<Button>Click me</Button>)
  const results = await axe(container)
  expect(results).toHaveNoViolations()
})
```

### Lighthouse CI

```yaml
name: Accessibility Audit
on: [push]
jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: treosh/lighthouse-ci-action@v12
        with:
          urls: |
            http://localhost:3000
          uploadArtifacts: true
          budgetPath: ./lighthouse-budget.json
```

### Lighthouse Budget

```json
{
  "ci": {
    "assert": {
      "assertions": {
        "categories:accessibility": ["error", { "minScore": 0.9 }],
        "color-contrast": "error",
        "document-title": "error",
        "html-has-lang": "error",
        "meta-viewport": "error",
        "valid-lang": "warn"
      }
    }
  }
}
```

### Next.js eslint-plugin-jsx-a11y

```javascript
module.exports = {
  extends: ["next/core-web-vitals", "plugin:jsx-a11y/recommended"],
  plugins: ["jsx-a11y"],
  rules: {
    "jsx-a11y/alt-text": "error",
    "jsx-a11y/anchor-is-valid": "error",
    "jsx-a11y/aria-props": "error",
    "jsx-a11y/aria-role": "error",
    "jsx-a11y/aria-unsupported-elements": "error",
    "jsx-a11y/click-events-have-key-events": "warn",
    "jsx-a11y/label-has-associated-control": "error",
    "jsx-a11y/mouse-events-have-key-events": "warn",
    "jsx-a11y/no-autofocus": "error",
    "jsx-a11y/no-static-element-interactions": "warn",
    "jsx-a11y/role-has-required-aria-props": "error",
  },
}
```

---

## Step 6: WCAG 2.1 Quick Checklist

### Perceivable

- [ ] All images have meaningful `alt` text
- [ ] Video has captions and audio has transcripts
- [ ] Color contrast meets AA (4.5:1 text, 3:1 large text)
- [ ] Information not conveyed by color alone
- [ ] Content resizes to 200% without loss

### Operable

- [ ] All functionality available via keyboard
- [ ] Focus indicator visible
- [ ] Skip navigation link provided
- [ ] No keyboard traps
- [ ] Enough time to read content (or extendable)
- [ ] No content flashes more than 3 times per second

### Understandable

- [ ] Language defined (`<html lang="en">`)
- [ ] Form labels associated with inputs
- [ ] Error messages clearly identify the problem and suggest fixes
- [ ] Navigation consistent across pages
- [ ] Predictable behavior on focus and input

### Robust

- [ ] Valid HTML markup
- [ ] ARIA used correctly (if needed)
- [ ] Name, role, value defined for all UI components
- [ ] Status messages announced to screen readers
