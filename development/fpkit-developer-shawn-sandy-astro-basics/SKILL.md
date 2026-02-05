---
name: fpkit-developer
description: Guide for building applications with @fpkit/acss components. This skill should be used when composing custom React components from fpkit primitives, validating CSS variable naming conventions, extending fpkit components with custom behavior, or ensuring accessibility compliance in fpkit-based applications. Use when the user needs help with component composition patterns, CSS customization, or accessibility testing. Not for developing the @fpkit/acss library itself.
version: 0.1.5
---

# FPKit Developer

A Claude Code skill for building applications with **@fpkit/acss** components.

---

## Purpose

This skill helps developers:

- **Compose custom components** from fpkit primitives
- **Validate CSS variables** against fpkit conventions
- **Maintain accessibility** when building with fpkit
- **Follow best practices** for component composition

**This skill is for:** Developers using @fpkit/acss in their applications

**Not for:** Developing the @fpkit/acss library itself (use `fpkit-component-builder` for that)

---

## Workflow

When a user requests a new component or feature, follow this workflow:

### Step 1: Analyze the Request

Understand what the user needs:

- What is the component supposed to do?
- What user interactions are required?
- Are there similar fpkit components?

**Ask clarifying questions** if the requirements are unclear.

---

### Step 2: Check for Existing fpkit Components

Review the [@fpkit/acss component catalog](https://github.com/shawn-sandy/acss/tree/main/packages/fpkit/src/components) or [Storybook](https://fpkit.netlify.app):

**Available components:**

- **Buttons:** Button (with `aria-disabled` pattern, focus management, performance optimized)
- **Links:** Link (auto security for external links, ref forwarding, prefetch support)
- **Cards:** Card, CardHeader, CardTitle, CardContent, CardFooter
- **Forms:** Input, Field, FieldLabel, FieldInput
- **Layout:** Header, Main, Footer, Aside, Nav
- **Typography:** Heading, Text
- **Dialogs:** Dialog, Modal
- **Feedback:** Alert, Badge, Tag
- **Data:** Table, List
- **Interactive:** Details, Popover
- **Icons:** Icon library

**Decision tree:**

```
1. CHECK: Does fpkit have the exact component?
   ✓ YES → Use it directly, customize with CSS variables
           (Skip to Step 6: Accessibility)
   ✗ NO  → Continue to next check

2. CHECK: Can it be built by composing 2+ fpkit components?
   ✓ YES → Proceed to Step 3 (Composition)
   ✗ NO  → Continue to next check

3. CHECK: Can an existing fpkit component be extended/wrapped?
   ✓ YES → Proceed to Step 4 (Extension)
   ✗ NO  → Continue to next check

4. BUILD: Component requires custom implementation
   → Proceed to Step 5 (Custom Implementation)
```

---

### Step 3: Compose from fpkit Components

**Create a new component file** that imports and combines fpkit components:

```tsx
// components/StatusButton.tsx
import { Button, Badge } from '@fpkit/acss'

export interface StatusButtonProps extends React.ComponentProps<typeof Button> {
  status: 'active' | 'inactive' | 'pending'
}

export const StatusButton = ({ status, children, ...props }: StatusButtonProps) => {
  return (
    <Button {...props}>
      {children}
      <Badge variant={status}>{status}</Badge>
    </Button>
  )
}
```

**Guidelines:**

- Import fpkit components using named imports
- Extend fpkit component prop types with TypeScript
- Spread `...props` to preserve all fpkit functionality
- Keep composition simple (≤ 3 levels deep)

**Reference:** See `references/composition.md` for patterns and examples

---

### Step 4: Extend fpkit Components

**Wrap an fpkit component** to add custom behavior:

```tsx
// components/LoadingButton.tsx
import { Button, type ButtonProps } from '@fpkit/acss'
import { useState } from 'react'

export interface LoadingButtonProps extends ButtonProps {
  loading?: boolean
  onClickAsync?: (e: React.MouseEvent) => Promise<void>
}

export const LoadingButton = ({
  loading,
  onClickAsync,
  children,
  ...props
}: LoadingButtonProps) => {
  const [isLoading, setIsLoading] = useState(loading)

  const handleClick = async (e: React.MouseEvent) => {
    if (onClickAsync) {
      setIsLoading(true)
      try {
        await onClickAsync(e)
      } finally {
        setIsLoading(false)
      }
    }
  }

  return (
    <Button {...props} disabled={isLoading || props.disabled} onClick={handleClick}>
      {isLoading ? 'Loading...' : children}
    </Button>
  )
}
```

**Guidelines:**

- **Extend fpkit prop types** (don't replace them)
- **Preserve all fpkit functionality** (aria-disabled, focus management, etc.)
- **Add custom logic** around fpkit components
- **Maintain accessibility** - fpkit Button automatically handles:
  - `aria-disabled` pattern for better keyboard accessibility
  - Focus management (stays in tab order when disabled)
  - Event prevention when disabled
  - Automatic className merging for `.is-disabled` styling

---

### Step 5: Custom Implementation

If the component is truly custom and can't use fpkit:

1. **Follow fpkit patterns:**
   - Use semantic HTML
   - Add proper ARIA attributes
   - Support keyboard navigation
   - Use rem units (not px)
   - Define CSS variables for theming

2. **Create styles (if needed):**

   ```scss
   // components/CustomComponent.scss
   .custom-component {
     padding: var(--custom-padding, 1rem);
     border-radius: var(--custom-radius, 0.375rem);
     background: var(--custom-bg, white);

     // Use rem units only!
     margin-bottom: 1rem; // NOT 16px
     gap: 0.5rem; // NOT 8px
   }
   ```

3. **Validate CSS variables** (for custom styles):

   ```bash
   python scripts/validate_css_vars.py components/
   ```

**Reference:** See `references/css-variables.md` for naming conventions

---

### Step 6: Ensure Accessibility

**Check accessibility compliance:**

- [ ] Uses semantic HTML (`<button>`, `<nav>`, etc.)
- [ ] All interactive elements are keyboard accessible
- [ ] Proper ARIA attributes (`aria-label`, `aria-describedby`, etc.)
- [ ] Visible focus indicators
- [ ] Color contrast meets WCAG AA (4.5:1 for normal text)
- [ ] Screen reader friendly (meaningful labels)

**Test:**

- Navigate with keyboard only (Tab, Enter, Escape)
- Use automated testing (jest-axe)
- Check Storybook a11y addon (if documenting in Storybook)

**Reference:** See `references/accessibility.md` for patterns

---

### Step 7: Document the Component (Optional)

When creating a reusable component for a team:

**Create a Storybook story:**

```tsx
// components/StatusButton.stories.tsx
import type { Meta, StoryObj } from '@storybook/react'
import { StatusButton } from './StatusButton'

const meta = {
  title: 'Components/StatusButton',
  component: StatusButton,
  tags: ['autodocs'],
} satisfies Meta<typeof StatusButton>

export default meta
type Story = StoryObj<typeof meta>

export const Active: Story = {
  args: {
    status: 'active',
    children: 'Server Status',
  },
}

export const Inactive: Story = {
  args: {
    status: 'inactive',
    children: 'Server Status',
  },
}
```

---

## Reference Documentation

### Quick Reference Search

When searching reference files for specific patterns, use these grep commands:

```bash
# Find composition patterns by type
grep -i "pattern.*:" references/composition.md

# Find specific composition examples
grep -i "iconbutton\|confirmbutton\|taginput" references/composition.md

# Find CSS variables by component
grep -i "\-\-btn\|--alert\|--card" references/css-variables.md

# Find CSS variable naming rules
grep -i "naming\|convention\|pattern" references/css-variables.md

# Find ARIA patterns and attributes
grep -i "aria-\|role=" references/accessibility.md

# Find WCAG requirements
grep -i "wcag\|contrast\|level aa" references/accessibility.md

# Find testing patterns
grep -i "describe\|test\|expect\|render" references/testing.md

# Find Storybook configuration
grep -i "meta\|story\|args" references/storybook.md

# Find architecture patterns
grep -i "polymorphic\|as prop\|compound" references/architecture.md
```

---

### Composition Patterns

**Read `references/composition.md`** when composing components. Covers:

- Decision tree (compose vs extend vs create)
- 5 common composition patterns with code examples
- Real-world examples (IconButton, ConfirmButton, TagInput)
- Anti-patterns to avoid (nesting depth, polymorphism misuse)
- TypeScript prop type patterns

**Common questions → Reference sections:**

- "How do I combine multiple fpkit components?" → Patterns 1-3
- "Should I compose or extend?" → Decision Tree
- "How deep can I nest components?" → Anti-Patterns (≤3 levels)
- "How do I type extended props?" → TypeScript Support

### CSS Variables

**Read `references/css-variables.md`** for customization guidance. Covers:

- Naming convention (`--component-property`)
- Discovery techniques (DevTools inspection, IDE autocomplete)
- Customization strategies (global theme, scoped overrides)
- Complete variable reference for Button, Alert, Card, and other components
- Framework integration patterns (React inline styles, CSS Modules, styled-components)

**Common questions → Reference sections:**

- "What CSS variables does Button support?" → Component Reference: Button
- "How do I customize globally vs per-component?" → Customization Strategies
- "How do I find available variables?" → Discovery Techniques
- "Can I use variables with styled-components?" → Framework Integration

### Accessibility

**Read `references/accessibility.md`** for WCAG compliance guidance. Covers:

- WCAG 2.1 Level AA compliance requirements
- ARIA patterns and attributes for interactive components
- Keyboard navigation requirements (Tab, Enter, Escape, Arrow keys)
- Form accessibility (labels, error messages, validation)
- Color contrast requirements (4.5:1 normal text, 3:1 large text)
- Testing approaches (manual keyboard testing + automated jest-axe)

**Common questions → Reference sections:**

- "What ARIA attributes do I need?" → ARIA Patterns
- "How do I make keyboard navigation work?" → Keyboard Navigation
- "What's the minimum color contrast?" → Color Contrast (4.5:1)
- "How do I test accessibility?" → Testing with jest-axe

### Architecture

**Read `references/architecture.md`** to understand fpkit design patterns. Covers:

- Polymorphic UI component foundation (render as different elements)
- Understanding the `as` prop for semantic flexibility
- Simple vs compound component patterns (when to use each)
- TypeScript support and prop type inference
- Styling architecture (data attributes for variants, CSS variables for theming)
- Props patterns and conventions (spreading, forwarding refs)

**Common questions → Reference sections:**

- "What is the `as` prop?" → Polymorphic Components
- "When should I use compound components?" → Component Patterns
- "How does prop spreading work?" → Props Patterns
- "How are variants implemented?" → Styling Architecture

### Testing

**Read `references/testing.md`** for component testing strategies. Covers:

- Vitest and React Testing Library setup and configuration
- Testing composed components (integration vs unit tests)
- Query best practices (prefer getByRole, getByLabelText over getByTestId)
- Event testing patterns (user clicks, keyboard interactions, form submissions)
- Accessibility testing with jest-axe (automated a11y checks)
- Async testing and loading states (waitFor, findBy queries)

**Common questions → Reference sections:**

- "How do I test composed components?" → Testing Composed Components
- "What query should I use?" → Query Best Practices (prefer getByRole)
- "How do I test keyboard events?" → Event Testing
- "How do I test accessibility?" → jest-axe Integration

### Storybook

**Read `references/storybook.md`** for documentation strategies. Covers:

- Storybook setup and configuration (addons, plugins)
- Story structure and patterns (CSF 3.0 format)
- Documenting composed components (props tables, descriptions)
- CSS variable customization stories (controls, args)
- Interactive testing with play functions (user-event)
- Accessibility testing in Storybook (a11y addon)

**Common questions → Reference sections:**

- "How do I document a composed component?" → Documenting Composed Components
- "How do I show CSS variable options?" → CSS Variable Customization
- "How do I add interactive tests?" → Play Functions
- "How do I test accessibility in Storybook?" → A11y Addon

---

## Tools

### CSS Variable Validation

Validate custom CSS variables against fpkit conventions:

```bash
# Validate a file
python scripts/validate_css_vars.py components/Button.scss

# Validate a directory
python scripts/validate_css_vars.py styles/

# Validate current directory
python scripts/validate_css_vars.py
```

**What it checks:**

- ✅ Naming pattern: `--{component}-{property}`
- ✅ rem units (not px)
- ✅ Approved abbreviations: bg, fs, fw, radius, gap
- ✅ Full words for: padding, margin, color, border, display, width, height

---

## Examples

Quick reference examples demonstrating key patterns. For detailed implementations and advanced patterns, see `references/composition.md`.

### Example: Simple Composition (StatusButton)

Combining Button + Badge to show status:

```tsx
import { Button, Badge } from '@fpkit/acss'

export interface StatusButtonProps extends React.ComponentProps<typeof Button> {
  status: 'active' | 'inactive' | 'pending'
}

export const StatusButton = ({ status, children, ...props }: StatusButtonProps) => {
  return (
    <Button {...props}>
      {children}
      <Badge variant={status}>{status}</Badge>
    </Button>
  )
}
```

**Key patterns demonstrated:**

- Import fpkit components with named imports
- Extend fpkit prop types with TypeScript
- Spread `...props` to preserve fpkit functionality
- Simple composition (2 components combined)

---

### More Complex Examples

For production-ready implementations with state management, validation, and advanced patterns:

- **IconButton** (Container + Content Pattern)
  See `references/composition.md` → Pattern 1: Container Component with Content
  Demonstrates: Icon positioning, flexible layout, semantic structure

- **ConfirmButton** (Stateful Wrapper Pattern)
  See `references/composition.md` → Pattern 4: Enhanced Wrapper with State
  Demonstrates: Dialog integration, async actions, confirmation flows

- **LoadingButton** (Async State Management)
  See SKILL.md → Step 4: Extend fpkit Components (lines 117-156)
  Demonstrates: Loading states, async handlers, disabled state management

- **TagInput** (Compound Composition Pattern)
  See `references/composition.md` → Pattern 5: Compound Components
  Demonstrates: Multi-component orchestration, keyboard events, array state

---

## Best Practices

### ✅ Do

- **Compose from fpkit** - Start with fpkit components to inherit built-in accessibility
- **Extend prop types** - Use TypeScript to extend fpkit types (preserves type safety)
- **Preserve accessibility** - fpkit uses `aria-disabled` for better keyboard accessibility
- **Use `onClick` for events** - Captures keyboard, mouse, touch, and assistive tech
- **Use CSS variables** - Customize with variables, not hardcoded styles
- **Validate CSS** - Run validation script on custom styles
- **Document compositions** - Document fpkit components used in JSDoc
- **Test integration** - Test how composed components work together
- **Add tooltips to disabled buttons** - fpkit's `aria-disabled` pattern allows this!

### ❌ Don't

- **Don't duplicate fpkit** - If it exists in fpkit, use it
- **Don't break accessibility** - Maintain ARIA and keyboard navigation
- **Don't use `onPointerDown` alone** - It doesn't fire for keyboard users
- **Don't override `disabled` handling** - Trust fpkit's `aria-disabled` pattern
- **Don't use px units** - Always use rem
- **Don't over-compose** - Keep composition depth ≤ 3 levels
- **Don't nest interactive elements** - No `<button>` inside `<a>`
- **Don't ignore polymorphism** - Use `as` prop instead of wrapping
- **Don't manually add `rel="noopener"` to external links** - fpkit Link does this automatically

---

## Troubleshooting

### CSS Variables Not Applying

1. Check specificity - ensure the selector has equal or higher specificity
2. Check cascade order - import fpkit CSS before custom overrides
3. Check typos - variable names are case-sensitive

### Component Not Keyboard Accessible

1. Ensure using semantic HTML (`<button>`, not `<div>`)
2. Add `role`, `tabIndex`, and keyboard handlers if needed
3. Check focus indicators are visible
4. Test with Tab, Enter, Space, Escape keys

### TypeScript Errors

1. Extend fpkit prop types: `interface MyProps extends ButtonProps`
2. Import types: `import { Button, type ButtonProps } from '@fpkit/acss'`
3. Spread props correctly: `<Button {...props}>`

---

## Resources

- **[fpkit Documentation](https://github.com/shawn-sandy/acss/tree/main/packages/fpkit/docs)** - Complete guides
- **[Storybook](https://fpkit.netlify.app/)** - Component examples
- **[npm Package](https://www.npmjs.com/package/@fpkit/acss)** - Installation and API
- **[GitHub](https://github.com/shawn-sandy/acss)** - Source code and issues

---

## Compatible with @fpkit/acss v0.1.x

This skill is designed for applications using `@fpkit/acss` version 1.x. For version-specific documentation, check the npm package documentation in `node_modules/@fpkit/acss/docs/`.
