---
name: gp-ui
description: Use when building React UIs for TheGP applications, migrating existing UIs to @gp/ui components, integrating Tailwind v4 with @gp/ui theme, or answering questions about available components, design tokens, icons, or setup. Activate when user mentions @gp/ui, TheGP design system, or asks about GP-specific UI patterns and components.
---

# @gp/ui Design System

TheGP's shared React component library with Tailwind theme integration.

## Quick Reference

**Import**: `import { Button, Card, Layout } from '@gp/ui'`
**Theme**: `@import "@gp/ui/theme";` in CSS
**Icons**: `import { SearchIcon, UserIcon } from '@gp/ui'`

## Available Components

| Component | Purpose |
|-----------|---------|
| Button | Primary actions with variants: primary, secondary, ghost, destructive |
| Badge | Status indicators: success, warning, error, info, neutral |
| Card | Container with Card.Header, Card.Body, Card.Footer |
| StatCard | Metric display with optional trend indicator |
| StatGrid | Key-value grid with formatting and copy support |
| Alert | Notifications: info, warning, error, success |
| Input | Text input with label, icons, validation states |
| TextArea | Multi-line input with auto-resize |
| Modal | Dialog overlays (Radix-based) with sizes, controlled/uncontrolled state |
| Dropdown | Menu system (Radix-based) with items, checkboxes, submenus |
| Tooltip | Hover hints (Radix-based) |
| TabBar | Horizontal tab navigation |
| Layout | App shell with header, sidebar, user menu |
| Sidebar | Collapsible navigation with responsive behavior |
| Skeleton | Loading placeholders |
| LoginPage | Full-screen login with branding |
| GPLogo | TheGP logo SVG |

## Resources

Load these as needed:

- **[references/components.md](references/components.md)**: Complete component API reference with props and examples
- **[references/setup.md](references/setup.md)**: Installation, Tailwind v4 integration, peer dependencies
- **[references/design-guide.md](references/design-guide.md)**: Colors, typography, spacing conventions
- **[references/icons.md](references/icons.md)**: Available icon exports and naming conventions

## Key Patterns

### Class Merging
Always use `cn()` for combining classes:
```tsx
import { cn } from '@gp/ui'
<div className={cn('base-class', condition && 'conditional-class', className)} />
```

### Compound Components
Card, Dropdown, Tooltip use dot notation:
```tsx
<Card>
  <Card.Header>Title</Card.Header>
  <Card.Body>Content</Card.Body>
</Card>
```

### Semantic Icons
Icons named by purpose, not appearance:
```tsx
import { BackIcon, SpinnerIcon, DeleteIcon } from '@gp/ui'
```

## Theme Tokens

Custom Tailwind colors available after importing theme:
- `orange-50` to `orange-900` (brand orange)
- `navy-50` to `navy-950` (dark navy)
- `cream` (off-white background)

## Peer Dependencies

Apps must install: `react`, `react-dom`, `lucide-react`, `@radix-ui/react-dialog`, `@radix-ui/react-dropdown-menu`, `@radix-ui/react-tooltip`, `@radix-ui/react-label`
