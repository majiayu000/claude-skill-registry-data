---
name: ui-component-builder
description: Build, convert, and optimize React/Vue/Svelte UI components with TypeScript, advanced patterns, animations, and accessibility
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# UI Component Builder

Expert skill for building production-ready UI components for component libraries. Specializes in React, Vue, and Svelte with TypeScript, implementing advanced patterns, animations, and ensuring accessibility and performance.

## Core Capabilities

### 1. Component Creation
- Create new components from scratch with TypeScript
- Implement compound components pattern
- Build components with render props
- Create custom hooks and composables
- Support for polymorphic components (as prop pattern)
- Generic component types for maximum reusability

### 2. Framework Conversion
Convert components seamlessly between frameworks:
- **React → Vue**: JSX to template/composition API
- **React → Svelte**: Hooks to reactive declarations
- **Vue → React**: Template to JSX, composables to hooks
- **Svelte → React**: Reactive syntax to useState/useEffect

Preserve functionality, props interface, and behavior while adapting to framework idioms.

### 3. Advanced Patterns Implementation

#### Compound Components
```typescript
// Parent component manages shared state
// Child components access via context
<Select>
  <Select.Trigger />
  <Select.Content>
    <Select.Item value="1">Option 1</Select.Item>
  </Select.Content>
</Select>
```

#### Render Props
```typescript
<DataFetcher url="/api/data">
  {({ data, loading, error }) => (
    // Render logic here
  )}
</DataFetcher>
```

#### Custom Hooks Pattern
```typescript
// Extract reusable logic
const { isOpen, open, close, toggle } = useDisclosure()
```

### 4. Animation Integration
- Integrate Framer Motion for React components
- Use transition/animation APIs for Vue/Svelte
- Create spring physics animations
- Implement gesture controls (drag, hover, tap)
- Build enter/exit animations
- Orchestrate complex animation sequences
- Optimize for 60fps performance

### 5. TypeScript Excellence
- Strict type safety with proper generic constraints
- Discriminated unions for component variants
- Type inference for props and state
- Utility types (Omit, Pick, Required, Partial)
- Type guards and narrowing
- Proper typing for refs, events, and children

### 6. Accessibility (a11y) First
- Semantic HTML elements
- ARIA attributes when needed (roles, labels, states)
- Keyboard navigation (Tab, Enter, Escape, Arrow keys)
- Focus management and focus trapping
- Screen reader announcements
- Color contrast compliance (WCAG AA/AAA)
- Reduced motion support

### 7. Performance Optimization
- React.memo / Vue computed / Svelte reactive statements
- useMemo, useCallback optimization
- Virtual scrolling for large lists
- Code splitting and lazy loading
- Bundle size analysis
- Avoid unnecessary re-renders
- Optimize event handlers

## Workflow

### Phase 1: Analysis & Planning
1. **Understand Requirements**
   - Component purpose and use cases
   - Required props and variants
   - Accessibility requirements
   - Animation needs
   - Performance constraints

2. **Review Existing Code**
   - Check for similar components
   - Identify reusable patterns
   - Review design system tokens
   - Check naming conventions

3. **Plan Implementation**
   - Choose appropriate patterns
   - Define component API (props interface)
   - Plan state management approach
   - Identify edge cases

### Phase 2: Implementation
1. **Create Base Structure**
   - Set up component file(s)
   - Define TypeScript interfaces
   - Implement basic rendering
   - Add prop validation

2. **Implement Core Logic**
   - Add state management
   - Implement event handlers
   - Apply business logic
   - Handle edge cases

3. **Add Styling**
   - Use design system tokens
   - Implement variants (size, color, state)
   - Add responsive behavior
   - Support theming (light/dark)

4. **Enhance with Features**
   - Add animations if needed
   - Implement keyboard navigation
   - Add ARIA attributes
   - Create controlled/uncontrolled variants

### Phase 3: Quality Assurance
1. **Accessibility Check**
   - Test keyboard navigation
   - Verify ARIA attributes
   - Check screen reader output
   - Validate color contrast

2. **Performance Review**
   - Check for unnecessary renders
   - Optimize heavy computations
   - Review bundle impact
   - Test with React DevTools Profiler

3. **Type Safety Verification**
   - No TypeScript errors
   - Props are properly typed
   - Type inference works correctly
   - Generic constraints are sound

4. **Cross-browser Testing**
   - Modern browsers support
   - Graceful degradation
   - Polyfills if needed

## Component Patterns Library

### Button Component Template
```typescript
import { forwardRef, type ButtonHTMLAttributes } from 'react'
import { cva, type VariantProps } from 'class-variance-authority'

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground hover:bg-primary/90',
        outline: 'border border-input bg-background hover:bg-accent',
        ghost: 'hover:bg-accent hover:text-accent-foreground',
      },
      size: {
        default: 'h-10 px-4 py-2',
        sm: 'h-9 rounded-md px-3',
        lg: 'h-11 rounded-md px-8',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
)

interface ButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={buttonVariants({ variant, size, className })}
        {...props}
      />
    )
  }
)

Button.displayName = 'Button'

export { Button, buttonVariants }
```

### Compound Component Template
```typescript
import { createContext, useContext, useState } from 'react'

interface TabsContextValue {
  activeTab: string
  setActiveTab: (tab: string) => void
}

const TabsContext = createContext<TabsContextValue | undefined>(undefined)

export function Tabs({ defaultValue, children }: TabsProps) {
  const [activeTab, setActiveTab] = useState(defaultValue)

  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div>{children}</div>
    </TabsContext.Provider>
  )
}

export function TabsList({ children }: TabsListProps) {
  return <div role="tablist">{children}</div>
}

export function TabsTrigger({ value, children }: TabsTriggerProps) {
  const context = useContext(TabsContext)
  const isActive = context?.activeTab === value

  return (
    <button
      role="tab"
      aria-selected={isActive}
      onClick={() => context?.setActiveTab(value)}
    >
      {children}
    </button>
  )
}

export function TabsContent({ value, children }: TabsContentProps) {
  const context = useContext(TabsContext)
  if (context?.activeTab !== value) return null

  return <div role="tabpanel">{children}</div>
}
```

### Animated Component Template (Framer Motion)
```typescript
import { motion, AnimatePresence } from 'framer-motion'
import { useState } from 'react'

export function Modal({ isOpen, onClose, children }: ModalProps) {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/50"
          />
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            transition={{ type: 'spring', duration: 0.3 }}
            className="fixed inset-0 flex items-center justify-center"
          >
            <div className="bg-white rounded-lg p-6 max-w-md w-full">
              {children}
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}
```

## Framework Conversion Guidelines

### React to Vue Conversion
```typescript
// REACT
function Counter() {
  const [count, setCount] = useState(0)
  useEffect(() => {
    console.log('Count changed:', count)
  }, [count])

  return <button onClick={() => setCount(c => c + 1)}>{count}</button>
}

// VUE (Composition API)
<script setup lang="ts">
import { ref, watch } from 'vue'

const count = ref(0)

watch(count, (newCount) => {
  console.log('Count changed:', newCount)
})
</script>

<template>
  <button @click="count++">{{ count }}</button>
</template>
```

### React to Svelte Conversion
```typescript
// REACT
function Counter() {
  const [count, setCount] = useState(0)

  return <button onClick={() => setCount(c => c + 1)}>{count}</button>
}

// SVELTE
<script lang="ts">
  let count = 0

  $: console.log('Count changed:', count)
</script>

<button on:click={() => count++}>
  {count}
</button>
```

## Best Practices

### Component Structure
- One component per file (with related subcomponents)
- Co-locate types, styles, and utilities
- Export component as named export
- Provide displayName for debugging

### Props Design
- Keep props interface simple and focused
- Use discriminated unions for variants
- Provide sensible defaults
- Support both controlled and uncontrolled modes
- Accept className for style overrides
- Forward refs when wrapping native elements

### State Management
- Lift state up when needed by multiple components
- Keep component-specific state local
- Use context sparingly (avoid prop drilling)
- Prefer composition over context

### Naming Conventions
- PascalCase for components
- camelCase for props and functions
- SCREAMING_SNAKE_CASE for constants
- Prefix custom hooks with "use"
- Prefix event handlers with "handle" or "on"

### File Organization
```
components/
  Button/
    Button.tsx           # Main component
    Button.types.ts      # Type definitions
    Button.styles.ts     # Styling (if separate)
    Button.test.tsx      # Unit tests
    index.ts             # Public exports
```

### Accessibility Checklist
- [ ] Semantic HTML elements used
- [ ] Keyboard navigation works
- [ ] Focus visible and manageable
- [ ] ARIA attributes where needed
- [ ] Screen reader tested
- [ ] Color contrast meets WCAG AA
- [ ] Supports prefers-reduced-motion

### Performance Checklist
- [ ] No unnecessary re-renders
- [ ] Heavy computations memoized
- [ ] Event handlers optimized
- [ ] Bundle size impact minimal
- [ ] Lazy loading where appropriate
- [ ] Virtual scrolling for large lists

## Common Patterns

### Polymorphic Component (as prop)
```typescript
type AsProp<C extends React.ElementType> = {
  as?: C
}

type PropsToOmit<C extends React.ElementType, P> = keyof (AsProp<C> & P)

type PolymorphicComponentProp<
  C extends React.ElementType,
  Props = {}
> = React.PropsWithChildren<Props & AsProp<C>> &
  Omit<React.ComponentPropsWithoutRef<C>, PropsToOmit<C, Props>>

type TextProps<C extends React.ElementType> = PolymorphicComponentProp<
  C,
  { color?: 'primary' | 'secondary' }
>

export function Text<C extends React.ElementType = 'span'>({
  as,
  color = 'primary',
  children,
  ...props
}: TextProps<C>) {
  const Component = as || 'span'
  return <Component className={color} {...props}>{children}</Component>
}

// Usage: <Text as="h1">Title</Text>
```

### Controlled/Uncontrolled Pattern
```typescript
interface InputProps {
  value?: string              // Controlled
  defaultValue?: string       // Uncontrolled
  onChange?: (value: string) => void
}

function Input({ value, defaultValue, onChange }: InputProps) {
  const [internalValue, setInternalValue] = useState(defaultValue ?? '')

  const isControlled = value !== undefined
  const currentValue = isControlled ? value : internalValue

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value
    if (!isControlled) {
      setInternalValue(newValue)
    }
    onChange?.(newValue)
  }

  return <input value={currentValue} onChange={handleChange} />
}
```

### Focus Trap (for Modals)
```typescript
import { useEffect, useRef } from 'react'

function useFocusTrap(isActive: boolean) {
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!isActive) return

    const container = containerRef.current
    if (!container) return

    const focusableElements = container.querySelectorAll(
      'a[href], button, textarea, input, select, [tabindex]:not([tabindex="-1"])'
    )

    const firstElement = focusableElements[0] as HTMLElement
    const lastElement = focusableElements[focusableElements.length - 1] as HTMLElement

    const handleTab = (e: KeyboardEvent) => {
      if (e.key !== 'Tab') return

      if (e.shiftKey && document.activeElement === firstElement) {
        e.preventDefault()
        lastElement.focus()
      } else if (!e.shiftKey && document.activeElement === lastElement) {
        e.preventDefault()
        firstElement.focus()
      }
    }

    container.addEventListener('keydown', handleTab)
    firstElement?.focus()

    return () => container.removeEventListener('keydown', handleTab)
  }, [isActive])

  return containerRef
}
```

## Tools & Dependencies

### Essential Tools
- **TypeScript**: Type safety and better DX
- **class-variance-authority (cva)**: Variant management
- **clsx / cn**: Conditional className composition
- **Framer Motion**: Advanced animations
- **React Hook Form**: Form state management
- **Zod**: Runtime validation

### Development Tools
- **Vite**: Fast development server
- **tsup**: TypeScript bundler
- **Vitest**: Testing framework
- **React Testing Library**: Component testing
- **Storybook**: Component development

## Tips for Success

1. **Start Simple**: Build basic functionality first, then add complexity
2. **Think in Components**: Break down complex UIs into smaller pieces
3. **Composition Over Inheritance**: Use composition patterns
4. **Test Early**: Write tests as you build
5. **Document Props**: Add JSDoc comments for prop descriptions
6. **Use Design Tokens**: Reference design system values
7. **Consider Edge Cases**: Empty states, loading, errors
8. **Mobile First**: Design for mobile, enhance for desktop
9. **Performance Budget**: Keep bundle size in check
10. **Accessibility Always**: Build accessible from the start

## When to Use This Skill

Activate this skill when you need to:
- Create new UI components from scratch
- Convert components between React/Vue/Svelte
- Implement advanced component patterns
- Add animations to components
- Optimize component performance
- Improve component accessibility
- Refactor existing components
- Build compound components
- Create polymorphic components
- Implement custom hooks/composables

## Output Format

When creating components, provide:
1. **Complete Component Code**: Fully typed and production-ready
2. **Usage Example**: Show how to use the component
3. **Props Documentation**: Describe all props with types
4. **Accessibility Notes**: Keyboard shortcuts and ARIA usage
5. **Performance Tips**: Any optimization considerations
6. **Styling Notes**: How to customize appearance

Always follow the project's existing conventions and patterns.
