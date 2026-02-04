---
name: component-patterns
description: React component patterns, styling conventions, and animation standards for CJS2026 UI development
---

# Component Patterns

## When to Activate

Use this skill when the agent needs to:
- Create new React components
- Add animations to existing components
- Apply consistent styling
- Understand the design system
- Build dashboard widgets or admin tabs

## Design System Overview

CJS2026 uses a **"Sketch & Parchment"** aesthetic with these foundations:

### Color Palette

```jsx
// Primary colors
text-brand-teal      // #2A9D8F - Primary brand
text-brand-ink       // #2C3E50 - Primary text
bg-brand-cream       // #F5F0E6 - Primary background
bg-brand-parchment   // #EDE8DC - Secondary sections
text-brand-cardinal  // #C84B31 - 10th anniversary accent

// Opacity variants for hierarchy
text-brand-ink/70    // Secondary text
text-brand-ink/50    // Subtle text
```

### Typography

```jsx
font-heading   // Playfair Display (serif) - Headlines
font-body      // Source Sans 3 (sans) - Body text
font-accent    // Caveat (handwritten) - Decorative
```

## Component Templates

### Standard Page Component

```jsx
import { motion } from 'framer-motion';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';

export default function PageName() {
  return (
    <div className="min-h-screen bg-brand-cream">
      <Navbar />

      <main className="pt-24 pb-16">
        <div className="max-w-4xl mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h1 className="font-heading text-4xl md:text-5xl text-brand-ink mb-8">
              Page Title
            </h1>

            <div className="card-sketch p-8">
              {/* Content */}
            </div>
          </motion.div>
        </div>
      </main>

      <Footer />
    </div>
  );
}
```

### Dashboard Widget Card

```jsx
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ delay: 0.3 }}  // Increment for stagger
  className="card-sketch p-6"
>
  <div className="flex items-center justify-between mb-4">
    <h3 className="font-heading text-xl text-brand-ink">
      Widget Title
    </h3>
    <span className="text-brand-teal">
      <IconComponent className="h-5 w-5" />
    </span>
  </div>

  <div className="space-y-3">
    {/* Widget content */}
  </div>

  <button className="btn-primary w-full mt-4">
    Action
  </button>
</motion.div>
```

### Admin Tab Content

```jsx
const renderTabContent = () => (
  <div className="space-y-6">
    <h2 className="font-admin-heading text-2xl font-bold text-admin-ink dark:text-white">
      Tab Title
    </h2>

    {/* Stats row */}
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div className={cardClass}>
        <div className="text-3xl font-bold text-admin-teal">123</div>
        <div className="text-sm text-gray-500">Metric Label</div>
      </div>
    </div>

    {/* Main content */}
    <div className={cardClass}>
      {/* ... */}
    </div>
  </div>
);
```

## Animation Patterns

### Entrance Animation

```jsx
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.6 }}
>
```

### Scroll-Triggered Animation

```jsx
<motion.div
  initial={{ opacity: 0, y: 20 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true }}
>
```

### Staggered Children

```jsx
{items.map((item, index) => (
  <motion.div
    key={item.id}
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ delay: index * 0.1 }}
  >
    {/* Item content */}
  </motion.div>
))}
```

## Card Styles

### Public Site Card

```jsx
<div className="card-sketch p-6">
  {/* Automatic double-border shadow effect */}
  {/* Hover: lift animation */}
</div>
```

### Admin Panel Card

```jsx
const cardClass = `rounded-lg border ${
  theme === 'ink'
    ? 'bg-gray-800 border-gray-700'
    : 'bg-white border-gray-200'
} p-6`;

<div className={cardClass}>
  {/* Theme-aware styling */}
</div>
```

## Button Styles

### Primary Button

```jsx
<button className="btn-primary">
  Click Me
</button>

// Or manually:
<button className="px-6 py-3 bg-brand-teal text-white font-body font-semibold
                   rounded-lg border-2 border-brand-teal-dark
                   shadow-[3px_3px_0_var(--teal-dark)]
                   hover:translate-x-[-2px] hover:translate-y-[-2px]
                   hover:shadow-[5px_5px_0_var(--teal-dark)]
                   transition-all duration-200">
```

## Context Usage

```jsx
import { useAuth } from '../contexts/AuthContext';

function Component() {
  const {
    currentUser,
    userProfile,
    saveSession,
    unsaveSession,
    isSessionSaved
  } = useAuth();

  // Check registration for feature gating
  const hasFullAccess = userProfile?.role === 'admin' ||
    ['registered', 'confirmed'].includes(userProfile?.registrationStatus);
}
```

## Responsive Patterns

```jsx
// Grid responsive
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">

// Text responsive
<h1 className="text-2xl md:text-4xl lg:text-5xl">

// Show/hide by breakpoint
<div className="hidden lg:block">  {/* Desktop only */}
<div className="lg:hidden">        {/* Mobile only */}
```

## Integration Points

- **cjs-architecture** - For understanding component hierarchy
- **cms-content-pipeline** - For CMS-controlled content in components

## AnimatePresence and forwardRef Pattern

When using `AnimatePresence` with `mode="popLayout"` for exit animations, child components must forward refs.

### The forwardRef Warning (2026-01-04)

**Problem**: Console warning about function components not accepting refs.

```
Warning: Function components cannot be given refs.
Did you mean to use React.forwardRef()?
Check the render method of `PopChild`.
```

**Cause**: `AnimatePresence` with `mode="popLayout"` measures elements via refs for layout animations.

**Solution**: Wrap components in `React.forwardRef()`:

```jsx
// BAD: Function component without ref forwarding
function Toast({ toast, onDismiss }) {
  return (
    <motion.div>
      {/* content */}
    </motion.div>
  )
}

// GOOD: Forward ref to the motion element
const Toast = React.forwardRef(function Toast({ toast, onDismiss }, ref) {
  return (
    <motion.div ref={ref}>
      {/* content */}
    </motion.div>
  )
})
```

**When to use forwardRef**:
- Components rendered inside `AnimatePresence`
- Components that need ref access for measurements
- Custom components used with Framer Motion layout animations

## Accessibility: Touch Targets

Mobile touch targets should be at least 44x44px for accessibility:

```jsx
<button
  className="p-3 min-w-[44px] min-h-[44px] flex items-center justify-center"
  aria-label="Descriptive label"
>
  <Icon className="w-6 h-6" />
</button>
```

## Guidelines

1. Use `card-sketch` class for public-facing cards
2. Use theme-aware `cardClass` for admin components
3. Apply Framer Motion for all entrance animations
4. Increment delay values for staggered animations
5. Use `font-heading` for titles, `font-body` for content
6. Always include mobile breakpoints in responsive designs
7. **Use forwardRef for components inside AnimatePresence**
8. **Ensure 44x44px minimum touch targets for mobile**
