---
name: panda-css-styling
description: Guide for styling components with Panda CSS in the SuperTool project. Use this when styling tool pages, creating layouts, or implementing the glassmorphic design system.
license: MIT
---

# Panda CSS Styling Guide

This skill teaches you how to style components using Panda CSS following the SuperTool design system.

## CRITICAL: Tool Pages Use Panda CSS, NOT Tailwind

**IMPORTANT**: Tool pages (`app/tools/**/page.tsx`) MUST use Panda CSS `css()` function.
- Tailwind CSS v4 is used for app layouts and general pages
- Tool pages require Panda CSS for type-safe, recipe-based styling

## Import Pattern

```typescript
import { css } from '@/styled-system/css'
// For UI components
import { Button } from '@/components/ui/button'
```

## Design System

### Color Palette

The project uses a dark theme with purple/pink/blue gradients:

```typescript
// CSS variables from globals.css
--color-bg-primary: rgb(10, 10, 15)
--color-bg-secondary: rgb(20, 20, 30)
--color-accent-purple: rgb(168, 85, 247)
--color-accent-pink: rgb(236, 72, 153)
--color-accent-blue: rgb(59, 130, 246)
```

### Glassmorphism Effect

Use this pattern consistently:

```typescript
className={css({
  bg: 'rgba(255, 255, 255, 0.05)',
  backdropFilter: 'blur(10px)',
  borderRadius: 'xl',
  border: '1px solid',
  borderColor: 'rgba(255, 255, 255, 0.1)',
  boxShadow: '0 8px 32px 0 rgba(0, 0, 0, 0.37)'
})}
```

Or use the `.glass` utility class from Tailwind for quick application.

## Standard Page Layout

Every tool page should follow this structure:

```typescript
'use client'

import { css } from '@/styled-system/css'

export default function ToolPage() {
  return (
    <main className={css({
      mx: 'auto',
      maxW: '7xl',
      w: 'full',
      px: { base: '4', sm: '6', md: '8' },
      py: { base: '6', sm: '8', md: '10' },
      spaceY: { base: '6', sm: '8', md: '10' }
    })}>
      {/* Tool Header */}
      <div className={css({ textAlign: 'center', spaceY: '4' })}>
        <h1 className={css({
          fontSize: { base: '3xl', sm: '4xl', md: '5xl' },
          fontWeight: 'bold',
          bgGradient: 'to-r',
          gradientFrom: 'purple.400',
          gradientTo: 'pink.600',
          bgClip: 'text'
        })}>
          Tool Title
        </h1>
        <p className={css({
          fontSize: { base: 'md', sm: 'lg' },
          color: 'gray.400'
        })}>
          Tool description
        </p>
      </div>

      {/* Tool Content */}
      <div className={css({
        bg: 'rgba(255, 255, 255, 0.05)',
        backdropFilter: 'blur(10px)',
        borderRadius: 'xl',
        border: '1px solid',
        borderColor: 'rgba(255, 255, 255, 0.1)',
        p: { base: '6', sm: '8' },
        spaceY: '6'
      })}>
        {/* Your content here */}
      </div>
    </main>
  )
}
```

## Responsive Design Pattern

**ALWAYS use responsive values** with base, sm, md, lg, xl breakpoints:

```typescript
// ✅ CORRECT
className={css({
  fontSize: { base: 'sm', sm: 'md', md: 'lg' },
  padding: { base: '4', sm: '6', md: '8' },
  gridTemplateColumns: { base: '1fr', sm: 'repeat(2, 1fr)', lg: 'repeat(3, 1fr)' }
})}

// ❌ WRONG - No responsive values
className={css({
  fontSize: 'lg',
  padding: '8'
})}
```

## Grid Layouts

**CRITICAL**: Use valid grid template column values:

```typescript
// ✅ CORRECT
className={css({
  display: 'grid',
  gridTemplateColumns: { base: '1fr', sm: 'repeat(2, 1fr)', lg: 'repeat(3, 1fr)' },
  gap: { base: '4', sm: '6' },
  w: 'full' // IMPORTANT: Always add w: 'full'
})}

// ❌ WRONG - Invalid grid values
className={css({
  display: 'grid',
  gridTemplateColumns: { base: 1, sm: 2, lg: 3 } // Numbers not valid!
})}
```

## Common Patterns

### 1. Card Component

```typescript
<div className={css({
  bg: 'rgba(255, 255, 255, 0.05)',
  backdropFilter: 'blur(10px)',
  borderRadius: 'xl',
  border: '1px solid',
  borderColor: 'rgba(255, 255, 255, 0.1)',
  p: { base: '4', sm: '6' },
  transition: 'all 0.3s',
  cursor: 'pointer',
  _hover: {
    bg: 'rgba(255, 255, 255, 0.08)',
    borderColor: 'rgba(168, 85, 247, 0.5)',
    transform: 'translateY(-2px)',
  }
})}>
  Card content
</div>
```

### 2. Button (Using UI Component)

```typescript
import { Button } from '@/components/ui/button'

<Button 
  onClick={handleClick}
  className={css({
    w: 'full',
    bg: 'linear-gradient(to right, rgb(168, 85, 247), rgb(236, 72, 153))',
    _hover: {
      opacity: 0.9
    }
  })}
>
  Click Me
</Button>
```

### 3. Input Field

```typescript
<input
  type="text"
  className={css({
    w: 'full',
    px: '4',
    py: '3',
    bg: 'rgba(255, 255, 255, 0.05)',
    border: '1px solid',
    borderColor: 'rgba(255, 255, 255, 0.1)',
    borderRadius: 'lg',
    color: 'white',
    fontSize: { base: 'sm', sm: 'md' },
    outline: 'none',
    transition: 'all 0.2s',
    _focus: {
      borderColor: 'purple.400',
      bg: 'rgba(255, 255, 255, 0.08)'
    },
    _placeholder: {
      color: 'gray.500'
    }
  })}
  placeholder="Enter text..."
/>
```

### 4. Flex Layouts

```typescript
// Row layout
<div className={css({
  display: 'flex',
  flexDirection: { base: 'column', sm: 'row' }, // Stack on mobile
  alignItems: 'center',
  justifyContent: 'space-between',
  gap: { base: '4', sm: '6' }
})}>
  <div>Item 1</div>
  <div>Item 2</div>
</div>

// Column layout
<div className={css({
  display: 'flex',
  flexDirection: 'column',
  gap: '4',
  alignItems: 'stretch'
})}>
  <div>Item 1</div>
  <div>Item 2</div>
</div>
```

### 5. Section Divider

```typescript
<div className={css({
  h: '1px',
  w: 'full',
  bg: 'linear-gradient(to right, transparent, rgba(168, 85, 247, 0.5), transparent)',
  my: { base: '6', sm: '8' }
})} />
```

### 6. Gradient Text

```typescript
<h2 className={css({
  fontSize: { base: '2xl', sm: '3xl', md: '4xl' },
  fontWeight: 'bold',
  bgGradient: 'to-r',
  gradientFrom: 'purple.400',
  gradientVia: 'pink.500',
  gradientTo: 'blue.500',
  bgClip: 'text',
  lineHeight: '1.2'
})}>
  Gradient Heading
</h2>
```

### 7. Loading Spinner

```typescript
<div className={css({
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  gap: '3',
  py: '8'
})}>
  <div className={css({
    w: '8',
    h: '8',
    border: '3px solid',
    borderColor: 'rgba(168, 85, 247, 0.2)',
    borderTopColor: 'purple.400',
    borderRadius: 'full',
    animation: 'spin 1s linear infinite'
  })} />
  <span className={css({ color: 'gray.400' })}>Loading...</span>
</div>
```

### 8. Result Display

```typescript
<div className={css({
  mt: '6',
  p: { base: '4', sm: '6' },
  bg: 'rgba(34, 197, 94, 0.1)',
  border: '1px solid',
  borderColor: 'rgba(34, 197, 94, 0.3)',
  borderRadius: 'lg'
})}>
  <h3 className={css({
    fontSize: { base: 'lg', sm: 'xl' },
    fontWeight: 'semibold',
    color: 'green.400',
    mb: '3'
  })}>
    Result
  </h3>
  <p className={css({ color: 'gray.300' })}>
    Result content here
  </p>
</div>
```

### 9. Error State

```typescript
<div className={css({
  p: { base: '4', sm: '6' },
  bg: 'rgba(239, 68, 68, 0.1)',
  border: '1px solid',
  borderColor: 'rgba(239, 68, 68, 0.3)',
  borderRadius: 'lg'
})}>
  <p className={css({ color: 'red.400' })}>
    Error message here
  </p>
</div>
```

### 10. Badge/Tag

```typescript
<span className={css({
  display: 'inline-flex',
  alignItems: 'center',
  px: '3',
  py: '1',
  bg: 'rgba(168, 85, 247, 0.2)',
  border: '1px solid',
  borderColor: 'rgba(168, 85, 247, 0.4)',
  borderRadius: 'full',
  fontSize: 'xs',
  fontWeight: 'medium',
  color: 'purple.300'
})}>
  New
</span>
```

## Mobile-First Requirements

### Touch Targets

**MINIMUM 44px for all interactive elements:**

```typescript
// ✅ CORRECT
<button className={css({
  minH: '44px',
  minW: '44px',
  px: '6',
  py: '3'
})}>
  Button
</button>

// ❌ WRONG - Too small
<button className={css({ p: '1' })}>Small</button>
```

### Typography Scale

```typescript
// Heading sizes
h1: { base: '3xl', sm: '4xl', md: '5xl' }
h2: { base: '2xl', sm: '3xl', md: '4xl' }
h3: { base: 'xl', sm: '2xl', md: '3xl' }

// Body text
body: { base: 'sm', sm: 'md' }
caption: { base: 'xs', sm: 'sm' }
```

### Spacing Scale

```typescript
// Section spacing
spaceY: { base: '6', sm: '8', md: '10' }

// Component spacing
gap: { base: '4', sm: '6', md: '8' }

// Padding
p: { base: '4', sm: '6', md: '8' }
```

## State Modifiers

Panda CSS supports pseudo-classes with `_` prefix:

```typescript
className={css({
  bg: 'purple.500',
  _hover: { bg: 'purple.600' },
  _focus: { outline: '2px solid', outlineColor: 'purple.400' },
  _active: { transform: 'scale(0.98)' },
  _disabled: { opacity: 0.5, cursor: 'not-allowed' },
  _placeholder: { color: 'gray.500' }
})}
```

## Animations

Use Tailwind animation utilities:

```typescript
className={css({
  animation: 'spin 1s linear infinite' // Spinner
})}

className={css({
  animation: 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite' // Pulse
})}

className={css({
  animation: 'bounce 1s infinite' // Bounce
})}
```

## Common Mistakes to Avoid

### ❌ WRONG: Using Tailwind classes on tool pages

```typescript
// Don't do this on tool pages
<div className="bg-gray-800 p-4 rounded-lg">
```

### ✅ CORRECT: Using Panda CSS

```typescript
<div className={css({
  bg: 'gray.800',
  p: '4',
  borderRadius: 'lg'
})}>
```

### ❌ WRONG: No responsive values

```typescript
<div className={css({ fontSize: 'lg' })}>
```

### ✅ CORRECT: Responsive values

```typescript
<div className={css({ fontSize: { base: 'md', sm: 'lg' } })}>
```

### ❌ WRONG: Invalid grid template

```typescript
gridTemplateColumns: { base: 1, sm: 2 }
```

### ✅ CORRECT: Valid grid template

```typescript
gridTemplateColumns: { base: '1fr', sm: 'repeat(2, 1fr)' }
```

### ❌ WRONG: Missing width on grid

```typescript
<div className={css({
  display: 'grid',
  gridTemplateColumns: 'repeat(3, 1fr)'
})}>
```

### ✅ CORRECT: Width specified

```typescript
<div className={css({
  display: 'grid',
  gridTemplateColumns: 'repeat(3, 1fr)',
  w: 'full'
})}>
```

## Reference Example

**Canonical implementation**: `app/tools/unit-converter/page.tsx`

This file demonstrates:
- Correct Panda CSS usage
- Responsive design patterns
- Glassmorphism styling
- Mobile-first approach
- Proper grid layouts

## UI Component Library

Use pre-built components from `components/ui/`:

```typescript
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Select } from '@/components/ui/select'
import { Checkbox } from '@/components/ui/checkbox'
```

These components already follow the design system and are accessible.

## Checklist

- [ ] Using Panda CSS `css()` function (not Tailwind utilities)
- [ ] Glassmorphism effect applied to cards
- [ ] Responsive values for all sizing properties
- [ ] Mobile-first breakpoints (base → sm → md → lg)
- [ ] Touch targets >= 44px
- [ ] Grid layouts use valid template values + `w: 'full'`
- [ ] Gradient text for headings
- [ ] Proper spacing (spaceY, gap, padding)
- [ ] State modifiers for interactivity (_hover, _focus)
- [ ] Dark theme colors used throughout
- [ ] Tested on mobile viewport
