---
name: css-author
description: Modern CSS organization with native @import, @layer cascade control, CSS nesting, design tokens, and element-focused selectors. AUTO-INVOKED when editing .css files.
allowed-tools: Read, Write, Edit
---

# CSS Author Skill

This skill provides patterns for organizing CSS in modern, maintainable ways **without build tools**. We leverage native CSS features: `@import` for modularization, `@layer` for cascade control, and nesting for readability.

## Philosophy

CSS should be:
1. **Native** - No preprocessors or build steps required
2. **Modular** - Organized by scope and purpose
3. **Predictable** - Cascade layers eliminate specificity wars
4. **Semantic** - Target elements, not class soup

---

## File Organization Hierarchy

```
styles/
├── main.css                 # Entry point - imports everything
├── _reset.css               # CSS reset/normalize
├── _tokens.css              # Design tokens (custom properties)
├── _layout.css              # Site-wide layout (grid, body structure)
├── _components.css          # Shared components (buttons, cards)
├── sections/
│   ├── _header.css          # Site header/nav
│   ├── _footer.css          # Site footer
│   └── _sidebar.css         # Sidebar patterns
├── pages/
│   ├── _home.css            # Homepage-specific styles
│   ├── _blog.css            # Blog listing/post styles
│   └── _contact.css         # Contact page styles
└── components/
    ├── _gallery.css         # Gallery grid component
    ├── _tag-list.css        # Tag component styles
    └── _data-table.css      # Table wrapper styles
```

### Naming Convention

- **Underscore prefix** (`_reset.css`): Partial files, imported by main.css
- **No prefix** (`main.css`): Entry point, linked in HTML
- **Lowercase with hyphens**: `_tag-list.css`, `_data-table.css`

---

## The Entry Point (`main.css`)

The main stylesheet declares layers and imports partials:

```css
/* Layer declaration - controls cascade order */
@layer reset, tokens, layout, sections, components, pages, responsive;

/* Reset (lowest priority) */
@import "_reset.css" layer(reset);

/* Design system tokens */
@import "_tokens.css" layer(tokens);

/* Site-wide layout */
@import "_layout.css" layer(layout);

/* Recurring sections */
@import "sections/_header.css" layer(sections);
@import "sections/_footer.css" layer(sections);
@import "sections/_sidebar.css" layer(sections);

/* Shared components */
@import "_components.css" layer(components);
@import "components/_gallery.css" layer(components);
@import "components/_tag-list.css" layer(components);
@import "components/_data-table.css" layer(components);

/* Page-specific styles */
@import "pages/_home.css" layer(pages);
@import "pages/_blog.css" layer(pages);
@import "pages/_contact.css" layer(pages);

/* Responsive overrides (highest priority) */
@layer responsive {
  @media (max-width: 768px) {
    /* Mobile overrides */
  }
}
```

---

## Design Tokens System

Design tokens are CSS custom properties that provide consistent, themeable values across your design system.

### Why Design Tokens?

Design tokens provide:
1. **Consistency** - Same values used everywhere
2. **Maintainability** - Change once, apply everywhere
3. **Theming** - Swap token values for different themes
4. **Documentation** - Token names describe purpose

### Token Categories

| Category | Purpose | Examples |
|----------|---------|----------|
| Colors | Brand, semantic, surface colors | `--primary`, `--error` |
| Spacing | Consistent gaps and padding | `--spacing-sm`, `--spacing-lg` |
| Typography | Font sizes, weights, heights | `--font-size-lg`, `--line-height-normal` |
| Effects | Shadows, transitions, borders | `--shadow-md`, `--transition-normal` |
| Layout | Widths, breakpoints | `--content-width`, `--sidebar-width` |

### Modern Color Formats

**Use OKLCH instead of hex/RGB.** OKLCH provides:
- Perceptually uniform lightness (consistent perceived brightness)
- Wider color gamut than sRGB
- Better color interpolation in gradients
- Easier programmatic color generation

| Format | Use Case | Example |
|--------|----------|---------|
| `oklch()` | Primary format for all colors | `oklch(55% 0.22 260)` |
| `light-dark()` | Theme-aware tokens | `light-dark(oklch(20% 0 0), oklch(95% 0 0))` |
| `color-mix()` | Blending, opacity | `color-mix(in oklch, var(--primary), transparent 50%)` |
| Relative colors | Variations from base | `oklch(from var(--primary) calc(l + 0.2) c h)` |

#### OKLCH Syntax

```css
/* oklch(lightness chroma hue) */
--primary: oklch(55% 0.22 260);  /* Blue */
--success: oklch(65% 0.2 145);   /* Green */
--warning: oklch(75% 0.18 85);   /* Orange */
--error: oklch(55% 0.22 25);     /* Red */
```

- **Lightness**: 0% (black) to 100% (white)
- **Chroma**: 0 (gray) to ~0.4 (vivid) - varies by hue
- **Hue**: 0-360 degrees (0=pink, 90=yellow, 180=cyan, 270=blue)

#### Relative Colors (Derive Variations)

Generate color variations programmatically from a base color:

```css
:root {
  --primary: oklch(55% 0.22 260);

  /* Lighter: increase lightness */
  --primary-light: oklch(from var(--primary) calc(l + 0.2) c h);

  /* Darker: decrease lightness */
  --primary-dark: oklch(from var(--primary) calc(l - 0.15) c h);

  /* Muted: reduce chroma */
  --primary-muted: oklch(from var(--primary) l calc(c - 0.1) h);

  /* Hover: slightly darker and more saturated */
  --primary-hover: oklch(from var(--primary) calc(l - 0.08) calc(c + 0.02) h);
}
```

#### Theme-Aware Colors with `light-dark()`

Single declarations for both light and dark themes:

```css
:root {
  color-scheme: light dark;  /* Required for light-dark() */

  /* Single token handles both themes */
  --text: light-dark(oklch(20% 0 0), oklch(95% 0 0));
  --surface: light-dark(oklch(100% 0 0), oklch(15% 0.02 260));
  --border: light-dark(oklch(90% 0.01 260), oklch(30% 0.02 260));
}
```

#### Color Mixing for Opacity/Blending

```css
/* Semi-transparent overlays */
--overlay-light: color-mix(in oklch, black, transparent 95%);
--overlay-medium: color-mix(in oklch, black, transparent 90%);

/* Elevated surfaces */
--surface-elevated: color-mix(in oklch, var(--surface), white 5%);

/* Blend two colors */
--accent-blend: color-mix(in oklch, var(--primary), var(--secondary) 30%);
```

#### Gradients with Color Space

Specify color space to prevent muddy midtones:

```css
/* Vibrant gradient interpolation */
background: linear-gradient(in oklch, var(--primary), var(--secondary));

/* For hue transitions, use longer path */
background: linear-gradient(in oklch longer hue, oklch(65% 0.25 0), oklch(65% 0.25 360));
```

#### Browser Fallbacks

For older browsers, provide hex fallback first:

```css
:root {
  --primary: #2563eb;  /* Fallback for older browsers */
  --primary: oklch(55% 0.22 260);
}
```

#### Automatic Contrast with `contrast-color()`

The `contrast-color()` function automatically selects black or white text based on background:

```css
/* Button with any background color */
button {
  background: var(--primary);
  color: contrast-color(var(--primary));
}

/* Dynamic accent backgrounds */
[data-accent] {
  background: var(--accent);
  color: contrast-color(var(--accent));
}
```

**Combining with `light-dark()`:**

```css
.badge {
  --bg: light-dark(var(--primary-light), var(--primary-dark));
  background: var(--bg);
  color: contrast-color(var(--bg));
}
```

**Limitations:**
- Returns only black (`#000`) or white (`#fff`)
- Uses WCAG 2 algorithm (may not be perceptually optimal for mid-tones)
- **Browser support:** Safari Technology Preview only (use as progressive enhancement)
- Does not guarantee WCAG compliance—verify contrast ratios for critical UI

**Best practice:** Use `contrast-color()` for dynamic/user-selected colors. For design system colors, manually define text colors to ensure optimal readability.

### Complete Token System

```css
/* _tokens.css */
@layer tokens {
  :root {
    /* Enable light-dark() function */
    color-scheme: light dark;

    /* ==================== COLORS (OKLCH) ==================== */

    /* Hue palette - define once, reuse everywhere */
    --hue-primary: 260;   /* Blue */
    --hue-secondary: 250; /* Slate */
    --hue-success: 145;   /* Green */
    --hue-warning: 85;    /* Orange */
    --hue-error: 25;      /* Red */
    --hue-info: 200;      /* Cyan */

    /* Brand colors with relative variations */
    --primary: oklch(55% 0.22 var(--hue-primary));
    --primary-hover: oklch(from var(--primary) calc(l - 0.08) calc(c + 0.02) h);
    --primary-light: oklch(from var(--primary) calc(l + 0.35) calc(c - 0.12) h);
    --secondary: oklch(50% 0.03 var(--hue-secondary));
    --secondary-hover: oklch(from var(--secondary) calc(l - 0.1) c h);

    /* Semantic colors */
    --success: oklch(60% 0.18 var(--hue-success));
    --success-light: oklch(from var(--success) calc(l + 0.32) calc(c - 0.1) h);
    --warning: oklch(75% 0.16 var(--hue-warning));
    --warning-light: oklch(from var(--warning) calc(l + 0.2) calc(c - 0.08) h);
    --error: oklch(55% 0.2 var(--hue-error));
    --error-light: oklch(from var(--error) calc(l + 0.38) calc(c - 0.12) h);
    --info: oklch(55% 0.14 var(--hue-info));
    --info-light: oklch(from var(--info) calc(l + 0.38) calc(c - 0.08) h);

    /* Theme-aware surface colors */
    --background: light-dark(oklch(100% 0 0), oklch(12% 0.02 var(--hue-primary)));
    --background-alt: light-dark(oklch(98% 0.005 var(--hue-primary)), oklch(16% 0.02 var(--hue-primary)));
    --surface: light-dark(oklch(100% 0 0), oklch(16% 0.02 var(--hue-primary)));
    --surface-elevated: light-dark(oklch(100% 0 0), oklch(22% 0.02 var(--hue-primary)));

    /* Theme-aware text colors */
    --text: light-dark(oklch(20% 0.02 var(--hue-primary)), oklch(96% 0.01 var(--hue-primary)));
    --text-muted: light-dark(oklch(45% 0.02 var(--hue-primary)), oklch(65% 0.02 var(--hue-primary)));
    --text-inverted: light-dark(oklch(100% 0 0), oklch(10% 0 0));

    /* Theme-aware border colors */
    --border: light-dark(oklch(90% 0.01 var(--hue-primary)), oklch(28% 0.02 var(--hue-primary)));
    --border-strong: light-dark(oklch(82% 0.01 var(--hue-primary)), oklch(38% 0.02 var(--hue-primary)));

    /* Theme-aware overlays using color-mix */
    --overlay-light: light-dark(
      color-mix(in oklch, black, transparent 95%),
      color-mix(in oklch, white, transparent 95%)
    );
    --overlay-medium: light-dark(
      color-mix(in oklch, black, transparent 90%),
      color-mix(in oklch, white, transparent 90%)
    );
    --overlay-strong: light-dark(
      color-mix(in oklch, black, transparent 80%),
      color-mix(in oklch, white, transparent 80%)
    );

    /* ==================== SPACING ==================== */

    --spacing-xs: 0.25rem;   /* 4px */
    --spacing-sm: 0.5rem;    /* 8px */
    --spacing-md: 1rem;      /* 16px */
    --spacing-lg: 1.5rem;    /* 24px */
    --spacing-xl: 2rem;      /* 32px */
    --spacing-2xl: 3rem;     /* 48px */
    --spacing-3xl: 4rem;     /* 64px */

    /* ==================== TYPOGRAPHY ==================== */

    /* Font families */
    --font-sans: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    --font-mono: ui-monospace, "Cascadia Code", "Source Code Pro", Menlo, monospace;
    --font-serif: Georgia, Cambria, "Times New Roman", Times, serif;

    /* Font sizes */
    --font-size-xs: 0.75rem;   /* 12px */
    --font-size-sm: 0.875rem;  /* 14px */
    --font-size-base: 1rem;    /* 16px */
    --font-size-lg: 1.125rem;  /* 18px */
    --font-size-xl: 1.25rem;   /* 20px */
    --font-size-2xl: 1.5rem;   /* 24px */
    --font-size-3xl: 1.875rem; /* 30px */
    --font-size-4xl: 2.25rem;  /* 36px */

    /* Font weights */
    --font-weight-normal: 400;
    --font-weight-medium: 500;
    --font-weight-semibold: 600;
    --font-weight-bold: 700;

    /* Line heights */
    --line-height-tight: 1.25;
    --line-height-normal: 1.5;
    --line-height-relaxed: 1.625;

    /* ==================== EFFECTS ==================== */

    /* Shadows */
    --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
    --shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.1);

    /* Transitions */
    --transition-fast: 0.15s ease;
    --transition-normal: 0.3s ease;
    --transition-slow: 0.5s ease;

    /* Border radius */
    --radius-sm: 0.25rem;
    --radius-md: 0.375rem;
    --radius-lg: 0.5rem;
    --radius-xl: 0.75rem;
    --radius-full: 9999px;

    /* ==================== LAYOUT ==================== */

    --content-width: 65ch;
    --content-width-wide: 80rem;
    --sidebar-width: 16rem;

    /* Z-index scale */
    --z-dropdown: 100;
    --z-sticky: 200;
    --z-modal: 300;
    --z-tooltip: 400;
  }
}
```

### Dark Theme Approach

**Recommended: Use `light-dark()` in the Complete Token System above.** This eliminates the need for duplicate token definitions.

#### User-Controlled Theme Toggle (Legacy Pattern)

For sites with theme toggle UI that override system preference, use CSS `:has()` to scope token overrides:

```css
/* Force dark mode when user selects dark */
:root:has(#theme-dark:checked) {
  color-scheme: dark;  /* Triggers light-dark() to use dark values */
}

/* Force light mode when user selects light */
:root:has(#theme-light:checked) {
  color-scheme: light;  /* Triggers light-dark() to use light values */
}

/* Auto follows system preference (default behavior) */
:root:has(#theme-auto:checked) {
  color-scheme: light dark;
}
```

### Component-Specific Tokens

```css
:root {
  /* Form tokens */
  --form-border: var(--border);
  --form-focus: var(--primary);
  --form-invalid: var(--error);
  --form-input-padding: var(--spacing-sm) var(--spacing-md);
  --form-input-radius: var(--radius-md);

  /* Button tokens */
  --button-padding: var(--spacing-sm) var(--spacing-lg);
  --button-radius: var(--radius-md);
  --button-primary-bg: var(--primary);
  --button-primary-text: var(--text-inverted);

  /* Card tokens */
  --card-padding: var(--spacing-lg);
  --card-radius: var(--radius-lg);
  --card-shadow: var(--shadow-sm);
  --card-bg: var(--surface);
}
```

### Token Naming Guidelines

| Pattern | Example | Purpose |
|---------|---------|---------|
| `--{category}` | `--primary`, `--error` | Base tokens (no `-color` suffix) |
| `--{category}-{variant}` | `--primary-hover`, `--success-light` | Token variations |
| `--{element}-{modifier}` | `--text-muted`, `--border-strong` | Semantic element tokens |

**Use semantic names, not literal values:**

| Avoid | Prefer |
|-------|--------|
| `--blue`, `--primary-color` | `--primary` |
| `--red`, `--error-color` | `--error` |
| `--16px` | `--spacing-md` |
| `#2563eb` (hex in code) | `var(--primary)` |

---

## CSS Layers (`@layer`)

### Why Layers?

Layers provide **explicit cascade control** regardless of selector specificity:

```css
@layer base, theme, utilities;

@layer utilities {
  .hidden { display: none !important; }
}

@layer base {
  button { display: inline-block; }
}

/* utilities wins over base, even with lower specificity */
```

### Recommended Layer Order

| Layer | Priority | Purpose |
|-------|----------|---------|
| `reset` | Lowest | Normalize browser defaults |
| `tokens` | Low | CSS custom properties |
| `layout` | Medium-Low | Body grid, main structure |
| `sections` | Medium | Header, footer, sidebar |
| `components` | Medium-High | Buttons, cards, form elements |
| `pages` | High | Page-specific overrides |
| `responsive` | Highest | Media query adjustments |

### Layer Benefits

1. **No specificity wars** - Later layers always win
2. **Predictable overrides** - Page styles override components
3. **Safe imports** - Third-party CSS can be isolated
4. **Clear organization** - Find styles by layer purpose

---

## Custom Element Display Behavior

Custom elements (hyphenated tags like `<product-card>`) have specific display quirks that require understanding.

### Browser Default: Inline

Browsers treat unknown elements as `display: inline`, breaking block-level layouts:

```html
<!-- Renders INLINE by default! -->
<product-card>
  <img src="product.jpg" alt="..." />
  <h3>Product Name</h3>
</product-card>
```

This causes layout issues because the element doesn't create a block formatting context.

### The `:not(:defined)` Solution

The `:not(:defined)` pseudo-class matches custom elements that haven't been registered with `customElements.define()`:

```css
/* In reset layer - catches ALL unregistered custom elements */
:not(:defined) {
  display: block;
}
```

This is ideal for CSS-only custom elements that will never be registered as Web Components.

### Layer Specificity Warning

**Critical:** Unlayered browser defaults beat layered CSS. Even with `@layer reset { ... }`, browser defaults can override your styles.

```css
/* May NOT work - layer has lower priority than browser default */
@layer reset {
  product-card {
    display: block;
  }
}

/* Solution: :not(:defined) has higher specificity */
:not(:defined) {
  display: block;
}
```

### The `:defined` Pseudo-Class

For registered Web Components, use `:defined` to style after JavaScript loads:

```css
/* Hide until component is defined */
product-card:not(:defined) {
  visibility: hidden;
}

/* Show when registered */
product-card:defined {
  visibility: visible;
}
```

### Block vs Inline Custom Elements

Not all custom elements should be block. Consider the content model:

| Element Type | Display | Examples |
|--------------|---------|----------|
| Container/Section | `block` | `product-card`, `hero-section`, `card-grid` |
| Badge/Indicator | `inline-flex` | `status-badge`, `tag-item` |
| Icon | `inline-flex` | `x-icon` |

Elements with `phrasing: true` in `elements.json` are designed to be inline.

---

## List Styling Patterns

Styling lists reliably requires understanding browser defaults and specificity.

### Removing Default Bullets

The most reliable pattern for navigation and card lists:

```css
/* In reset layer */
ul, ol {
  list-style: none;
  padding: 0;
  margin: 0;
}
```

**Warning:** `list-style-type: none` alone may not work in all contexts. Use the shorthand `list-style: none` for reliability.

### Accessibility Note

When you remove bullets from a list, screen readers may not announce it as a list in Safari/VoiceOver. Add `role="list"` to preserve semantics:

```html
<ul role="list">
  <li>Item with no bullet but announced as list</li>
</ul>
```

### Custom Markers with ::marker

For custom bullets, use the `::marker` pseudo-element:

```css
li::marker {
  color: var(--primary);
  content: "→ ";
}

/* For specific lists */
ul[data-style="checkmarks"] li::marker {
  content: "✓ ";
  color: var(--success);
}
```

### Numbered Lists with Custom Styling

```css
ol {
  counter-reset: list-counter;
  list-style: none;
}

ol li {
  counter-increment: list-counter;
}

ol li::before {
  content: counter(list-counter) ". ";
  color: var(--primary);
  font-weight: var(--font-weight-semibold);
}
```

### When to Use Each Pattern

| Pattern | Use Case |
|---------|----------|
| `list-style: none` | Navigation, card grids, tab lists |
| `::marker` | Prose lists with custom bullet style |
| `counter()` | Numbered steps, ordered lists with custom numbers |

---

## CSS Scope (`@scope`)

The `@scope` at-rule limits selector reach to a specific DOM subtree without increasing specificity. While `@layer` controls cascade order, `@scope` controls where selectors can match.

### Why `@scope`?

| Without @scope | With @scope |
|----------------|-------------|
| Selectors leak globally | Selectors limited to subtree |
| Need long descendant chains | Short selectors, explicit boundaries |
| High specificity for isolation | Low specificity preserved |

### Basic Syntax

```css
@scope (product-card) {
  /* These only match inside <product-card> */
  img {
    border-radius: var(--radius-md);
  }

  h3 {
    font-size: var(--font-size-lg);
  }
}
```

The scoping root (`product-card`) doesn't add to selector specificity—`img` remains `(0,0,1)`.

### The `:scope` Pseudo-Class

Reference the scoping root itself:

```css
@scope (blog-card) {
  :scope {
    /* Styles the <blog-card> element */
    display: grid;
    gap: var(--spacing-md);
  }

  h3 {
    /* Styles <h3> inside <blog-card> */
    margin: 0;
  }
}
```

### Donut Scope Pattern

Exclude nested sections with a lower boundary using `to`:

```css
/* Style card chrome, but not user content inside */
@scope (blog-card) to (.card-content) {
  img {
    /* Only matches images in card header/footer, not in content */
    border: 2px solid var(--border);
  }
}
```

Use cases for donut scope:
- Style component wrapper but not slotted content
- Style card header/footer but not body
- Apply theme to shell but let content inherit differently

### `@scope` with `@layer`

Combine scope and layers for full control:

```css
@layer components {
  @scope (product-card) {
    :scope {
      container-type: inline-size;
      padding: var(--spacing-lg);
    }

    img {
      width: 100%;
      aspect-ratio: 4/3;
      object-fit: cover;
    }

    @container (min-width: 400px) {
      :scope {
        display: grid;
        grid-template-columns: 200px 1fr;
      }
    }
  }
}
```

### `@scope` vs Element Selectors

Both work for our custom element approach:

```css
/* Element selector (our typical pattern) */
product-card {
  display: grid;
}

product-card img {
  border-radius: var(--radius-md);
}

/* @scope equivalent - cleaner for many child rules */
@scope (product-card) {
  :scope {
    display: grid;
  }

  img {
    border-radius: var(--radius-md);
  }

  h3 { }
  p { }
  footer { }
}
```

**When to use `@scope`:**
- Component has many child element rules
- Need donut scope to exclude nested content
- Want to group all component styles in one block

**When element selectors suffice:**
- Simple components with few rules
- Already using nesting effectively

### Prelude-less Scope (Inline Styles)

In component HTML, scope without a selector:

```html
<product-card>
  <style>
    @scope {
      :scope { display: grid; }
      img { border-radius: var(--radius-md); }
    }
  </style>
  <img src="..." alt="..." />
  <h3>Product Name</h3>
</product-card>
```

The scope automatically targets the parent element.

### Important Limitation

`@scope` limits selector reach, **not inheritance**. Inherited properties like `color` still cascade into excluded donut holes:

```css
@scope (.card) to (.content) {
  :scope {
    color: blue;  /* .content still inherits blue! */
  }
}
```

To prevent inheritance, reset properties explicitly on the excluded element.

### Browser Support

- Chrome 118+, Edge 118+, Safari 17.4+, Firefox 146+
- Wide support (90%+) - safe to use without fallbacks

---

## Native CSS Nesting

Modern browsers support CSS nesting, reducing repetition:

```css
/* Without nesting */
nav { }
nav ul { }
nav a { }
nav a:hover { }

/* With nesting */
nav {
  & ul {
    display: flex;
    gap: var(--spacing-lg);
  }

  & a {
    padding: var(--spacing-sm) var(--spacing-md);

    &:hover {
      background: var(--overlay-light);
    }

    &[aria-current="page"] {
      background: var(--overlay-strong);
    }
  }
}
```

### Nesting Rules

1. **Use `&` for clarity** - Always prefix nested selectors with `&`
2. **Limit depth** - No more than 3-4 levels deep
3. **Keep related styles together** - Element and its states
4. **Avoid over-nesting** - If selectors get complex, flatten

### Nesting with Media Queries

Media queries can be nested inside selectors:

```css
header {
  padding: var(--spacing-lg);

  @media (max-width: 768px) {
    padding: var(--spacing-md);
  }
}
```

---

## Element-Focused CSS (Classless)

### Target Semantic HTML

Instead of inventing classes, style semantic elements:

```css
/* Avoid */
.header-nav { }
.nav-list { }
.nav-link { }

/* Prefer */
header nav { }
header nav ul { }
header nav a { }
```

### Custom Elements as Styling Hooks

Custom elements provide semantic styling targets without classes:

```css
/* Instead of .form-group { } */
form-field { }

/* Instead of .product-card { } */
product-card { }

/* Instead of .table-wrapper { } */
table-wrapper { }
```

### When Classes Are Appropriate

Use classes sparingly for:

| Use Case | Example |
|----------|---------|
| Multi-variant components | `.card`, `.card-featured` |
| View transition names | `.vt-card-1` (when data-* insufficient) |
| Third-party integration | Classes required by libraries |

**Never use classes for state.** Use `data-*` attributes instead.

---

## Scope Hierarchy

| Level | Scope | Contents |
|-------|-------|----------|
| **Tokens** | Entire site | Colors, spacing, typography, effects |
| **Layout** | Body structure | Grid areas, view transitions, body rules |
| **Sections** | Recurring site parts | Header, footer, sidebar, navigation |
| **Components** | Reusable blocks | Cards, buttons, forms, tables, tags |
| **Pages** | Single page types | Homepage hero, blog post, contact form |

### When to Create a New File

| Scenario | Action |
|----------|--------|
| New custom element | Create `components/_element-name.css` |
| New page type with unique styles | Create `pages/_page-name.css` |
| New recurring section | Create `sections/_section-name.css` |
| New design token category | Extend `_tokens.css` |

---

## Adding a New CSS File

### 1. Create the Partial

```css
/* components/_gallery.css */
@layer components {
  gallery-grid {
    display: grid;
    gap: var(--spacing-md);

    &[data-columns="2"] { grid-template-columns: repeat(2, 1fr); }
    &[data-columns="3"] { grid-template-columns: repeat(3, 1fr); }
    &[data-columns="4"] { grid-template-columns: repeat(4, 1fr); }
  }
}
```

### 2. Add Import to main.css

```css
/* In main.css, add to appropriate section */
@import "components/_gallery.css" layer(components);
```

### 3. File Template

Every partial should follow this structure:

```css
/* components/_example.css */
@layer components {
  /* Element styles */
  example-element {
    /* Base styles */

    /* State variants via data attributes */
    &[data-state="active"] { }

    /* Nested elements */
    & .inner { }

    /* Responsive adjustments */
    @media (max-width: 768px) { }
  }
}
```

---

## CSS Import Performance

### Browser Behavior

Modern browsers handle `@import` efficiently:
- Parallel fetching when imports are at the start
- Caching of individual files
- No render-blocking beyond the cascade order

### Best Practices

1. **All imports at the top** - Before any other CSS
2. **Layer declaration first** - `@layer` before `@import`
3. **Use HTTP/2** - Multiplexing handles multiple files well
4. **Consider concatenation** for production if needed

### When to Consolidate

For very high-traffic sites, you may want to concatenate CSS:

```bash
# Simple concatenation for production
cat styles/_reset.css styles/_tokens.css styles/_layout.css > styles/bundle.css
```

But for most projects, native imports work well.

---

## Responsive Design Pattern

### Mobile-First vs Desktop-First

We use **desktop-first** with `max-width` queries, grouped in the `responsive` layer:

```css
@layer responsive {
  @media (max-width: 1024px) {
    /* Tablet adjustments */
  }

  @media (max-width: 768px) {
    /* Mobile adjustments */
  }

  @media (max-width: 480px) {
    /* Small mobile adjustments */
  }
}
```

### Breakpoint Tokens

Define breakpoints as documentation (CSS can't use variables in media queries):

```css
/* _tokens.css */
:root {
  /* Breakpoints (for reference - use literal values in @media) */
  /* --breakpoint-xl: 1280px; */
  /* --breakpoint-lg: 1024px; */
  /* --breakpoint-md: 768px; */
  /* --breakpoint-sm: 480px; */
}
```

---

## Container Queries (`@container`)

Container queries enable **component-scoped responsive design**. Unlike media queries (which respond to viewport size), container queries respond to the size of a parent container.

### Why Container Queries?

| Media Queries | Container Queries |
|---------------|-------------------|
| Respond to viewport | Respond to container |
| Global breakpoints | Component-specific |
| Same component, same layout everywhere | Same component adapts to context |

**Use case:** A card component that displays horizontally in a wide sidebar but stacks vertically in a narrow sidebar—without knowing where it's placed.

### Defining a Container

Use `container-type` to establish a containment context:

```css
/* Any element can be a container */
sidebar-panel {
  container-type: inline-size;  /* Width-based queries */
  container-name: sidebar;      /* Optional: name for targeting */
}

/* Shorthand */
main-content {
  container: content / inline-size;  /* name / type */
}
```

#### Container Types

| Type | Queries On | Use When |
|------|-----------|----------|
| `inline-size` | Width only | Most common - responsive layouts |
| `size` | Width and height | Rare - when height matters |
| `normal` | No size queries | Style queries only |

**Recommendation:** Use `inline-size` for 99% of cases.

### Writing Container Queries

```css
/* Query any ancestor container */
@container (min-width: 400px) {
  blog-card {
    display: grid;
    grid-template-columns: 200px 1fr;
  }
}

/* Query a specific named container */
@container sidebar (max-width: 300px) {
  blog-card {
    flex-direction: column;
  }
}
```

### Container Query Units

Container-relative units for truly fluid components:

| Unit | Meaning |
|------|---------|
| `cqw` | 1% of container width |
| `cqh` | 1% of container height |
| `cqi` | 1% of container inline size |
| `cqb` | 1% of container block size |
| `cqmin` | Smaller of `cqi` or `cqb` |
| `cqmax` | Larger of `cqi` or `cqb` |

#### Fluid Typography with Container Units

```css
blog-card h3 {
  /* Font scales with container width, respects user zoom */
  font-size: clamp(1rem, 0.875rem + 0.5cqi, 1.5rem);
}
```

#### Rhythm-Aligned Spacing

Combine container units with `lh` (line-height) units for vertical rhythm:

```css
blog-card {
  /* Gap scales with container but rounds to quarter-line increments */
  --gap: round(up, 2cqi, 0.25lh);
  gap: var(--gap);
}
```

The `round()` function ensures spacing aligns to the typographic grid.

#### Important Limitation

**Container units cannot measure the element they're applied to.** This would create a circular dependency. Use nested elements or wrapper patterns:

```css
/* WRONG - card can't size based on its own container */
product-card {
  container-type: inline-size;
  padding: 2cqi;  /* Measures parent, not self! */
}

/* CORRECT - children measure the card container */
product-card {
  container-type: inline-size;
}

product-card > * {
  padding: 2cqi;  /* Now measures product-card */
}
```

### Container Queries with Layers

Container queries integrate naturally with the layer system:

```css
@layer components {
  /* Define containers at the component wrapper level */
  card-container {
    container-type: inline-size;
  }

  /* Base card styles */
  blog-card {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-md);
  }

  /* Container-responsive layout */
  @container (min-width: 500px) {
    blog-card {
      flex-direction: row;
    }

    blog-card img {
      width: 40%;
      flex-shrink: 0;
    }
  }
}
```

### Pattern: Self-Contained Responsive Components

Make components that adapt without external configuration:

```css
/* components/_product-card.css */
@layer components {
  product-card {
    /* The card IS its own container */
    container-type: inline-size;

    display: grid;
    gap: var(--spacing-md);
    padding: var(--spacing-lg);
  }

  /* Compact layout (narrow) */
  @container (max-width: 299px) {
    product-card {
      text-align: center;

      & img {
        margin-inline: auto;
        max-width: 150px;
      }
    }
  }

  /* Standard layout (medium) */
  @container (min-width: 300px) and (max-width: 499px) {
    product-card {
      grid-template-columns: 1fr;
    }
  }

  /* Wide layout (large) */
  @container (min-width: 500px) {
    product-card {
      grid-template-columns: 200px 1fr;
      grid-template-rows: auto 1fr auto;

      & img {
        grid-row: 1 / -1;
      }
    }
  }
}
```

### Container Queries vs Media Queries

Use both—they serve different purposes:

```css
@layer components {
  blog-card {
    container-type: inline-size;
  }

  /* Container query: responds to where card is placed */
  @container (min-width: 400px) {
    blog-card {
      grid-template-columns: 150px 1fr;
    }
  }
}

@layer responsive {
  /* Media query: global layout changes */
  @media (max-width: 768px) {
    .card-grid {
      grid-template-columns: 1fr;  /* Stack cards on mobile */
    }
  }
}
```

### Nesting Container Queries

Container queries can be nested inside element selectors:

```css
sidebar-panel {
  container-type: inline-size;

  & blog-card {
    padding: var(--spacing-md);

    @container (min-width: 350px) {
      padding: var(--spacing-lg);
      display: grid;
      grid-template-columns: 100px 1fr;
    }
  }
}
```

### Container Query Checklist

When implementing container queries:

- [ ] Set `container-type: inline-size` on the containing element
- [ ] Use `container-name` when multiple containers need targeting
- [ ] Prefer `min-width` for progressive enhancement
- [ ] Use container units (`cqi`, `cqw`) for fluid typography/spacing
- [ ] Apply container units to **children**, not the container element itself
- [ ] Use `round()` with `lh` units for rhythm-aligned spacing
- [ ] Keep container queries in the same layer as component styles
- [ ] Test components in various container widths

---

## CSS Subgrid

Subgrid allows nested elements to participate in their parent's grid, enabling alignment across nested structures without duplicating track definitions.

### Why Subgrid?

| Without Subgrid | With Subgrid |
|-----------------|--------------|
| Nested grids are independent | Child inherits parent's tracks |
| Must duplicate track sizes | Single source of truth |
| Alignment breaks across nesting | Perfect alignment across levels |

### Basic Subgrid Pattern

```css
/* Parent grid */
.card-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--spacing-lg);
}

/* Card spans parent columns, subgrids rows */
.card {
  display: grid;
  grid-template-rows: auto 1fr auto;  /* header, content, footer */
}

/* With subgrid: all cards align their internal rows */
.card-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: auto 1fr auto;  /* Define rows at parent level */
  gap: var(--spacing-lg);
}

.card {
  display: grid;
  grid-row: span 3;
  grid-template-rows: subgrid;  /* Inherit parent's row tracks */
}
```

### Subgrid for Form Alignment

Align labels and inputs across form fields:

```css
form {
  display: grid;
  grid-template-columns: max-content 1fr;
  gap: var(--spacing-md);
}

form-field {
  display: grid;
  grid-column: span 2;
  grid-template-columns: subgrid;
}

form-field label {
  grid-column: 1;
}

form-field input {
  grid-column: 2;
}
```

### Subgrid for Card Components

Cards with aligned headers, content, and footers:

```css
/* Define consistent structure at grid level */
product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  grid-auto-rows: auto 1fr auto;  /* image, details, actions */
  gap: var(--spacing-lg);
}

product-card {
  display: grid;
  grid-row: span 3;
  grid-template-rows: subgrid;
  gap: var(--spacing-md);
}

product-card img { grid-row: 1; }
product-card .details { grid-row: 2; }
product-card .actions { grid-row: 3; }
```

### Subgrid in Both Directions

Inherit both column and row tracks:

```css
.parent {
  display: grid;
  grid-template-columns: 1fr 2fr 1fr;
  grid-template-rows: auto 1fr auto;
}

.child {
  grid-column: 1 / -1;
  grid-row: 1 / -1;
  display: grid;
  grid-template-columns: subgrid;
  grid-template-rows: subgrid;
}
```

### Named Lines with Subgrid

Named lines pass through to subgrid:

```css
.layout {
  display: grid;
  grid-template-columns:
    [full-start] 1fr
    [content-start] minmax(0, 60ch)
    [content-end] 1fr
    [full-end];
}

.content {
  grid-column: full-start / full-end;
  display: grid;
  grid-template-columns: subgrid;
}

/* Child can use parent's named lines */
.content h1 {
  grid-column: content-start / content-end;
}

.content .full-bleed {
  grid-column: full-start / full-end;
}
```

### When to Use Subgrid

| Use Case | Benefit |
|----------|---------|
| Card grids | Aligned headers/footers across cards |
| Form layouts | Labels and inputs align vertically |
| Data tables | Column alignment in complex cells |
| Multi-level navigation | Consistent column widths |
| Article layouts | Full-bleed elements with named lines |

### Browser Support Note

Subgrid has good modern browser support (90%+). For older browsers, the fallback is a regular nested grid which may not align perfectly but remains functional.

---

## CSS Logical Properties

Logical properties replace physical direction properties (left, right, top, bottom) with **flow-relative** alternatives. This enables layouts that automatically adapt to different writing modes and text directions.

### Why Logical Properties?

| Physical Properties | Logical Properties |
|--------------------|-------------------|
| Fixed to screen edges | Adapt to text direction |
| Break in RTL languages | Work in any writing mode |
| Require RTL overrides | Automatically flip |
| `margin-left: 1rem` | `margin-inline-start: 1rem` |

**Benefits:**

- **Internationalization** - Layouts work in Arabic, Hebrew, and other RTL languages
- **Future-proof** - Vertical writing modes (CJK) work automatically
- **Consistency** - One codebase for all languages
- **Semantic** - Properties describe intent, not position

### The Logical Model

CSS logical properties use two axes:

| Axis | Direction | Physical Equivalent |
|------|-----------|---------------------|
| **Block** | Vertical (in LTR/RTL) | Top ↔ Bottom |
| **Inline** | Horizontal (in LTR/RTL) | Left ↔ Right |

Each axis has two edges:

| Edge | Block Axis | Inline Axis (LTR) | Inline Axis (RTL) |
|------|------------|-------------------|-------------------|
| **Start** | Top | Left | Right |
| **End** | Bottom | Right | Left |

### Property Mappings

#### Margins

| Physical | Logical |
|----------|---------|
| `margin-top` | `margin-block-start` |
| `margin-bottom` | `margin-block-end` |
| `margin-left` | `margin-inline-start` |
| `margin-right` | `margin-inline-end` |

**Shorthand properties:**

```css
/* Two values: start and end */
margin-block: 1rem 2rem;   /* top: 1rem, bottom: 2rem */
margin-inline: 1rem 2rem;  /* left: 1rem (LTR), right: 1rem (RTL) */

/* Single value: both start and end */
margin-block: 1rem;        /* top and bottom */
margin-inline: 1rem;       /* left and right */
```

#### Padding

Same pattern as margins:

```css
padding-block: var(--spacing-lg);
padding-inline: var(--spacing-md);

/* Individual sides */
padding-block-start: var(--spacing-lg);
padding-inline-end: var(--spacing-sm);
```

#### Sizing

| Physical | Logical |
|----------|---------|
| `width` | `inline-size` |
| `height` | `block-size` |
| `min-width` | `min-inline-size` |
| `max-height` | `max-block-size` |

```css
blog-card {
  inline-size: 100%;
  max-inline-size: 40rem;
  min-block-size: 200px;
}
```

#### Positioning

| Physical | Logical |
|----------|---------|
| `top` | `inset-block-start` |
| `bottom` | `inset-block-end` |
| `left` | `inset-inline-start` |
| `right` | `inset-inline-end` |

**Shorthand:**

```css
/* All four sides */
inset: 0;  /* Same as top: 0; right: 0; bottom: 0; left: 0; */

/* Block and inline axes */
inset-block: 0;   /* top and bottom */
inset-inline: 0;  /* left and right */
```

#### Borders

```css
/* Border on one logical side */
border-inline-start: 3px solid var(--primary);

/* Border radius */
border-start-start-radius: var(--radius-lg);  /* top-left in LTR */
border-end-start-radius: var(--radius-lg);    /* bottom-left in LTR */
```

#### Text Alignment

| Physical | Logical |
|----------|---------|
| `text-align: left` | `text-align: start` |
| `text-align: right` | `text-align: end` |

### Common Patterns

#### Centering with Logical Properties

```css
/* Center horizontally (works in RTL) */
blog-card {
  margin-inline: auto;
  max-inline-size: 40rem;
}
```

#### Icon + Text Spacing

```css
/* Space between icon and text, flips in RTL */
button svg {
  margin-inline-end: var(--spacing-sm);
}
```

#### Sidebar Layout

```css
/* Sidebar on the start edge (left in LTR, right in RTL) */
main-layout {
  display: grid;
  grid-template-columns: 250px 1fr;
}

sidebar-panel {
  border-inline-end: 1px solid var(--border);
  padding-inline-end: var(--spacing-lg);
}
```

#### Card with Accent Border

```css
/* Accent border on start edge */
blog-card[data-featured] {
  border-inline-start: 4px solid var(--primary);
  padding-inline-start: var(--spacing-lg);
}
```

### Migration Guide

When converting existing CSS:

```css
/* Before */
.card {
  margin-left: 1rem;
  margin-right: 1rem;
  padding-top: 2rem;
  padding-bottom: 1rem;
  border-left: 3px solid blue;
  text-align: left;
}

/* After */
.card {
  margin-inline: 1rem;
  padding-block: 2rem 1rem;
  border-inline-start: 3px solid blue;
  text-align: start;
}
```

### When to Keep Physical Properties

Some properties should remain physical:

| Property | Keep Physical When |
|----------|-------------------|
| `top`, `left`, etc. | Fixed position relative to viewport |
| `transform` | Animations that shouldn't flip |
| `box-shadow` | Light source should stay consistent |
| `background-position` | Image positioning shouldn't flip |

```css
/* Physical: shadow direction stays consistent */
blog-card {
  box-shadow: 2px 2px 8px oklch(0% 0 0 / 0.15);
}

/* Logical: border flips with text direction */
blog-card {
  border-inline-start: 3px solid var(--primary);
}
```

### Integration with Design Tokens

Define spacing tokens and use them with logical properties:

```css
/* _tokens.css */
:root {
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;
}

/* Component using logical properties with tokens */
article {
  padding-block: var(--spacing-xl);
  padding-inline: var(--spacing-lg);
  margin-block-end: var(--spacing-lg);
}
```

### Browser Support

Logical properties have excellent browser support (95%+). For older browsers:

```css
/* Fallback pattern (only if supporting very old browsers) */
blog-card {
  margin-left: 1rem;  /* Fallback */
  margin-inline-start: 1rem;  /* Modern browsers */
}
```

---

## Example: Complete Component File

```css
/* components/_blog-card.css */
@layer components {
  blog-card {
    display: grid;
    gap: var(--spacing-md);
    padding: var(--spacing-lg);
    background: var(--surface);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-sm);
    transition: box-shadow var(--transition-normal);

    /* Hover effect */
    &:hover {
      box-shadow: var(--shadow-md);
    }

    /* Featured variant */
    &[data-featured] {
      border-inline-start: 4px solid var(--primary);
    }

    /* Child elements */
    & h3 {
      margin: 0;
      font-size: var(--font-size-lg);
    }

    & time {
      color: var(--text-muted);
      font-size: var(--font-size-sm);
    }

    & p {
      margin: 0;
      line-height: var(--line-height-relaxed);
    }

    /* Responsive */
    @media (max-width: 768px) {
      padding: var(--spacing-md);
    }
  }
}
```

---

## CSS Baseline

[Baseline](https://web.dev/baseline) defines which CSS features are available across all major browsers. Our linter warns when using features outside Baseline Newly available status.

### Baseline Tiers

| Status | Meaning | Our Approach |
|--------|---------|--------------|
| **Widely available** | 30+ months in all browsers | Use freely |
| **Newly available** | Recently in all browsers | Use freely (our threshold) |
| **Limited availability** | Not in all browsers | Requires `@supports` |

### Progressive Enhancement for Non-Baseline

Features outside Baseline must be wrapped in `@supports`:

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

The linter allows non-Baseline CSS inside `@supports` blocks.

### Common Non-Baseline Features

Some features we document may not yet be Baseline. Always check and use `@supports`:

```css
/* contrast-color() - Safari Tech Preview only */
@supports (color: contrast-color(red)) {
  .dynamic-bg {
    color: contrast-color(var(--bg));
  }
}

/* text-wrap: pretty - recently Baseline */
@supports (text-wrap: pretty) {
  article p {
    text-wrap: pretty;
  }
}
```

### Checking Baseline Status

- [web.dev/baseline](https://web.dev/baseline) - Feature status lookup
- [caniuse.com](https://caniuse.com) - Detailed browser support
- Run `npm run lint:css` - Linter warns on non-Baseline features

---

## Checklist for CSS Architecture

When setting up or reviewing CSS:

### Structure
- [ ] Layer declaration at top of main.css
- [ ] All imports use `layer()` syntax
- [ ] Files organized by scope (tokens, layout, sections, components, pages)
- [ ] No classes used for state (use `data-*` attributes)
- [ ] Custom elements used as styling hooks
- [ ] Nesting limited to 3-4 levels
- [ ] Responsive styles in `responsive` layer
- [ ] Design tokens in `_tokens.css`
- [ ] Consider `@scope` for components with many child rules or donut patterns

### Colors
- [ ] Colors defined in OKLCH format, not hex or RGB
- [ ] `color-scheme: light dark` declared in `:root`
- [ ] Theme-aware tokens use `light-dark()` function
- [ ] Color variations use relative colors (not separate tokens)
- [ ] Gradients specify color space: `linear-gradient(in oklch, ...)`
- [ ] Hex fallback provided before OKLCH for older browsers (if needed)

### Layout
- [ ] Container queries used for component-scoped responsiveness
- [ ] Components define `container-type` when children need to adapt
- [ ] Logical properties used for margins, padding, and borders
- [ ] `margin-inline` / `padding-block` instead of physical directions
- [ ] `text-align: start` instead of `text-align: left`
- [ ] Physical properties only where semantically appropriate (shadows, transforms)

### Baseline
- [ ] Non-Baseline features wrapped in `@supports`
- [ ] Baseline-safe fallback provided before enhancement
- [ ] `npm run lint:css` passes without baseline warnings

## Skills to Consider Before Writing

When authoring CSS, consider invoking these related skills:

| CSS Feature | Invoke Skill | Why |
|-------------|--------------|-----|
| Animations, transitions | **animation-motion** | Proper keyframes, scroll-driven effects, reduced-motion |
| Print styles (@media print) | **print-styles** | Print-specific layout, page breaks, hiding nav |
| Icon styling | **icons** | Use `<x-icon>` component, not inline SVG |
| Dark/light themes | **data-attributes** | State via `data-theme`, not classes |
| Responsive images | **responsive-images** | Image sizing, aspect ratios, art direction |

### When Styling Components with Icons

When styling buttons, toggles, or UI elements that need icons, ensure the HTML uses `<x-icon>`:

```css
/* Styling icons is simple when using x-icon */
button x-icon {
  color: currentColor;
}

button:hover x-icon {
  color: var(--primary);
}
```

See the **icons** skill before adding any visual indicators to HTML.

## Related Skills

- **layout-grid** - Fluid grid systems, responsive columns, resolution-independent layouts
- **typography** - Type scale, hierarchy, rhythm, text-wrap, font pairing
- **animation-motion** - CSS animations, transitions, and scroll-driven effects
- **print-styles** - Write print-friendly CSS using @media print
- **icons** - Lucide icon library with `<x-icon>` Web Component
- **data-attributes** - Using data-* attributes for state and variants
- **xhtml-author** - Write valid XHTML-strict HTML5 markup
- **responsive-images** - Modern responsive image techniques
- **progressive-enhancement** - HTML-first development with CSS-only interactivity
