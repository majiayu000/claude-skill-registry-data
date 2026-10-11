---
name: bootstrap
description: Bootstrap — responsive grid for legacy, server-rendered, WordPress.
---

## Detection Signals

- `bootstrap` in `package.json` OR `bootstrap` CSS/JS in HTML `<link>`/`<script>` tags
- `react-bootstrap` or `bootstrap-vue` packages
- `data-bs-*` attributes in HTML elements
- `.container`, `.row`, `.col-*` class patterns
- `.btn`, `.card`, `.modal`, `.navbar`, `.dropdown` class patterns

## MCP Setup

No official MCP server is available for Bootstrap.

> Reference the Bootstrap 5 docs at [getbootstrap.com/docs](https://getbootstrap.com/docs/5.3/). Configure a documentation search MCP in your CLI's settings if one is available.

## Core Concepts

| Concept | Detail |
|---------|--------|
| **12-column grid** | `.container` → `.row` → `.col-*` — always nest in this order |
| **Breakpoints** | `xs` (<576px), `sm` (576px), `md` (768px), `lg` (992px), `xl` (1200px), `xxl` (1400px) |
| **Utility classes** | Spacing `m-*/p-*`, display `d-*`, flex `d-flex/gap-*`, text `text-*`, color `text-*/bg-*` |
| **JS components** | Modal, dropdown, tooltip, collapse require Bootstrap's JS bundle or `data-bs-*` API |
| **Sass variables** | The canonical way to customize Bootstrap before its CSS is compiled |

## Component Patterns

```html
<!-- Grid — always: container → row → col -->
<div class="container">
  <div class="row g-3">
    <div class="col-12 col-md-6 col-lg-4">Content</div>
  </div>
</div>

<!-- Buttons -->
<button class="btn btn-primary">Primary</button>
<button class="btn btn-outline-secondary btn-sm">Small outline</button>

<!-- Modal — via data attributes, no JS needed for trigger -->
<button data-bs-toggle="modal" data-bs-target="#confirmModal">Open</button>
<div class="modal fade" id="confirmModal" tabindex="-1">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">...</div>
      <div class="modal-body">...</div>
    </div>
  </div>
</div>
```

## React Bootstrap Pattern

When `react-bootstrap` is present, use components — not raw class strings:

```tsx
import { Button, Modal, Container, Row, Col } from 'react-bootstrap'

// Correct — component manages refs and ARIA
<Button variant="primary" size="sm" onClick={handleClick} />

// Wrong — bypasses react-bootstrap's event and ref management
<button className="btn btn-primary btn-sm" onClick={handleClick} />
```

## Version Check

**Bootstrap 4 vs 5** — APIs differ. Confirm version in `package.json` before writing classes:
- Spacing: `ml-*`/`mr-*` (v4) → `ms-*`/`me-*` (v5)
- Flex gap: not available in v4
- Grid: `.row-cols-*` added in v5

## Critical Rules

- **Never mix Bootstrap grid with a custom grid** — pick one layout system per project
- **Use Bootstrap spacing utilities** — `m-*/p-*/gap-*` consistently; don't introduce arbitrary pixel values that break the spacing rhythm
- **Interactive components need Bootstrap JS** — modal, dropdown, tooltip, and collapse won't function without the JS bundle or Popper.js
- **React projects: use `react-bootstrap`** — raw HTML + class strings bypass ref and ARIA management
- **Customize via Sass variables** — overriding Bootstrap CSS with higher specificity causes maintenance problems; set `$primary: #yourcolor` before the Bootstrap import
