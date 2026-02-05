---
name: ui-component
description: |
  Reusable UI component design and implementation methodology.
  Integrates design tokens, accessibility (a11y via W3C APG), and semantic HTML.
  Reference for building accessible, theme-compliant React components.
---

# UI Component Skill

## Component Design Principles

### 1. Design Token Integration

Use CSS custom properties from design tokens:

```tsx
// ✅ Use CSS variables
const variantStyles = {
  primary: "bg-primary text-primary-foreground hover:bg-primary-hover",
  secondary: "bg-secondary text-secondary-foreground hover:bg-secondary-hover",
}

// ❌ Don't hardcode colors
const badStyles = {
  primary: "bg-cyan-600 text-white hover:bg-cyan-700",
}
```

### 2. Composition over Configuration

Prefer composable components over complex prop APIs:

```tsx
// ✅ Composable
<Button iconBefore={<Plus />}>Add Item</Button>
<Button iconAfter={<ChevronRight />}>Next</Button>

// ❌ Over-configured
<Button icon="plus" iconPosition="left" iconSize="sm">
  Add Item
</Button>
```

### 3. Accessible by Default

Build accessibility into the component API:

```tsx
interface IconButtonProps {
  icon: ReactNode
  "aria-label": string  // Required, not optional
  pressed?: boolean     // Maps to aria-pressed
}

// Forces accessible usage
<IconButton icon={<X />} aria-label="Close" />
```

## Component Template

React 19 では `forwardRef` は非推奨です。`ref` を通常の props として受け取ります。

```tsx
import type { ComponentProps, ReactNode, Ref } from "react"

export type ButtonVariant = "primary" | "secondary" | "ghost" | "destructive"
export type ButtonSize = "sm" | "md" | "lg"

export interface ButtonProps extends ComponentProps<"button"> {
  variant?: ButtonVariant
  size?: ButtonSize
  iconBefore?: ReactNode
  iconAfter?: ReactNode
  /** Ref to the button element */
  ref?: Ref<HTMLButtonElement>
}

const variantStyles: Record<ButtonVariant, string> = {
  primary: "bg-primary text-primary-foreground hover:bg-primary-hover",
  secondary: "bg-secondary text-secondary-foreground hover:bg-secondary-hover",
  ghost: "bg-transparent text-foreground hover:bg-accent",
  destructive: "bg-destructive text-destructive-foreground hover:bg-destructive-hover",
}

const sizeStyles: Record<ButtonSize, string> = {
  sm: "h-8 px-3 text-sm gap-1.5",
  md: "h-9 px-4 text-sm gap-2",
  lg: "h-10 px-5 text-base gap-2",
}

export function Button({
  variant = "primary",
  size = "md",
  className = "",
  ref,
  ...props
}: ButtonProps) {
  return (
    <button
      ref={ref}
      type="button"
      className={`
        inline-flex items-center justify-center font-medium rounded-md
        transition-colors
        focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring
        disabled:opacity-50 disabled:pointer-events-none
        ${variantStyles[variant]}
        ${sizeStyles[size]}
        ${className}
      `}
      {...props}
    />
  )
}
```

## HTML Semantic Structure (WHATWG/W3C)

Reference: [WHATWG HTML Living Standard](https://html.spec.whatwg.org/)

### Sectioning Elements

| Element | Purpose | Usage |
|---------|---------|-------|
| `<main>` | Primary content (one per page) | App main content area |
| `<nav>` | Navigation links | Menu bar, sidebar navigation |
| `<article>` | Self-contained content | Cards, posts, widgets |
| `<section>` | Thematic grouping with heading | Content sections |
| `<aside>` | Tangentially related content | Sidebars, tooltips |
| `<header>` | Introductory content | Page/section header |
| `<footer>` | Footer content | Page/section footer |

### DOM Structure Examples

```tsx
// Card with semantic structure
<article>
  <header>
    <h2>{title}</h2>
  </header>
  <div>{content}</div>
  <footer>{actions}</footer>
</article>

// Navigation menu
<nav aria-label="Main navigation">
  <ul role="menubar">
    <li role="none">
      <button role="menuitem">File</button>
    </li>
  </ul>
</nav>

// Page layout
<main>
  <h1>Page Title</h1>
  <section>
    <h2>Section Title</h2>
    {content}
  </section>
</main>
<aside aria-label="Sidebar">{sidebar}</aside>
```

### Heading Hierarchy

Maintain logical heading structure:

```tsx
// ✅ Correct hierarchy
<main>
  <h1>Application</h1>
  <section>
    <h2>Section</h2>
    <h3>Subsection</h3>
  </section>
</main>

// ❌ Skipped levels
<main>
  <h1>Application</h1>
  <h3>Section</h3>  {/* Skipped h2 */}
</main>
```

## WAI-ARIA Patterns (W3C APG)

Reference: [W3C ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/)

### Button Pattern

Source: [APG Button Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/button/)

```tsx
// Standard button
<button type="button">Save</button>

// Icon-only button (requires aria-label)
<button type="button" aria-label="Close">
  <X aria-hidden="true" />
</button>

// Toggle button
<button type="button" aria-pressed={isPressed}>
  <Star aria-hidden="true" />
</button>

// Menu button
<button
  type="button"
  aria-haspopup="menu"
  aria-expanded={isOpen}
  aria-controls="menu-id"
>
  Options
</button>
```

**Keyboard:** `Space` / `Enter` activates button

### Menu Button Pattern

Source: [APG Menu Button Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/menu-button/)

```tsx
<div>
  <button
    aria-haspopup="menu"
    aria-expanded={isOpen}
    aria-controls="dropdown"
  >
    Options
  </button>
  {isOpen && (
    <ul id="dropdown" role="menu" aria-label="Options">
      <li role="none">
        <button role="menuitem">Copy</button>
      </li>
      <li role="none">
        <button role="menuitem">Paste</button>
      </li>
    </ul>
  )}
</div>
```

**Keyboard:**
- `Enter` / `Space` / `↓`: Open menu, focus first item
- `↑`: Open menu, focus last item
- `Escape`: Close menu

### Tabs Pattern

Source: [APG Tabs Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/tabs/)

```tsx
<div>
  <div role="tablist" aria-label="Settings">
    <button
      role="tab"
      id="tab-1"
      aria-selected={active === 0}
      aria-controls="panel-1"
      tabIndex={active === 0 ? 0 : -1}
    >
      General
    </button>
    <button
      role="tab"
      id="tab-2"
      aria-selected={active === 1}
      aria-controls="panel-2"
      tabIndex={active === 1 ? 0 : -1}
    >
      Advanced
    </button>
  </div>
  <div
    role="tabpanel"
    id="panel-1"
    aria-labelledby="tab-1"
    tabIndex={0}
    hidden={active !== 0}
  >
    General settings
  </div>
</div>
```

**Keyboard:**
- `Tab`: Enter/exit tablist
- `←` / `→`: Navigate tabs (horizontal)
- `Home` / `End`: First/last tab

### Dialog Pattern

Source: [APG Dialog Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/)

```tsx
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="dialog-title"
  aria-describedby="dialog-desc"
>
  <h2 id="dialog-title">Confirm</h2>
  <p id="dialog-desc">Are you sure?</p>
  <button>Cancel</button>
  <button>Confirm</button>
</div>
```

**Keyboard:**
- `Tab`: Cycle focus within dialog (trapped)
- `Escape`: Close dialog

## Modern Web Platform APIs

### Popover API (Native Popovers)

Use native popover for tooltips, menus, and dialogs without JS positioning:

```tsx
// Trigger button
<button popovertarget="my-popover">Open Menu</button>

// Popover content (auto-positioned, light-dismiss)
<div id="my-popover" popover>
  <p>Popover content here</p>
</div>
```

**Attributes:**
- `popover` / `popover="auto"`: Light-dismiss (click outside closes)
- `popover="manual"`: Requires explicit close
- `popovertarget`: Links button to popover
- `popovertargetaction`: `toggle` (default), `show`, `hide`

```tsx
// Controlled popover with React
function Menu() {
  const popoverRef = useRef<HTMLDivElement>(null)

  return (
    <>
      <button popovertarget="menu">Options</button>
      <div
        ref={popoverRef}
        id="menu"
        popover="auto"
        onToggle={(e) => console.log(e.newState)} // 'open' | 'closed'
      >
        <button onClick={() => popoverRef.current?.hidePopover()}>
          Close
        </button>
      </div>
    </>
  )
}
```

### inert Attribute

Disable all interactions and remove from accessibility tree:

```tsx
// Modal with inert background
<>
  <div inert={isModalOpen}>
    {/* Main content - disabled when modal is open */}
    <nav>...</nav>
    <main>...</main>
  </div>

  {isModalOpen && (
    <dialog open>
      {/* Only this is interactive */}
    </dialog>
  )}
</>
```

**Use cases:**
- Modal backgrounds
- Off-screen content in carousels
- Collapsed accordion panels
- Hidden drawer content

### <dialog> Element

Native modal with proper focus management:

```tsx
function Dialog({ open, onClose, children }) {
  const dialogRef = useRef<HTMLDialogElement>(null)

  useEffect(() => {
    const dialog = dialogRef.current
    if (open) {
      dialog?.showModal()  // Traps focus, adds backdrop
    } else {
      dialog?.close()
    }
  }, [open])

  return (
    <dialog
      ref={dialogRef}
      onClose={onClose}
      onCancel={onClose}  // Escape key
    >
      {children}
    </dialog>
  )
}
```

```css
/* Native backdrop styling */
dialog::backdrop {
  background: oklch(0% 0 0 / 50%);
  backdrop-filter: blur(4px);
}
```

## A11y Requirements

### Touch Targets (WCAG 2.5.8)

Minimum 24×24 CSS pixels:

```tsx
const sizeStyles = {
  sm: "min-w-6 min-h-6",   // 24px minimum
  md: "min-w-8 min-h-8",   // 32px
  lg: "min-w-10 min-h-10", // 40px
}
```

### Focus Ring (WCAG 2.4.7)

Visible focus indicator:

```tsx
className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
```

### Color Contrast (WCAG 1.4.3 / 1.4.11)

| Element | Minimum Ratio |
|---------|---------------|
| Normal text | 4.5:1 |
| Large text (18px+ or 14px bold) | 3:1 |
| UI components & graphics | 3:1 |

### ARIA Quick Reference

| Component | Required Attributes |
|-----------|---------------------|
| Icon button | `aria-label` |
| Toggle button | `aria-pressed` |
| Expandable | `aria-expanded`, `aria-controls` |
| Menu button | `aria-haspopup="menu"`, `aria-expanded` |
| Tab | `role="tab"`, `aria-selected`, `aria-controls` |
| Tablist | `role="tablist"`, `aria-label` |
| Tabpanel | `role="tabpanel"`, `aria-labelledby` |
| Dialog | `role="dialog"`, `aria-modal`, `aria-labelledby` |
| Menu | `role="menu"`, `aria-label` |
| Menuitem | `role="menuitem"` |

### Disabled State

```tsx
// Native disabled (removes from tab order)
<button disabled>Disabled</button>

// aria-disabled (stays in tab order, announced as disabled)
<button aria-disabled="true">Disabled</button>
```

### Disabled Cursor Style

Use `disabled:cursor-not-allowed` instead of `disabled:pointer-events-none` for interactive elements.

`pointer-events-none` hides the cursor feedback, preventing users from understanding why the element is unclickable.

### Reduced Motion (WCAG 2.3.3)

```tsx
className="motion-safe:transition-all motion-reduce:transition-none"
```

## Styling Patterns

### Variant Styles Pattern

```tsx
const variantStyles: Record<ButtonVariant, string> = {
  primary: "bg-primary text-primary-foreground",
  secondary: "bg-secondary text-secondary-foreground",
}

className={`${variantStyles[variant]} ${sizeStyles[size]}`}
```

### CSS Grid for Internal Layout

```tsx
<button className="grid grid-cols-[auto_1fr_auto] gap-2 items-center">
  {iconBefore}
  <span>{children}</span>
  {iconAfter}
</button>
```

### Container Queries

```tsx
<div className="@container">
  <div className="@sm:flex-row @md:grid-cols-3">
    {content}
  </div>
</div>
```

## Export Pattern

```tsx
// components/index.ts
export { Button } from "./Button"
export type { ButtonProps, ButtonVariant, ButtonSize } from "./Button"

// index.ts
export * from "./components"
```

## Component Checklist

**Design & Structure:**
- [ ] Uses design tokens (no hardcoded colors/spacing)
- [ ] Uses semantic HTML elements
- [ ] Maintains logical heading hierarchy
- [ ] Accepts `ref` as a prop (React 19 pattern, not forwardRef)
- [ ] Exports types alongside component

**Accessibility (WAI-ARIA):**
- [ ] Follows W3C APG pattern for component type
- [ ] Required ARIA attributes in props interface
- [ ] Meets touch target requirements (24×24 min)
- [ ] Has visible focus ring
- [ ] Color contrast meets WCAG requirements
- [ ] Works with keyboard navigation
- [ ] Respects `prefers-reduced-motion`

**Testing:**
- [ ] Storybook stories (variant/size/state showcases)
- [ ] A11y tests with play functions
- [ ] Passes a11y addon checks

## References

- [WHATWG HTML Living Standard](https://html.spec.whatwg.org/)
- [W3C ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/)
- [W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- [MDN Web Docs - ARIA](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA)
