---
name: Pattern Demo Generator
description: Scaffold interactive React demo components for AI design patterns with design system integration, starter tests, and documentation
---

# Pattern Demo Generator Skill

This skill speeds up pattern completion by generating interactive demo components that showcase each AI design pattern in action, complete with tests and documentation.

## When to Use This Skill

Claude will automatically invoke this skill when:
- You ask to "create a demo for pattern"
- You request "generate interactive component"
- You say "build demo UI for pattern"
- You want "example implementation"
- Working on a pattern and need the demo component

## What This Skill Creates

For each pattern, this skill generates:

```
Pattern Demo Output
├── Interactive Component
│   └── src/components/examples/[PatternName]Example.tsx
├── Component Tests
│   └── src/components/examples/__tests__/[PatternName]Example.test.tsx
├── Documentation
│   └── Comments in component explaining pattern
└── Integration
    └── Auto-linked in pattern page at /patterns/[pattern-slug]
```

## Available Demo Patterns (Fully Completed)

These have demos you can reference:

1. **Contextual Assistance** - Smart help based on context
2. **Progressive Disclosure** - Gradual feature revelation
3. **Human-in-the-Loop** - Human oversight in automation
4. **Explainable AI** - Transparent AI decisions
5. **Conversational UI** - Natural language chat
6. **Adaptive Interfaces** - Behavior-driven optimization
7. **Multimodal Interaction** - Multiple input modes
8. **Guided Learning** - AI tutorials and onboarding
9. **Augmented Creation** - AI-assisted content
10. **Responsible AI** - Ethics and bias mitigation
11. **Error Recovery** - Graceful failures
12. **Collaborative AI** - Human-AI partnership

## Demo Generation Workflow

### Step 1: Choose a Pattern

Select from the 12 patterns requiring demos:

1. **Predictive Anticipation** - Proactive suggestions
2. **Ambient Intelligence** - Context-aware background processing
3. **Confidence Visualization** - Show AI certainty levels
4. **Safe Exploration** - Risk-free experimentation
5. **Feedback Loops** - Learn from user interactions
6. **Graceful Handoff** - Seamless AI→Human transition
7. **Context Switching** - Manage multiple conversation contexts
8. **Intelligent Caching** - Smart data persistence
9. **Progressive Enhancement** - Layered feature availability
10. **Privacy-First Design** - Data minimization & control
11. **Selective Memory** - User-controlled AI memory
12. **Universal Access** - Inclusive design

### Step 2: Analyze Reference Demos

Review a similar completed demo to understand the structure:

```bash
# Look at Contextual Assistance demo (reference)
cat src/components/examples/ContextualAssistanceExample.tsx

# Check its test
cat src/components/examples/__tests__/ContextualAssistanceExample.test.tsx
```

**Common Demo Patterns**:
- Show before/after state
- Include interactive controls
- Demonstrate pattern benefits
- Show how AI enhances UX
- Include error/edge cases

### Step 3: Generate Component Skeleton

Use this template as starting point:

```typescript
// src/components/examples/[PatternName]Example.tsx

'use client'

import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'

/**
 * [PatternName] Example Component
 *
 * This component demonstrates the [PatternName] AI design pattern.
 *
 * Pattern Description:
 * [2-3 sentence explanation of what this pattern does]
 *
 * Key Features:
 * - Feature 1
 * - Feature 2
 * - Feature 3
 */

export const [PatternName]Example: React.FC = () => {
  const [state, setState] = useState('initial')
  const [isLoading, setIsLoading] = useState(false)

  const handleInteraction = async () => {
    setIsLoading(true)
    // Simulate AI processing
    await new Promise(resolve => setTimeout(resolve, 1000))
    setState('updated')
    setIsLoading(false)
  }

  return (
    <div
      data-testid="[pattern-slug]-demo"
      className="space-y-6 p-6"
    >
      {/* Pattern Title & Description */}
      <div>
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
          Interactive Demo
        </h3>
        <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
          [Description of what user can interact with]
        </p>
      </div>

      {/* Interactive Content */}
      <Card className="p-6">
        <AnimatePresence mode="wait">
          {state === 'initial' && (
            <motion.div
              key="initial"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="space-y-4"
            >
              {/* Initial state content */}
              <p className="text-gray-700 dark:text-gray-300">
                [Initial state description]
              </p>
              <Button onClick={handleInteraction} loading={isLoading}>
                [Action to trigger pattern]
              </Button>
            </motion.div>
          )}

          {state === 'updated' && (
            <motion.div
              key="updated"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="space-y-4"
            >
              {/* Updated state showing pattern in action */}
              <p className="text-gray-700 dark:text-gray-300">
                [Updated state - pattern effect visible]
              </p>
              <Button variant="outline" onClick={() => setState('initial')}>
                Reset
              </Button>
            </motion.div>
          )}
        </AnimatePresence>
      </Card>

      {/* Pattern Benefits */}
      <div className="space-y-3">
        <h4 className="text-sm font-semibold text-gray-900 dark:text-white">
          Pattern Benefits:
        </h4>
        <ul className="space-y-2">
          <li className="flex gap-3">
            <span className="text-green-600 dark:text-green-400">✓</span>
            <span className="text-sm text-gray-700 dark:text-gray-300">
              Benefit 1
            </span>
          </li>
          <li className="flex gap-3">
            <span className="text-green-600 dark:text-green-400">✓</span>
            <span className="text-sm text-gray-700 dark:text-gray-300">
              Benefit 2
            </span>
          </li>
        </ul>
      </div>
    </div>
  )
}

export default [PatternName]Example
```

### Step 4: Implement Interactive Behaviors

Your demo should:

✅ **Show Pattern in Action**
- Before/after states
- Clear visual change when pattern activates
- Smooth animations with framer-motion

✅ **Include Interactive Controls**
- Buttons to trigger pattern
- Input fields to control behavior
- Toggles for different modes

✅ **Demonstrate Benefits**
- Show how pattern improves UX
- Explain what's happening
- Display results/outcomes

✅ **Handle Edge Cases**
- Loading states with spinners
- Error states with recovery
- Empty states when appropriate

✅ **Use Design System**
- Import from `@/components/ui/`
- Use existing Button, Card, Badge components
- Follow Tailwind utilities
- Support dark mode with `dark:` prefix

### Step 5: Add Framer Motion Animations

Most demos use animations to show the pattern:

```typescript
// State transitions with AnimatePresence
<AnimatePresence mode="wait">
  {isExpanded && (
    <motion.div
      initial={{ opacity: 0, height: 0 }}
      animate={{ opacity: 1, height: 'auto' }}
      exit={{ opacity: 0, height: 0 }}
      transition={{ duration: 0.3 }}
    >
      Content
    </motion.div>
  )}
</AnimatePresence>

// Hover effects
<motion.button
  whileHover={{ scale: 1.05 }}
  whileTap={{ scale: 0.95 }}
  onClick={handleClick}
>
  Click me
</motion.button>

// Progress indicators
<motion.div
  initial={{ width: 0 }}
  animate={{ width: '100%' }}
  transition={{ duration: 2 }}
  className="h-1 bg-blue-500"
/>
```

### Step 6: Create Component Tests

```typescript
// src/components/examples/__tests__/[PatternName]Example.test.tsx

import React from 'react'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { [PatternName]Example } from '../[PatternName]Example'

describe('[PatternName]Example', () => {
  it('renders without crashing', () => {
    render(<[PatternName]Example />)
    expect(screen.getByTestId('[pattern-slug]-demo')).toBeInTheDocument()
  })

  it('displays initial state', () => {
    render(<[PatternName]Example />)
    expect(screen.getByText(/[initial state text]/)).toBeInTheDocument()
  })

  it('responds to user interaction', async () => {
    const user = userEvent.setup()
    render(<[PatternName]Example />)

    const button = screen.getByRole('button', { name: /[action text]/ })
    await user.click(button)

    await waitFor(() => {
      expect(screen.getByText(/[updated state text]/)).toBeInTheDocument()
    })
  })

  it('shows loading state during interaction', async () => {
    const user = userEvent.setup()
    render(<[PatternName]Example />)

    const button = screen.getByRole('button', { name: /[action text]/ })
    await user.click(button)

    // Loading state visible briefly
    expect(screen.getByRole('button')).toHaveAttribute('disabled')
  })

  it('matches snapshot', () => {
    const { container } = render(<[PatternName]Example />)
    expect(container).toMatchSnapshot()
  })

  it('resets to initial state', async () => {
    const user = userEvent.setup()
    render(<[PatternName]Example />)

    // Trigger update
    await user.click(screen.getByRole('button', { name: /[action text]/ }))

    // Click reset
    await user.click(screen.getByRole('button', { name: /Reset/ }))

    expect(screen.getByText(/[initial state text]/)).toBeInTheDocument()
  })

  it('is accessible', () => {
    render(<[PatternName]Example />)
    const button = screen.getByRole('button')
    expect(button).toHaveAccessibleName()
  })
})
```

### Step 7: Test the Component

```bash
# Run tests for your demo
npm test -- --testPathPattern="[PatternName]Example"

# Check coverage
npm run test:coverage -- --testPathPattern="[PatternName]Example"

# Watch mode for development
npm run test:watch -- [PatternName]Example
```

### Step 8: Register Component in Pattern Data

Add demo component to pattern definition:

```typescript
// src/data/patterns/patterns/[pattern-slug]/index.ts

import { [PatternName]Example } from '@/components/examples/[PatternName]Example'

export const [patternSlug]Pattern = {
  // ... other pattern data
  demo: {
    component: [PatternName]Example,
    description: 'Interactive demonstration of [pattern name]',
  }
}
```

### Step 9: Verify in Browser

```bash
npm run dev
# Visit http://localhost:3000/patterns/[pattern-slug]
# Test the interactive demo
# Check on mobile (responsive design)
# Test dark mode toggle
```

## Demo Component Best Practices

### ✅ Do's

1. **Keep it simple** - Focus on demonstrating ONE pattern clearly
2. **Make it interactive** - User should be able to interact with demo
3. **Show before/after** - Clearly display pattern effect
4. **Use existing components** - Reuse Button, Card, Badge from design system
5. **Add explanations** - Comments and text describing what's happening
6. **Test thoroughly** - Every interaction should be tested
7. **Support dark mode** - Use `dark:` Tailwind utilities
8. **Make it responsive** - Works on mobile, tablet, desktop

### ❌ Don'ts

1. **Don't make it complex** - Keep demo focused and clean
2. **Don't ignore accessibility** - ARIA labels, keyboard navigation
3. **Don't hardcode sizes** - Use Tailwind utilities
4. **Don't forget edge cases** - Handle loading, error, empty states
5. **Don't skip tests** - Every demo needs tests
6. **Don't use external fonts/images** - Use what's already available
7. **Don't forget snapshot tests** - Include for UI regression detection

## Batch Generate All Missing Demos

```bash
npm run generate-missing-demos
```

This command:
1. Identifies patterns without demo components
2. Generates skeleton components for all
3. Runs tests to verify
4. Reports which demos still need implementation

## Commands Reference

```bash
# Start dev server
npm run dev

# Run component tests
npm test -- --testPathPattern="Example"

# Run specific demo tests
npm test -- [PatternName]Example.test.tsx

# Test coverage for demos
npm run test:coverage -- --testPathPattern="examples"

# Generate missing demos
npm run generate-missing-demos
```

## Demo Structure in Pattern Page

When completed, demos appear on pattern pages:

```
/patterns/[pattern-slug]
├── Pattern Title & Description
├── Interactive Demo Component ← Generated here
├── Code Examples
├── Guidelines
├── Considerations
└── Benefits
```

## Integration with Pattern Development Skill

When using Pattern Development skill:
- Demo component generation is part of checklist
- Demos are validated in step "Build/update interactive demo component"
- Tests are part of "Add/update component tests"

---

**Goal**: Create engaging, interactive demos that showcase each AI design pattern in action, making it clear how the pattern improves user experience and AI interactions.
