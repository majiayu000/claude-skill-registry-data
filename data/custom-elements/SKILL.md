---
name: custom-elements
description: Define and use custom HTML elements. Use when creating new components, defining custom tags, or using project-specific elements beyond standard HTML5.
allowed-tools: Read, Write, Edit, Bash
---

# Custom Elements Skill

This skill provides guidance for defining and using custom HTML elements in this project.

## Two Definition Systems

| System | File | Purpose |
|--------|------|---------|
| **HTML Validation** | `.claude/schemas/elements.json` | Validates custom elements in HTML (html-validate) |
| **Custom Elements Manifest** | `custom-elements.json` | Documents components for IDEs, Storybook, docs |

**Both are recommended** - elements.json for build-time HTML validation, CEM for runtime tooling.

See [MANIFEST.md](./MANIFEST.md) for Custom Elements Manifest generation.

## Using Existing Elements

Check `.claude/schemas/elements.json` for defined custom elements:

| Element | Type | Purpose |
|---------|------|---------|
| `product-card` | Block | Product display with sku, price attributes |
| `icon-element` | Void | Self-closing icon with required name attribute |
| `user-avatar` | Void | Avatar with required src, alt and optional size |
| `status-badge` | Inline | Status indicator with type (success/warning/error/info) |
| `data-table` | Block | Data table with source, sortable attributes |
| `nav-menu` | Block | Navigation with orientation (horizontal/vertical) |

## Usage Examples

```html
<!-- Product card with attributes -->
<product-card sku="ABC123" price="29.99">
  <h2>Product Name</h2>
  <p>Product description here.</p>
</product-card>

<!-- Void element (self-closing) -->
<icon-element name="star"/>
<user-avatar src="/avatar.jpg" alt="John Doe" size="medium"/>

<!-- Inline element -->
<p>Status: <status-badge type="success">Active</status-badge></p>

<!-- Block elements -->
<nav-menu orientation="horizontal">
  <ul>
    <li><a href="/">Home</a></li>
  </ul>
</nav-menu>

<data-table source="/api/users" sortable="">
  <!-- Table content -->
</data-table>
```

## Ad-hoc Custom Elements

For one-off custom elements not worth defining in `.claude/schemas/elements.json`, use the `x-*` prefix:

```html
<x-highlight>Important text</x-highlight>
<x-tooltip data-text="Help text">Hover me</x-tooltip>
<x-badge>New</x-badge>
```

The `x-*` pattern is excluded from validation by default.

## Defining New Elements

### Using Slash Command

```
/add-element my-widget
```

### Manual Definition

Add to `.claude/schemas/elements.json`:

```json
{
  "my-element": {
    "flow": true,
    "phrasing": false,
    "permittedContent": ["@flow"],
    "attributes": {
      "required-attr": { "required": true },
      "optional-attr": { "required": false }
    }
  }
}
```

## Element Schema Reference

### Content Model

| Property | Values | Description |
|----------|--------|-------------|
| `flow` | boolean | Can appear where flow content is expected |
| `phrasing` | boolean | Can appear where phrasing content is expected |
| `void` | boolean | Self-closing element (no content) |
| `permittedContent` | array | What content is allowed inside |

### Permitted Content Values

- `@flow` - Flow content (most elements)
- `@phrasing` - Phrasing content (inline elements)
- `@interactive` - Interactive elements
- `["p", "div"]` - Specific elements only

### Attribute Definitions

```json
{
  "attributes": {
    "name": {
      "required": true           // Must be present
    },
    "type": {
      "required": false,
      "enum": ["a", "b", "c"]    // Restricted values
    },
    "enabled": {
      "boolean": true            // Boolean attribute
    }
  }
}
```

## Complete Examples

### Block Element

```json
{
  "card-component": {
    "flow": true,
    "phrasing": false,
    "permittedContent": ["@flow"],
    "attributes": {
      "variant": {
        "required": false,
        "enum": ["default", "outlined", "elevated"]
      },
      "clickable": {
        "boolean": true
      }
    }
  }
}
```

Usage:
```html
<card-component variant="elevated" clickable="">
  <h2>Card Title</h2>
  <p>Card content</p>
</card-component>
```

### Void Element

```json
{
  "loading-spinner": {
    "void": true,
    "flow": true,
    "phrasing": true,
    "attributes": {
      "size": {
        "enum": ["small", "medium", "large"]
      }
    }
  }
}
```

Usage:
```html
<loading-spinner size="medium"/>
```

### Inline Element

```json
{
  "price-tag": {
    "flow": true,
    "phrasing": true,
    "permittedContent": ["@phrasing"],
    "attributes": {
      "currency": {
        "required": false,
        "enum": ["USD", "EUR", "GBP"]
      }
    }
  }
}
```

Usage:
```html
<p>Price: <price-tag currency="USD">29.99</price-tag></p>
```

## Naming Conventions

- Use lowercase with hyphens: `my-element`
- Names must contain a hyphen (web component spec)
- Be descriptive: `product-card` not `pc`
- Use consistent prefixes for related elements: `form-input`, `form-select`, `form-button`

---

## CSS-Only vs Full Web Components

Custom elements can be used in two distinct ways. Choose based on your needs.

### CSS-Only Custom Elements

Use the element as a semantic styling hook without JavaScript:

```html
<product-card>
  <img src="product.jpg" alt="Widget Pro" />
  <h3>Widget Pro</h3>
  <p>The best widget money can buy.</p>
</product-card>
```

```css
product-card {
  display: block;  /* Required: browsers default to inline */
  padding: var(--spacing-lg);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
}
```

**Characteristics:**
- No JavaScript required
- No `customElements.define()` call
- Matches `:not(:defined)` pseudo-class
- Requires explicit `display: block` (handled by shared reset)
- Content is in light DOM (no Shadow DOM)
- Styles work immediately, no FOUC

**Best for:**
- Semantic styling hooks (replacing `.card` classes)
- Progressive enhancement base
- Static content components
- Simple layout containers

### Full Web Components

Register the element with JavaScript for encapsulated behavior:

```javascript
class ProductCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.shadowRoot.innerHTML = `
      <style>
        :host { display: block; }
        /* Encapsulated styles */
      </style>
      <slot></slot>
    `;
  }
}

customElements.define('product-card', ProductCard);
```

**Characteristics:**
- Requires JavaScript
- Registered via `customElements.define()`
- Matches `:defined` pseudo-class after registration
- Can use Shadow DOM for style encapsulation
- Can have custom properties, methods, lifecycle hooks

**Best for:**
- Interactive components requiring JS
- Reusable across different projects
- Components needing encapsulated styles
- Complex state management

### When to Choose Each

| Factor | CSS-Only | Full Web Component |
|--------|----------|-------------------|
| JavaScript required | No | Yes |
| Works without JS | Yes | Needs fallback |
| Style encapsulation | No (global CSS) | Yes (Shadow DOM) |
| Complexity | Low | Higher |
| Interactivity | CSS-only (`:has`, `:checked`) | Full JS capability |
| Browser default display | `inline` (needs reset) | Controlled in `:host` |
| Progressive enhancement | Natural | Requires planning |

### Styling Considerations

**CSS-only elements need explicit display:**

The shared reset (`_reset.css`) handles this automatically with:

```css
:not(:defined) {
  display: block;
}
```

If you need a different display value, override it in your component CSS:

```css
product-card {
  display: grid;  /* Overrides the reset's block */
}
```

**Web Components control their own display:**

```javascript
// Inside the component
this.shadowRoot.innerHTML = `
  <style>
    :host {
      display: block;
      /* Component defines its own display */
    }
  </style>
  ...
`;
```

### The x-* Pattern for Ad-Hoc Elements

For one-off custom elements, use the `x-*` prefix (e.g., `<x-highlight>`). These:
- Are excluded from HTML validation by default
- Work well as CSS-only elements
- Signal "ad-hoc, not reusable" to other developers

```html
<p>This is <x-highlight>important text</x-highlight> in a paragraph.</p>
```

```css
x-highlight {
  background: var(--warning-light);
  padding-inline: var(--spacing-xs);
}
```

## Related Skills

- **javascript-author** - Write vanilla JavaScript for Web Components with function...
- **data-attributes** - Using data-* attributes as the HTML/CSS/JS bridge for sta...
- **state-management** - Client-side state patterns for Web Components
- **accessibility-checker** - Ensure WCAG2AA accessibility compliance
