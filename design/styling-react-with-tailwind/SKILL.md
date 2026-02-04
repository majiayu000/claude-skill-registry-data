---
name: styling-react-with-tailwind
description: |
  Use when building React components with Tailwind CSS in this codebase. Covers token usage, tv() patterns, and component structure.
---

**References:**
- [Guide](./guide.md) - details on token system and patterns

## Overview

This codebase uses:
- **Tailwind CSS** with semantic design tokens via `tw-colors` plugin
- **tailwind-variants** (`tv()`) for type-safe variant styling
- **Rose Pine** color palette (light: Dawn, dark: Moon)

## Token System

### Color Token Pattern
```
{property}-{category}-{semantic}
```

**Text tokens:**
- `text-text-base` - Primary body text
- `text-text-muted` - Secondary/subtle text
- `text-text-link` - Interactive link color (iris purple)
- `text-text-strong` - Emphasized text

**Background tokens:**
- `bg-background-base` - Page background
- `bg-background-card` - Card surfaces
- `bg-background-button` - Button backgrounds
- `bg-background-informative` - Info callouts

**Border tokens:**
- `border-border-muted` - Subtle borders
- `border-border-input` - Form field borders
- `border-border-informative` - Info borders

### Spacing & Layout
Standard Tailwind spacing scale. Use semantic sizing:
- `p-4`, `gap-2`, `m-0` - standard spacing
- `max-w-7xl` - content width constraints

## Component Patterns

### Pattern 1: Slots (Multi-element components)
Use when component has multiple styled children.

```tsx
import { tv, VariantProps } from 'tailwind-variants';
import { classnames } from '~/core/classnames';

const Styles = tv({
  slots: {
    root: ['flex', 'items-center', 'gap-2'],
    label: ['text-text-base', 'font-medium'],
    icon: ['text-text-muted', 'w-4', 'h-4'],
  },
  variants: {
    size: {
      sm: { root: 'p-2', label: 'text-sm' },
      md: { root: 'p-4', label: 'text-base' },
    },
    intent: {
      primary: { root: 'bg-background-button', label: 'text-text-strong' },
      ghost: { root: 'bg-transparent', label: 'text-text-muted' },
    },
  },
  defaultVariants: {
    size: 'md',
    intent: 'primary',
  },
});

type StyleProps = VariantProps<typeof Styles>;
type Props = StyleProps & {
  className?: string;
  children: React.ReactNode;
};

export function MyComponent(props: Props) {
  const styles = Styles({ size: props.size, intent: props.intent });
  return (
    <div className={classnames(styles.root(), props.className)}>
      <span className={styles.icon()}>*</span>
      <span className={styles.label()}>{props.children}</span>
    </div>
  );
}
```

### Pattern 2: Base (Single-element components)
Use when component is a single styled element.

```tsx
import { tv, VariantProps } from 'tailwind-variants';
import { classnames } from '~/core/classnames';

const Styles = tv({
  base: [
    'border',
    'border-border-muted',
    'rounded',
    'transition-colors',
  ],
  variants: {
    variant: {
      solid: 'border-2',
      dashed: 'border-dashed',
    },
  },
  defaultVariants: {
    variant: 'solid',
  },
});

type Props = VariantProps<typeof Styles> & {
  className?: string;
};

export function Divider(props: Props) {
  const styles = Styles({ variant: props.variant });
  return <hr className={classnames(styles, props.className)} />;
}
```

### Pattern 3: Compound Variants
For conditional style combinations:

```tsx
const Styles = tv({
  base: ['rounded', 'px-4', 'py-2'],
  variants: {
    intent: { primary: '', danger: '' },
    disabled: { true: 'opacity-50 cursor-not-allowed' },
  },
  compoundVariants: [
    {
      intent: 'primary',
      disabled: false,
      class: 'bg-background-button hover:bg-background-hover',
    },
    {
      intent: 'danger',
      disabled: false,
      class: 'bg-red-500 hover:bg-red-600',
    },
  ],
});
```

## Key Utilities

### classnames()
Always use for merging classes safely:
```tsx
import { classnames } from '~/core/classnames';

// Merges and deduplicates Tailwind classes
classnames(styles.root(), props.className, isActive && 'ring-2');
```

### Box with asChild
For polymorphic components:
```tsx
import { Box } from '~/components/ds/box/Box';

<Box asChild className="text-text-link">
  <a href="/path">Link styled as Box</a>
</Box>
```

## Quick Reference

| Need | Use |
|------|-----|
| Multiple styled elements | `tv({ slots: { ... } })` |
| Single styled element | `tv({ base: [...] })` |
| Variant types | `VariantProps<typeof Styles>` |
| Merge classes | `classnames(a, b, c)` |
| Conditional variants | `compoundVariants: [...]` |
| Purple accent | `text-text-link`, `text-text-strong` |
| Muted text | `text-text-muted` |
| Card background | `bg-background-card` |

## Common Mistakes

1. **Using raw colors** - Always use semantic tokens (`text-text-base` not `text-gray-900`)
2. **Forgetting classnames()** - Props className won't merge properly without it
3. **Destructuring props** - Use `props.x` not `{ x }` per codebase convention
4. **Missing VariantProps** - Always type variants for IDE completion
