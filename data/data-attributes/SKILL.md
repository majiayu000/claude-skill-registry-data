---
name: data-attributes
description: Using data-* attributes as the HTML/CSS/JS bridge for state, variants, and configuration. Use when managing element state, styling variants, or configuring behavior without JavaScript classes.
allowed-tools: Read, Write, Edit
---

# Data Attributes Skill

This skill covers the use of `data-*` attributes as the preferred mechanism for state management, variant styling, and configuration in HTML-first development.

## Philosophy

**Data attributes replace classes for dynamic concerns.** While semantic elements and custom elements handle structure, `data-*` attributes handle:
- **State** (`data-expanded`, `data-loading`, `data-valid`)
- **Variants** (`data-type`, `data-variant`, `data-topic`)
- **Configuration** (`data-columns`, `data-size`, `data-animation`)

This creates a clean **HTML/CSS/JS bridge** where markup declares intent, CSS responds to it, and JavaScript (when needed) manipulates data attributes rather than class lists.

---

## Why Data Attributes Over Classes?

| Aspect | Classes | Data Attributes |
|--------|---------|-----------------|
| **Semantics** | Presentation-focused | Meaning-focused |
| **State** | `.is-active`, `.is-loading` | `data-state="active"` |
| **Variants** | `.btn-primary`, `.btn-large` | `data-variant="primary"` |
| **JS Access** | `classList.toggle('active')` | `dataset.state = "active"` |
| **Validation** | Cannot validate values | Can define allowed values |
| **Readability** | Class soup | Self-documenting |
| **CSS Selectors** | `.btn.primary.large` | `button[data-variant="primary"]` |

---

## The Bridge Pattern

```
HTML:   <element data-state="value">     → Declares state/config
CSS:    [data-state="value"] { }         → Styles based on state
JS:     element.dataset.state = "new"    → Updates state (if needed)
```

This separation means:
- HTML declares what the element **is**
- CSS defines how states **look**
- JavaScript only changes **data attributes**, not classes

---

## Categories of Data Attributes

### 1. State Attributes

Track the current state of an element:

```html
<!-- Expanded/collapsed -->
<nav data-expanded="false">...</nav>

<!-- Loading states -->
<button data-state="idle">Submit</button>
<button data-state="loading">Submitting...</button>
<button data-state="success">Sent!</button>
<button data-state="error">Failed</button>

<!-- Form validation -->
<form-field data-valid>...</form-field>
<form-field data-invalid>...</form-field>

<!-- Visibility -->
<modal-dialog data-open>...</modal-dialog>
```

### 2. Variant Attributes

Define visual or behavioral variants:

```html
<!-- Type/category -->
<status-badge data-type="success">Active</status-badge>
<status-badge data-type="warning">Pending</status-badge>
<status-badge data-type="error">Failed</status-badge>

<!-- Topic/tag styling -->
<tag-topic data-topic="css">CSS</tag-topic>
<tag-topic data-topic="html">HTML</tag-topic>
<tag-topic data-topic="a11y">Accessibility</tag-topic>

<!-- Size variants -->
<user-avatar data-size="small" src="..." alt="..."/>
<user-avatar data-size="medium" src="..." alt="..."/>
<user-avatar data-size="large" src="..." alt="..."/>
```

### 3. Configuration Attributes

Configure component behavior or layout:

```html
<!-- Grid configuration -->
<gallery-grid data-columns="3" data-gap="md">...</gallery-grid>

<!-- Animation settings -->
<carousel data-autoplay data-interval="5000">...</carousel>

<!-- Sort/filter settings -->
<data-table data-sortable data-sort-column="date">...</data-table>

<!-- Menu orientation -->
<nav-menu data-orientation="horizontal">...</nav-menu>
<nav-menu data-orientation="vertical">...</nav-menu>
```

---

## CSS Selectors for Data Attributes

### Attribute Presence (Boolean)

```css
/* Element has data-featured (any value or no value) */
article[data-featured] {
  border-left: 4px solid var(--primary-color);
}

/* Element has data-required */
form-field[data-required] label::after {
  content: " *";
  color: var(--error-color);
}
```

### Exact Value Match

```css
/* Exact match */
nav[data-expanded="true"] {
  max-height: 500px;
}

nav[data-expanded="false"] {
  max-height: 0;
  overflow: hidden;
}
```

### Multiple Values

```css
/* Different states */
button[data-state="loading"] {
  opacity: 0.6;
  pointer-events: none;
}

button[data-state="success"] {
  background-color: var(--success-color);
}

button[data-state="error"] {
  background-color: var(--error-color);
}
```

### Partial Match Selectors

```css
/* Contains (anywhere in value) */
[data-tags*="featured"] { }

/* Starts with */
[data-category^="blog"] { }

/* Ends with */
[data-file$=".pdf"] { }

/* Space-separated word */
[data-tags~="important"] { }
```

---

## Common Patterns

### Expandable Navigation

```html
<header>
  <input type="checkbox" id="nav-toggle" hidden/>
  <label for="nav-toggle" data-nav-trigger>Menu</label>
  <nav data-mobile-nav>
    <ul>...</ul>
  </nav>
</header>
```

```css
nav[data-mobile-nav] {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease;
}

#nav-toggle:checked ~ nav[data-mobile-nav] {
  max-height: 500px;
}
```

### Theme Variants

```html
<article data-theme="light">...</article>
<article data-theme="dark">...</article>
```

```css
article[data-theme="light"] {
  --bg: white;
  --text: #1f2937;
}

article[data-theme="dark"] {
  --bg: #1f2937;
  --text: white;
}
```

### Loading Button

```html
<button type="submit" data-state="idle">
  <span data-label>Submit</span>
  <span data-loader hidden>Loading...</span>
</button>
```

```css
button[data-state="loading"] {
  pointer-events: none;
  opacity: 0.7;

  & [data-label] { display: none; }
  & [data-loader] { display: inline; }
}
```

### Tag/Topic Styling

```html
<tag-list>
  <tag-topic data-topic="css">CSS</tag-topic>
  <tag-topic data-topic="html">HTML</tag-topic>
  <tag-topic data-topic="js">JavaScript</tag-topic>
  <tag-topic data-topic="a11y">Accessibility</tag-topic>
</tag-list>
```

```css
tag-topic {
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.875rem;
}

tag-topic[data-topic="css"] {
  background: #dbeafe;
  color: #1e40af;
}

tag-topic[data-topic="html"] {
  background: #fee2e2;
  color: #991b1b;
}

tag-topic[data-topic="js"] {
  background: #fef3c7;
  color: #92400e;
}

tag-topic[data-topic="a11y"] {
  background: #d1fae5;
  color: #065f46;
}
```

### Grid Configuration

```html
<gallery-grid data-columns="2">...</gallery-grid>
<gallery-grid data-columns="3">...</gallery-grid>
<gallery-grid data-columns="4">...</gallery-grid>
```

```css
gallery-grid {
  display: grid;
  gap: var(--spacing-md);
}

gallery-grid[data-columns="2"] {
  grid-template-columns: repeat(2, 1fr);
}

gallery-grid[data-columns="3"] {
  grid-template-columns: repeat(3, 1fr);
}

gallery-grid[data-columns="4"] {
  grid-template-columns: repeat(4, 1fr);
}
```

---

## JavaScript Integration

When JavaScript is needed, use the `dataset` API:

### Reading Data Attributes

```javascript
const nav = document.querySelector('nav');

// Read attribute
const isExpanded = nav.dataset.expanded === 'true';

// Check presence (boolean attributes)
const isFeatured = nav.hasAttribute('data-featured');
```

### Setting Data Attributes

```javascript
// Set value
nav.dataset.expanded = 'true';

// Toggle boolean
if (nav.hasAttribute('data-featured')) {
  nav.removeAttribute('data-featured');
} else {
  nav.setAttribute('data-featured', '');
}

// State machine pattern
button.dataset.state = 'loading';
// After async operation
button.dataset.state = 'success';
```

### Event Delegation

```javascript
document.addEventListener('click', (event) => {
  const trigger = event.target.closest('[data-action]');
  if (!trigger) return;

  const action = trigger.dataset.action;
  // Handle action
});
```

---

## Validation in elements.json

Define allowed data attributes and their values:

```json
{
  "status-badge": {
    "flow": true,
    "phrasing": true,
    "permittedContent": ["@phrasing"],
    "attributes": {
      "data-type": {
        "required": false,
        "enum": ["success", "warning", "error", "info"]
      }
    }
  },
  "gallery-grid": {
    "flow": true,
    "permittedContent": ["@flow"],
    "attributes": {
      "data-columns": {
        "required": false,
        "enum": ["2", "3", "4"]
      },
      "data-gap": {
        "required": false,
        "enum": ["sm", "md", "lg"]
      }
    }
  }
}
```

---

## Naming Conventions

### State Attributes

| Pattern | Examples |
|---------|----------|
| `data-state` | `data-state="loading"`, `data-state="error"` |
| `data-{adjective}` | `data-expanded`, `data-selected`, `data-active` |
| Boolean presence | `data-featured`, `data-disabled`, `data-required` |

### Variant Attributes

| Pattern | Examples |
|---------|----------|
| `data-type` | `data-type="success"`, `data-type="warning"` |
| `data-variant` | `data-variant="primary"`, `data-variant="outline"` |
| `data-{category}` | `data-topic="css"`, `data-size="large"` |

### Configuration Attributes

| Pattern | Examples |
|---------|----------|
| `data-{property}` | `data-columns="3"`, `data-gap="md"` |
| `data-{setting}` | `data-autoplay`, `data-loop` |

---

## Checklist

When using data attributes:

- [ ] Use `data-*` for state, not classes
- [ ] Use boolean attributes (presence/absence) for true/false states
- [ ] Use value attributes for multiple states or variants
- [ ] Define allowed values in `elements.json` where possible
- [ ] Use consistent naming patterns across the project
- [ ] Prefer `data-state` for multi-state components
- [ ] Use `dataset` API in JavaScript, not `getAttribute`
- [ ] Document attribute purposes in component skills

## Related Skills

- **custom-elements** - Define and use custom HTML elements
- **javascript-author** - Write vanilla JavaScript for Web Components with function...
- **css-author** - Modern CSS organization with native @import, @layer casca...
- **progressive-enhancement** - HTML-first development with CSS-only interactivity patterns
