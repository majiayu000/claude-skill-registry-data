---
name: system-components
description: Build reusable, consistent UI components with well-defined APIs and complete state coverage. Use when creating or reviewing components, props, variants, configuration vs composition, compound components, controlled/uncontrolled patterns, component states, CVA, asChild/render delegation, ref forwarding, icon system conventions, or "this component API feels wrong". Uses Radix, Base UI, and shadcn/ui as examples where that stack is already appropriate; do not add those dependencies automatically. Does NOT cover broad component terminology, icon names, button labels, feature names, or product names (use system-naming). Does NOT cover token architecture or theming (use system-tokens), composite patterns such as forms/navigation/tables (use system-patterns), or visual design, animation, and platform quirks (use the relevant surface skill).
---

# Components

How to build reusable UI components with consistent APIs and complete state coverage. system-tokens provides the values. This skill provides the structure.

Based on the component patterns of [Radix](https://www.radix-ui.com/primitives), [Base UI](https://base-ui.com), and [shadcn/ui](https://ui.shadcn.com). Treat these as preferred examples when a project already uses that stack, not as automatic dependency choices for every web interface.

For the shared design philosophy, see `references/design-philosophy.md`.

**Apply this whenever creating or reviewing a component.** For broad component, icon, and user-facing label terminology, use system-naming. For accessibility across all skills, see `references/accessibility.md`. For multi-skill task sequencing, see `references/composition.md`.

For API polish, safe button defaults, error boundary strategy, promotion rules, and file shape guidance, read `references/api-polish.md`.

---

## Prop Conventions

The same concept uses the same prop name on every component in the system.

### Standard props

| Prop | Type | Purpose |
|---|---|---|
| `variant` | string union | Visual style (`"default"`, `"destructive"`, `"outline"`, `"ghost"`) |
| `size` | string union | Dimensional scale (`"sm"`, `"md"`, `"lg"`) |
| `disabled` | boolean | Non-interactive state |
| `loading` | boolean | Shows activity indicator, prevents interaction |
| `open` | boolean | Controls visibility (dropdowns, modals, popovers) |
| `className` | string | Style override, merged via `cn()` |
| `ref` | React ref | DOM access |

### Rules

- **No `is` prefix on booleans.** `disabled`, `loading`, `open`. Not `isDisabled`, `isLoading`, `isOpen`.
- **String unions over booleans for multi-value dimensions.** `size="sm"` not `small={true}`. A boolean can only ever have two states; a string union is extensible.
- **Callbacks: `on{Event}` for native, `on{Prop}Change` for custom.** `onChange`, `onClick` follow the DOM. `onValueChange`, `onOpenChange` are component-specific state callbacks.
- **Every optional prop has a documented default.** If `size` defaults to `"md"`, that's in the type definition or JSDoc.

---

## Variant System (CVA)

Use [class-variance-authority](https://cva.style) for type-safe variant maps in Tailwind projects that already accept CVA. In non-Tailwind or dependency-sensitive projects, keep the same finite-variant model with the project's existing styling mechanism.

```tsx
import { cva, type VariantProps } from "class-variance-authority";

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md font-medium transition-colors",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline: "border border-input bg-background hover:bg-accent",
        ghost: "hover:bg-accent hover:text-accent-foreground",
      },
      size: {
        sm: "h-8 px-3 text-sm",
        md: "h-10 px-4 text-sm",
        lg: "h-12 px-6 text-base",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "md",
    },
  }
);
```

Always include `defaultVariants`. Variant names must be identical strings across the entire system. Not `"danger"` on one component and `"destructive"` on another.

---

## Forwarding

Every component, no exceptions:

- **Forwards `ref`** to the root DOM element
- **Merges `className`** via the `cn()` utility (clsx + tailwind-merge)
- **Spreads rest props** onto the root element
- **Sets `displayName`** for DevTools identification

Note: React 19 makes `ref` a regular prop, removing the need for `forwardRef`. The pattern below works for React 18; for React 19+, accept `ref` directly in the props object.

```tsx
import { forwardRef } from "react";
import { cn } from "@/lib/utils";

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, ...props }, ref) => (
    <button
      ref={ref}
      className={cn(buttonVariants({ variant, size }), className)}
      {...props}
    />
  )
);
Button.displayName = "Button";
```

### Native defaults

Button components default to `type="button"`. Native `<button>` submits forms by default, which causes accidental submissions when the component is used inside a form. Use `type="submit"` only for the explicit submit action.

---

## Controlled and Uncontrolled

Every stateful component supports both modes:

- **Uncontrolled:** `defaultValue` prop. The component manages its own state. Works out of the box with no wiring.
- **Controlled:** `value` + `on{Prop}Change` props. The consumer owns the state. Required for form libraries, URL sync, cross-component coordination.

```tsx
// Uncontrolled: works immediately, no state management needed
<Select defaultValue="option-a">

// Controlled: consumer owns the state
<Select value={selected} onValueChange={setSelected}>
```

A component that only supports controlled mode forces boilerplate on every consumer. A component that only supports uncontrolled mode can't participate in forms or shared state. Always support both.

---

## Composition

### When to configure vs compose

**Configuration (props)** works when variations are predictable, finite, and the component controls all layout.

Good configuration: `<Button variant="destructive" size="lg">`. The variations are enumerable. The component owns the layout.

**Composition (compound components)** works when the consumer needs control over structure, ordering, or content.

Good composition: `<Dialog.Trigger>`, `<Dialog.Content>`, `<Dialog.Title>`, `<Dialog.Close>`. The consumer decides what goes inside, in what order.

### The decision rule

If you're adding a 4th content prop (`title`, `description`, `icon`, `footer`, `action`...), stop and decompose into compound parts. Content props don't scale. A component with 6 content props is impossible to use without reading its docs.

### Compound component naming

`{Parent}.{Part}`: `Dialog.Trigger`, `Dialog.Content`, `Dialog.Title`. Parts are only valid inside their parent. The parent provides context (usually via React context).

```tsx
<Card>
  <Card.Header>
    <Card.Title>Title</Card.Title>
    <Card.Description>Description</Card.Description>
  </Card.Header>
  <Card.Content>...</Card.Content>
  <Card.Footer>
    <Button>Action</Button>
  </Card.Footer>
</Card>
```

### Slots

When a component needs a single flexible insertion point, use `children`. When it needs multiple named insertion points, use compound components for complex content or explicit slot props (`header`, `footer`) for simple elements.

Compound components are preferable when the slot content is complex or varies structurally. Slot props work for elements that are always the same shape (a single string, a single icon).

### Customisability band

Keep components in the middle: not so rigid that consumers fork them, not so loose that every usage re-implements the design system. Finite visual decisions are props. Structural variation is composition. Arbitrary style escape hatches are a last resort.

### Render delegation

When a component needs to render as a different element (a `Button` that renders as an `<a>`, a `ListItem` that renders as a `<link>`), support `asChild` (Radix pattern) or `render` prop (Base UI pattern).

```tsx
// asChild: the Button renders as whatever its child is
<Button asChild>
  <a href="/settings">Settings</a>
</Button>
```

Do not use the `as` prop pattern. It loses type safety because the prop types don't update when the rendered element changes.

---

## Component State Coverage

Every component must account for all states it can exist in. Missing states are the most common source of "this feels unfinished."

### Interactive states

Every interactive component (buttons, inputs, toggles, links, tabs) must handle:

| State | What it looks like |
|---|---|
| **Default** | Resting appearance |
| **Hover** | Visual change on pointer (scoped to `@media (hover: hover)`, per surface-details) |
| **Focus** | Visible focus ring on keyboard navigation |
| **Active/Pressed** | Momentary feedback during click/tap (scale 0.97, per surface-motion) |
| **Disabled** | Visually muted, non-interactive, with inline explanation (not tooltip, per surface-details) |
| **Loading** | Activity indicator, prevents duplicate interaction |

### Content states

Every component that displays data (lists, tables, cards, feeds) must handle:

| State | What it looks like |
|---|---|
| **Empty** | Designed prompt to create the first item, with CTA and optional templates |
| **Loading** | Skeleton that mirrors actual content structure (never a generic spinner) |
| **Error** | Clear error message with a retry action |
| **Partial** | Some data loaded, more available (pagination indicator, "load more") |
| **Complete** | All data visible, no further loading indicators |

Complex data components distinguish empty, loading, and error states. They may accept an error fallback, but they must not hide errors behind an empty state.

### The rule

List every state a component can be in before writing code. If a state is missing from the design, ask for it. Shipping without disabled, empty, or error states is shipping an incomplete component.

### Quality contract

Shared components must encode the complete state model for their role. Do not rely on each consumer to patch missing disabled, loading, focus, empty, error, or partial states. If the component cannot represent a state that the product can enter, extend the component contract before adding another one-off wrapper.

Incomplete shared components create product entropy: every downstream workaround becomes another place for behaviour, copy, accessibility, and visual treatment to drift.

---

## Icon System

### Colour inheritance

Icons inherit colour from their parent via `currentColor`. No explicit colour props needed in most cases.

```tsx
<Button variant="destructive">
  <TrashIcon /> Delete   {/* icon inherits destructive text colour */}
</Button>
```

Set `fill` or `stroke` to `currentColor` in all icon SVGs.

### Sizing

Icon sizes come from the system-tokens icon scale (`--icon-xs` through `--icon-xl`). Default size for inline icons is `--icon-md` (20px, 1.25rem).

### Consistency

All icons in the system share the same stroke weight, corner radius on internal shapes, optical sizing, and pixel grid alignment.

Commit to one icon library (Lucide, Heroicons, Phosphor). Mixing libraries produces visible inconsistency in stroke weight and style.

### Accessibility

Decorative icons (next to text that already describes the action) get `aria-hidden="true"`. Standalone icon buttons get an explicit `aria-label`.

---

## Accessibility

Every component must be usable without a mouse and understandable without vision.

- **Keyboard:** Enter, Space, Escape, Arrow keys as appropriate. Tab order follows visual order. Sequential lists use roving tabindex (surface-details).
- **ARIA:** Semantic HTML first. Add ARIA only when native semantics are insufficient.
- **Focus:** Visible focus ring on keyboard navigation. Modals trap focus; return it on close. Focus rings follow border-radius (surface-details).
- **Colour:** Never use colour as the sole indicator of state (surface-colour).
- **States:** Disabled elements have inline explanation, not tooltip (surface-details).

Headless libraries (Radix, React Aria, Ariakit, Base UI) handle most of this. When building from scratch, test with keyboard and a screen reader.

---

## Tools

| Tool | Purpose | Install if adopted |
|---|---|---|
| [CVA](https://cva.style) | Type-safe variant maps | `npm i class-variance-authority` |
| [@radix-ui/react-slot](https://www.radix-ui.com/primitives/utilities/slot) | `Slot` for `asChild` delegation | `npm i @radix-ui/react-slot` |
| [Base UI](https://base-ui.com) | Unstyled components with `render` delegation | `npm i @base-ui-components/react` |
| [clsx](https://github.com/lukeed/clsx) + [tailwind-merge](https://github.com/dcastil/tailwind-merge) | `cn()` utility | `npm i clsx tailwind-merge` |

```ts
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

---

## Anti-Patterns

1. **Inconsistent prop names.** `isDisabled` on one component, `disabled` on another.
2. **Inconsistent variant strings.** `"danger"` here, `"destructive"` there.
3. **Monolithic content props.** 5+ content props instead of compound parts.
4. **Missing states.** No hover, disabled, loading, empty, or error treatment.
5. **`as` prop for polymorphism.** Loses type safety. Use `asChild` or `render`.
6. **Controlled-only components.** Forces boilerplate on every consumer.
7. **Mixed icon libraries.** Lucide in nav, Heroicons in forms. Pick one.
8. **Decorative icons without `aria-hidden`.** Screen readers announce meaningless icon content.
9. **Generic spinners for loading.** Skeletons should mirror actual content structure.
10. **Button without explicit type.** Defaults to submit inside forms.
11. **Empty state used for errors.** Empty and failed are different product states.
12. **Incomplete shared state model.** Consumers have to patch missing states with one-off wrappers.

---

## Checklist

### API
- Every component accepts `className` and forwards `ref`
- Prop names follow conventions (`variant`, `size`, `disabled`, `loading`)
- No `is` prefix on booleans
- Multi-value dimensions use string unions
- Every optional prop has a documented default
- Button components default to `type="button"`
- `displayName` set on every component
- Rest props spread onto root element

### Variants
- CVA (or equivalent) used for variant declarations
- `defaultVariants` always set
- Variant names identical across all components
- Same size scale (`sm`, `md`, `lg`) everywhere

### Composition
- Components with 4+ content props use compound pattern
- Finite visual choices are props; structural variation is composition
- Compound parts named `{Parent}.{Part}`
- Render delegation via `asChild` or `render` (not `as`)
- Stateful components support both controlled and uncontrolled

### States
- Every interactive component: default, hover, focus, active, disabled, loading
- Every data component: empty, loading, error, partial, complete
- Skeletons mirror actual content structure
- Disabled states have inline explanation
- Shared components encode states centrally, not through downstream one-off fixes

### Icons
- Single icon library throughout
- Icons inherit colour via `currentColor`
- Decorative icons have `aria-hidden="true"`
- Standalone icon buttons have `aria-label`

---

## Learning from Usage

After completing a component task, review the output against the checklist. Append findings to `learnings.md` in this skill's folder. Installed learnings are local runtime notes preserved across suite updates; consult `learnings.md` before starting any new task.
