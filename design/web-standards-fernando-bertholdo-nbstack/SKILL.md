---
name: web-standards
description: Use when reviewing or building web interfaces for accessibility compliance, component patterns, form handling, typography, performance, animations, and UX patterns aligned with modern web standards and Vercel's guidelines.
---

# UI Web Standards

## Overview

Comprehensive guidance for building accessible, performant, and user-friendly web interfaces aligned with Vercel's Web Interface Guidelines. Covers accessibility compliance (WCAG 2.1 AA), component patterns, form handling, animations, typography, navigation, and anti-patterns to avoid.

## When to Use

- **Reviewing** HTML, React, Vue, Svelte components for accessibility and standards compliance
- **Building** forms, buttons, links, modals, navigation, lists, and interactive elements
- **Optimizing** performance via virtualization, lazy loading, and animation handling
- **Implementing** animations, transitions, or motion-sensitive designs
- **Handling** dark mode, i18n, localization, or theme-aware components
- **Debugging** focus states, keyboard navigation, or screen reader announcements
- **Designing** UX copy, error messages, loading states, or empty states

## When NOT to Use

- Styling decisions unrelated to accessibility, performance, or UX patterns
- Branding or visual design guidelines (use design system skill instead)
- Backend logic or server-side rendering patterns (use architecture reviews)
- Non-web platforms (native mobile, desktop apps, terminal UIs)

---

## Accessibility

### Semantic HTML First

**Use semantic elements; never `<div onClick>` for interactive content:**

- `<button>` for actions (submit, cancel, toggle, delete)
- `<a>` or `<Link>` for navigation (internal/external)
- `<label>` for form controls (inputs, checkboxes, radios, selects)
- `<table>` for tabular data (with `<thead>`, `<tbody>`, proper headers)
- `<nav>`, `<main>`, `<header>`, `<footer>`, `<section>`, `<article>` for structure

**Anti-pattern:**
```jsx
<div onClick={handleClick} role="button">
  Click me
</div>
```

**Correct:**
```jsx
<button onClick={handleClick}>
  Click me
</button>
```

### ARIA Labels & Roles

- **Icon-only buttons** require `aria-label="..."` describing intent
- **Form controls** without visible labels require `aria-label` or `aria-labelledby`
- **Inputs** with labels: use `<label htmlFor="id">` (clickable target) or `aria-label`
- **Interactive elements**: expose role via semantic HTML; use `role="..."` only when semantic element unavailable
- **Decorative icons**: apply `aria-hidden="true"` to skip in accessibility tree
- **Dynamic content**: async updates use `aria-live="polite"` (toasts, validation messages, status updates)
- **Skip links**: include skip-to-main link at top of page

**Example:**
```jsx
{/* Icon-only button */}
<button aria-label="Close modal" onClick={closeModal}>
  <CloseIcon />
</button>

{/* Decorative icon */}
<span aria-hidden="true">✓</span>

{/* Form with label */}
<label htmlFor="email">Email</label>
<input id="email" type="email" name="email" />

{/* Live region for async updates */}
<div aria-live="polite" aria-atomic="true">
  {validationError}
</div>
```

### Keyboard Navigation

- **Interactive elements** (`<button>`, `<a>`, `<input>`, etc.) are keyboard-focusable by default
- **Custom interactive elements** require `onKeyDown` or `onKeyUp` handlers
- **Common patterns:**
  - **Button/Link**: Space/Enter to activate
  - **Checkbox**: Space to toggle
  - **Radio Group**: Arrow keys to navigate, Space to select
  - **Menu**: Arrow keys + Escape to close
  - **Modal**: Escape to close (if permitted), Tab trapped to modal
  - **Autocomplete**: Arrow keys to navigate, Enter to select, Escape to close

**Example:**
```jsx
const MyButton = ({ onClick, disabled }) => (
  <button
    onClick={onClick}
    onKeyDown={(e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        onClick(e);
      }
    }}
    disabled={disabled}
  >
    Click or press Enter/Space
  </button>
);
```

### Form Accessibility

- **Every form control** must have a visible label or `aria-label`
- **Labels clickable** via `htmlFor` attribute or label wrapping control
- **Semantic input types**: `type="email"`, `type="tel"`, `type="url"`, `type="number"` (enables mobile keyboards, browser validation)
- **Autocomplete**: use meaningful `autocomplete` attribute (e.g., `autocomplete="email"`, `autocomplete="current-password"`)
- **Spellcheck**: disable for email, code, username: `spellCheck={false}`
- **Error states:**
  - Display error inline next to field
  - Focus first invalid field on submit
  - Use `aria-describedby` to link input to error: `<input aria-describedby="email-error" /><div id="email-error">{error}</div>`
- **Checkboxes & Radios:**
  - Label and control share single hit target (label wraps input or uses `htmlFor`)
  - Group related radios with `<fieldset>` and `<legend>`

**Example:**
```jsx
<div>
  <label htmlFor="email">Email address</label>
  <input
    id="email"
    name="email"
    type="email"
    autoComplete="email"
    spellCheck={false}
    aria-describedby={error ? "email-error" : undefined}
    required
  />
  {error && <div id="email-error" style={{ color: "red" }}>{error}</div>}
</div>

{/* Checkbox with label as hit target */}
<label>
  <input type="checkbox" name="terms" required />
  I agree to the terms
</label>

{/* Radio group */}
<fieldset>
  <legend>Preferred contact method</legend>
  <label>
    <input type="radio" name="contact" value="email" />
    Email
  </label>
  <label>
    <input type="radio" name="contact" value="phone" />
    Phone
  </label>
</fieldset>
```

### Images

- **All `<img>` tags** require `alt` text (descriptive) or `alt=""` (if purely decorative)
- **Decorative images** use `alt=""` and `aria-hidden="true"`
- **Content images** describe purpose/subject in alt text (e.g., "Team photo at 2024 conference", not just "photo")

**Example:**
```jsx
{/* Content image */}
<img src="team.jpg" alt="Team photo at 2024 annual conference" />

{/* Decorative divider */}
<img src="divider.svg" alt="" aria-hidden="true" />
```

### Headings & Structure

- **Hierarchical headings** from `<h1>` to `<h6>` (skip levels only deliberately)
- **Single `<h1>` per page** (page title)
- **Include skip link** before main content: `<a href="#main-content">Skip to main content</a>`
- **Heading anchors**: add `scroll-margin-top` to avoid overlap with fixed headers

**Example:**
```jsx
<a href="#main-content" className="sr-only">Skip to main content</a>

<h1>Page Title</h1>
<section>
  <h2 id="features" style={{ scrollMarginTop: "80px" }}>Features</h2>
  {/* ... */}
</section>

<style>
  .sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border-width: 0;
  }
</style>
```

---

## Focus States

### Visible Focus Indicators

- **Never remove outlines** without visible replacement
- **Prefer `:focus-visible`** over `:focus` (avoids outline on mouse click, shows on keyboard)
- **Required indicator**: ring or border on focus; sufficient contrast (3:1 minimum)
- **Style example**: `focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-blue-500`

**Anti-pattern:**
```css
button {
  outline: none; /* ❌ Removes focus completely */
}
```

**Correct:**
```css
button:focus-visible {
  outline: 2px solid #0066cc;
  outline-offset: 2px;
}

/* Tailwind equivalent */
button {
  @apply focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-blue-500;
}
```

### Compound Controls

- **Groups of controls** (tabs, segmented buttons, option groups) use `:focus-within` to show parent focus state
- **Example**: tab group highlights when any tab is focused

**Example:**
```css
.tab-group:focus-within {
  border-color: #0066cc;
}

.tab-group button:focus-visible {
  outline: none; /* Outlined by parent :focus-within */
}
```

---

## Forms

### Validation & Error Handling

**Submit button states:**
- **Enabled** by default (accept input)
- **Disabled + spinner** while request in flight
- **Re-enabled** on success or error
- **Clear label** while loading (e.g., "Saving..." not spinner-only)

**Error handling:**
- Inline errors next to fields (not top of form)
- Focus first invalid field on submit
- Specific error messages with fix/next step (not "Invalid input")
- Clear syntax for required fields (asterisk or label text)

**Example:**
```jsx
const [isLoading, setIsLoading] = useState(false);
const [errors, setErrors] = useState({});

const handleSubmit = async (e) => {
  e.preventDefault();
  setIsLoading(true);
  try {
    await submitForm(formData);
  } catch (err) {
    setErrors(err.validationErrors);
    // Focus first error field
    const firstErrorField = Object.keys(err.validationErrors)[0];
    document.getElementById(firstErrorField)?.focus();
  } finally {
    setIsLoading(false);
  }
};

return (
  <form onSubmit={handleSubmit}>
    <div>
      <label htmlFor="email">Email *</label>
      <input
        id="email"
        type="email"
        name="email"
        autoComplete="email"
        aria-describedby={errors.email ? "email-error" : undefined}
      />
      {errors.email && (
        <div id="email-error" role="alert">
          {errors.email} – Try a different email address.
        </div>
      )}
    </div>

    <button type="submit" disabled={isLoading}>
      {isLoading ? "Saving..." : "Save"}
    </button>
  </form>
);
```

### Autocomplete & Input Handling

- **Never block paste**: avoid `onPaste` with `preventDefault()`
- **Meaningful `name` attributes**: assist password managers and form restoration
- **Disable autocomplete** for non-auth fields to prevent password manager popup: `autoComplete="off"`
- **Enable for auth fields** (email, password): let password manager assist
- **`inputmode` attribute**: hint at mobile keyboard (e.g., `inputMode="email"` for email-like fields)

**Example:**
```jsx
{/* Auth field - allow password manager */}
<input
  type="email"
  name="email"
  autoComplete="email"
/>

{/* Non-auth field - disable password manager */}
<input
  type="text"
  name="search-query"
  autoComplete="off"
  inputMode="search"
/>

{/* Phone number */}
<input
  type="tel"
  name="phone"
  autoComplete="tel"
  inputMode="tel"
  placeholder="555-123-4567…"
/>
```

### Placeholders

- **Placeholders not labels**: show example format, not required instruction
- **End with `…`** to indicate example: `placeholder="john@example.com…"`
- **Short, descriptive**: help user understand expected input

---

## Animation

### Respect Motion Preferences

**Always honor `prefers-reduced-motion`:**

```css
/* Disable animations for users who prefer reduced motion */
@media (prefers-reduced-motion: reduce) {
  * {
    animation: none !important;
    transition: none !important;
  }
}
```

**JavaScript check:**
```jsx
const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

if (!prefersReducedMotion) {
  // Apply animation
}
```

### Animation Best Practices

- **Only animate** `transform` and `opacity` (GPU-accelerated)
- **Never** `transition: all` – list properties explicitly
- **Set `transform-origin`** when rotating/scaling
- **SVG animations**: wrap with `<g>`, set `transform-box: fill-box; transform-origin: center`
- **Interruptible**: animations should respond to user input (e.g., close modal during fade-out)
- **Reasonable duration**: 200–400ms for micro-interactions, 500–800ms for page transitions
- **Easing**: use cubic-bezier or ease-in-out; avoid linear for motion

**Anti-pattern:**
```css
/* ❌ Slow, janky, disrespects prefers-reduced-motion */
transition: all 2s linear;
```

**Correct:**
```css
/* ✅ GPU-accelerated, respectful, smooth */
@media (prefers-reduced-motion: no-preference) {
  .fade-in {
    animation: fadeIn 0.3s ease-out;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Explicit properties, not "all" */
transition: opacity 0.3s ease-out, transform 0.3s ease-out;
```

**SVG example:**
```jsx
<svg viewBox="0 0 100 100" style={{ transformBox: "fill-box", transformOrigin: "center" }}>
  <g style={{ transform: "rotate(45deg)" }}>
    <circle cx="50" cy="50" r="40" />
  </g>
</svg>
```

---

## Typography

### Text Formatting

- **Ellipsis**: use `…` (HTML entity `&hellip;`), not `...` (three periods)
- **Quotes**: use curly quotes `"` `"` (HTML entities `&ldquo;` `&rdquo;`), not straight `"`
- **Non-breaking spaces** for:
  - Measurements: `10&nbsp;MB`, `5&nbsp;GB`
  - Shortcuts: `⌘&nbsp;K`, `Ctrl&nbsp;+&nbsp;K`
  - Brand/product names: `GitHub&nbsp;Copilot`
  - Prevent orphaned words at line breaks

**Example:**
```jsx
<p>Use ⌘&nbsp;K to open the command palette.</p>
<p>Download the file (50&nbsp;MB) for offline access.</p>
<p>{item.name}&nbsp;—&nbsp;{item.category}</p>
```

### Number & Date Formatting

- **Loading states** end with `…`: "Loading…", "Saving…", not "Loading" or spinners-only
- **Tabular numbers**: use `font-variant-numeric: tabular-nums` for columns of numbers (ensures monospace alignment)
- **Date/Time**: use `Intl.DateTimeFormat`, never hardcoded formats
- **Numbers**: use `Intl.NumberFormat` with locale awareness

**Example:**
```jsx
{/* Locale-aware date */}
const formattedDate = new Intl.DateTimeFormat("en-US", {
  year: "numeric",
  month: "long",
  day: "numeric",
}).format(new Date());

{/* Locale-aware number */}
const formattedNumber = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
}).format(1234.56);

{/* Tabular numbers (aligned columns) */}
<table style={{ fontVariantNumeric: "tabular-nums" }}>
  <tr>
    <td>1,234.56</td>
  </tr>
</table>
```

---

## Content Handling

### Text Overflow

- **Long text**: apply `truncate`, `line-clamp-*` (Tailwind), or `text-wrap: balance` for headings
- **Flex children**: always set `min-w-0` to allow child truncation (flex doesn't shrink below content size by default)
- **Break long words**: use `break-words` or `word-break: break-word` as fallback

**Example:**
```jsx
{/* Truncate long email */}
<div style={{ overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
  verylongemailaddress@example.com
</div>

{/* Line clamp */}
<p style={{ display: "-webkit-box", WebkitLineClamp: 2, WebkitBoxOrient: "vertical", overflow: "hidden" }}>
  Multi-line text truncated after 2 lines…
</p>

{/* Flex container with truncation */}
<div style={{ display: "flex", minWidth: 0 }}>
  <span style={{ overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
    Long text
  </span>
</div>
```

### Empty States

- **Gracefully handle** empty lists, no results, no data scenarios
- **Show message**: "No items yet" with optional action (import, create, etc.)
- **Avoid blank screens**: empty state is content, not an error

**Example:**
```jsx
{items.length === 0 ? (
  <div style={{ textAlign: "center", padding: "40px" }}>
    <p>No deployments yet.</p>
    <button onClick={openCreateDialog}>Create your first deployment</button>
  </div>
) : (
  {/* Items list */}
)}
```

### Input Anticipation

- **Anticipate short, average, and very long inputs**
- **Test with:** real domain data, edge cases, longest valid inputs
- **Adjust layout** for mobile vs desktop (stack vs side-by-side)

---

## Images

### Image Dimensions & Optimization

- **Every `<img>` must have explicit `width` and `height`** (prevents Cumulative Layout Shift - CLS)
- **Aspect ratio**: specify as number (e.g., `16 / 9`) or via CSS for `<img>` responsive scaling
- **Lazy loading**: below-fold images use `loading="lazy"`
- **Above-fold**: use `priority` (Next.js) or `fetchpriority="high"`
- **Modern formats**: serve WebP with fallback (via `<picture>` or `srcset`)

**Example:**
```jsx
{/* Above-fold, priority */}
<img
  src="hero.jpg"
  alt="Hero image"
  width={1200}
  height={600}
  priority
/>

{/* Below-fold, lazy load */}
<img
  src="feature.jpg"
  alt="Feature overview"
  width={800}
  height={600}
  loading="lazy"
/>

{/* Responsive with aspect ratio */}
<img
  src="responsive.jpg"
  alt="Responsive image"
  width={400}
  height={300}
  style={{ aspectRatio: "4 / 3", width: "100%", height: "auto" }}
/>

{/* Modern formats */}
<picture>
  <source srcSet="image.webp" type="image/webp" />
  <source srcSet="image.jpg" type="image/jpeg" />
  <img src="image.jpg" alt="Fallback" width={400} height={300} />
</picture>
```

---

## Performance

### Virtualization

- **Large lists** (>50 items): virtualize with `content-visibility: auto` or library (e.g., `virtua`, `react-window`, `react-virtual`)
- **Unvirtualized lists render off-screen DOM**, causing layout thrashing and slow scrolling
- **Virtual scroll**: only render visible items + buffer

**Example:**
```jsx
import { Virtualizer } from "virtua";

<Virtualizer>
  {items.map((item) => (
    <div key={item.id}>{item.name}</div>
  ))}
</Virtualizer>

{/* CSS-based virtualization */}
<div style={{ contentVisibility: "auto" }}>
  {/* Large list */}
</div>
```

### Layout Thrashing

**Anti-pattern: reading layout in render (causes forced reflows):**
```jsx
{/* ❌ Triggers layout recalculation every render */}
<div>
  {items.map((item) => {
    const height = document.getElementById(item.id)?.offsetHeight;
    return <div key={item.id} style={{ height }}>{item.name}</div>;
  })}
</div>
```

**Correct: batch reads/writes or avoid measurements in render:**
```jsx
useLayoutEffect(() => {
  // Batch read
  const rect = containerRef.current?.getBoundingClientRect();
  // Batch write
  setLayout(rect);
}, []);

// Or use ResizeObserver for responsive measurements
useEffect(() => {
  const observer = new ResizeObserver(([entry]) => {
    setWidth(entry.contentRect.width);
  });
  observer.observe(containerRef.current);
  return () => observer.disconnect();
}, []);
```

### Forms: Controlled vs Uncontrolled

- **Prefer uncontrolled** inputs (no state per keystroke)
- **Controlled inputs** must have cheap `onChange` handlers (avoid expensive computations per keystroke)
- **Use `defaultValue`** when form has initial state but input is uncontrolled

**Example:**
```jsx
{/* Uncontrolled - simpler, more performant */}
<input type="text" defaultValue="initial" />

{/* Controlled - only if needed for real-time validation/masking */}
const [value, setValue] = useState("");
return (
  <input
    value={value}
    onChange={(e) => setValue(e.target.value)} {/* Keep cheap */}
  />
);
```

### Font & Network Performance

- **Critical fonts**: preload with `<link rel="preload" as="font" href="..." type="font/..." crossOrigin>`
- **Use `font-display: swap`** to show fallback immediately (avoid invisible text while loading)
- **CDN domains**: warm with `<link rel="preconnect" href="https://cdn.example.com">`

**Example:**
```html
<head>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preload" href="/font.woff2" as="font" type="font/woff2" crossOrigin />
  <style>
    @font-face {
      font-family: "CustomFont";
      src: url("/font.woff2") format("woff2");
      font-display: swap;
    }
  </style>
</head>
```

---

## Navigation & State

### URL as Source of Truth

- **Query params** reflect UI state: filters, tabs, pagination, expanded panels, sorting
- **Sync state to URL** (use `nuqs`, `next/router`, or similar library)
- **Deep linking**: user can share/bookmark URL and restore full state
- **Back button** works intuitively (doesn't require custom handler for simple navigation)

**Example:**
```jsx
import { useQueryState } from "next-usp"; // or similar

export default function ProductList() {
  const [tab, setTab] = useQueryState("tab", { defaultValue: "all" });
  const [sort, setSort] = useQueryState("sort", { defaultValue: "name" });

  return (
    <div>
      <button onClick={() => setTab("featured")} data-active={tab === "featured"}>
        Featured
      </button>
      <select value={sort} onChange={(e) => setSort(e.target.value)}>
        <option value="name">Name</option>
        <option value="price">Price</option>
      </select>
      {/* URL: ?tab=featured&sort=price */}
    </div>
  );
}
```

### Links & Navigation

- **Use `<a>` or `<Link>`** for navigation (enables Cmd/Ctrl+click, middle-click, new tab)
- **Never `onClick` on `<div>`** for navigation
- **Button vs Link**: button = action, link = navigation

**Anti-pattern:**
```jsx
<div onClick={() => navigate("/page")}>Go to page</div>
```

**Correct:**
```jsx
<a href="/page">Go to page</a>
{/* or Next.js */}
<Link href="/page">Go to page</Link>
```

### Destructive Actions

- **Require confirmation** (modal/dialog) or **undo window** (toast with "Undo" button)
- **Avoid accidental clicks**: clear label ("Delete permanently", not "Delete"), secondary button style
- **After destructive action**: show success confirmation (not silent success)

**Example:**
```jsx
const handleDelete = async () => {
  const confirmed = window.confirm("Are you sure? This cannot be undone.");
  if (!confirmed) return;

  try {
    await deleteItem(id);
    showToast("Item deleted", {
      action: "Undo",
      onAction: () => restoreItem(id),
    });
  } catch (err) {
    showToast("Failed to delete item", { type: "error" });
  }
};

return (
  <button onClick={handleDelete} style={{ background: "red", color: "white" }}>
    Delete permanently
  </button>
);
```

---

## Touch & Interaction

### Touch Targets

- **Minimum 44×44px** touch target (or larger on mobile)
- **`touch-action: manipulation`**: prevents double-tap zoom delay (safe on mobile)
- **Intentional `-webkit-tap-highlight-color`**: replace default gray highlight

**Example:**
```css
button {
  min-width: 44px;
  min-height: 44px;
  touch-action: manipulation;
  -webkit-tap-highlight-color: rgba(0, 0, 0, 0.1);
}
```

### Scrolling & Overflow

- **Modal/drawer**: `overscroll-behavior: contain` prevents scroll-through
- **Full-bleed images**: `overflow-x: hidden` on body, ensure content doesn't overflow
- **Momentum scrolling** (iOS): use `-webkit-overflow-scrolling: touch` (deprecated but still supported)

**Example:**
```css
.modal {
  overscroll-behavior: contain;
  overflow-y: auto;
}

body {
  overflow-x: hidden;
}
```

### Drag & Drop

- **Disable text selection** during drag: `user-select: none`
- **Mark dragged elements `inert`** to prevent nested interaction
- **Visual feedback**: cursor change, opacity, or highlight

**Example:**
```jsx
const [isDragging, setIsDragging] = useState(false);

const handleDragStart = (e) => {
  setIsDragging(true);
  e.dataTransfer.effectAllowed = "move";
};

return (
  <div
    draggable
    onDragStart={handleDragStart}
    onDragEnd={() => setIsDragging(false)}
    style={{
      userSelect: "none",
      cursor: isDragging ? "grabbing" : "grab",
      opacity: isDragging ? 0.7 : 1,
    }}
  >
    Drag me
  </div>
);
```

### Auto-focus

- **Desktop only**: auto-focus primary input on page load (good UX)
- **Mobile**: skip auto-focus (keyboard appears unexpectedly, obscures content)
- **Single, clear purpose**: avoid auto-focus in multi-input forms (confusing)

**Example:**
```jsx
const isMobile = /iPhone|iPad|Android/.test(navigator.userAgent);

return (
  <input
    autoFocus={!isMobile}
    placeholder="Start typing…"
  />
);
```

---

## Safe Areas & Layout

### Notches & Safe Areas

- **Full-bleed layouts** (hero images, sidebars): account for notches using `env(safe-area-inset-*)`
- **iPhone notch**: left/top/right/bottom insets
- **Padding**: add padding for critical content

**Example:**
```css
.header {
  padding-left: max(1rem, env(safe-area-inset-left));
  padding-right: max(1rem, env(safe-area-inset-right));
  padding-top: max(1rem, env(safe-area-inset-top));
}

body {
  padding-bottom: env(safe-area-inset-bottom);
}
```

### Container Overflow

- **`overflow-x: hidden`** on containers to hide off-screen content
- **Ensure content doesn't overflow horizontally** (test responsive breakpoints)
- **Flex/Grid**: prefer layout algorithms over JS measurement

---

## Dark Mode & Theming

### Color Scheme & Defaults

- **`color-scheme: dark`** on `<html>` or root element (fixes scrollbar, input borders in dark mode)
- **Explicit `background-color` and `color`** on form inputs (Windows dark mode needs this)
- **`<meta name="theme-color">`** matches page background color (affects browser UI)

**Example:**
```html
<html style="color-scheme: dark">
  <head>
    <meta name="theme-color" content="#1a1a1a" />
  </head>
</html>

<style>
  input,
  select,
  textarea {
    background-color: #fff;
    color: #000;
  }

  @media (prefers-color-scheme: dark) {
    input,
    select,
    textarea {
      background-color: #222;
      color: #fff;
    }
  }
</style>
```

---

## Localization & i18n

### Date, Number, and Language Handling

- **`Intl.DateTimeFormat`**: never hardcode date formats
- **`Intl.NumberFormat`**: handle currency, thousands separators, percentages
- **`Accept-Language` header** or `navigator.languages[0]`**: detect locale (never IP-based)
- **`lang` attribute** on `<html>`: aids screen readers and spell-check

**Example:**
```jsx
const userLocale = navigator.language; // "en-US", "fr-FR", etc.

const formattedDate = new Intl.DateTimeFormat(userLocale, {
  year: "numeric",
  month: "long",
  day: "numeric",
}).format(new Date());

const formattedCurrency = new Intl.NumberFormat(userLocale, {
  style: "currency",
  currency: "USD",
}).format(1234.56);

return (
  <html lang={userLocale.split("-")[0]}>
    <div>{formattedDate}</div>
    <div>{formattedCurrency}</div>
  </html>
);
```

---

## Hydration Safety

### Server-Side Rendering (SSR) & Hydration

- **Inputs with `value`** require `onChange` handler or use `defaultValue` for uncontrolled
- **Avoid hydration mismatch** for date/time (server renders different value than client)
- **`suppressHydrationWarning`** only as last resort for intentional client-only content

**Anti-pattern (hydration mismatch):**
```jsx
{/* Server renders "Fri Mar 30 2026", client renders today's date */}
<div>{new Date().toLocaleDateString()}</div>
```

**Correct:**
```jsx
const [isMounted, setIsMounted] = useState(false);

useEffect(() => setIsMounted(true), []);

return (
  <div>{isMounted ? new Date().toLocaleDateString() : null}</div>
);
```

---

## Hover & Interactive States

### Hover States

- **Interactive elements** (buttons, links) require `:hover` state (CSS or Tailwind)
- **Hover increases contrast** or changes color/shadow (clear feedback)
- **Avoid relying on hover alone** for important info (mobile has no hover)

**Example:**
```css
button {
  background-color: #0066cc;
  transition: background-color 0.2s ease-out;
}

button:hover {
  background-color: #0052a3;
}

/* Tailwind */
button {
  @apply bg-blue-600 hover:bg-blue-700 transition-colors;
}
```

### Active & Disabled States

- **Active state** (`:active`, `.active`): visual feedback for pressed button
- **Disabled state**: reduced opacity, `cursor: not-allowed`, no hover effect

**Example:**
```css
button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

button:disabled:hover {
  background-color: #0066cc; /* No change on hover when disabled */
}
```

---

## Content & Copy

### Writing Style

- **Active voice**: "Install the CLI" not "The CLI will be installed"
- **Second person**: "You can deploy" not "One can deploy" or "I can deploy"
- **Avoid first person**: "Submit your form" not "I will submit your form"
- **Title Case** for headings/buttons (Chicago Manual of Style)
- **Numerals** for quantities: "8 deployments" not "eight deployments"
- **Specific button labels**: "Save API Key" not "Continue"
- **Ampersand** (`&`) over "and" in space-constrained labels
- **Errors include fix/next step**: "Email invalid – try a different address" not "Invalid email"

**Example:**
```jsx
{/* ✓ Active, second person, specific */}
<button>Save Your API Key</button>

{/* ✓ Error with fix */}
<div>Email invalid – Enter a different address.</div>

{/* ✓ Numerals, active */}
{count} deployments available

{/* ✓ Title Case */}
<h2>Build & Deploy</h2>
```

---

## Anti-patterns to Flag

| Anti-pattern | Issue | Fix |
|---|---|---|
| `user-scalable=no` or `maximum-scale=1` | Disables zoom; accessibility failure | Remove; allow pinch zoom |
| `onPaste` with `preventDefault` | Blocks paste; user frustration | Allow paste; validate input after |
| `transition: all` | Slow, unpredictable animations | List properties: `transition: opacity 0.3s, transform 0.3s` |
| `outline-none` without `:focus-visible` replacement | No focus indicator; keyboard navigation breaks | Add `:focus-visible:ring-2` or equivalent |
| Inline `onClick` on `<div>` | Not a button semantically; fails accessibility | Use `<button>` |
| `<div role="button">` with `onClick` | Fake button; missing keyboard handlers | Use `<button>` |
| Missing image `width`/`height` | Layout shift; poor LCP | Add explicit dimensions |
| Large array `.map()` without virtualization | Slow scroll; DOM bloat | Use `virtua`, `react-window`, or `content-visibility: auto` |
| Form control without label | Accessibility failure | Add `<label>` or `aria-label` |
| Icon button without `aria-label` | Unclear intent; screen reader says "button" | Add descriptive `aria-label` |
| Hardcoded date/time formats | Breaks in other locales | Use `Intl.DateTimeFormat` |
| Auto-focus without justification | Keyboard appears on mobile; confusing | Use `autoFocus={!isMobile}` or skip |
| `color-scheme` missing | Dark mode form inputs broken | Add `color-scheme: dark` to root |
| Decorative images without `alt=""` | Clutter accessibility tree | Add `alt=""` and `aria-hidden="true"` |
| Query params not in URL | Can't share state; no deep linking | Use `nuqs` or router to sync URL |
| `display: none` for accessibility | Content removed from layout and tree | Use visually hidden class (see Headings section) |

---

## Review Output Format

**Group findings by file using `file:line` format (clickable in VS Code):**

```
src/components/Button.tsx:12
❌ Icon-only button missing aria-label: <button><CloseIcon /></button>
Fix: Add aria-label="Close modal"

src/pages/form.tsx:34
❌ Inputs without labels or aria-label
Fix: Add <label htmlFor="email"> or aria-label="Email address"

src/styles/globals.css:2
❌ outline-none without :focus-visible replacement
Fix: Add :focus-visible { outline: 2px solid #0066cc; }

src/components/List.tsx:5
⚠ Large array .map() without virtualization (250+ items)
Suggest: Add content-visibility: auto or use virtua library
```

**Terse descriptions. Skip explanation unless fix non-obvious. No preamble.**

---

## Review Checklist

### Accessibility (WCAG 2.1 AA)

- [ ] Semantic HTML: `<button>`, `<a>`, `<label>` used correctly
- [ ] Icon-only buttons have `aria-label`
- [ ] Form inputs have visible labels or `aria-label`
- [ ] Keyboard navigation works (Tab, Enter, Space, Arrow keys, Escape)
- [ ] Focus indicators visible (`:focus-visible` or `ring-*`)
- [ ] Images have `alt` text (descriptive) or `alt=""` (decorative)
- [ ] Decorative icons have `aria-hidden="true"`
- [ ] Async updates use `aria-live="polite"`
- [ ] Color not sole means of conveying info (test grayscale)
- [ ] Contrast ratio ≥ 4.5:1 for normal text, ≥ 3:1 for large text
- [ ] Headings hierarchical (`<h1>`–`<h6>` in order)

### Forms

- [ ] Inputs have `name` and `autoComplete` attributes
- [ ] Semantic input types (`email`, `tel`, `number`, `url`)
- [ ] Paste not blocked (`onPaste` event doesn't preventDefault)
- [ ] Error messages inline, focused on submit
- [ ] Submit button disabled during request
- [ ] Non-auth fields have `autoComplete="off"`

### Performance

- [ ] Images have explicit `width` and `height`
- [ ] Below-fold images have `loading="lazy"`
- [ ] Lists >50 items virtualized
- [ ] Animations use `transform`/`opacity` only
- [ ] No `transition: all`
- [ ] Fonts use `font-display: swap`

### Animation & Motion

- [ ] `prefers-reduced-motion` respected
- [ ] Animations interruptible
- [ ] Duration reasonable (200–800ms)

### Dark Mode & Theming

- [ ] `color-scheme: dark` on root
- [ ] Form inputs have explicit colors in dark mode
- [ ] `<meta name="theme-color">` set

### Localization

- [ ] Dates use `Intl.DateTimeFormat`
- [ ] Numbers use `Intl.NumberFormat`
- [ ] `lang` attribute on `<html>`
- [ ] No hardcoded format strings

### Typography & Content

- [ ] Ellipsis (`…`), not `...`
- [ ] Curly quotes (`"` `"`), not straight `"`
- [ ] Loading states end with `…`
- [ ] Button labels specific and active voice
- [ ] Error messages include fix/next step

### Navigation & State

- [ ] Query params reflect UI state
- [ ] Links use `<a>` or `<Link>` (not `<div onClick>`)
- [ ] Destructive actions require confirmation

### Touch & Mobile

- [ ] Touch targets ≥ 44×44px
- [ ] `touch-action: manipulation` set
- [ ] Auto-focus skipped on mobile
- [ ] Safe areas considered (`env(safe-area-inset-*)`)

### Hydration (SSR)

- [ ] No hydration mismatch (date/time values)
- [ ] Controlled inputs have `onChange`
- [ ] Uncontrolled inputs use `defaultValue`
