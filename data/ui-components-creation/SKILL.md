---
name: ui-components-creation
description: Guide for creating reusable UI components. Use this when asked to create a new component, extract shared UI logic, or add to the component library.
license: MIT
---

# UI Components Creation Guide

This skill guides you through creating reusable UI components in the SuperTool application following React 19, TypeScript, and Panda CSS best practices.

## When to Create a Reusable Component

### ✅ Create a Component When:

1. **Multiple Usage** - The component will be used in 2+ tools or pages
2. **Complex Logic** - State management or interaction logic can be abstracted
3. **Common Pattern** - It's a standard UI pattern (buttons, inputs, modals, tabs)
4. **Consistency** - You want to enforce consistent styling/behavior across the app
5. **Testing** - Complex logic benefits from isolated unit tests

**Examples:**
- Tabs component (used in GraphQL Playground, API Tester, etc.)
- Label component (used in all forms)
- Button, Input, Card (used everywhere)
- Dialog, Toast, Dropdown (common UI patterns)

### ❌ Don't Create a Component When:

1. **One-Time Use** - Only used in a single tool with no reuse plans
2. **Tool-Specific Logic** - Contains business logic tied to specific tool functionality
3. **Trivial Elements** - Simple divs with minimal styling (use inline Panda CSS)
4. **Premature Abstraction** - Wait until you need it in 2+ places before extracting

**Examples:**
- GraphQL query executor logic (specific to GraphQL tool)
- PDF merger UI (specific to PDF tool)
- One-off badges or status indicators
- Tool-specific layout containers

## Component Creation Checklist

- [ ] Component serves 2+ use cases or is a standard UI pattern
- [ ] TypeScript interface extends proper base types (HTMLAttributes, etc.)
- [ ] Panda CSS used for all styling (no Tailwind utilities)
- [ ] Component is composable with `className` prop support
- [ ] Accessibility requirements met (ARIA, keyboard navigation)
- [ ] Props are well-documented with JSDoc comments
- [ ] Unit tests created with >= 95% coverage
- [ ] Component added to index file if part of public API

## Step-by-Step Component Creation

### 1. Determine Component Location

**File:** `components/ui/component-name.tsx`

**Naming Convention:**
- Use kebab-case for filenames: `button.tsx`, `text-area.tsx`, `tabs.tsx`
- Use PascalCase for component names: `Button`, `TextArea`, `Tabs`

### 2. Create the Component File

**Template Structure:**

```typescript
'use client'

import { type HTMLAttributes, forwardRef } from 'react'
import { css, cx } from '@/styled-system/css'

// Define props interface extending base HTML element
export interface ComponentNameProps extends HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'outlined' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
  // Add component-specific props
}

/**
 * ComponentName - Brief description
 * 
 * @example
 * <ComponentName variant="outlined" size="md">
 *   Content
 * </ComponentName>
 */
export const ComponentName = forwardRef<HTMLDivElement, ComponentNameProps>(
  ({ variant = 'default', size = 'md', disabled = false, className, children, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cx(
          css({
            // Base styles
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            rounded: 'md',
            transition: 'all 0.2s',
            
            // Variant styles
            ...(variant === 'default' && {
              bg: 'purple.600',
              color: 'white',
              _hover: { bg: 'purple.700' },
            }),
            ...(variant === 'outlined' && {
              border: '1px solid',
              borderColor: 'purple.500',
              color: 'purple.400',
              _hover: { bg: 'purple.950' },
            }),
            
            // Size styles
            ...(size === 'sm' && { px: '3', py: '1.5', fontSize: 'sm' }),
            ...(size === 'md' && { px: '4', py: '2', fontSize: 'md' }),
            ...(size === 'lg' && { px: '6', py: '3', fontSize: 'lg' }),
            
            // Disabled state
            ...(disabled && {
              opacity: 0.5,
              cursor: 'not-allowed',
              pointerEvents: 'none',
            }),
          }),
          className
        )}
        {...props}
      >
        {children}
      </div>
    )
  }
)

ComponentName.displayName = 'ComponentName'
```

### 3. Real-World Example: Label Component

**File:** `components/ui/label.tsx`

```typescript
'use client'

import type { LabelHTMLAttributes } from 'react'
import { css, cx } from '@/styled-system/css'

export interface LabelProps extends LabelHTMLAttributes<HTMLLabelElement> {
  required?: boolean
}

/**
 * Label component for form inputs
 * 
 * @example
 * <Label htmlFor="email">Email Address</Label>
 * <Input id="email" type="email" />
 */
// biome-ignore lint/a11y/noLabelWithoutControl: Label component is used with htmlFor prop
export const Label = ({ required, className, children, ...props }: LabelProps) => {
  return (
    <label
      className={cx(
        css({
          display: 'block',
          fontSize: 'sm',
          fontWeight: 'medium',
          color: 'gray.100',
          mb: 2,
        }),
        className
      )}
      {...props}
    >
      {children}
      {required && <span className={css({ color: 'red.500', ml: 1 })}>*</span>}
    </label>
  )
}
```

**Usage:**
```typescript
<Label htmlFor="username" required>Username</Label>
<Input id="username" type="text" />
```

### 4. Real-World Example: Tabs Component with Context

**File:** `components/ui/tabs.tsx`

For components with shared state, use React Context:

```typescript
'use client'

import { type HTMLAttributes, type ReactNode, createContext, useContext, useState } from 'react'
import { css, cx } from '@/styled-system/css'

// Context for shared tab state
interface TabsContextValue {
  activeTab: string
  setActiveTab: (value: string) => void
}

const TabsContext = createContext<TabsContextValue | undefined>(undefined)

function useTabsContext() {
  const context = useContext(TabsContext)
  if (!context) {
    throw new Error('Tabs components must be used within Tabs provider')
  }
  return context
}

// Main Tabs container (provider)
export interface TabsProps extends HTMLAttributes<HTMLDivElement> {
  defaultValue: string
  children: ReactNode
}

export function Tabs({ defaultValue, children, className, ...props }: TabsProps) {
  const [activeTab, setActiveTab] = useState(defaultValue)

  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div className={cx(css({ w: 'full' }), className)} {...props}>
        {children}
      </div>
    </TabsContext.Provider>
  )
}

// Tabs list (container for triggers)
export interface TabsListProps extends HTMLAttributes<HTMLDivElement> {}

export function TabsList({ children, className, ...props }: TabsListProps) {
  return (
    <div
      role="tablist"
      className={cx(
        css({
          display: 'flex',
          gap: 1,
          borderBottom: '1px solid',
          borderColor: 'gray.700',
          mb: 4,
        }),
        className
      )}
      {...props}
    >
      {children}
    </div>
  )
}

// Individual tab trigger (button)
export interface TabsTriggerProps extends HTMLAttributes<HTMLButtonElement> {
  value: string
}

export function TabsTrigger({ value, children, className, ...props }: TabsTriggerProps) {
  const { activeTab, setActiveTab } = useTabsContext()
  const isActive = activeTab === value

  return (
    <button
      type="button"
      role="tab"
      aria-selected={isActive}
      onClick={() => setActiveTab(value)}
      className={cx(
        css({
          px: 4,
          py: 2,
          fontSize: 'sm',
          fontWeight: 'medium',
          color: isActive ? 'purple.400' : 'gray.400',
          borderBottom: '2px solid',
          borderColor: isActive ? 'purple.400' : 'transparent',
          transition: 'all 0.2s',
          cursor: 'pointer',
          bg: 'transparent',
          _hover: {
            color: isActive ? 'purple.300' : 'gray.300',
          },
        }),
        className
      )}
      {...props}
    >
      {children}
    </button>
  )
}

// Tab content panel
export interface TabsContentProps extends HTMLAttributes<HTMLDivElement> {
  value: string
}

export function TabsContent({ value, children, className, ...props }: TabsContentProps) {
  const { activeTab } = useTabsContext()

  if (activeTab !== value) return null

  return (
    <div
      role="tabpanel"
      className={cx(css({ py: 4 }), className)}
      {...props}
    >
      {children}
    </div>
  )
}
```

**Usage:**
```typescript
<Tabs defaultValue="variables">
  <TabsList>
    <TabsTrigger value="variables">Variables</TabsTrigger>
    <TabsTrigger value="headers">Headers</TabsTrigger>
    <TabsTrigger value="samples">Samples</TabsTrigger>
  </TabsList>
  
  <TabsContent value="variables">
    <Textarea placeholder="Enter variables..." />
  </TabsContent>
  
  <TabsContent value="headers">
    <Textarea placeholder="Enter headers..." />
  </TabsContent>
  
  <TabsContent value="samples">
    <div>Sample queries...</div>
  </TabsContent>
</Tabs>
```

### 5. Accessibility Requirements

All interactive components **MUST** meet these requirements:

#### For Buttons and Clickable Elements:
```typescript
<button
  type="button"                    // Explicit type
  onClick={handleClick}            // Click handler
  onKeyDown={handleKeyDown}        // Keyboard support (Enter/Space)
  aria-label="Descriptive label"  // For icon-only buttons
  disabled={isDisabled}            // Disable state
>
```

#### For Form Elements:
```typescript
<Label htmlFor="input-id">Label Text</Label>
<Input
  id="input-id"                    // Match Label htmlFor
  aria-required={isRequired}       // Required state
  aria-invalid={hasError}          // Error state
  aria-describedby="error-id"      // Link to error message
/>
{hasError && <p id="error-id">Error message</p>}
```

#### For Custom Components:
```typescript
<div
  role="tablist"                   // Appropriate ARIA role
  aria-label="Settings tabs"      // Descriptive label
>
  <button
    role="tab"
    aria-selected={isActive}       // Selection state
    aria-controls="panel-id"       // Link to panel
    tabIndex={isActive ? 0 : -1}   // Keyboard navigation
  >
```

**Accessibility Checklist:**
- [ ] Interactive elements use semantic HTML (`<button>`, `<a>`, `<input>`)
- [ ] Form inputs have associated labels (via `htmlFor` or wrapping)
- [ ] Keyboard navigation works (Tab, Enter, Space, Arrow keys)
- [ ] Focus states are visible and styled
- [ ] ARIA roles and attributes used correctly
- [ ] Color contrast meets WCAG AA standards (4.5:1 for text)
- [ ] Screen reader announces states and changes

### 6. Panda CSS Styling Patterns

**Base Styles:**
```typescript
css({
  // Layout
  display: 'flex',
  flexDirection: 'column',
  gap: 4,
  w: 'full',
  maxW: '7xl',
  
  // Spacing
  px: { base: '4', sm: '6', md: '8' },
  py: { base: '6', sm: '8', md: '10' },
  
  // Colors
  bg: 'gray.900',
  color: 'gray.100',
  borderColor: 'gray.700',
  
  // Glassmorphism
  bg: 'rgba(255, 255, 255, 0.05)',
  backdropFilter: 'blur(10px)',
  border: '1px solid',
  borderColor: 'rgba(255, 255, 255, 0.1)',
  
  // Gradients
  bgGradient: 'to-r',
  gradientFrom: 'purple.400',
  gradientTo: 'pink.600',
  bgClip: 'text',
  
  // States
  _hover: { bg: 'purple.700' },
  _focus: { outline: '2px solid', outlineColor: 'purple.500' },
  _disabled: { opacity: 0.5, cursor: 'not-allowed' },
  
  // Responsive
  fontSize: { base: 'sm', md: 'md', lg: 'lg' },
  gridTemplateColumns: { base: '1fr', sm: 'repeat(2, 1fr)', lg: 'repeat(3, 1fr)' },
})
```

**Combining Styles:**
```typescript
import { cx } from '@/styled-system/css'

<div className={cx(baseStyles, conditionalStyles, className)} />
```

### 7. TypeScript Interface Patterns

**Extending HTML Elements:**
```typescript
// For div elements
export interface CardProps extends HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'outlined'
}

// For button elements
export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  loading?: boolean
}

// For input elements
export interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  error?: string
}

// For form elements
export interface LabelProps extends LabelHTMLAttributes<HTMLLabelElement> {
  required?: boolean
}
```

**Using forwardRef for Refs:**
```typescript
export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ children, className, ...props }, ref) => {
    return (
      <button ref={ref} className={className} {...props}>
        {children}
      </button>
    )
  }
)

Button.displayName = 'Button'
```

### 8. Create Component Tests

**File:** `components/ui/__tests__/component-name.test.tsx`

```typescript
import { describe, expect, it } from 'vitest'
import { render, screen } from '@testing-library/react'
import { userEvent } from '@testing-library/user-event'
import { ComponentName } from '../component-name'

describe('ComponentName', () => {
  it('renders with default props', () => {
    render(<ComponentName>Content</ComponentName>)
    expect(screen.getByText('Content')).toBeInTheDocument()
  })

  it('applies variant styles correctly', () => {
    const { container } = render(
      <ComponentName variant="outlined">Content</ComponentName>
    )
    const element = container.firstChild as HTMLElement
    expect(element).toHaveClass('outlined')
  })

  it('handles click events', async () => {
    const handleClick = vi.fn()
    render(<ComponentName onClick={handleClick}>Click Me</ComponentName>)
    
    await userEvent.click(screen.getByText('Click Me'))
    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  it('respects disabled state', async () => {
    const handleClick = vi.fn()
    render(
      <ComponentName disabled onClick={handleClick}>
        Disabled
      </ComponentName>
    )
    
    await userEvent.click(screen.getByText('Disabled'))
    expect(handleClick).not.toHaveBeenCalled()
  })

  it('forwards ref correctly', () => {
    const ref = createRef<HTMLDivElement>()
    render(<ComponentName ref={ref}>Content</ComponentName>)
    expect(ref.current).toBeInstanceOf(HTMLDivElement)
  })

  it('merges custom className with base styles', () => {
    const { container } = render(
      <ComponentName className="custom-class">Content</ComponentName>
    )
    expect(container.firstChild).toHaveClass('custom-class')
  })

  it('supports keyboard navigation', async () => {
    const handleClick = vi.fn()
    render(<ComponentName onClick={handleClick}>Press Enter</ComponentName>)
    
    const element = screen.getByText('Press Enter')
    element.focus()
    await userEvent.keyboard('{Enter}')
    expect(handleClick).toHaveBeenCalled()
  })

  it('meets accessibility requirements', () => {
    render(
      <ComponentName role="button" aria-label="Accessible button">
        Content
      </ComponentName>
    )
    const element = screen.getByRole('button')
    expect(element).toHaveAccessibleName('Accessible button')
  })
})
```

**Test Coverage Checklist:**
- [ ] Default rendering with no props
- [ ] All prop variants (size, variant, state)
- [ ] Event handlers (onClick, onChange, onFocus, etc.)
- [ ] Disabled state behavior
- [ ] Ref forwarding
- [ ] Custom className merging
- [ ] Keyboard interactions
- [ ] Accessibility attributes
- [ ] Edge cases (empty content, long text, etc.)

**Run Tests:**
```bash
pnpm test components/ui/__tests__/component-name.test.tsx
pnpm test -- --coverage
```

### 9. Document the Component

Add JSDoc comments:

```typescript
/**
 * Button component for user actions
 * 
 * @example
 * // Primary button
 * <Button variant="primary" size="md" onClick={handleClick}>
 *   Click Me
 * </Button>
 * 
 * @example
 * // Disabled button with icon
 * <Button disabled>
 *   <Icon /> Loading...
 * </Button>
 * 
 * @param variant - Visual style: 'primary' | 'secondary' | 'ghost'
 * @param size - Button size: 'sm' | 'md' | 'lg'
 * @param disabled - Disable button interactions
 */
export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  /** Visual style variant */
  variant?: 'primary' | 'secondary' | 'ghost'
  
  /** Button size */
  size?: 'sm' | 'md' | 'lg'
  
  /** Loading state - shows spinner */
  loading?: boolean
}
```

## Common Component Patterns

### 1. Button Component
- Variants: primary, secondary, ghost, danger
- Sizes: sm, md, lg
- States: default, hover, active, disabled, loading
- Icon support (left/right)

### 2. Input Component
- Types: text, email, password, number, tel, url
- States: default, focus, error, disabled
- Optional label, error message, helper text
- Icon support (left/right)

### 3. Card Component
- Composable: Card > CardHeader > CardTitle/CardDescription > CardContent > CardFooter
- Variants: default, outlined, ghost
- Optional hover effect

### 4. Dialog/Modal Component
- Open/close state management
- Backdrop with blur
- Keyboard handling (Escape to close)
- Focus trap
- Portal rendering

### 5. Tabs Component
- Context-based state sharing
- Keyboard navigation (Arrow keys)
- Accessibility (role="tablist", role="tab", aria-selected)
- Composable: Tabs > TabsList > TabsTrigger + TabsContent

### 6. Dropdown Component
- Click/hover trigger
- Portal rendering
- Keyboard navigation
- Accessible (aria-expanded, aria-haspopup)

## Biome Lint Exceptions

When and how to use `biome-ignore` comments:

### ✅ Valid Use Cases:

```typescript
// 1. Label component with htmlFor (not an actual error)
// biome-ignore lint/a11y/noLabelWithoutControl: Label component is used with htmlFor prop
<label htmlFor="input-id">...</label>

// 2. Intentional any type with justification
// biome-ignore lint/suspicious/noExplicitAny: JSON.parse returns unknown type
const parsed: any = JSON.parse(jsonString)

// 3. Validated HTML from trusted source
// biome-ignore lint/security/noDangerouslySetInnerHtml: JSON-LD structured data is validated
<script dangerouslySetInnerHTML={{ __html: jsonLd }} />
```

### ❌ Invalid Use Cases:

```typescript
// Don't ignore legitimate issues
// biome-ignore lint/a11y/useKeyWithClickEvents
<div onClick={handleClick} />  // Use <button> instead!

// Don't ignore without explanation
// biome-ignore
const result = doSomething()

// Don't ignore multiple rules at once
// biome-ignore lint/suspicious/noExplicitAny lint/complexity/noBannedTypes
```

## Anti-Patterns to Avoid

### ❌ Don't Use Tailwind in Component Files

```typescript
// WRONG
<button className="bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded">
  Click Me
</button>

// CORRECT
<button className={css({
  bg: 'purple.600',
  _hover: { bg: 'purple.700' },
  px: 4,
  py: 2,
  rounded: 'md'
})}>
  Click Me
</button>
```

### ❌ Don't Use Div for Interactive Elements

```typescript
// WRONG
<div onClick={handleClick} className={css({ cursor: 'pointer' })}>
  Click Me
</div>

// CORRECT
<button type="button" onClick={handleClick}>
  Click Me
</button>
```

### ❌ Don't Forget Keyboard Support

```typescript
// WRONG
<div onClick={handleClick}>Click</div>

// CORRECT
<button
  type="button"
  onClick={handleClick}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      handleClick()
    }
  }}
>
  Click
</button>
```

### ❌ Don't Use Index as Key

```typescript
// WRONG
{items.map((item, index) => <Item key={index} {...item} />)}

// CORRECT
{items.map(item => <Item key={item.id} {...item} />)}
```

## Reference Implementations

Study these existing components:

- **Button** (`components/ui/button.tsx`) - Variants, sizes, loading state
- **Input** (`components/ui/input.tsx`) - Form integration, error states
- **Card** (`components/ui/card.tsx`) - Composable pattern with subcomponents
- **Label** (`components/ui/label.tsx`) - Simple, accessible form label
- **Tabs** (`components/ui/tabs.tsx`) - Context API for state sharing
- **Textarea** (`components/ui/textarea.tsx`) - Multi-line input with auto-resize

## Testing Strategy

### Unit Tests (Required)
- Test each component in isolation
- Mock external dependencies
- Test all prop variations
- Test user interactions
- Test accessibility features
- Achieve >= 95% coverage

### Integration Tests (Optional)
- Test component compositions
- Test with real form libraries
- Test with routing

## Performance Considerations

1. **Use `memo()` sparingly** - Only for expensive components
2. **Avoid inline object/array creation** - Define outside render
3. **Use `useCallback` for handlers** - Only if passed to memoized children
4. **Lazy load heavy components** - Use `lazy()` for dialogs, modals
5. **Optimize re-renders** - Use React DevTools Profiler

## Component Library Structure

```
components/
├── ui/                           # Reusable UI components
│   ├── button.tsx
│   ├── input.tsx
│   ├── card.tsx
│   ├── label.tsx               # NEW
│   ├── tabs.tsx                # NEW
│   ├── dialog.tsx
│   ├── dropdown.tsx
│   └── __tests__/              # Component tests
│       ├── button.test.tsx
│       ├── input.test.tsx
│       ├── label.test.tsx      # Required for new components
│       └── tabs.test.tsx       # Required for new components
├── features/                    # Feature-specific components
├── layout/                      # Layout components
└── providers/                   # Context providers
```

## Next Steps After Creating Component

1. **Add to exports** (if needed):
   ```typescript
   // components/ui/index.ts
   export { Button } from './button'
   export { Label } from './label'
   export { Tabs, TabsList, TabsTrigger, TabsContent } from './tabs'
   ```

2. **Document in Storybook** (if available):
   - Create `component-name.stories.tsx`
   - Show all variants and states
   - Provide usage examples

3. **Update design system docs**:
   - Add component to design system
   - Include do's and don'ts
   - Show accessibility guidelines

4. **Create usage examples**:
   - Add to example page
   - Show common patterns
   - Document edge cases

## Related Resources

- **Panda CSS Skill** (`.github/skills/panda-css-styling/SKILL.md`) - Styling patterns
- **Frontend Specialist Agent** (`.github/agents/frontend-panda-css-specialist.agent.md`) - Component architecture
- **Testing Coverage Skill** (`.github/skills/testing-coverage/SKILL.md`) - Testing patterns
- **New Tool Development Skill** (`.github/skills/new-tool-development/SKILL.md`) - Tool creation

## Summary

Creating reusable components:
1. ✅ Determine if extraction is necessary (2+ uses, common pattern)
2. ✅ Create in `components/ui/` with proper naming
3. ✅ Use TypeScript interfaces extending HTML element types
4. ✅ Style with Panda CSS (never Tailwind in components)
5. ✅ Meet accessibility requirements (ARIA, keyboard, semantics)
6. ✅ Write comprehensive tests (>= 95% coverage)
7. ✅ Document with JSDoc comments and examples
8. ✅ Use `forwardRef` for ref support
9. ✅ Support composition with `className` prop
10. ✅ Follow existing component patterns

**Remember:** Only create components when you have a clear reuse case or it's a standard UI pattern. When in doubt, keep logic in the tool page and extract later when the pattern emerges.
