---
name: atomic-design
description: Build an Atomic Design system from Figma style guides - extract tokens, create atoms/molecules/organisms/templates/pages as reusable component libraries. Use when building or extending a design system or component library.
---

# Atomic Design System

## When to Use

| Trigger | Action |
|---|---|
| Create a component | Extract from Figma -> Build |
| Style element | Check Figma specs -> Apply |
| Extract tokens | Use this skill |
| Build page/form/layout | Switch to atomic-page-builder |

## Critical Rule: Figma Is Source of Truth

Extract and implement from Figma exactly. Never guess design values.

1. EXTRACT FROM FIGMA (mandatory) - Figma MCP: get_code_connect_map / get_node. Copy colors, spacing, typography, effects. Document ALL extracted values.
2. COMPARE WITH EXISTING - check current tokens/*.json. If Figma differs -> UPDATE tokens (Figma wins always).
3. IMPLEMENT EXACTLY - match Figma specs 1:1. No rounding, no improvements, no creative freedom.

### Zero Deviation Policy

| Forbidden | Correct |
|---|---|
| Round 13px to 12px | Use exact 13px |
| Change #3B82F6 to #3F85F7 | Use exact #3B82F6 |
| Add shadow not in Figma | No shadow if not designed |
| Improve spacing | Exact spacing from Figma |

## Figma MCP Commands

```typescript
figma.get_node(file_key, node_id)        // Get component specs
figma.get_code_connect_map(file_key, node_id)  // Get code snippets
figma.get_styles(file_key, style_type)   // Get styles
figma.get_local_variables(file_key)      // Get design tokens
```

## Design Tokens

| Need | File | Key Values |
|---|---|---|
| Colors | tokens/colors.json | semantic.primary, semantic.error |
| Typography | tokens/typography.json | semantic.heading-1, semantic.body |
| Spacing | tokens/spacing.json | semantic.component-padding |
| Components | tokens/components.json | button.variants, input.states |
| Breakpoints | tokens/breakpoints.json | md: 768px, lg: 1024px |

Use semantic token names, never primitives:

```css
color: var(--color-primary);              /* DO */
padding: var(--spacing-component-padding);/* DO */
color: var(--blue-500);  /* Wrong - primitive */
padding: 16px;           /* Wrong - hardcoded */
```

## Atomic Hierarchy

```
PAGES      -> Dashboard, Settings, UserProfile
TEMPLATES  -> DashboardLayout, AuthLayout
ORGANISMS  -> Header, Sidebar, Form, DataTable
MOLECULES  -> FormField, SearchBar, Card, NavItem
ATOMS      -> Button, Input, Typography, Icon
TOKENS     -> colors, typography, spacing (FROM FIGMA)
```

| Level | Rule | Example |
|---|---|---|
| Atom | Uses ONLY tokens | Button uses color/spacing tokens |
| Molecule | Combines 2+ Atoms | FormField = Label + Input + ErrorText |
| Organism | Combines Molecules + Atoms | Header = Logo + NavItems + UserMenu |
| Template | Layout structure, no content | DashboardLayout |
| Page | Template + real content | Dashboard |

## Core Rules

### 1. Props = Content/Behavior Only

```typescript
// Correct
interface ButtonProps {
  children: ReactNode;
  onClick: () => void;
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
}
// Wrong - visual props exposed
interface ButtonProps {
  backgroundColor?: string;  // NO
  fontSize?: string;         // NO
}
```

### 2. All Styles Encapsulated

```css
.button {
  background: var(--color-primary);
  padding: var(--spacing-button-padding-y) var(--spacing-button-padding-x);
  font-size: var(--font-size-button);
}
```

### 3. Responsive Built-In

```css
.card { padding: var(--spacing-4); }  /* Mobile */
@media (min-width: 768px) { .card { padding: var(--spacing-6); } }  /* Tablet */
@media (min-width: 1024px) { .card { padding: var(--spacing-8); } } /* Desktop */
```

### 4. Accessibility Required

```tsx
<button
  aria-label={iconOnly ? label : undefined}
  aria-busy={loading}
  aria-disabled={disabled}
>
```

## Workflow: Create New Component

### Step 0: Extract from Figma (mandatory)

1. Open Figma Dev Mode (Shift+D)
2. Select component
3. Extract: dimensions, padding, colors, typography, effects, border radius
4. Document ALL extracted values
5. Compare with existing tokens
6. Update tokens if Figma differs

### Step 1: Classify Level

```
Is component breakable into smaller parts?
  No  -> ATOM
  Yes -> What does it compose?
    Only Atoms      -> MOLECULE
    Molecules+Atoms -> ORGANISM
```

### Step 2: Create Files

```
src/design-system/atoms/Button/
  Button.tsx          # Component + Props
  Button.module.css   # All styles (tokens only)
  Button.test.tsx     # Tests
  index.ts            # Export
```

### Step 3: Implement Pattern

Head every component file with the Figma provenance comment:

```tsx
/**
 * @figma https://figma.com/file/xxx/Design-System?node-id=123
 * @extracted 2024-01-15
 * All values from Figma - DO NOT MODIFY without designer approval.
 */
```

Props: content/behavior only, e.g. `variant?: 'primary' | 'secondary' | 'ghost' | 'danger'`, `size?: 'sm' | 'md' | 'lg'`, `disabled?`, `onClick?`, `children`. Styles come from `./Button.module.css` via `clsx(styles.button, styles[variant], styles[size])`. Full template: references/component-templates.md

## Checklist Before Delivery

- [ ] Specs extracted from Figma (not guessed)
- [ ] Tokens updated if Figma values differ
- [ ] NO values rounded or improved
- [ ] Visual comparison shows 0% difference from Figma
- [ ] Correct atomic level
- [ ] Uses ONLY semantic tokens
- [ ] Props are content/behavior only
- [ ] Responsive at all breakpoints
- [ ] TypeScript interfaces complete
- [ ] Accessibility attributes
- [ ] Figma link documented

## References

| File | When to Read |
|---|---|
| tokens/*.json | Need specific token values |
| references/figma-design-fidelity.md | Figma extraction guide |
| references/design-deviation-rules.md | Zero deviation policy |
| references/atomic-hierarchy.md | Component examples |
| references/component-templates.md | Copy-paste templates |
| references/responsive-patterns.md | Responsive patterns |
