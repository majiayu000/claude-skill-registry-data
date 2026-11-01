---
name: ui-ux-premium
description: UI/UX Designer — Premium Trading Interface — Institutional capability and runbook for ui-ux-premium.
---

# SKILL: UI/UX Designer — Premium Trading Interface
## Domain: Design System, Glassmorphism, Dark Mode, Trading UI

**Activation triggers:** new page design, component styling, design token
update, responsive layout, animation, accessibility, color system.

---

## Design System Tokens

```typescript
// app/src/shared/tokens/colors.ts — Integral Market design language
export const tokens = {
  // Primary: Cyan-Blue gradient (action, brand)
  cyan:   { DEFAULT: '#00d4ff', dark: '#0099cc', light: '#66e8ff' },
  blue:   { DEFAULT: '#0066ff', dark: '#0044cc', light: '#4499ff' },

  // Surface: Deep navy layering
  navy:   {
    950: '#030712',   // page background
    900: '#0a0f1e',   // card background
    800: '#111827',   // elevated surface
    700: '#1f2937',   // border color
    600: '#374151',   // muted border
  },

  // Semantic
  green:  { DEFAULT: '#22c55e', dark: '#16a34a' },   // profit, success
  red:    { DEFAULT: '#ef4444', dark: '#dc2626' },   // loss, error
  yellow: { DEFAULT: '#eab308', dark: '#ca8a04' },   // warning
  purple: { DEFAULT: '#a855f7', dark: '#9333ea' },   // premium features
};
```

---

## Glassmorphism Component Pattern

```tsx
// Standard glass card used throughout expert modules
function GlassCard({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    <div className={cn(
      "bg-navy-900/50 backdrop-blur-xl",
      "border border-navy-800 rounded-2xl",
      "shadow-2xl shadow-black/20",
      className
    )}>
      {children}
    </div>
  );
}

// Gradient border accent (imCharts, imJournal headers)
const gradientBorder = {
  background: 'linear-gradient(135deg, rgba(0,212,255,0.15), rgba(0,102,255,0.08))',
  borderImage: 'linear-gradient(135deg, rgba(0,212,255,0.3), rgba(0,102,255,0.2)) 1',
};
```

---

## Trading UI Color Semantics

```tsx
// Profit/Loss coloring — ALWAYS consistent
const pnlColor = (value: number) =>
  value > 0 ? 'text-green-400' : value < 0 ? 'text-red-400' : 'text-gray-400';

const pnlBg = (value: number) =>
  value > 0 ? 'bg-green-500/10 border-green-500/20'
            : value < 0 ? 'bg-red-500/10 border-red-500/20'
            : 'bg-gray-500/10 border-gray-500/20';

// Account status pill
const accountPillStyle = (connected: boolean) => ({
  background: connected ? 'rgba(0,212,255,0.06)' : 'rgba(255,100,60,0.06)',
  borderColor: connected ? 'rgba(0,212,255,0.2)'  : 'rgba(255,100,60,0.25)',
  color:       connected ? tokens.cyan.DEFAULT      : '#ff6644',
});
```

---

## Responsive Layout Standards

```tsx
// Mobile-first breakpoints (Tailwind)
// sm: 640px, md: 768px, lg: 1024px, xl: 1280px, 2xl: 1536px

// Header: hide labels on mobile, show on sm+
<span className="hidden sm:inline">{account.display_name}</span>

// Grid: 1 col mobile, 2 cols tablet, 3 cols desktop
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">

// Chart panels: full height on desktop, scrollable on mobile
<div className="h-screen lg:h-full overflow-auto lg:overflow-hidden">
```

---

## Animation Standards

```tsx
// Use Framer Motion for page transitions
import { motion } from 'framer-motion';

const pageVariants = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0, transition: { duration: 0.3 } },
  exit:    { opacity: 0, y: -10 },
};

<motion.div {...pageVariants}>
  <PageContent />
</motion.div>

// Micro-interactions: tailwind transitions
<button className="transition-all duration-200 hover:scale-105 active:scale-95">

// Loading states: skeleton screens (not spinners for content)
<div className="animate-pulse bg-navy-800 rounded-lg h-16 w-full" />
```

---

## Accessibility Standards

```tsx
// All interactive elements: keyboard accessible + aria labels
<button
  onClick={onConnect}
  aria-label="Connect broker account"
  title="Connect broker account"
  className="focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:ring-offset-2 focus:ring-offset-navy-900"
>

// Color: never rely on color alone (add icon/text)
// Contrast: minimum 4.5:1 for normal text, 3:1 for large text
// Focus: visible focus ring on all interactive elements
```

---

## Anti-Patterns

```
✗ Hardcoded hex colors outside design tokens
✗ Fixed pixel heights on dynamic content containers
✗ Missing loading and empty states
✗ Text contrast below WCAG AA
✗ onClick only (no keyboard support)
✗ Animations without prefers-reduced-motion respect
✗ Inconsistent spacing (use Tailwind spacing scale only)
✗ Z-index wars (define a z-index scale: modal=50, tooltip=40, etc.)
```
