---
name: button-unification
description: Standardize button component heights, padding, and transitions across all variants. Ensures consistent appearance for default, outline, secondary, ghost, and link variants. Updates button.tsx with unified styles.
---

# Button Unification

Standardize the button component for consistent heights, padding, and transitions across all variants.

## Workflow

1. **Find Button Component** - Locate `website/components/ui/button.tsx`
2. **Audit Current Styles** - Review existing buttonVariants
3. **Standardize Heights** - Unified height per size
4. **Standardize Padding** - Consistent padding per size
5. **Standardize Typography** - Same font size and weight and variant
6. **Unify Border-Radius** - Same radius for all variants
7. **Unify Transitions** - Same transition for all variants
8. **Background** - Ensure background styles are consistent for each variant
9. **Icon Sizes** - Standardize icon button dimensions for each size
10. **Text Color** - Ensure text colors are consistent per variant
11. **Verify Consistency** - Test all variant + size combinations

## Size Specifications

### Heights (Unified)

| Size | Height | Class |
|------|--------|-------|
| default | 36px | h-9 |
| sm | 32px | h-8 |
| lg | 40px | h-10 |
| icon | 36px | size-9 |
| icon-sm | 32px | size-8 |
| icon-lg | 40px | size-10 |

### Padding (Unified)

| Size | Horizontal | With Icon | Gap |
|------|------------|-----------|-----|
| default | px-4 | has-[>svg]:px-3 | gap-2 |
| sm | px-3 | has-[>svg]:px-2.5 | gap-1.5 |
| lg | px-6 | has-[>svg]:px-4 | gap-2 |

## Base Styles (All Variants)

All button variants share these base styles:

```tsx
// Base class (applied to ALL variants)
"inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm text-white font-medium transition-all"
```

Key unified properties:
- `rounded-md` - Consistent border radius
- `text-sm font-medium text-white` - Consistent typography
- `transition-all` - Consistent transitions
- `gap-2` (or gap-1.5 for sm) - Consistent spacing

## Updated buttonVariants

See references/button-patterns.md for the complete CVA configuration.

```tsx
const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-all disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg:not([class*='size-'])]:size-4 shrink-0 [&_svg]:shrink-0 outline-none focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px]",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-white hover:bg-destructive/90",
        outline: "border bg-background shadow-xs hover:bg-accent hover:text-accent-foreground",
        secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-9 px-4 py-2 has-[>svg]:px-3",
        sm: "h-8 gap-1.5 px-3 has-[>svg]:px-2.5",
        lg: "h-10 px-6 has-[>svg]:px-4",
        icon: "size-9",
        "icon-sm": "size-8",
        "icon-lg": "size-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);
```

## Visual Consistency Check

After updating, verify:

1. **Same Height** - Buttons in a row align perfectly
2. **Same Padding** - Text has consistent spacing
3. **Same Radius** - Corners match across variants
4. **Same Transition** - Hover effects are smooth and consistent
5. **Same Font** - Text appears identical size
6. **Icon Sizes** - Icon buttons have correct dimensions

## Button with Next.js Link

When a button needs to navigate, use the `asChild` prop with Next.js `<Link>`:

```tsx
import Link from "next/link";
import { Button } from "@/components/ui/button";

// Correct pattern - Button wraps Link with asChild
<Button asChild>
  <Link href="/login">Login</Link>
</Button>

<Button asChild variant="outline" size="sm">
  <Link href="/contact">Contact</Link>
</Button>

<Button asChild variant="ghost" size="icon">
  <Link href="/settings">
    <Settings className="size-4" />
  </Link>
</Button>
```

**Key points:**
- Always use `asChild` prop when wrapping Link
- Link is the child, Button provides styling
- Works with all variants and sizes
- Preserves Next.js client-side navigation

**DO NOT do this:**
```tsx
// WRONG - Button onClick with router.push
<Button onClick={() => router.push('/login')}>Login</Button>

// WRONG - Link wrapping Button
<Link href="/login"><Button>Login</Button></Link>
```

## Testing

Test all variant + size combinations:

```tsx
// All variants at same size should have identical height
<div className="flex gap-2">
  <Button variant="default">Default</Button>
  <Button variant="outline">Outline</Button>
  <Button variant="secondary">Secondary</Button>
  <Button variant="ghost">Ghost</Button>
</div>
```

## Checklist

- [ ] All sizes have unified heights (h-9, h-8, h-10)
- [ ] All sizes have unified padding (px-4, px-3, px-6)
- [ ] All variants use rounded-md
- [ ] All variants use transition-all
- [ ] All sizes use text-sm font-medium
- [ ] Icon sizes use square dimensions (size-9, size-8, size-10)
- [ ] Gap is consistent per size (gap-2, gap-1.5)
- [ ] Focus ring styles are consistent across variants
- [ ] Navigation buttons use `asChild` with `<Link>`
